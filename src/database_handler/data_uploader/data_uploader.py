import logging
from glob import glob
import pandas as pd

from database_handler.data_uploader.utils import (
    standardize_year_column,
    standardize_county_column,
)
from database_handler.data_uploader.constants import SOCRATA_KEY_COLUMNS

# TODO add a data refresher module for re-normalizing

logger = logging.getLogger(__name__)


class DataUploader:
    # TODO make inputs just population data, economic data
    # That way you can not worry about whether it's the whole data or just some
    # and a separate process can decide whether or not to use data in DB or new data
    # and a separate process can call this module to re-normalize all of the data
    # in the case of updated historicals
    def __init__(self, db_engine, population_data):
        self.db_engine = db_engine
        self.population_data = population_data

    @staticmethod
    def load_socrata_data(dataset):
        logging.info(f"Normalizing {dataset}!")
        data_list = []
        for f_name in glob(f"./data/socrata_economic_data/{dataset}/*.json"):
            data_list.append(pd.read_json(f_name))
        logger.info("Merging data!")
        data = pd.concat(data_list)
        data = standardize_year_column(socrata_data=data, socrata_dataset=dataset)
        data = standardize_county_column(socrata_data=data)
        return data

    def upload_data(self):
        for dataset in SOCRATA_KEY_COLUMNS.keys():
            table_name = dataset.rstrip("_by_county")
            socrata_data = self.load_socrata_data(dataset)
            logger.info(f"{dataset} data merged!")
            try:
                if "population" in SOCRATA_KEY_COLUMNS[dataset].keys():
                    socrata_data = normalize_socrata_data(
                        self.population_data, socrata_data, dataset
                    )
                socrata_data.to_sql(
                    table_name, con=self.db_engine, if_exists="replace"
                )
            except KeyError:  # need to handle that unemployment by race dataset that has region and not county
                pass


def normalize_socrata_data(
    population_data: pd.DataFrame, socrata_data: pd.DataFrame, socrata_dataset: str
):
    logger.info(f"Normalizing population data for {socrata_dataset}!")
    melted_population_data = (
        population_data.reset_index()
        .melt(["County"])
        .rename(columns={"variable": "year", "County": "county"})
    )
    melted_population_data.year = melted_population_data.year.astype(int)
    filtered_population_data = melted_population_data[
        (melted_population_data["year"] <= max(socrata_data.year))
        & (melted_population_data["year"] >= min(socrata_data.year))
    ]
    merged_data = socrata_data.merge(
        filtered_population_data, how="left", on=["county", "year"]
    ).rename(columns={"value": "population"})
    if "population" in SOCRATA_KEY_COLUMNS[socrata_dataset].keys():
        for unweighted_variable in SOCRATA_KEY_COLUMNS[socrata_dataset]["population"]:
            logging.info(f"Converting {unweighted_variable} to rate!")
            merged_data[f"{unweighted_variable}_rate"] = (
                merged_data[unweighted_variable].astype(float)
                / merged_data["population"]
            ) * 100
    logger.info(f"Merged data ::\n {merged_data}")
    return merged_data
