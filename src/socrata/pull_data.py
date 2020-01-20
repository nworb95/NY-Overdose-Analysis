import logging
import os
import re
import json
import pandas as pd
from config import NY_OVERDOSE_DATA
from sodapy import Socrata


def get_dataset_string(json_string):
    """

    :param json_string:
    :return:
    """
    return re.search(r"resource/(.*).json", json_string).group(1)


def get_data(client, dataset_string, offset, limit=50000):
    """

    :param client:
    :param dataset_string:
    :param offset:
    :param limit:
    :return:
    """
    return client.get(dataset_string, limit=limit, offset=offset)


def paginate_data(client, table, name):
    """
    :param client:
    :param table:
    :param table_name:
    :return:
    """
    offset = 0  # make this len of table in db to only get new data
    file_path = "/var/app/output/{}/".format(name)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    while client.get(table, limit=10000, offset=offset):
        data = pd.DataFrame.from_records(get_data(client, table, offset))
        logging.info(data.head())
        try:
            data.to_json(file_path + "{}.json".format(offset))
        except Exception as e:
            logging.warning(e)
        offset += len(data)
        logging.info(
            "Downloaded output to {}".format(file_path + "{}.json".format(offset))
        )


def get_clients():
    """

    :return:
    """
    return (
        Socrata("data.ny.gov", os.environ["SOCRATA_TOKEN"], timeout=30),
        Socrata("health.data.ny.gov", os.environ["SOCRATA_TOKEN"], timeout=30),
    )


def download_data(url, name, ny_state_data_client, ny_health_data_client):
    """

    :param name:
    :param url:
    :param ny_state_data_client:
    :param ny_health_data_client:
    :return:
    """
    table_string = get_dataset_string(url)
    if "health.data.ny" not in url:
        client = ny_state_data_client
        logging.info("Using NY Data Socrata client!")
    else:
        client = ny_health_data_client
        logging.info("Using NY Health Data Socrata client!")
    table_description = client.get_metadata(table_string)["name"]
    logging.info("Downloading table: %s", table_description)
    paginate_data(client, table_string, name)


def pull_socrata_data():
    """
    Initializes postgres database with freshly scraped Socrata data.
    :return: Updated NY countywise Socrata data
    """
    with open(NY_OVERDOSE_DATA, "r") as f:
        table_name_mapping = json.load(f)
    ny_state_data_client, ny_health_data_client = get_clients()
    logging.info("Connected to Socrata clients!")
    for url, name in table_name_mapping.items():
        download_data(url, name, ny_state_data_client, ny_health_data_client)
    ny_health_data_client.close()
    ny_state_data_client.close()
