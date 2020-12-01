from io import BytesIO

import numpy as np
import pandas as pd
import requests
import logging
import os

from requests.exceptions import ReadTimeout
from database_handler.utils.retry import retry
from database_handler.population_puller.constants import (
    COUNTY_LIST,
    HISTORICAL_DATA_URL,
    HISTORICAL_POPULATION_COLUMNS,
    PROJECTED_DATA_UNFORMATTED_URL,
    PROJECTED_POPULATION_COLUMNS,
    PROJECTED_DROP_COLUMNS,
    POPULATION_DATA_CACHE,
    MISSING_POPULATION_YEARS,
)

logger = logging.getLogger(__name__)


class PopulationPuller:
    def __init__(self):
        if self._check_if_cornell_dir_exists():
            logger.info("Reading cached county-wise NY population data from Cornell!")
            self._historical_data = pd.read_json(POPULATION_DATA_CACHE % "historical")
            self._projected_data = pd.read_json(POPULATION_DATA_CACHE % "projected")
        else:
            logger.info("Pulling county-wise NY population data from Cornell!")
            self._historical_data = self._pull_historical_population_data()
            self._projected_data = self._pull_projected_population_data()
        self.population_data = self._merge_population_data()
        self.population_data.to_json(POPULATION_DATA_CACHE % "merged")

    def _merge_population_data(self):
        logging.info("Merging population data!")
        df = pd.merge(self._historical_data, self._projected_data, on="County")
        cols = [x for x in df.columns.tolist() if x != "County"]
        for i in cols:
            df[i] = df[i].astype(int)
        interpolated_df = self._interpolate_missing_data(df)
        return interpolated_df

    def _pull_projected_population_data(self):
        logger.info(
            f"Getting projected population data from {PROJECTED_DATA_UNFORMATTED_URL}"
        )
        data = self._process_projected_population_files()
        # Filters to the all-genders and ages bucket.
        filtered_df = data[
            (data["SEX_DESCR"] == "All") & (data["AGEGRP_DESCR"] == "Total")
        ]
        filtered_df = filtered_df.rename(columns=PROJECTED_POPULATION_COLUMNS).drop(
            PROJECTED_DROP_COLUMNS, axis=1,
        )
        projected_data = filtered_df.reset_index().drop(["index"], axis=1)
        logger.info(f"{projected_data}")
        projected_data.to_json(POPULATION_DATA_CACHE % "projected")
        return projected_data

    @retry(ReadTimeout)
    def _pull_historical_population_data(self):
        logger.info(f"Getting historical population data from {HISTORICAL_DATA_URL}!")
        raw_data = pd.read_excel(
            BytesIO(requests.get(HISTORICAL_DATA_URL).content), skiprows=3
        )[:-8]
        data = raw_data.rename(columns=HISTORICAL_POPULATION_COLUMNS).drop(
            ["Unnamed: 1", "Unnamed: 12"], axis=1
        )
        data["County"] = data["County"].str.replace(".", "")
        # Filter out all-New York data
        historical_data = data[~(data["County"] == "New York")]
        logger.info(f"{historical_data}")
        historical_data.to_json(POPULATION_DATA_CACHE % "historical")
        return historical_data

    @staticmethod
    def _process_projected_population_files():
        projection_df_list = []
        for request in COUNTY_LIST:
            logger.info(f"Pulling data for {request}!")
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
    def _check_if_cornell_dir_exists():
        # TODO make this compare last historical population data point in SQLite with one at source
        if not os.path.exists("data/cornell_population_data"):
            os.makedirs("data/cornell_population_data")
            return False
        else:
            return True

    @staticmethod
    def _transpose_data_for_interpolation(sorted_df: pd.DataFrame):
        """
        Transposes the data for interpolation.
        This is a silly workaround because I didn't feel like debugging scipy.
        """
        transpose_df = sorted_df.transpose()
        transpose_df.columns = transpose_df.iloc[-1]
        transpose_df = transpose_df.iloc[:-1]
        for col in transpose_df:
            transpose_df[col] = pd.to_numeric(transpose_df[col], errors="coerce")
        transpose_df.index = transpose_df.index.map(np.datetime64)
        return transpose_df

    def _interpolate_missing_data(self, formatted_df: pd.DataFrame):
        """
        Interpolates missing population data with the akima spline method
        """
        big_df = pd.concat(
            [formatted_df, pd.DataFrame(columns=MISSING_POPULATION_YEARS)], sort=False
        )
        for year in MISSING_POPULATION_YEARS:
            big_df[year] = pd.to_numeric(big_df[year], errors="coerce")
        sorted_df = big_df[big_df.columns.sort_values()]
        transpose_df = self._transpose_data_for_interpolation(sorted_df)
        interpolated_df = transpose_df.interpolate(method="akima")
        interpolated_df.index = interpolated_df.index.strftime("%Y")
        interpolated_df = interpolated_df.transpose()
        # I forget, why do I do this?
        # TODO remember why I do this part!
        for year in MISSING_POPULATION_YEARS:
            interpolated_df[year] = interpolated_df[year].astype(float)
        return interpolated_df
