from io import BytesIO

import pandas as pd
import requests
import logging
import os

from src.cornell.constants import (
    COUNTY_LIST,
    HISTORICAL_DATA_URL,
    PROJECTED_DATA_UNFORMATTED_URL,
    POPULATION_DATA_CACHE,
)
from src.cornell.utils import (
    clean_historical_population_data,
    clean_projected_population_data,
    merge_population_data,
)


class CornellPopulationData:
    def __init__(self):
        if self._check_if_cornell_dir_exists():
            logging.info("Reading cached county-wise NY population data from Cornell!")
            self.historical_data = pd.read_json(POPULATION_DATA_CACHE % "historical")
            self.projected_data = pd.read_json(POPULATION_DATA_CACHE % "projected")
        else:
            logging.info("Pulling county-wise NY population data from Cornell!")
            self.historical_data = self._pull_historical_population_data()
            self.projected_data = self._pull_projected_population_data()
        self.merged_data = merge_population_data(
            historical_df=self.historical_data, projected_df=self.projected_data
        )

    def _pull_projected_population_data(self):
        logging.info(
            f"Getting projected population data from {PROJECTED_DATA_UNFORMATTED_URL}"
        )
        projected_data = self._process_projected_population_files()
        clean_projected_data = clean_projected_population_data(projected_data)
        logging.info(f"{clean_projected_data}")
        self._cache_population_data(data=clean_projected_data, datatype="projected")
        return clean_projected_data

    def _pull_historical_population_data(self):
        logging.info(f"Getting historical population data from {HISTORICAL_DATA_URL}!")
        data = pd.read_excel(
            BytesIO(requests.get(HISTORICAL_DATA_URL).content), skiprows=3
        )[:-8]
        historical_data = clean_historical_population_data(data)
        logging.info(f"{historical_data}")
        self._cache_population_data(data=historical_data, datatype="historical")
        return historical_data

    @staticmethod
    def _process_projected_population_files():
        projection_df_list = []
        for request in COUNTY_LIST:
            logging.info(f"Pulling data for {request}!")
            projection_df_list.append(
                pd.read_excel(
                    BytesIO(
                        requests.get(
                            PROJECTED_DATA_UNFORMATTED_URL.format(request)
                        ).content
                    )
                )
            )
        return pd.concat(projection_df_list)

    @staticmethod
    def _cache_population_data(data: pd.DataFrame, datatype: str):
        logging.info(
            f"Caching historical population data! :: {POPULATION_DATA_CACHE % datatype}"
        )
        data.to_json(POPULATION_DATA_CACHE % datatype)

    @staticmethod
    def _check_if_cornell_dir_exists():
        if not os.path.exists("data/cornell_population_data"):
            os.makedirs("data/cornell_population_data")
            return False
        else:
            return True
