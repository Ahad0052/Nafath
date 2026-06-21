import os
from datetime import datetime, timedelta

import pandas as pd
import requests
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from sqlalchemy import create_engine

API_KEY = os.getenv("GOLD_API_KEY")

def extract_gold():
    if not API_KEY:
        raise ValueError("GOLD_API_KEY is not set")

    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

def transform_gold(ti):
    data = ti.xcom_pull(task_ids="extract_gold")
    
    # Convert UNIX timestamp to human-readable format for MySQL
    formatted_time = pd.to_datetime(data["timestamp"], unit='s')
    
    transformed = {
        "symbol": data["metal"],
        "price": data["price"],
        "currency": data["currency"],
        "timestamp": str(formatted_time)
    }
    ti.xcom_push(key="gold_data", value=transformed)

def save_csv(ti):
    record = ti.xcom_pull(task_ids="transform_gold", key="gold_data")
    df = pd.DataFrame([record])
    data_dir = os.getenv("GOLD_DATA_DIR", "/opt/airflow/data")
    filename = "gold_prices.csv"
    path = os.path.join(data_dir, filename)

    try:
        write_csv(df, path)
    except OSError:
        fallback_path = os.path.join(os.getenv("AIRFLOW_HOME", "/opt/airflow"), filename)
        write_csv(df, fallback_path)

def write_csv(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if os.path.exists(path):
        df.to_csv(path, mode="a", header=False, index=False)
    else:
        df.to_csv(path, index=False)

def load_mysql(ti):
    record = ti.xcom_pull(task_ids="transform_gold", key="gold_data")
    df = pd.DataFrame([record])
    
    # Format timestamp column back to datetime object for clean SQL injection
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    engine = create_engine("mysql+pymysql://root:root@mysql:3306/gold_db", pool_pre_ping=True)
    try:
        df.to_sql("gold_prices", engine, if_exists="append", index=False)
    finally:
        engine.dispose()

with DAG(
    dag_id="gold_price_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=2),
    },
) as dag:

    extract = PythonOperator(
        task_id="extract_gold",
        python_callable=extract_gold
    )

    transform = PythonOperator(
        task_id="transform_gold",
        python_callable=transform_gold
    )

    csv_task = PythonOperator(
        task_id="save_csv",
        python_callable=save_csv
    )

    mysql_task = PythonOperator(
        task_id="load_mysql",
        python_callable=load_mysql
    )

    extract >> transform >> [csv_task, mysql_task]
