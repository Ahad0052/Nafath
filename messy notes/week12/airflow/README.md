# Gold Airflow ETL Project

This project runs a beginner-friendly data engineering pipeline with Docker, Apache Airflow, GoldAPI, Pandas, CSV storage, and MySQL.

## Project Flow

GoldAPI -> Airflow DAG -> Extract -> Transform -> Save CSV -> Load MySQL

## Setup

1. Create a local `.env` file:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace `YOUR_GOLDAPI_KEY` with your GoldAPI key.

3. Build and start the containers:

   ```powershell
   .\start.ps1
   ```

4. Open Airflow:

   ```text
   http://localhost:8080
   ```

5. Find the standalone Airflow password:

   ```bash
   docker logs airflow
   ```

6. Enable and trigger the `gold_price_pipeline` DAG.

## Verify CSV Output

```powershell
docker exec -it airflow bash
cat /opt/airflow/data/gold_prices.csv
```

## Verify MySQL Output

```powershell
docker exec -it mysql mysql -uroot -proot
USE gold_db;
SELECT * FROM gold_prices;
```

## Reset The Project Containers

```powershell
.\reset.ps1
```
