import logging
import os
import re
import json

import pandas as pd
from sodapy import Socrata
from sqlalchemy import create_engine

# TODO make this a class -- database_generator? database_refresher?
# TODO -- rationalize variable names

with open("data/ny_sources.json", "r") as f:
    table_name_mapping = json.load(f)


def get_postgres_engine():
    """

    :return:
    """
    engine = create_engine("postgresql://postgres:postgres@db:5432/postgres")
    return engine.connect()


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


def download_data(client, table, name):
    """
    :param client:
    :param table:
    :param table_name:
    :return:
    """
    offset = 0  # make this len of table in db to only get new data
    file_path = "output/{}/".format(name)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    conn = get_postgres_engine()
    while client.get(table, limit=10000, offset=offset):
        data = pd.DataFrame.from_records(get_data(client, table, offset))
        logging.info(data.head())
        data.to_json(file_path + "{}.json".format(offset))
        offset += len(data)
        logging.info("Downloaded output to %d", file_path + "{}.json".format(offset))
    conn.close()


def get_socrata_clients():
    """

    :return:
    """
    return (
        Socrata("data.ny.gov", os.environ["SOCRATA_TOKEN"], timeout=30),
        Socrata("health.data.ny.gov", os.environ["SOCRATA_TOKEN"], timeout=30),
    )


def load_data(url, name, ny_state_data_client, ny_health_data_client):
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
    download_data(client, table_string, name)


def seed_database():
    """
    Initializes postgres database with freshly scraped Socrata data.
    :return:
    """
    ny_state_data_client, ny_health_data_client = get_socrata_clients()
    logging.info("Connected to Socrata clients!")
    for url, name in table_name_mapping.items():
        load_data(url, name, ny_state_data_client, ny_health_data_client)
        logging.info("Uploaded table %s successfully!", name)
    ny_health_data_client.close()
    ny_state_data_client.close()
