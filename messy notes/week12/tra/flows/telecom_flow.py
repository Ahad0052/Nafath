from prefect import flow, task
import pandas as pd
import sqlite3
import os


@task(retries=2)
def extract_task():

    file_path = "data/raw/Labor force in the Telecom Sector-2.xlsx"

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    df = pd.read_excel(
        file_path,
        sheet_name="التوظيف"
    )

    print(f"Rows Loaded: {len(df)}")

    return df


@task
def transform_task(df):

    df.columns = [
        "year",
        "total_employees",
        "omani_employees",
        "expat_employees",
        "tra_total",
        "tra_omani",
        "tra_expat"
    ]

    df = df.dropna()

    df["employee_growth_rate"] = (
        df["total_employees"]
        .pct_change()
        * 100
    )

    df["omanization_rate"] = (
        df["omani_employees"]
        /
        df["total_employees"]
        * 100
    )

    df["expat_ratio"] = (
        df["expat_employees"]
        /
        df["total_employees"]
        * 100
    )

    df["employee_growth_rate"] = (
        df["employee_growth_rate"]
        .fillna(0)
    )

    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(
        "data/processed/telecom_analytics.csv",
        index=False
    )

    print("Transformation Complete")

    return df


@task
def load_task(df):

    os.makedirs("db", exist_ok=True)

    conn = sqlite3.connect(
        "db/telecom.db"
    )

    raw_df = df[
        [
            "year",
            "total_employees",
            "omani_employees",
            "expat_employees",
            "tra_total",
            "tra_omani",
            "tra_expat"
        ]
    ]

    raw_df.to_sql(
        "raw_telecom_data",
        conn,
        if_exists="replace",
        index=False
    )

    df.to_sql(
        "telecom_analytics",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Database Loaded")


@flow(name="TRA Telecom Pipeline")
def telecom_pipeline():

    df = extract_task()

    transformed = transform_task(df)

    load_task(transformed)

    print("Pipeline Finished Successfully")


if __name__ == "__main__":
    telecom_pipeline()