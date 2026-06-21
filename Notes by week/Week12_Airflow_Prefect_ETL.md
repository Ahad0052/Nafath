# 🐍 Week 12 — Apache Airflow, Prefect + Docker & Real-World ETL
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [What is Workflow Orchestration?](#1-what-is-workflow-orchestration)
2. [Apache Airflow — Core Concepts](#2-apache-airflow--core-concepts)
3. [Project 1 — Gold Price ETL with Airflow](#3-project-1--gold-price-etl-with-airflow)
4. [Airflow + Docker Compose](#4-airflow--docker-compose)
5. [XCom — Passing Data Between Tasks](#5-xcom--passing-data-between-tasks)
6. [Prefect + Docker Compose](#6-prefect--docker-compose)
7. [Project 2 — Gold Price ETL with Prefect + Docker](#7-project-2--gold-price-etl-with-prefect--docker)
8. [Project 3 — TRA Telecom Analytics Pipeline](#8-project-3--tra-telecom-analytics-pipeline)
9. [Airflow vs Prefect — Comparison](#9-airflow-vs-prefect--comparison)
10. [Notes & Tasks](#10-notes--tasks)

---

## 1. What is Workflow Orchestration?

> Orchestration tools manage **when**, **how**, and **in what order** pipeline tasks run — and what to do when they fail.

### Without Orchestration
```
python pipeline.py   # runs once, you watch it, no retry, no scheduling, no history
```

### With Orchestration
```
✅ Schedule runs automatically (hourly, daily, cron)
✅ Retry failed tasks without restarting the whole pipeline
✅ Visual UI showing run history, task state, and logs
✅ Alerting when something goes wrong
```

### Airflow vs Prefect (week 12 covers both)
| Feature | Apache Airflow | Prefect |
|---------|---------------|---------|
| Pipeline unit | DAG (Directed Acyclic Graph) | Flow |
| Task unit | Operator | `@task` decorated function |
| Schedule | cron string in DAG definition | `cron=` in `.serve()` |
| Data passing | XCom | Return values |
| UI | Built-in web UI (port 8080) | Prefect Server UI (port 4200) |
| Setup | Heavier — needs its own DB | Lighter — pure Python |

---

## 2. Apache Airflow — Core Concepts

### DAG — Directed Acyclic Graph
> A DAG is the Airflow equivalent of a Prefect `@flow` — it defines the pipeline and how tasks connect.

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG(
    dag_id="my_pipeline",          # unique name shown in UI
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",            # cron or preset: @daily, @hourly, @once
    catchup=False,                 # don't backfill missed runs
    tags=["etl", "gold"],          # group DAGs in UI
) as dag:
    task_a = PythonOperator(
        task_id="step_one",
        python_callable=my_function,
    )
    task_b = PythonOperator(
        task_id="step_two",
        python_callable=my_other_function,
    )

    task_a >> task_b               # task_b runs after task_a
```

### Key DAG Parameters
| Parameter | Purpose |
|-----------|---------|
| `dag_id` | Unique identifier — shown in Airflow UI |
| `start_date` | When the DAG becomes active |
| `schedule` | How often to run — cron string or `@hourly`, `@daily` |
| `catchup=False` | Skip missed runs (always set this unless you need backfills) |
| `tags` | Labels to group and filter DAGs in the UI |

### PythonOperator
> The most common Airflow operator — runs any Python function as a task.

```python
from airflow.operators.python import PythonOperator

task = PythonOperator(
    task_id="extract_gold",
    python_callable=extract_gold,    # the function to call
)
```

### Task Dependencies
```python
# Linear chain
extract >> transform >> load

# Fan-out (transform runs after extract, then both csv and mysql run in parallel)
extract >> transform >> [csv_task, mysql_task]
```

---

## 3. Project 1 — Gold Price ETL with Airflow

> Fetches live gold prices from goldapi.io on an hourly schedule and loads to both CSV and MySQL.

### DAG Structure
```
extract_gold >> transform_gold >> save_csv
                               >> load_mysql
```

### extract_gold()
```python
def extract_gold() -> dict:
    response = requests.get(
        "https://www.goldapi.io/api/XAU/USD",
        headers={
            "x-access-token": os.getenv("GOLD_API_KEY"),
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
```

### transform_gold() — uses XCom
```python
def transform_gold(ti) -> None:
    data = ti.xcom_pull(task_ids="extract_gold")    # pull from previous task
    record = {
        "symbol":    data.get("metal", "XAU"),
        "price":     float(data["price"]),
        "currency":  data.get("currency", "USD"),
        "timestamp": _format_timestamp(data.get("timestamp")),
    }
    ti.xcom_push(key="gold_data", value=record)     # push for next task
```

### Timestamp Normalisation Helper
```python
def _format_timestamp(value) -> str:
    # API can return: None, Unix ms int, Unix s int, or ISO string
    if value is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, (int, float)):
        # Convert ms to s if timestamp is in milliseconds
        timestamp = value / 1000 if value > 10_000_000_000 else value
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    text_value = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text_value).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
```

### load_mysql() — SQLAlchemy + CREATE IF NOT EXISTS
```python
from sqlalchemy import create_engine, text

MYSQL_URL = "mysql+pymysql://root:root@mysql:3306/gold_db"

def load_mysql(ti) -> None:
    record = ti.xcom_pull(task_ids="transform_gold", key="gold_data")
    df = pd.DataFrame([record])
    engine = create_engine(MYSQL_URL)

    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS gold_prices (
                id        INT AUTO_INCREMENT PRIMARY KEY,
                symbol    VARCHAR(50)  NOT NULL,
                price     FLOAT        NOT NULL,
                currency  VARCHAR(20)  NOT NULL,
                timestamp DATETIME     NOT NULL
            )
        """))
        df.to_sql("gold_prices", connection, if_exists="append", index=False)
```

### Full DAG Definition
```python
with DAG(
    dag_id="gold_price_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["gold", "etl", "mysql"],
) as dag:

    extract   = PythonOperator(task_id="extract_gold",   python_callable=extract_gold)
    transform = PythonOperator(task_id="transform_gold", python_callable=transform_gold)
    csv_task  = PythonOperator(task_id="save_csv",       python_callable=save_csv)
    mysql_task= PythonOperator(task_id="load_mysql",     python_callable=load_mysql)

    extract >> transform >> csv_task >> mysql_task
```

---

## 4. Airflow + Docker Compose

### Dockerfile
```dockerfile
FROM apache/airflow:3.0.4

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
```

### docker-compose.yaml
```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: gold_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-proot"]
      interval: 10s
      timeout: 5s
      retries: 10

  airflow:
    build: .
    container_name: airflow
    restart: unless-stopped
    depends_on:
      mysql:
        condition: service_healthy     # waits for MySQL to be ready
    ports:
      - "8080:8080"                    # Airflow UI
    environment:
      GOLD_API_KEY: ${GOLD_API_KEY}
      AIRFLOW__CORE__LOAD_EXAMPLES: "false"
    volumes:
      - ./dags:/opt/airflow/dags       # mount DAGs folder — hot reload
      - ./data:/opt/airflow/data
    command: standalone

volumes:
  mysql_data:
```

### Key patterns
- `condition: service_healthy` — Airflow won't start until MySQL healthcheck passes
- `volumes: ./dags:/opt/airflow/dags` — edit DAGs locally, Airflow picks them up immediately
- `command: standalone` — runs all Airflow components in one container (scheduler + webserver + database)
- `AIRFLOW__CORE__LOAD_EXAMPLES: "false"` — hides the 30+ example DAGs from the UI

### Accessing Airflow UI
```bash
docker-compose up --build
# http://localhost:8080
# default credentials: admin / admin
```

---

## 5. XCom — Passing Data Between Tasks

> **XCom** (Cross-Communication) is Airflow's built-in mechanism for passing data between tasks. Without it, tasks are isolated and can't share results.

```python
# PUSH — store a value from this task
def my_task(ti):
    result = {"price": 3200.5, "currency": "USD"}
    ti.xcom_push(key="gold_data", value=result)

# PULL — retrieve a value from another task
def next_task(ti):
    data = ti.xcom_pull(task_ids="my_task", key="gold_data")
    print(data["price"])
```

> 💡 In Prefect, tasks pass data by simply returning values — much simpler. XCom is one of Airflow's rough edges compared to Prefect.

---

## 6. Prefect + Docker Compose

> Running Prefect with Docker Compose gives you a **persistent UI server** with scheduling — not just a one-off local run.

### docker-compose.yml (4 services)
```yaml
services:
  prefect-server:
    image: prefecthq/prefect:3-latest
    command: prefect server start --host 0.0.0.0
    ports:
      - "4200:4200"                     # Prefect UI
    healthcheck:
      test: ["CMD", "python", "/debug/debug_healthcheck.py"]
      interval: 10s
      retries: 12
      start_period: 90s                 # give server time to fully boot

  worker:
    image: prefecthq/prefect:3-latest
    command: >
      sh -c "prefect work-pool create default --type process 2>/dev/null || true
      && prefect worker start --pool default"
    depends_on:
      prefect-server:
        condition: service_healthy
    environment:
      - PREFECT_API_URL=http://prefect-server:4200/api

  mysql:
    image: mysql:8
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: golddb
    ports:
      - "3308:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-proot"]
      interval: 10s
      retries: 12
      start_period: 90s

  app:
    build: .
    depends_on:
      prefect-server:
        condition: service_healthy
      mysql:
        condition: service_healthy
    environment:
      - PREFECT_API_URL=http://prefect-server:4200/api
    volumes:
      - ./data:/app/data
```

### Serving a Flow with a Cron Schedule
```python
# Instead of gold_pipeline() — runs once
# Use .serve() to register with the Prefect server and run on a schedule

gold_pipeline.serve(
    name="gold-price-etl",
    cron="*/2 * * * *",          # every 2 minutes
    tags=["gold", "etl"],
)
```

### Startup Race Condition — Health Check Pattern
```python
# Problem: app container starts before Prefect server is fully ready
# Solution: poll the API health endpoint before calling .serve()

import httpx, time

server_ready = False
for i in range(15):
    try:
        response = httpx.get("http://prefect-server:4200/api/health")
        if response.status_code == 200:
            server_ready = True
            break
    except httpx.ConnectError:
        print(f"Prefect not ready yet (attempt {i+1}/15), retrying in 3s...")
        time.sleep(3)

if not server_ready:
    exit(1)

gold_pipeline.serve(name="gold-price-etl", cron="*/2 * * * *")
```

> 💡 `depends_on: condition: service_healthy` in Docker Compose is not always enough — containers can be "healthy" before the application inside is fully initialised. Polling in code gives you true readiness.

---

## 7. Project 2 — Gold Price ETL with Prefect + Docker

> Same gold pipeline from Week 11, now running **inside Docker** with a live Prefect server, a worker, and MySQL — all in one `docker-compose up`.

### flow.py — Key Additions vs Week 11
```python
@task
def transform(data):
    # Defensive check — crash with a clear message if API key is wrong
    if "price" not in data:
        raise ValueError(
            f"Expected key 'price' not found. Full API response: {data}"
        )
    return {
        "datetime":       datetime.now(),
        "price_usd":      data["price"],
        "price_gram_24k": data.get("price_gram_24k", 0),
        "price_gram_22k": data.get("price_gram_22k", 0),
        "price_gram_21k": data.get("price_gram_21k", 0),
        "change_percent": data.get("chp", 0),
        "api_timestamp":  data.get("timestamp"),
        "metal":          data.get("metal", "XAU"),
        "currency":       data.get("currency", "USD"),
    }

@task
def load_to_mysql(record):
    conn = mysql.connector.connect(
        host="mysql", user="root", password="root", database="golddb"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gold_prices (
            id             INT AUTO_INCREMENT PRIMARY KEY,
            datetime       DATETIME,
            price_usd      DECIMAL(12,4),
            price_gram_24k DECIMAL(12,4),
            price_gram_22k DECIMAL(12,4),
            price_gram_21k DECIMAL(12,4),
            change_percent DECIMAL(8,4),
            api_timestamp  BIGINT,
            metal          VARCHAR(10),
            currency       VARCHAR(10),
            created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        INSERT INTO gold_prices (
            datetime, price_usd, price_gram_24k, price_gram_22k,
            price_gram_21k, change_percent, api_timestamp, metal, currency
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        record["datetime"], record["price_usd"], record["price_gram_24k"],
        record["price_gram_22k"], record["price_gram_21k"], record["change_percent"],
        record["api_timestamp"], record["metal"], record["currency"],
    ))
    conn.commit()
    cursor.close()
    conn.close()
```

---

## 8. Project 3 — TRA Telecom Analytics Pipeline

> A Prefect ETL pipeline that processes **official TRA Oman labor force data** from an Excel file and loads it into SQLite.

### Dataset
- **Source:** Telecommunications Regulatory Authority (TRA) Oman
- **File:** `Labor force in the Telecom Sector-2.xlsx`
- **Sheet:** `التوظيف` (Arabic — Employment)

### Pipeline Structure
```
Extract (Excel) → Transform (clean + derive metrics) → Load (SQLite — 2 tables)
```

### extract_task()
```python
@task(retries=2)
def extract_task():
    df = pd.read_excel(
        "data/raw/Labor force in the Telecom Sector-2.xlsx",
        sheet_name="التوظيف"           # Arabic sheet name — pandas handles it
    )
    print(f"Rows Loaded: {len(df)}")
    return df
```

### transform_task() — Rename + Derive Metrics
```python
@task
def transform_task(df):
    df.columns = [
        "year", "total_employees", "omani_employees",
        "expat_employees", "tra_total", "tra_omani", "tra_expat"
    ]
    df = df.dropna()

    # Derived metrics
    df["employee_growth_rate"] = df["total_employees"].pct_change() * 100
    df["omanization_rate"]     = df["omani_employees"] / df["total_employees"] * 100
    df["expat_ratio"]          = df["expat_employees"] / df["total_employees"] * 100
    df["employee_growth_rate"] = df["employee_growth_rate"].fillna(0)

    df.to_csv("data/processed/telecom_analytics.csv", index=False)
    return df
```

### load_task() — Two Tables in SQLite
```python
@task
def load_task(df):
    conn = sqlite3.connect("db/telecom.db")

    # Raw table — original columns only
    raw_df = df[["year","total_employees","omani_employees",
                 "expat_employees","tra_total","tra_omani","tra_expat"]]
    raw_df.to_sql("raw_telecom_data", conn, if_exists="replace", index=False)

    # Analytics table — includes derived metrics
    df.to_sql("telecom_analytics", conn, if_exists="replace", index=False)

    conn.close()
```

### Business Insights
| Metric | Insight |
|--------|---------|
| `employee_growth_rate` | Year-on-year workforce growth — tied to broadband expansion and digital transformation |
| `omanization_rate` | % of Omani nationals in telecom workforce — tracks nationalisation progress |
| `expat_ratio` | Complement of Omanization — shows dependence on expatriate labour |

### SQLite Schema
```sql
CREATE TABLE raw_telecom_data (
    year INTEGER, total_employees INTEGER,
    omani_employees INTEGER, expat_employees INTEGER,
    tra_total INTEGER, tra_omani INTEGER, tra_expat INTEGER
);

CREATE TABLE telecom_analytics (
    year INTEGER, total_employees INTEGER,
    omani_employees INTEGER, expat_employees INTEGER,
    tra_total INTEGER, tra_omani INTEGER, tra_expat INTEGER,
    employee_growth_rate REAL,
    omanization_rate REAL,
    expat_ratio REAL
);
```

---

## 9. Airflow vs Prefect — Comparison

| | Apache Airflow | Prefect |
|--|---------------|---------|
| **Pipeline definition** | `with DAG(...) as dag:` | `@flow` decorator |
| **Task definition** | `PythonOperator(python_callable=fn)` | `@task` decorator on the function |
| **Data between tasks** | XCom — explicit push/pull | Return values — natural Python |
| **Scheduling** | `schedule=` in DAG | `cron=` in `.serve()` |
| **UI port** | 8080 | 4200 |
| **Setup complexity** | Higher — needs metadata DB, scheduler, webserver | Lower — lightweight server |
| **Best for** | Complex enterprise pipelines, large teams | Simpler setups, faster iteration |
| **Docker image** | `apache/airflow:3.0.4` | `prefecthq/prefect:3-latest` |

---

## 10. Notes & Tasks

| # | Note |
|---|------|
| 📝 | `catchup=False` in Airflow — always set this unless you explicitly need backfills |
| 📝 | `>>` in Airflow sets task dependency — `a >> b` means b runs after a |
| 📝 | XCom is Airflow's data-passing mechanism — `ti.xcom_push()` / `ti.xcom_pull()` |
| 📝 | `condition: service_healthy` in Docker Compose doesn't guarantee app readiness — poll in code too |
| 📝 | `gold_pipeline.serve(cron="*/2 * * * *")` — registers the flow with Prefect server on a schedule |
| 📝 | `AIRFLOW__CORE__LOAD_EXAMPLES: "false"` — remove the 30+ demo DAGs from the UI |
| 📝 | `command: standalone` — runs Airflow's scheduler + webserver in one container (good for dev) |
| 📝 | `pd.read_excel(sheet_name="التوظيف")` — pandas handles Arabic sheet names natively |
| 📝 | Two SQLite tables: raw (original) + analytics (with derived metrics) — good separation |
| 📝 | `pct_change()` computes row-by-row percentage change — useful for growth rates |
| 🔧 | **Task:** Add email alerting to Airflow when a task fails |
| 🔧 | **Task:** Explore `@hourly` vs cron strings — `0 * * * *` is the same as `@hourly` |
| 🔧 | **Task:** Add a fourth task to the TRA pipeline that generates a summary report |
| 🔧 | **Task:** Connect the TRA SQLite DB to a visualisation tool (Streamlit or Power BI) |
| 🔧 | **Task:** Try Airflow's `BashOperator` and `EmailOperator` |

---

*📅 Notes taken: June 2026*
