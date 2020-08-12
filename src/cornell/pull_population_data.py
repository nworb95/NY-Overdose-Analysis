from io import BytesIO

import pandas as pd
import requests
import logging
import os

from src.cornell.constants import (
    COUNTY_LIST,
    HISTORICAL_DATA_URL,
    PROJECTED_DATA_UNFORMATTED_URL,
    HISTORICAL_POPULATION_DATA_CACHE,
    PROJECTED_POPULATION_DATA_CACHE,
)
from src.cornell.clean_population_data import (
    clean_historical_population_data,
    clean_projected_population_data,
    merge_population_data,
)

if not os.path.exists("data/cornell_population_data"):
    os.makedirs("data/cornell_population_data")


def check_for_projected_population_data():
    if os.path.exists(PROJECTED_POPULATION_DATA_CACHE):
        logging.info("Projected data found in cache!")
        return True
    else:
        return False


def get_historical_population_data():
    logging.info(f"Getting historical population data from {HISTORICAL_DATA_URL}!")
    return pd.read_excel(
        BytesIO(requests.get(HISTORICAL_DATA_URL).content), skiprows=3,
    )[:-8]


def cache_historical_population_data(df: pd.DataFrame):
    logging.info(
        f"Caching historical population data! :: {HISTORICAL_POPULATION_DATA_CACHE}"
    )
    df.to_json(HISTORICAL_POPULATION_DATA_CACHE)


def pull_historical_population_data():
    logging.info("Pulling historical data!")
    df = get_historical_population_data()
    clean_df = clean_historical_population_data(df)
    logging.info(f"{clean_df}")
    cache_historical_population_data(clean_df)
    return clean_df


def get_projected_population_data():
    logging.info(
        f"Getting projected population data from {PROJECTED_DATA_UNFORMATTED_URL}"
    )
    projection_df_list = []
    for request in COUNTY_LIST:
        logging.info(f"Pulling data for {request}!")
        projection_df_list.append(
            pd.read_excel(
                BytesIO(
                    requests.get(PROJECTED_DATA_UNFORMATTED_URL.format(request)).content
                )
            )
        )
    return pd.concat(projection_df_list)


def cache_projected_population_data(df: pd.DataFrame):
    logging.info(
        f"Caching projected population data! :: {PROJECTED_POPULATION_DATA_CACHE}"
    )
    df.to_json(PROJECTED_POPULATION_DATA_CACHE)


def pull_projected_population_data():
    # TODO make these all just pull/clean/get?
    logging.info("Pulling projected population data!")
    df = get_projected_population_data()
    clean_df = clean_projected_population_data(df)
    logging.info(f"{clean_df}")
    cache_projected_population_data(clean_df)
    return clean_df


def pull_cornell_population_data():
    """
    Pulls county-wise NY population data from Cornell.
    :return: merged population data
    """
    logging.info("Pulling county-wise NY population data from Cornell!")
    projected_data_exists = check_for_projected_population_data()
    if not projected_data_exists:
        projected_data = pull_projected_population_data()
    else:
        projected_data = pd.read_json(PROJECTED_POPULATION_DATA_CACHE)
    historical_data = pull_historical_population_data()
    merged_data = merge_population_data(historical_data, projected_data)
    return merged_data
