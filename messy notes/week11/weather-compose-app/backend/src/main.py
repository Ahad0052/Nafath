import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Keep your original imports
from extract import extract_weather
from transform import transform_weather
from load import load_to_csv

# 1. Initialize Flask and enable CORS so Streamlit can talk to it
app = Flask(__name__)
CORS(app)

# 2. Change your main logic into a Flask route
@app.route('/weather', methods=['GET'])
def get_weather():
    # Get the city name sent by the Streamlit frontend
    # Default to "Muscat" if no city is provided
    city = request.args.get('city', 'Muscat') 
    
    print(f"Starting ETL Pipeline for city: {city}")
    
    try:
        # Pass the dynamic city to your extract function 
        # (Note: You might need to update extract_weather() to accept a 'city' argument!)
        raw_data = extract_weather(city) 
        
        # Transform the data
        transformed_data = transform_weather(raw_data)
        
        # Load/Save to CSV
        load_to_csv(transformed_data)
        
        print("ETL Pipeline Completed Successfully")
        
        # 3. Return the transformed data as JSON back to Streamlit
        return jsonify(transformed_data), 200

    except Exception as e:
        print(f"ETL Pipeline Failed: {e}")
        return jsonify({"error": str(e)}), 500

# 4. Run the Flask server on port 5000
if __name__ == "__main__":
    # host="0.0.0.0" is critical for Docker to map the ports correctly
    app.run(host="0.0.0.0", port=5000, debug=True)