from prefect import flow, task
import requests
import pandas as pd
import mysql.connector
import os
from datetime import datetime


API_KEY = ""




@task
def extract():


    print("Fetching gold prices...")


    url = "https://www.goldapi.io/api/XAU/USD"


    headers = {
        "x-access-token": API_KEY
    }


    response = requests.get(url, headers=headers)


    return response.json()




@task
def transform(data):


    print("Transforming data...")


    record = {
        "datetime": datetime.now(),
        "price_usd": data["price"],
        "price_gram_24k": data["price_gram_24k"],
        "price_gram_22k": data["price_gram_22k"],
        "price_gram_21k": data["price_gram_21k"],
        "change_percent": data["chp"]
    }


    return record




@task
def load_to_csv(record):


    print("Saving to CSV...")


    file_path = "data/gold_prices.csv"


    df = pd.DataFrame([record])


    if os.path.exists(file_path):


        df.to_csv(
            file_path,
            mode="a",
            header=False,
            index=False
        )


    else:


        df.to_csv(
            file_path,
            index=False
        )


    print("CSV Updated Successfully")




@task
def load_to_mysql(record):


    print("Loading to MySQL...")


    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gold_db"
    )


    cursor = conn.cursor()


    query = """
    INSERT INTO gold_prices
    (
        datetime,
        price_usd,
        price_gram_24k,
        price_gram_22k,
        price_gram_21k,
        change_percent
    )
    VALUES (%s,%s,%s,%s,%s,%s)
    """


    values = (
        str(record["datetime"]),
        record["price_usd"],
        record["price_gram_24k"],
        record["price_gram_22k"],
        record["price_gram_21k"],
        record["change_percent"]
    )


    cursor.execute(query, values)


    conn.commit()


    cursor.close()
    conn.close()


    print("Data Loaded To MySQL")




@flow(name="Gold Price ETL Pipeline")
def gold_pipeline():


    data = extract()


    record = transform(data)


    load_to_csv(record)


    load_to_mysql(record)


    print("Pipeline Completed")




#if __name__ == "__main__":
   # gold_pipeline()

from prefect.client.schemas.schedules import CronSchedule

if __name__ == "__main__":
    gold_pipeline.serve(
        name="gold-price-etl",
        cron="*/2 * * * *"  # every 2 minutes
    )