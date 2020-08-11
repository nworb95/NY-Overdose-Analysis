from io import BytesIO

import pandas as pd
import requests
import logging
from datetime import datetime

from src.cornell.constants import COUNTY_LIST
from src.cornell.clean_population_data import (
    clean_historical_population_data,
    clean_projected_population_data,
    merge_population_data
)


cornell_log_format = "%(asctime)s - %(message)s"

logging.basicConfig(
    format=cornell_log_format,
    level=logging.INFO,
    filename="./logs/{}_cornell_data_pull.log".format(datetime.now().strftime("%Y_%m_%d")),
    filemode="w",
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(cornell_log_format)
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


def get_historical_population_data():
    return pd.read_excel(
        BytesIO(
            requests.get(
                "https://labor.ny.gov/stats/nys/CO-EST00INT-01-36.xlsx"
            ).content
        ),
        skiprows=3,
    )[:-8]


def cache_historical_population_data(df):
    df.to_json("./data/cache/actual_ny_population_data.json")


def pull_historical_population_data():
    df = get_historical_population_data()
    clean_df = clean_historical_population_data(df)
    cache_historical_population_data(clean_df)
    return clean_df


def get_projected_population_data():
    projection_df_list = []
    for request in COUNTY_LIST:
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


def pull_cornell_population_data():
    projected_data = pull_projected_population_data()
    historical_data = pull_projected_population_data()
    merged_data = merge_population_data(historical_data, projected_data)
    return merged_data
