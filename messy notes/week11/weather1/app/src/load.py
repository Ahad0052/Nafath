import pandas as pd
import os

FILE_PATH = "data/weather.csv"

def load_to_csv(record):

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
    