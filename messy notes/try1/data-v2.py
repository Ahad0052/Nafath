import osmnx as ox
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================================
# CONFIGURATION
# ============================================================

PLACE_NAME = "Muscat Governorate, Oman"

# Number of unique roads to simulate
# Increase if your PC has enough RAM/storage
ROAD_SAMPLE_SIZE = 500

# Traffic observation every 4 hours
INTERVAL_HOURS = 4

# Historical period
YEARS_HISTORY = 3

# ============================================================
# DOWNLOAD MUSCAT ROAD NETWORK
# ============================================================

print(f"Downloading road network for {PLACE_NAME}...")

graph = ox.graph_from_place(
    PLACE_NAME,
    network_type="drive"
)

nodes, edges = ox.graph_to_gdfs(graph)

print(f"Downloaded {len(edges):,} road segments")

# ============================================================
# EXTRACT ROAD NAMES
# ============================================================

roads = edges.copy()

roads = roads[roads["name"].notna()]

# Some roads have multiple names stored as lists
roads = roads.explode("name")

# Remove empty names
roads = roads[roads["name"].notna()]

# Keep only useful columns
columns = ["name"]

if "maxspeed" in roads.columns:
    columns.append("maxspeed")

roads = roads[columns].copy()

# Remove duplicate road names
roads = roads.drop_duplicates(subset=["name"])

print(f"Found {len(roads):,} unique named roads")

# Save road list
roads[["name"]].to_csv(
    "muscat_all_named_roads.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Saved road names to muscat_all_named_roads.csv")

# ============================================================
# SAMPLE ROADS FOR ML DATASET
# ============================================================

if len(roads) > ROAD_SAMPLE_SIZE:
    roads = roads.sample(
        ROAD_SAMPLE_SIZE,
        random_state=42
    )

print(f"Using {len(roads)} roads for simulation")

# ============================================================
# CLEAN SPEED LIMITS
# ============================================================

if "maxspeed" in roads.columns:

    roads["speed_limit"] = (
        roads["maxspeed"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(float)
    )

    roads["speed_limit"] = roads["speed_limit"].fillna(80)

else:
    roads["speed_limit"] = 80

# ============================================================
# CREATE HISTORICAL TIMESTAMPS
# ============================================================

start_date = datetime.now() - timedelta(days=365 * YEARS_HISTORY)

date_list = [
    start_date + timedelta(hours=x)
    for x in range(
        0,
        YEARS_HISTORY * 365 * 24,
        INTERVAL_HOURS
    )
]

print(f"Generated {len(date_list):,} timestamps")

# ============================================================
# GENERATE TRAFFIC DATA
# ============================================================

print("Generating synthetic traffic history...")

records = []

for _, road in roads.iterrows():

    road_name = str(road["name"])
    speed_limit = float(road["speed_limit"])

    for dt in date_list:

        hour = dt.hour
        day_of_week = dt.weekday()

        # Default free-flow
        traffic_factor = np.random.uniform(0.80, 1.00)

        # Oman work week:
        # Sunday(6) -> Thursday(3)
        if day_of_week not in [4, 5]:

            # Morning rush
            if 7 <= hour <= 9:
                traffic_factor = np.random.uniform(0.30, 0.50)

            # Afternoon rush
            elif 14 <= hour <= 16:
                traffic_factor = np.random.uniform(0.40, 0.60)

            # Evening
            elif 17 <= hour <= 20:
                traffic_factor = np.random.uniform(0.50, 0.75)

        else:
            # Weekend evenings
            if 18 <= hour <= 22:
                traffic_factor = np.random.uniform(0.50, 0.70)

        observed_speed = round(
            speed_limit * traffic_factor,
            2
        )

        congestion_index = round(
            1 - traffic_factor,
            2
        )

        records.append(
            {
                "road_name": road_name,
                "speed_limit": speed_limit,
                "timestamp": dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "hour": hour,
                "day_of_week": day_of_week,
                "observed_speed_kmh": observed_speed,
                "congestion_index": congestion_index
            }
        )

# ============================================================
# CREATE DATAFRAME
# ============================================================

ml_dataset = pd.DataFrame(records)

print(f"Generated {len(ml_dataset):,} rows")

# ============================================================
# SAVE DATASET
# ============================================================

output_file = "muscat_historical_traffic_dataset.csv"

ml_dataset.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("\nSUCCESS")
print(f"Dataset saved: {output_file}")
print(f"Rows: {len(ml_dataset):,}")

print("\nSample:")
print(ml_dataset.head())

