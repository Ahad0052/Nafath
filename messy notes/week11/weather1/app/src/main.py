from extract import extract_weather
from transform import transform_weather
from load import load_to_csv

def run_etl():

    print("Starting ETL Pipeline")

    raw_data = extract_weather()

    transformed_data = transform_weather(raw_data)

    load_to_csv(transformed_data)

    print("ETL Pipeline Completed")

if __name__ == "__main__":
    run_etl()
