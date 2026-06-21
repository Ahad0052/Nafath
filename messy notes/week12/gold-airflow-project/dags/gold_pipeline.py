from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

from datetime import datetime, timedelta
import requests
import pandas as pd
import os

from sqlalchemy import create_engine


API_KEY = os.getenv("GOLD_API_KEY")
CSV_PATH = "/opt/airflow/data/gold_prices.csv"
MYSQL_URL = os.getenv("MYSQL_URL", "mysql+pymysql://root:root@mysql:3306/gold_db")


def extract_gold():
    if not API_KEY:
        raise ValueError("GOLD_API_KEY is missing. Add it to docker-compose.yaml.")

    url = "https://www.goldapi.io/api/XAU/USD"

    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    if "price" not in data:
        raise ValueError(f"GoldAPI did not return a price. Response: {data}")

    return data


def transform_gold(ti):

    data = ti.xcom_pull(task_ids="extract_gold")
    if not data:
        raise ValueError("No data was found from extract_gold.")

    transformed = {
        "symbol": data.get("metal", "XAU"),
        "price": data["price"],
        "currency": data.get("currency", "USD"),
        "timestamp": data["timestamp"],
        "created_at": datetime.utcnow().isoformat(timespec="seconds")
    }
    return transformed


def save_csv(ti):

    record = ti.xcom_pull(task_ids="transform_gold")
    if not record:
        raise ValueError("No transformed gold record was found in XCom.")

    df = pd.DataFrame([record])
    folder = os.path.dirname(CSV_PATH)
    os.makedirs(folder, exist_ok=True)

    file_exists = os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0

    df.to_csv(
        CSV_PATH,
        mode="a" if file_exists else "w",
        header=not file_exists,
        index=False
    )
    print(f"Saved CSV row to {CSV_PATH}: {record}")


def load_mysql(ti):

    record = ti.xcom_pull(task_ids="transform_gold")
    if not record:
        raise ValueError("No transformed gold record was found in XCom.")

    df = pd.DataFrame([record])

    engine = create_engine(MYSQL_URL)

    df.to_sql(
        "gold_prices",
        engine,
        if_exists="append",
        index=False
    )


with DAG(

    dag_id="gold_price_pipeline",

    start_date=datetime(2025, 1, 1),

    schedule="@hourly",

    catchup=False,

    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
    }

) as dag:

    extract = PythonOperator(
        task_id="extract_gold",
        python_callable=extract_gold
    )

    transform = PythonOperator(
        task_id="transform_gold",
        python_callable=transform_gold
    )
    save_csv_task = PythonOperator(
        task_id="save_csv",
        python_callable=save_csv
    )
    mysql_task = PythonOperator(
        task_id="load_mysql",
        python_callable=load_mysql
    )
   
    extract >> transform
    transform >> save_csv_task
    transform >> mysql_task
