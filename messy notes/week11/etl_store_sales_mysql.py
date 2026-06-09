"""
ETL Pipeline - Store Sales → MySQL
====================================
Tables created:
  - store    (store_id PK, store_name)
  - customer (customer_id PK, customer_uuid)
  - product  (product_id PK, product_name)
  - sales    (sale_id PK, store_id FK, customer_id FK, product_id FK,
              qty, unit_price, currency_type, unit_price_omr,
              total_price_omr, sale_date)

Run from the week11 folder:
  python etl_store_sales_mysql.py
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error

# ============================================================
# CONFIG — update credentials as needed
# ============================================================
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",
    "database": "store_sales_db",
}

CSV_FILES = [
    "store_sales_1.csv",
    "store_sales_2.csv",
    "store_sales_3.csv",
]

USD_TO_OMR = 0.385  # fixed exchange rate

# ============================================================
# STEP 1: EXTRACT
# ============================================================
dfs = [pd.read_csv(f) for f in CSV_FILES]
raw = pd.concat(dfs, ignore_index=True)
print(f"[EXTRACT] {len(raw)} rows loaded from {len(CSV_FILES)} files.")

# ============================================================
# STEP 2: TRANSFORM
# ============================================================

# Text normalisation
raw["StoreID"]      = raw["StoreID"].str.strip().str.upper().str.replace("-", "_")
raw["CurrencyType"] = raw["CurrencyType"].str.strip().str.upper()
raw["ProductName"]  = raw["ProductName"].str.strip().str.title()

# Remove junk product names (single/nonsense words from store_3)
JUNK_NAMES = {"Line", "Actually", "Case", "Black", "On", "Soon", "Skill"}
raw = raw[~raw["ProductName"].isin(JUNK_NAMES)]

# Type conversion
raw["Qty"]        = pd.to_numeric(raw["Qty"],        errors="coerce")
raw["Unit_Price"] = pd.to_numeric(raw["Unit_Price"], errors="coerce")
raw["SaleDate"]   = pd.to_datetime(raw["SaleDate"],  errors="coerce", dayfirst=False)

# Drop rows with no SaleDate (unusable)
raw = raw.dropna(subset=["SaleDate"])

# Impute Unit_Price: per-product median, then global median
global_price_med = raw["Unit_Price"].median()
raw["Unit_Price"] = raw.groupby("ProductName")["Unit_Price"].transform(
    lambda x: x.fillna(x.median())
)
raw["Unit_Price"] = raw["Unit_Price"].fillna(global_price_med)

# Impute Qty: per-product median, then global median
global_qty_med = raw["Qty"].median()
raw["Qty"] = raw.groupby("ProductName")["Qty"].transform(
    lambda x: x.fillna(x.median())
)
raw["Qty"] = raw["Qty"].fillna(global_qty_med).round().astype(int)

# Fill remaining missing values
raw["CurrencyType"] = raw["CurrencyType"].fillna("USD")
raw["CustomerID"]   = raw["CustomerID"].fillna("UNKNOWN")

# Currency conversion → OMR
raw["Unit_Price_OMR"] = raw.apply(
    lambda r: round(r["Unit_Price"] * (USD_TO_OMR if r["CurrencyType"] == "USD" else 1.0), 4),
    axis=1
)
raw["Total_Price_OMR"] = (raw["Qty"] * raw["Unit_Price_OMR"]).round(4)

print(f"[TRANSFORM] Clean dataset: {len(raw)} rows, 0 nulls.")

# ============================================================
# STEP 3: BUILD DIMENSION + FACT TABLES
# ============================================================

# store dimension
stores_df = pd.DataFrame({"store_name": sorted(raw["StoreID"].unique())}).reset_index(drop=True)
stores_df.index += 1
stores_df = stores_df.rename_axis("store_id").reset_index()

# customer dimension
customers_df = pd.DataFrame({"customer_uuid": sorted(raw["CustomerID"].unique())}).reset_index(drop=True)
customers_df.index += 1
customers_df = customers_df.rename_axis("customer_id").reset_index()

# product dimension
products_df = pd.DataFrame({"product_name": sorted(raw["ProductName"].unique())}).reset_index(drop=True)
products_df.index += 1
products_df = products_df.rename_axis("product_id").reset_index()

# Map foreign keys back onto raw
raw["store_id"]    = raw["StoreID"].map(stores_df.set_index("store_name")["store_id"])
raw["customer_id"] = raw["CustomerID"].map(customers_df.set_index("customer_uuid")["customer_id"])
raw["product_id"]  = raw["ProductName"].map(products_df.set_index("product_name")["product_id"])

# sales fact table
sales_df = raw[["store_id", "customer_id", "product_id",
                "Qty", "Unit_Price", "CurrencyType",
                "Unit_Price_OMR", "Total_Price_OMR", "SaleDate"]].copy()
sales_df.columns = ["store_id", "customer_id", "product_id",
                    "qty", "unit_price", "currency_type",
                    "unit_price_omr", "total_price_omr", "sale_date"]
sales_df = sales_df.reset_index(drop=True)
sales_df.index += 1
sales_df = sales_df.rename_axis("sale_id").reset_index()

# ============================================================
# STEP 4: LOAD INTO MYSQL
# ============================================================
print("\n[LOAD] Connecting to MySQL ...")

try:
    # Create database if it doesn't exist
    init = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    c = init.cursor()
    c.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
    init.commit()
    c.close()
    init.close()
    print(f"[LOAD] Database `{DB_CONFIG['database']}` ready.")

    conn = mysql.connector.connect(**DB_CONFIG)
    cur  = conn.cursor()

    # DDL — drop in FK order, then recreate
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    for t in ("sales", "store", "customer", "product"):
        cur.execute(f"DROP TABLE IF EXISTS `{t}`")

    cur.execute("""
        CREATE TABLE store (
            store_id   INT          PRIMARY KEY,
            store_name VARCHAR(100) NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE customer (
            customer_id   INT          PRIMARY KEY,
            customer_uuid VARCHAR(100) NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE product (
            product_id   INT          PRIMARY KEY,
            product_name VARCHAR(150) NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE sales (
            sale_id         INT            PRIMARY KEY,
            store_id        INT            NOT NULL,
            customer_id     INT            NOT NULL,
            product_id      INT            NOT NULL,
            qty             INT            NOT NULL,
            unit_price      DECIMAL(10,4)  NOT NULL,
            currency_type   VARCHAR(10),
            unit_price_omr  DECIMAL(10,4)  NOT NULL,
            total_price_omr DECIMAL(10,4)  NOT NULL,
            sale_date       DATE           NOT NULL,
            FOREIGN KEY (store_id)    REFERENCES store(store_id),
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (product_id)  REFERENCES product(product_id)
        )
    """)
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
    print("[LOAD] Tables created: store, customer, product, sales")

    # Insert store
    cur.executemany(
        "INSERT INTO store (store_id, store_name) VALUES (%s, %s)",
        [(int(r.store_id), r.store_name) for _, r in stores_df.iterrows()]
    )
    conn.commit()
    print(f"[LOAD] store      -> {len(stores_df)} rows")

    # Insert customer
    cur.executemany(
        "INSERT INTO customer (customer_id, customer_uuid) VALUES (%s, %s)",
        [(int(r.customer_id), r.customer_uuid) for _, r in customers_df.iterrows()]
    )
    conn.commit()
    print(f"[LOAD] customer   -> {len(customers_df)} rows")

    # Insert product
    cur.executemany(
        "INSERT INTO product (product_id, product_name) VALUES (%s, %s)",
        [(int(r.product_id), r.product_name) for _, r in products_df.iterrows()]
    )
    conn.commit()
    print(f"[LOAD] product    -> {len(products_df)} rows")

    # Insert sales (batch)
    sales_rows = [
        (
            int(r.sale_id), int(r.store_id), int(r.customer_id), int(r.product_id),
            int(r.qty), float(r.unit_price), r.currency_type,
            float(r.unit_price_omr), float(r.total_price_omr),
            r.sale_date.date() if hasattr(r.sale_date, "date") else r.sale_date
        )
        for _, r in sales_df.iterrows()
    ]
    cur.executemany("""
        INSERT INTO sales
          (sale_id, store_id, customer_id, product_id,
           qty, unit_price, currency_type,
           unit_price_omr, total_price_omr, sale_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, sales_rows)
    conn.commit()
    print(f"[LOAD] sales      -> {len(sales_rows)} rows")

    # Verification
    print("\n========== VERIFICATION ==========")
    for table in ("store", "customer", "product", "sales"):
        cur.execute(f"SELECT COUNT(*) FROM `{table}`")
        print(f"  {table:<12}: {cur.fetchone()[0]:>5} rows")

    cur.execute("""
        SELECT p.product_name, SUM(s.total_price_omr) AS revenue
        FROM sales s JOIN product p USING (product_id)
        GROUP BY p.product_name
        ORDER BY revenue DESC LIMIT 5
    """)
    print("\nTop 5 products by revenue (OMR):")
    for name, rev in cur.fetchall():
        print(f"  {name:<35} {float(rev):>8.2f} OMR")
    print("===================================")

    cur.close()
    conn.close()
    print("\n[DONE] ETL complete - all data loaded into MySQL successfully!")

except Error as e:
    print(f"[ERROR] MySQL: {e}")
    raise
