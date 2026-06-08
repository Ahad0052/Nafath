"""
ETL Pipeline - OpenWeatherMap → MySQL Workbench
================================================
Runs every 1 minute automatically.

Tables created in `weather_db`:
  - city        (city_id PK, city_name, country, latitude, longitude)
  - weather_raw (record_id PK, city_id FK, fetched_at,
                 temp_c, feels_like_c, temp_min_c, temp_max_c,
                 humidity_pct, pressure_hpa, visibility_m,
                 wind_speed_ms, wind_deg, cloudiness_pct,
                 weather_main, weather_desc, sunrise_utc, sunset_utc)

Steps:
  1. EXTRACT  - Call OpenWeatherMap Current Weather API
  2. TRANSFORM - Clean, type-cast, unit-convert, handle nulls
  3. LOAD      - Upsert into MySQL Workbench (localhost)

Run:
  python etl_weather_mysql.py
"""

import time
import sys
import schedule
import requests
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# ============================================================
# CONFIG — update your API key and cities here
# ============================================================
API_KEY = "0e1c8d13e239eec0f772c626df2fea99"   # <- paste your key from openweathermap.org/api_keys

CITIES = [
    "Muscat",
    "Dubai",
    "London",
    "New York",
    "Tokyo",
]

DB_CONFIG = {
    "username": "root",
    "password": "Q)(RZ5t9",
    "host":     "localhost",
    "database": "weather_db",
}

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ============================================================
# DATABASE ENGINE
# ============================================================
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}",
    echo=False,
)

# ============================================================
# STEP 0: ENSURE DATABASE EXISTS
# ============================================================
def ensure_database():
    import pymysql
    conn = pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["username"],
        password=DB_CONFIG["password"],
    )
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
    conn.commit()
    conn.close()
    print(f"[INIT] Database `{DB_CONFIG['database']}` ready.")


