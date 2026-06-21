from __future__ import annotations

from datetime import datetime, timezone
import os

import pandas as pd
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine, text


API_KEY = os.getenv("GOLD_API_KEY")
API_URL = "https://www.goldapi.io/api/XAU/USD"
CSV_PATH = "/opt/airflow/data/gold_prices.csv"
MYSQL_URL = "mysql+pymysql://root:root@mysql:3306/gold_db"


def extract_gold() -> dict:
    if not API_KEY or API_KEY == "YOUR_GOLDAPI_KEY":
        raise ValueError("Set GOLD_API_KEY in your environment before running the DAG.")

    response = requests.get(
        API_URL,
        headers={
            "x-access-token": API_KEY,
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _format_timestamp(value: object) -> str:
    if value is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(value, (int, float)):
        timestamp = value / 1000 if value > 10_000_000_000 else value
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    text_value = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text_value).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def transform_gold(ti) -> None:
    data = ti.xcom_pull(task_ids="extract_gold")
    record = {
        "symbol": data.get("metal", "XAU"),
        "price": float(data["price"]),
        "currency": data.get("currency", "USD"),
        "timestamp": _format_timestamp(data.get("timestamp")),
    }
    ti.xcom_push(key="gold_data", value=record)


def save_csv(ti) -> None:
    record = ti.xcom_pull(task_ids="transform_gold", key="gold_data")
    df = pd.DataFrame([record])
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    df.to_csv(CSV_PATH, mode="a", header=not os.path.exists(CSV_PATH), index=False)


def load_mysql(ti) -> None:
    record = ti.xcom_pull(task_ids="transform_gold", key="gold_data")
    df = pd.DataFrame([record])
    engine = create_engine(MYSQL_URL)

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS gold_prices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    symbol VARCHAR(50) NOT NULL,
                    price FLOAT NOT NULL,
                    currency VARCHAR(20) NOT NULL,
                    timestamp DATETIME NOT NULL
                )
                """
            )
        )
        df.to_sql("gold_prices", connection, if_exists="append", index=False)


with DAG(
    dag_id="gold_price_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["gold", "etl", "mysql"],
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
