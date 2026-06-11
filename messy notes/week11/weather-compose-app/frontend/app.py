import os
import requests
import streamlit as st

# Keep this! Docker Compose will override 'localhost' with 'weather-backend'
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

# Page configuration for a nicer look
st.set_page_config(page_title="Weather Dashboard", page_icon="🌤", layout="centered")

st.title("🌤 Weather ETL Dashboard")
st.write("Real-time weather data processed through our Python ETL pipeline.")

# City Input Box
city = st.text_input("Enter City", "Muscat")

if st.button("Get Weather", type="primary"):
    if not city.strip():
        st.warning("Please enter a valid city name.")
    else:
        try:
            # 1. Show a loading spinner while the ETL pipeline runs in the backend
            with st.spinner(f"Running ETL Pipeline for {city}..."):
                response = requests.get(f"{BACKEND_URL}/weather", params={"city": city}, timeout=10)
                response.raise_for_status()
                data = response.json()

            # 2. Handle Errors safely
            if isinstance(data, dict) and "error" in data:
                st.error(f"Backend Error: {data['error']}")
            else:
                st.success("✨ ETL Pipeline Executed and Loaded to CSV Successfully!")
                st.subheader(f"📊 Weather Analysis for {city}")
                
                # 3. Clean Display of your Transformed Data
                # (Adjust these keys to match the exact keys returned by your transform_weather script)
                st.write(data) 
                
                # Example of displaying nicely using metric cards if your keys match:
                # col1, col2 = st.columns(2)
                # with col1:
                #     st.metric(label="Temperature", value=f"{data.get('temperature', 'N/A')}°C")
                # with col2:
                #     st.metric(label="Condition", value=data.get('description', 'N/A'))

        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to the backend at {BACKEND_URL}. Is the Flask server running?")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")


