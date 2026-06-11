# 🐍 Week 11 — ETL Pipelines, Docker & Workflow Orchestration
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [What is an ETL Pipeline?](#1-what-is-an-etl-pipeline)
2. [Project 1 — Store Sales ETL → MySQL](#2-project-1--store-sales-etl--mysql)
3. [Project 2 — Weather ETL (Basic)](#3-project-2--weather-etl-basic)
4. [Project 3 — Weather ETL + Docker](#4-project-3--weather-etl--docker)
5. [Project 4 — Weather ETL + Docker Compose (Backend + Frontend)](#5-project-4--weather-etl--docker-compose-backend--frontend)
6. [Project 5 — Gold Price ETL + Prefect](#6-project-5--gold-price-etl--prefect)
7. [Docker — Core Concepts](#7-docker--core-concepts)
8. [Prefect — Workflow Orchestration](#8-prefect--workflow-orchestration)
9. [Star Schema — Dimensional Modelling](#9-star-schema--dimensional-modelling)
10. [Notes & Tasks](#10-notes--tasks)

---

## 1. What is an ETL Pipeline?

> **ETL = Extract → Transform → Load**
> A pipeline that moves data from a source, cleans it, and loads it into a destination.

```
[Source]        [Transform]        [Destination]
API / CSV  →   clean, reshape   →  MySQL / CSV / warehouse
```

### Why structure it as three separate steps?
- **Separation of concerns** — each step has one job and can be tested independently
- **Reusability** — swap the source or destination without rewriting the logic
- **Debuggability** — when something breaks, you know exactly which step failed

### ETL vs ELT
| | ETL | ELT |
|--|-----|-----|
| Transform | Before loading | After loading |
| Best for | Relational DBs, strict schemas | Data warehouses (BigQuery, Snowflake) |

---

## 2. Project 1 — Store Sales ETL → MySQL

> Merges 3 messy CSV files, cleans them, and loads a normalised star schema into MySQL.

### Pipeline Structure
```
store_sales_1.csv ┐
store_sales_2.csv ├─ EXTRACT ─→ TRANSFORM ─→ LOAD into MySQL
store_sales_3.csv ┘
```

### Step 1 — Extract
```python
import pandas as pd

CSV_FILES = ["store_sales_1.csv", "store_sales_2.csv", "store_sales_3.csv"]
dfs = [pd.read_csv(f) for f in CSV_FILES]
raw = pd.concat(dfs, ignore_index=True)
print(f"[EXTRACT] {len(raw)} rows loaded from {len(CSV_FILES)} files.")
```

### Step 2 — Transform
```python
# Text normalisation
raw["StoreID"]      = raw["StoreID"].str.strip().str.upper().str.replace("-", "_")
raw["CurrencyType"] = raw["CurrencyType"].str.strip().str.upper()
raw["ProductName"]  = raw["ProductName"].str.strip().str.title()

# Remove junk product names from store_3
JUNK_NAMES = {"Line", "Actually", "Case", "Black", "On", "Soon", "Skill"}
raw = raw[~raw["ProductName"].isin(JUNK_NAMES)]

# Type conversion + null handling
raw["Qty"]        = pd.to_numeric(raw["Qty"],        errors="coerce")
raw["Unit_Price"] = pd.to_numeric(raw["Unit_Price"], errors="coerce")
raw["SaleDate"]   = pd.to_datetime(raw["SaleDate"],  errors="coerce")
raw = raw.dropna(subset=["SaleDate"])

# Impute missing prices using per-product median, then global median
raw["Unit_Price"] = raw.groupby("ProductName")["Unit_Price"].transform(
    lambda x: x.fillna(x.median())
)
raw["Unit_Price"] = raw["Unit_Price"].fillna(raw["Unit_Price"].median())

# Currency conversion to OMR
USD_TO_OMR = 0.385
raw["Unit_Price_OMR"]  = raw.apply(
    lambda r: round(r["Unit_Price"] * (USD_TO_OMR if r["CurrencyType"] == "USD" else 1.0), 4),
    axis=1
)
raw["Total_Price_OMR"] = (raw["Qty"] * raw["Unit_Price_OMR"]).round(4)
```

### Step 3 — Build Star Schema Dimension Tables
```python
# store dimension
stores_df = pd.DataFrame({"store_name": sorted(raw["StoreID"].unique())})
stores_df.index += 1
stores_df = stores_df.rename_axis("store_id").reset_index()

# customer dimension
customers_df = pd.DataFrame({"customer_uuid": sorted(raw["CustomerID"].unique())})
customers_df.index += 1
customers_df = customers_df.rename_axis("customer_id").reset_index()

# product dimension
products_df = pd.DataFrame({"product_name": sorted(raw["ProductName"].unique())})
products_df.index += 1
products_df = products_df.rename_axis("product_id").reset_index()

# Map FKs back onto raw and build sales fact table
raw["store_id"]    = raw["StoreID"].map(stores_df.set_index("store_name")["store_id"])
raw["customer_id"] = raw["CustomerID"].map(customers_df.set_index("customer_uuid")["customer_id"])
raw["product_id"]  = raw["ProductName"].map(products_df.set_index("product_name")["product_id"])
```

### Step 4 — Load into MySQL
```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="store_sales_db"
)
cur = conn.cursor()

# Create tables with FK relationships
cur.execute("""
    CREATE TABLE sales (
        sale_id         INT PRIMARY KEY,
        store_id        INT NOT NULL,
        customer_id     INT NOT NULL,
        product_id      INT NOT NULL,
        qty             INT NOT NULL,
        unit_price      DECIMAL(10,4),
        currency_type   VARCHAR(10),
        unit_price_omr  DECIMAL(10,4),
        total_price_omr DECIMAL(10,4),
        sale_date       DATE NOT NULL,
        FOREIGN KEY (store_id)    REFERENCES store(store_id),
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
        FOREIGN KEY (product_id)  REFERENCES product(product_id)
    )
""")

# Batch insert
cur.executemany("INSERT INTO sales VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", rows)
conn.commit()
```

---

## 3. Project 2 — Weather ETL (Basic)

> A simple 3-file ETL pipeline that calls the OpenWeatherMap API and saves output to CSV.

### Project Structure
```
weather/
├── src/
│   ├── extract.py     ← calls OpenWeatherMap API
│   ├── transform.py   ← flattens JSON to dict
│   ├── load.py        ← appends to CSV
│   └── main.py        ← orchestrates all three steps
├── data/
│   └── weather.csv
├── dockerfile
└── requirements.txt
```

### extract.py
```python
import requests, os
from dotenv import load_dotenv

def extract_weather():
    load_dotenv(override=True)
    api_key = os.getenv("API_KEY")
    city    = os.getenv("CITY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

### transform.py
```python
def transform_weather(data):
    return {
        "city":        data["name"],
        "temperature": data["main"]["temp"],
        "humidity":    data["main"]["humidity"],
        "pressure":    data["main"]["pressure"],
        "weather":     data["weather"][0]["main"]
    }
```

### load.py
```python
import pandas as pd, os

FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "weather.csv")

def load_to_csv(record):
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    df = pd.DataFrame([record])
    if os.path.exists(FILE_PATH):
        df.to_csv(FILE_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(FILE_PATH, index=False)
    print("CSV updated successfully")
```

### main.py
```python
from extract import extract_weather
from transform import transform_weather
from load import load_to_csv

def run_etl():
    raw_data        = extract_weather()
    transformed     = transform_weather(raw_data)
    load_to_csv(transformed)

if __name__ == "__main__":
    run_etl()
```

> 💡 **Key pattern:** `main.py` never contains business logic — it only calls the three steps in order. This keeps each file testable in isolation.

---

## 4. Project 3 — Weather ETL + Docker

> Same ETL pipeline, but packaged inside a Docker container so it runs anywhere — no local Python setup needed.

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
```

### requirements.txt
```
requests
pandas
python-dotenv
```

### Build & Run
```bash
# Build the image
docker build -t weather-etl .

# Run with .env file injected
docker run --env-file .env weather-etl
```

> 💡 **Why Docker?** Your code runs in an isolated environment with the exact Python version and packages it needs — regardless of what's installed on the host machine.

---

## 5. Project 4 — Weather ETL + Docker Compose (Backend + Frontend)

> Splits the ETL into a **Flask backend** and a **Streamlit frontend**, each in its own container, wired together with Docker Compose.

### Architecture
```
[User Browser]
      │
      ▼
[Streamlit Frontend  :8501] ──HTTP──→ [Flask Backend :5000]
                                              │
                                        Extract → Transform → Load (CSV)
                                              │
                                     [OpenWeatherMap API]
```

### docker-compose.yml
```yaml
services:
  weather-backend:
    build: ./backend
    container_name: weather-backend
    ports:
      - "5000:5000"
    env_file:
      - .env

  weather-frontend:
    build: ./frontend
    container_name: weather-frontend
    ports:
      - "8501:8501"
    environment:
      BACKEND_URL: http://weather-backend:5000
    depends_on:
      - weather-backend
```

### Backend — Flask API (src/main.py)
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from extract import extract_weather
from transform import transform_weather
from load import load_to_csv

app = Flask(__name__)
CORS(app)

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Muscat')
    try:
        raw         = extract_weather(city)
        transformed = transform_weather(raw)
        load_to_csv(transformed)
        return jsonify(transformed), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

> 💡 **`host="0.0.0.0"`** is required in Docker — it means "listen on all network interfaces inside the container" so Docker can map the port to the host.

### Frontend — Streamlit (app.py)
```python
import os, requests, streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

st.title("🌤 Weather ETL Dashboard")
city = st.text_input("Enter City", "Muscat")

if st.button("Get Weather", type="primary"):
    with st.spinner(f"Running ETL Pipeline for {city}..."):
        response = requests.get(f"{BACKEND_URL}/weather", params={"city": city}, timeout=10)
        data = response.json()
    st.success("ETL Pipeline Executed Successfully!")
    st.write(data)
```

### Run Everything
```bash
docker-compose up --build
# Frontend: http://localhost:8501
# Backend:  http://localhost:5000
```

### Key Docker Compose Concepts
| Concept | Explanation |
|---------|-------------|
| `services` | Each service = one container |
| `build` | Path to the Dockerfile for this service |
| `ports` | `"host:container"` port mapping |
| `env_file` | Inject a `.env` file into the container |
| `environment` | Set individual env vars |
| `depends_on` | Start this service after another one |

---

## 6. Project 5 — Gold Price ETL + Prefect

> Uses the **Prefect** library to orchestrate an ETL pipeline that fetches live gold prices and loads them to both CSV and MySQL.

### Prefect Decorators
```python
from prefect import flow, task

@task                        # a single unit of work
def extract():
    ...

@task
def transform(data):
    ...

@task
def load_to_csv(record):
    ...

@task
def load_to_mysql(record):
    ...

@flow(name="Gold Price ETL Pipeline")   # the full pipeline
def gold_pipeline():
    data   = extract()
    record = transform(data)
    load_to_csv(record)
    load_to_mysql(record)
```

### extract() — goldapi.io
```python
import requests

@task
def extract():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()
```

### transform()
```python
from datetime import datetime

@task
def transform(data):
    return {
        "datetime":       datetime.now(),
        "price_usd":      data["price"],
        "price_gram_24k": data["price_gram_24k"],
        "price_gram_22k": data["price_gram_22k"],
        "price_gram_21k": data["price_gram_21k"],
        "change_percent": data["chp"]
    }
```

### load_to_csv() — Append Mode
```python
import pandas as pd, os

@task
def load_to_csv(record):
    file_path = "data/gold_prices.csv"
    df = pd.DataFrame([record])
    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, index=False)
```

### Why Prefect?
| Feature | What it gives you |
|---------|------------------|
| `@task` decorator | Automatic retry, logging, state tracking per step |
| `@flow` decorator | Visual run history in Prefect UI |
| Scheduling | Run pipelines on a cron schedule from the UI |
| Observability | See exactly which task failed and why |

> 💡 Prefect turns a plain Python script into an observable, schedulable, retryable pipeline — without changing the logic.

---

## 7. Docker — Core Concepts

### Key Terms
| Term | Meaning |
|------|---------|
| **Image** | Blueprint — built from a Dockerfile, read-only |
| **Container** | Running instance of an image |
| **Dockerfile** | Recipe for building an image |
| **Docker Compose** | Tool for running multi-container apps |
| **Volume** | Persistent storage that survives container restarts |
| **Port mapping** | `"8501:8501"` → host port : container port |

### Dockerfile Anatomy
```dockerfile
FROM python:3.11-slim          # base image
WORKDIR /app                   # working directory inside container
COPY requirements.txt .        # copy files in
RUN pip install -r requirements.txt   # run commands at build time
COPY . .                       # copy rest of project
EXPOSE 5000                    # document which port the app uses
CMD ["python", "src/main.py"]  # command to run when container starts
```

### Essential Commands
```bash
docker build -t my-app .           # build image from Dockerfile in current dir
docker run my-app                  # run container from image
docker run --env-file .env my-app  # inject environment variables
docker ps                          # list running containers
docker stop <container_id>         # stop a container
docker images                      # list all images

docker-compose up --build          # build and start all services
docker-compose down                # stop and remove all containers
docker-compose logs                # view logs from all services
```

### .env Pattern — Never Hardcode Secrets
```bash
# .env file (never commit to git)
API_KEY=abc123
CITY=Muscat
DB_PASSWORD=secret
```

```python
# In Python
from dotenv import load_dotenv
import os

load_dotenv(override=True)
api_key = os.getenv("API_KEY")
```

---

## 8. Prefect — Workflow Orchestration

> Prefect adds **observability and scheduling** to plain Python functions with two decorators.

```python
from prefect import flow, task

@task(retries=3, retry_delay_seconds=10)   # retry on failure
def fetch_data():
    ...

@flow(name="My Pipeline", log_prints=True)
def my_pipeline():
    data = fetch_data()
    ...

if __name__ == "__main__":
    my_pipeline()    # run locally
```

### Prefect UI
```bash
prefect server start      # launch local Prefect UI
# http://localhost:4200
```

> The UI shows: every flow run, which tasks passed/failed, logs, duration, and run history — all without writing any logging code yourself.

---

## 9. Star Schema — Dimensional Modelling

> The store sales ETL produced a **star schema** — the standard structure for analytical databases.

```
              [store]
                 │
[customer] ──[sales]── [product]
```

### Fact vs Dimension Tables
| Table Type | Contains | Example |
|-----------|---------|---------|
| **Fact** | Measurements, events | `sales` (qty, price, date) |
| **Dimension** | Descriptive attributes | `store`, `customer`, `product` |

### Why Star Schema?
- Fast aggregation queries (`GROUP BY`, `SUM`)
- Easy to understand and extend
- Natural fit for BI tools like Power BI

---

## 10. Notes & Tasks

| # | Note |
|---|------|
| 📝 | ETL = Extract → Transform → Load — always keep the three steps separate |
| 📝 | `main.py` should only call the three steps — never contain business logic itself |
| 📝 | Impute missing values using per-group median first, then global median as fallback |
| 📝 | `pd.concat(dfs, ignore_index=True)` — reset the index when merging multiple CSVs |
| 📝 | `host="0.0.0.0"` in Flask is required inside Docker — `localhost` won't work |
| 📝 | `depends_on` in Docker Compose ensures containers start in the right order |
| 📝 | Prefect `@task` gives you retries, logging, and state tracking for free |
| 📝 | Never hardcode credentials — always use `.env` + `python-dotenv` |
| 📝 | `docker-compose up --build` rebuilds images; `docker-compose up` reuses existing ones |
| 📝 | Star schema = fact table (measurements) + dimension tables (descriptions) |
| 🔧 | **Task:** Add a scheduler to the weather ETL using `schedule` or Prefect |
| 🔧 | **Task:** Extend the gold pipeline to also load into MySQL |
| 🔧 | **Task:** Add a volume to the Docker Compose app so CSV data persists across restarts |
| 🔧 | **Task:** Push the weather ETL image to Docker Hub |
| 🔧 | **Task:** Explore `schedule` library for lightweight local cron jobs |

---

*📅 Notes taken: June 2026*
