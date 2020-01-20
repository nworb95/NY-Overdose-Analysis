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


def clean_actual_population_data(df):
    # TODO does this belong in a clean_data script?
    df = df.rename(columns={"Unnamed: 0": "County", "Unnamed: 13": "2010"}).drop(
        ["Unnamed: 1", "Unnamed: 12"], axis=1
    )
    df["County"] = df["County"].str.replace(".", "")
    return df[~(df["County"] == "New York")]


def cache_actual_population_data(df):
    df.to_json("./raw_data/actual_ny_population_data.json")


def pull_actual_population_data():
    df = get_actual_population_data()
    clean_df = clean_actual_population_data(df)
    cache_actual_population_data(clean_df)
    return clean_df
