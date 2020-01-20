import requests
import pandas as pd
from io import BytesIO


def get_actual_population_data():
    return pd.read_excel(
        BytesIO(
            requests.get(
                "https://labor.ny.gov/stats/nys/CO-EST00INT-01-36.xlsx"
            ).content
        ),
        skiprows=3,
    )[:-8]


def cache_actual_population_data(df):
    df.to_json("./raw_data/actual_ny_population_data.json")


def pull_actual_population_data():
    df = get_actual_population_data()
    cache_actual_population_data(df)
