# Gold Airflow Project

This project runs a beginner-friendly ETL pipeline with Docker, Apache Airflow,
GoldAPI, Pandas, CSV storage, and MySQL.

## What It Does

1. Extracts the current XAU/USD gold price from GoldAPI.
2. Transforms the API response into a simple record.
3. Appends the record to `data/gold_prices.csv`.
4. Loads the same record into the MySQL `gold_prices` table.

## Start the Project

```bash
docker compose build
docker compose up -d
```

Open Airflow:

```text
http://localhost:8080
```

Airflow standalone prints the generated admin password in the container logs:

```bash
docker logs airflow
```

Look for the username and password, then enable and trigger:

```text
gold_price_pipeline
```

## Check the CSV

```bash
docker exec -it airflow bash
cat /opt/airflow/data/gold_prices.csv
```

## Check MySQL

```bash
docker exec -it mysql mysql -uroot -proot
USE gold_db;
SELECT * FROM gold_prices;
```
