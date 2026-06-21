import osmnx as ox
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print(" Fetching real Muscat freeway structures...")
place_name = "Muscat, Oman"
freeway_filter = '["highway"~"motorway|trunk|primary"]'

graph = ox.graph_from_place(place_name, network_type="drive", custom_filter=freeway_filter)
nodes, edges = ox.graph_to_gdfs(graph)

# Clean up our real road base
roads = edges[["name", "maxspeed"]].dropna(subset=['name']).copy()
# Standardize speed limits to numbers (defaulting to 100 if missing)
roads['speed_limit'] = roads['maxspeed'].astype(str).str.extract(r'(\d+)').astype(float).fillna(100)

print(f" Loaded {len(roads)} real Muscat road links. Simulating 3-Year historical timelines...")

# Generate a list of timestamps over the past 3 years (sampling specific intervals to keep files manageable)
start_date = datetime.now() - timedelta(days=3*365)
date_list = [start_date + timedelta(hours=x) for x in range(0, 3*365*24, 4)] # Sample every 4 hours

ml_records = []

# Generate dynamic traffic attributes matching real-world Oman behavior patterns
for index, row in roads.head(50).iterrows(): # Using top 50 segments for performance
    for dt in date_list:
        hour = dt.hour
        day_of_week = dt.weekday() # 4 = Friday, 5 = Saturday in western convention, align to Oman weekend
        
        # Base multiplier for speed
        traffic_factor = 1.0
        
        # Define Omani Rush Hours (Morning: 7-9 AM school/office, Afternoon: 2-4 PM homebound)
        if day_of_week not in [4, 5]: # Weekdays (Sunday - Thursday)
            if 7 <= hour <= 9:
                traffic_factor = np.random.uniform(0.3, 0.5) # Heavy drop in speed
            elif 14 <= hour <= 16:
                traffic_factor = np.random.uniform(0.4, 0.6) # Moderate drop
            else:
                traffic_factor = np.random.uniform(0.8, 1.0) # Free flowing
        else: # Weekends (Friday/Saturday evening congestion near commercial spots)
            if 18 <= hour <= 22:
                traffic_factor = np.random.uniform(0.5, 0.7)
            else:
                traffic_factor = np.random.uniform(0.9, 1.0)
                
        observed_speed = round(row['speed_limit'] * traffic_factor, 2)
        
        # Calculate Congestion Index (0 = Free flow, 1 = Gridlock)
        congestion_index = round(1.0 - traffic_factor, 2)
        
        ml_records.append({
            "road_name": row['name'],
            "speed_limit": row['speed_limit'],
            "timestamp": dt.strftime('%Y-%m-%d %H:%M:%S'),
            "hour": hour,
            "day_of_week": day_of_week,
            "observed_speed_kmh": observed_speed,
            "congestion_index": congestion_index # Target Variable for ML
        })

# Convert to ML ready DataFrame
ml_dataset = pd.DataFrame(ml_records)

# Save to CSV for your ML models
ml_dataset.to_csv("muscat_historical_traffic_dataset.csv", index=False)
print("\nSuccess! ML Dataset compiled and saved as 'muscat_historical_traffic_dataset.csv'")
print(f"Total Rows generated for training: {len(ml_dataset)}")
print(ml_dataset.head(10))