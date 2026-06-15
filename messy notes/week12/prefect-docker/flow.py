from prefect import flow, task
import requests
import pandas as pd
import mysql.connector
import os
import time
import httpx
from datetime import datetime

DEBUG_LOG = "/debug/debug-72a1c8.log"

def _debug_log(hypothesis_id, location, message, data):
    # #region agent log
    import json
    entry = {
        "sessionId": "72a1c8",
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    try:
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except OSError:
        pass
    # #endregion

API_KEY = ""

@task
def extract():
    print("Fetching gold prices...")
    url = "https://www.goldapi.io/api/XAU/USD"
    
    # Make sure you place your real API key token inside this string!
    headers = {
        "x-access-token": API_KEY if API_KEY else "YOUR_TOKEN_HERE"
    }

    response = requests.get(url, headers=headers)
    json_data = response.json()
    
    # Safely print out the payload so you can see what keys are actually present
    print(f"API raw response payload: {json_data}")
    return json_data

@task
def transform(data):
    print("Transforming data...")
    
    # Defensive programming: catch missing key errors cleanly
    if "price" not in data:
        raise ValueError(f"Expected key 'price' not found in response data. Full API response was: {data}")

    record = {
        "datetime": datetime.now(),
        "price_usd": data["price"],
        "price_gram_24k": data.get("price_gram_24k", 0),
        "price_gram_22k": data.get("price_gram_22k", 0),
        "price_gram_21k": data.get("price_gram_21k", 0),
        "change_percent": data.get("chp", 0),
        "api_timestamp": data.get("timestamp"),
        "metal": data.get("metal", "XAU"),
        "currency": data.get("currency", "USD"),
    }

    return record
@task
def load_to_csv(record):
    print("Saving to CSV...")
    file_path = "data/gold_prices.csv"
    csv_columns = [
        "datetime", "price_usd", "price_gram_24k",
        "price_gram_22k", "price_gram_21k", "change_percent",
    ]
    df = pd.DataFrame([{col: record[col] for col in csv_columns}])
    
    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, index=False)
    print("CSV Updated Successfully")

@task
def load_to_mysql(record):
    print("Loading to MySQL...")
    # #region agent log
    _debug_log("H6", "flow.py:load_to_mysql", "mysql_load_start", {"record_keys": list(record.keys())})
    # #endregion
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root",
            database="golddb"
        )
    except mysql.connector.Error as exc:
        # #region agent log
        _debug_log("H6", "flow.py:load_to_mysql", "mysql_connect_failed", {"error": str(exc)})
        # #endregion
        raise
    cursor = conn.cursor()

    print("Ensuring target database schema exists...")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS gold_prices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        datetime DATETIME,
        price_usd DECIMAL(12, 4),
        price_gram_24k DECIMAL(12, 4),
        price_gram_22k DECIMAL(12, 4),
        price_gram_21k DECIMAL(12, 4),
        change_percent DECIMAL(8, 4),
        api_timestamp BIGINT,
        metal VARCHAR(10),
        currency VARCHAR(10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)

    print("Executing database insertion...")
    query = """
    INSERT INTO gold_prices (
        datetime, price_usd, price_gram_24k, price_gram_22k,
        price_gram_21k, change_percent, api_timestamp, metal, currency
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        record["datetime"],
        record["price_usd"],
        record["price_gram_24k"],
        record["price_gram_22k"],
        record["price_gram_21k"],
        record["change_percent"],
        record["api_timestamp"],
        record["metal"],
        record["currency"],
    )
    
    cursor.execute(query, values)
    conn.commit()
    # #region agent log
    _debug_log("H6", "flow.py:load_to_mysql", "mysql_insert_success", {"row_count": cursor.rowcount})
    # #endregion
    cursor.close()
    conn.close()
    print("MySQL Loading Complete!")
@flow(name="Gold Price ETL Pipeline")
def gold_pipeline():
    data = extract()
    record = transform(data)
    load_to_csv(record)
    load_to_mysql(record)
    print("Pipeline Completed")

if __name__ == "__main__":
    # --- PREVENT RACE CONDITION ON STARTUP ---
    print("Checking connection to Prefect Server API...")
    server_ready = False
    for i in range(15):
        try:
            # Pings the internal docker-compose service network address
            response = httpx.get("http://prefect-server:4200/api/health")
            if response.status_code == 200:
                print("Successfully paired with Prefect Server API!")
                server_ready = True
                break
        except httpx.ConnectError:
            print(f"Prefect Server isn't fully initialized yet (attempt {i+1}/15). Retrying in 3s...")
            time.sleep(3)

    if not server_ready:
        # #region agent log
        _debug_log("H7", "flow.py:main", "prefect_server_unreachable", {"attempts": 15})
        # #endregion
        print("Could not connect to Prefect Server API. Exiting script to avoid a silent crash.")
        exit(1)

    # #region agent log
    _debug_log("H8", "flow.py:main", "prefect_serve_starting", {"deployment": "gold-price-etl"})
    # #endregion
    # --- SERVE FLOW WITH CRON SCHEDULE ---
    gold_pipeline.serve(
        name="gold-price-etl",
        cron="*/2 * * * *",
        tags=["gold", "etl"],
    )