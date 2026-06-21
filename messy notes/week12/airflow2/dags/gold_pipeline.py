from __future__ import annotations

from datetime import datetime
import os

import pandas as pd
import requests
from sqlalchemy import create_engine

try:
    from airflow.sdk import DAG
except ImportError:
    from airflow import DAG

try:
    from airflow.providers.standard.operators.python import PythonOperator
except ImportError:
    from airflow.operators.python import PythonOperator


API_KEY = os.getenv("GOLD_API_KEY")
API_URL = "https://www.goldapi.io/api/XAU/USD"
CSV_PATH = "/opt/airflow/data/gold_prices.csv"
MYSQL_URL = "mysql+pymysql://root:root@mysql:3306/gold_db"


def extract_gold():
    if not API_KEY:
        raise ValueError("GOLD_API_KEY is missing. Add it to the .env file.")

    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json",
    }

    response = requests.get(API_URL, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    if "price" not in data:
        raise ValueError(f"GoldAPI response did not include a price: {data}")

    return data


def _format_timestamp(value):
    if value is None:
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(value, (int, float)):
        return datetime.utcfromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")

    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return str(value)


def transform_gold(ti):
    data = ti.xcom_pull(task_ids="extract_gold")

    transformed = {
        "symbol": data.get("metal", "XAU"),
        "price": float(data["price"]),
        "currency": data.get("currency", "USD"),
        "timestamp": _format_timestamp(data.get("timestamp")),
    }

    ti.xcom_push(key="gold_data", value=transformed)


def save_csv(ti):
    record = ti.xcom_pull(task_ids="transform_gold", key="gold_data")
    df = pd.DataFrame([record])

    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    df.to_csv(
        CSV_PATH,
        mode="a" if os.path.exists(CSV_PATH) else "w",
        header=not os.path.exists(CSV_PATH),
        index=False,
    )


def load_mysql(ti):
    record = ti.xcom_pull(task_ids="transform_gold", key="gold_data")
    df = pd.DataFrame([record])

    engine = create_engine(MYSQL_URL)
    df.to_sql("gold_prices", engine, if_exists="append", index=False)


with DAG(
    dag_id="gold_price_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["gold", "etl", "beginner"],
) as dag:
    extract = PythonOperator(
        task_id="extract_gold",
        python_callable=extract_gold,
    )

    transform = PythonOperator(
        task_id="transform_gold",
        python_callable=transform_gold,
    )

    csv_task = PythonOperator(
        task_id="save_csv",
        python_callable=save_csv,
    )

    mysql_task = PythonOperator(
        task_id="load_mysql",
        python_callable=load_mysql,
    )

    extract >> transform >> csv_task >> mysql_task
