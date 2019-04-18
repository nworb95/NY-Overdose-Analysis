import modin.pandas as pd
import re
from sodapy import Socrata
import logging
from sqlalchemy import create_engine
import os

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def connect_to_mysql():
    """
    Connects to local mysql database to cache downloaded data.
    :return: engine
    """
    return create_engine(
        "mysql://root:{}@localhost".format(os.environ["MYSQL_LOCAL_PASS"])
    )


def get_dataset_string(json_string):
    """
    Grabs dataset string from URL.
    :param json_string:
    :return: dataset_string
    """
    return re.search(r"resource/(.*).json", json_string).group(1)


def get_data(client, dataset_string, offset, limit):
    """
    :param client: aiohttp ClientSession
    :param dataset_string: string identifier for dataset
    :param offset:
    :param limit:
    :return: json
    """
    return client.get(dataset_string, limit=limit, offset=offset)


def download_data(client, table):
    offset = 0
    limit = 50000
    results = []
    while client.get(table, limit=limit, offset=offset):
        data = pd.DataFrame.from_records(get_data(client, table, offset, limit))
        results.append(data)
        offset += len(data)
        logger.info("Downloaded %d rows!", offset)
    return pd.concat(results)


def load_data(json_string):
    """
    Works around default 1000 limit for reading from Socrata jsons.
    :param json_string:
    :return: dictionary with dataframe as value and table title as key
    """
    if "health.data.ny" not in json_string:
        client = Socrata("data.ny.gov", os.environ["SOCRATA_TOKEN"])
        logger.info("Connected to NY Data Socrata client!")
    else:
        client = Socrata("health.data.ny.gov", os.environ["SOCRATA_TOKEN"])
        logger.info("Connected to NY Health Data Socrata client!")
    table_string = get_dataset_string(json_string)
    table_title = client.get_metadata(table_string)
    return {table_title: download_data(client, table_string)}


def main():
    ts = time()