# ============================================================
# STEP 1: CREATE TABLES
# ============================================================
def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS city (
                city_id      INT AUTO_INCREMENT PRIMARY KEY,
                city_name    VARCHAR(100) NOT NULL,
                country      VARCHAR(10),
                latitude     DECIMAL(9,6),
                longitude    DECIMAL(9,6),
                UNIQUE KEY uq_city (city_name, country)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS weather_raw (
                record_id       INT AUTO_INCREMENT PRIMARY KEY,
                city_id         INT NOT NULL,
                fetched_at      DATETIME NOT NULL,
                temp_c          DECIMAL(6,2),
                feels_like_c    DECIMAL(6,2),
                temp_min_c      DECIMAL(6,2),
                temp_max_c      DECIMAL(6,2),
                humidity_pct    TINYINT UNSIGNED,
                pressure_hpa    SMALLINT UNSIGNED,
                visibility_m    INT,
                wind_speed_ms   DECIMAL(6,2),
                wind_deg        SMALLINT UNSIGNED,
                cloudiness_pct  TINYINT UNSIGNED,
                weather_main    VARCHAR(50),
                weather_desc    VARCHAR(100),
                sunrise_utc     DATETIME,
                sunset_utc      DATETIME,
                FOREIGN KEY (city_id) REFERENCES city(city_id)
            )
        """))

        conn.commit()
    print("[INIT] Tables `city` and `weather_raw` ready.")


# ============================================================
# STEP 2: EXTRACT - fetch raw JSON from OpenWeatherMap API
# ============================================================
def extract(city_name: str):
    params = {
        "q":     city_name,
        "appid": API_KEY,
        "units": "metric",   # Celsius
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        print(f"[EXTRACT] HTTP error for '{city_name}': {e}")
    except requests.exceptions.ConnectionError:
        print(f"[EXTRACT] Connection error - check internet/API key.")
    except requests.exceptions.Timeout:
        print(f"[EXTRACT] Timeout for '{city_name}'.")
    return None


# ============================================================
# STEP 3: TRANSFORM - clean + normalise one API response
# ============================================================
def transform(raw: dict) -> dict:
    """
    Flatten the nested OpenWeatherMap JSON into a clean flat dict.
    Handles missing keys gracefully with None fallbacks.
    """

    def safe_get(d, *keys, default=None):
        """Safely navigate nested dict keys."""
        for k in keys:
            if not isinstance(d, dict):
                return default
            d = d.get(k, default)
        return d

    def to_float_rounded(val):
        if val is None:
            return None
        return round(float(val), 2)

    def ts_to_datetime(ts):
        """Unix timestamp -> UTC datetime."""
        if ts is None:
            return None
        try:
            return datetime.fromtimestamp(int(ts), tz=timezone.utc).replace(tzinfo=None)
        except Exception:
            return None

    # --- City metadata ---
    city_name  = safe_get(raw, "name", default="").strip().title()
    country    = safe_get(raw, "sys", "country", default="").strip().upper()
    latitude   = safe_get(raw, "coord", "lat")
    longitude  = safe_get(raw, "coord", "lon")

    # Validate coords range
    if latitude is not None:
        latitude = float(latitude) if -90 <= float(latitude) <= 90 else None
    if longitude is not None:
        longitude = float(longitude) if -180 <= float(longitude) <= 180 else None

    # --- Main weather fields ---
    temp_c       = to_float_rounded(safe_get(raw, "main", "temp"))
    feels_like_c = to_float_rounded(safe_get(raw, "main", "feels_like"))
    temp_min_c   = to_float_rounded(safe_get(raw, "main", "temp_min"))
    temp_max_c   = to_float_rounded(safe_get(raw, "main", "temp_max"))

    # Humidity: must be 0-100
    humidity = safe_get(raw, "main", "humidity")
    humidity_pct = int(humidity) if humidity is not None and 0 <= int(humidity) <= 100 else None

    # Pressure: must be > 0
    pressure = safe_get(raw, "main", "pressure")
    pressure_hpa = int(pressure) if pressure is not None and int(pressure) > 0 else None

    # Visibility
    vis = safe_get(raw, "visibility")
    visibility_m = int(vis) if vis is not None else None

    # Wind
    wind_speed = safe_get(raw, "wind", "speed")
    wind_speed_ms = round(float(wind_speed), 2) if wind_speed is not None else None
    wind_deg = safe_get(raw, "wind", "deg")
    wind_deg = int(wind_deg) if wind_deg is not None and 0 <= int(wind_deg) <= 360 else None

    # Clouds
    clouds = safe_get(raw, "clouds", "all")
    cloudiness_pct = int(clouds) if clouds is not None and 0 <= int(clouds) <= 100 else None

    # Weather description (list, take first element)
    weather_list = raw.get("weather", [{}])
    weather_main = weather_list[0].get("main", "").strip().title() if weather_list else None
    weather_desc = weather_list[0].get("description", "").strip().capitalize() if weather_list else None

    # Sunrise / Sunset
    sunrise_utc = ts_to_datetime(safe_get(raw, "sys", "sunrise"))
    sunset_utc  = ts_to_datetime(safe_get(raw, "sys", "sunset"))

    return {
        # city fields
        "city_name":  city_name,
        "country":    country,
        "latitude":   latitude,
        "longitude":  longitude,
        # weather fields
        "fetched_at":      datetime.utcnow(),
        "temp_c":          temp_c,
        "feels_like_c":    feels_like_c,
        "temp_min_c":      temp_min_c,
        "temp_max_c":      temp_max_c,
        "humidity_pct":    humidity_pct,
        "pressure_hpa":    pressure_hpa,
        "visibility_m":    visibility_m,
        "wind_speed_ms":   wind_speed_ms,
        "wind_deg":        wind_deg,
        "cloudiness_pct":  cloudiness_pct,
        "weather_main":    weather_main,
        "weather_desc":    weather_desc,
        "sunrise_utc":     sunrise_utc,
        "sunset_utc":      sunset_utc,
    }


# ============================================================
# STEP 4: LOAD - upsert city, then insert weather record
# ============================================================
def load(record: dict):
    city_upsert = text("""
        INSERT INTO city (city_name, country, latitude, longitude)
        VALUES (:city_name, :country, :latitude, :longitude)
        ON DUPLICATE KEY UPDATE
            latitude  = VALUES(latitude),
            longitude = VALUES(longitude)
    """)

    city_id_query = text("""
        SELECT city_id FROM city
        WHERE city_name = :city_name AND country = :country
    """)

    weather_insert = text("""
        INSERT INTO weather_raw (
            city_id, fetched_at,
            temp_c, feels_like_c, temp_min_c, temp_max_c,
            humidity_pct, pressure_hpa, visibility_m,
            wind_speed_ms, wind_deg, cloudiness_pct,
            weather_main, weather_desc,
            sunrise_utc, sunset_utc
        ) VALUES (
            :city_id, :fetched_at,
            :temp_c, :feels_like_c, :temp_min_c, :temp_max_c,
            :humidity_pct, :pressure_hpa, :visibility_m,
            :wind_speed_ms, :wind_deg, :cloudiness_pct,
            :weather_main, :weather_desc,
            :sunrise_utc, :sunset_utc
        )
    """)

    try:
        with engine.begin() as conn:
            # Upsert city
            conn.execute(city_upsert, {
                "city_name": record["city_name"],
                "country":   record["country"],
                "latitude":  record["latitude"],
                "longitude": record["longitude"],
            })

            # Get city_id
            result = conn.execute(city_id_query, {
                "city_name": record["city_name"],
                "country":   record["country"],
            })
            city_id = result.fetchone()[0]

            # Insert weather reading
            conn.execute(weather_insert, {**record, "city_id": city_id})

    except SQLAlchemyError as e:
        print(f"[LOAD] DB error for {record['city_name']}: {e}")
        raise


# ============================================================
# MAIN ETL FUNCTION - called every 1 minute by scheduler
# ============================================================
def run_etl_pipeline():
    print(f"\n{'='*50}")
    print(f"  ETL Job Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    results = []
    for city in CITIES:
        print(f"\n[ETL] Processing: {city}")

        # EXTRACT
        raw_json = extract(city)
        if raw_json is None:
            print(f"  [SKIP] No data returned for '{city}'.")
            continue

        # TRANSFORM
        clean_record = transform(raw_json)

        # Sanity check
        if clean_record["temp_c"] is None:
            print(f"  [SKIP] Temperature missing after transform for '{city}'.")
            continue

        # LOAD
        load(clean_record)

        results.append(clean_record)
        print(
            f"  OK {clean_record['city_name']}, {clean_record['country']} | "
            f"{clean_record['temp_c']}C, feels {clean_record['feels_like_c']}C | "
            f"{clean_record['weather_desc']} | "
            f"Humidity {clean_record['humidity_pct']}% | "
            f"Wind {clean_record['wind_speed_ms']} m/s"
        )

    # Summary
    if results:
        df = pd.DataFrame(results)[["city_name", "country", "temp_c", "humidity_pct",
                                     "wind_speed_ms", "weather_desc"]]
        print(f"\n{'='*50}")
        print("  SUMMARY - latest readings loaded into MySQL")
        print(f"{'='*50}")
        print(df.to_string(index=False))
        print(f"\n  Total records inserted: {len(results)} / {len(CITIES)} cities")

    print(f"\n  ETL Job Finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")


# ============================================================
# ENTRY POINT - run once immediately, then every 1 minute
# ============================================================
if __name__ == "__main__":
    # One-time setup
    ensure_database()
    create_tables()

    # Run immediately on startup
    run_etl_pipeline()

    # Schedule every 1 minute (skip inside interactive notebooks)
    if not hasattr(sys, "ps1"):
        schedule.every(1).minutes.do(run_etl_pipeline)
        print("[Scheduler] Running every 1 minute. Press Ctrl+C to stop.\n")
        while True:
            schedule.run_pending()
            time.sleep(1)
