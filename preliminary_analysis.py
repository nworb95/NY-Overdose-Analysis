import modin.pandas as pd
import re
from sodapy import Socrata
import logging
from time import time
import asyncio
import aiohttp

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def get_dataset_string(json_string):
    """
    Grabs dataset string from URL.
    :param json_string:
    :return: dataset_string
    """
    return re.search(r"resource/(.*).json", json_string).group(1)


async def get_data(client, dataset_string, offset, limit):
    """
    :param client: aiohttp ClientSession
    :param dataset_string: string identifier for dataset
    :param offset:
    :param limit:
    :return: json
    """
    return client.get(dataset_string, limit=limit, offset=offset)


def offset_data(json_string):
    """
    Works around default 1000 limit for reading from Socrata jsons.
    :param json_string:
    :return: final_data_frame
    """
    if "health.data.ny" not in json_string:
        client = Socrata("data.ny.gov", None)
    else:
        client = Socrata("health.data.ny.gov", None)
    offset = 0
    limit = 1000
    dataset = get_dataset_string(json_string)
    results = []
    while client.get(dataset, limit=limit, offset=offset):
        data = pd.DataFrame.from_records(
            get_data(client, dataset, offset, limit)
        )
        results.append(data)
        offset = +limit

    return pd.concat(results)


def main():
    ts = time()
