from io import BytesIO

import pandas as pd
import requests

from src.cornell import county_list
from src.cornell.clean_data import (
    clean_actual_population_data,
    clean_projected_population_data,
)


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
    df.to_json("./data/cache/actual_ny_population_data.json")


def pull_actual_population_data():
    df = get_actual_population_data()
    clean_df = clean_actual_population_data(df)
    cache_actual_population_data(clean_df)
    return clean_df


def get_projected_population_data():
    projection_df_list = []
    for request in county_list:
        projection_df_list.append(
            pd.read_excel(
                BytesIO(
                    requests.get(
                        "https://pad.human.cornell.edu/counties/expprojdata.cfm?county={}".format(
                            request
                        )
                    ).content
                )
            )
        )
    return pd.concat(projection_df_list)


def cache_projected_population_data(df):
    df.to_json("./data/cache/projected_ny_population_data.json")


def pull_projected_population_data():
    df = get_projected_population_data()
    clean_df = clean_projected_population_data(df)
    cache_projected_population_data(clean_df)
    return clean_df
