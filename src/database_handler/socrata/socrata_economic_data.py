import logging
import os
import re
import json
from glob import glob
import pandas as pd
from sodapy import Socrata
from requests.exceptions import ReadTimeout

from database_handler.utils.retry import retry
from database_handler.socrata.constants import NY_OVERDOSE_DATA, NY_DATA_DIR

logger = logging.getLogger(__name__)


class SocrataEconomicData:
    def __init__(self):
        with open(NY_OVERDOSE_DATA, "r") as f:
            self._table_name_mapping = json.load(f)
        if not os.path.exists(NY_DATA_DIR):
            logger.info("Socrata data directory doesn't exist -- creating now")
            os.mkdir(NY_DATA_DIR)
        self._ny_state_data_client = Socrata("data.ny.gov", os.environ["SOCRATA_TOKEN"], timeout=100)
        self._ny_health_data_client = Socrata("health.data.ny.gov", os.environ["SOCRATA_TOKEN"], timeout=100)
        logger.info("Connected to Socrata clients!")
        # for url, name in self._table_name_mapping.items():
        #     self._download_data(url, name)
        self._download_data("https://health.data.ny.gov/resource/sn5m-dv52.json", "opioid_deaths_by_county")
        self._ny_health_data_client.close()
        self._ny_health_data_client.close()
        logger.info("Economic data updated!")

    def _download_data(self, url, name):
        """
        Downloads latest Socrata data from NY Public Data.
        :param name:
        :param url:
        :return:
        """
        table_string = self._get_dataset_string(url)
        if "health.data.ny" not in url:
            client = self._ny_state_data_client
            logger.info("Using NY Data Socrata client!")
        else:
            client = self._ny_health_data_client
            logger.info("Using NY Health Data Socrata client!")
        table_description = client.get_metadata(table_string)["name"]
        logger.info("Downloading table: %s", table_description)
        self._paginate_data(client, table_string, name)

    @retry(ReadTimeout)
    def _paginate_data(self, client, table, name):
        """
        :param client:
        :param table:
        :param name:
        :return:
        """
        table_dir = f"{NY_DATA_DIR}{name}/"
        if not os.path.exists(table_dir):
            os.mkdir(table_dir)
            offset = 0
        else:
            offset = self._get_table_length(table_dir)
        client.timeout = 50
        logger.info("Pulling latest data!")
        while client.get(table, limit=10000, offset=offset):
            data = pd.DataFrame.from_records(client.get(table, limit=10000, offset=offset))
            logger.info(data.head())
            try:
                data.to_json(table_dir + f"{offset}.json")
            except Exception as e:
                logger.warning(e)
            offset += len(data)
            logger.info(
                f"Downloaded output to {table_dir + f'{offset}.json'}"
            )

    @staticmethod
    def _get_dataset_string(json_string: str):
        """
        Grabs the dataset name from the cached json file.
        :param json_string:
        :return:
        """
        return re.search(r"resource/(.*).json", json_string).group(1)

    @staticmethod
    def _get_table_length(table_dir):
        json_paths = glob(table_dir + "*.json")
        last_json = max([int(f.lstrip(table_dir).rstrip(".json")) for f in json_paths])
        data = pd.read_json(table_dir + str(last_json) + ".json")
        return len(data) + last_json

    @staticmethod
    def _get_all_tables():
        return next(os.walk(NY_DATA_DIR))[1]
