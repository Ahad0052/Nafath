import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, "data", "weather.csv")

def load_to_csv(record):

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    df = pd.DataFrame([record])

    if os.path.exists(FILE_PATH):
        df.to_csv(
            FILE_PATH,
            mode="a",
            header=False,
            index=False
        )
    else:
        df.to_csv(
            FILE_PATH,
            index=False
        )

    print("CSV updated successfully")