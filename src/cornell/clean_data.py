import pandas as pd


def clean_actual_population_data(df):
    df = df.rename(columns={"Unnamed: 0": "County", "Unnamed: 13": "2010"}).drop(
        ["Unnamed: 1", "Unnamed: 12"], axis=1
    )
    df["County"] = df["County"].str.replace(".", "")
    return df[~(df["County"] == "New York")]