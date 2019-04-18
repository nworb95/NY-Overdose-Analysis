import pandas as pd
import re
from sodapy import Socrata
import logging
from sqlalchemy import create_engine
import os

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

table_name_mapping = {'https://health.data.ny.gov/resource/7728-g3f6.json': 'dropouts_by_county',
                      'https://health.data.ny.gov/resource/sn5m-dv52.json': 'opioid_deaths_by_county',
                      'https://health.data.ny.gov/resource/rv8x-4fm3.json': 'inpatient_discharges_by_county',
                      'https://health.data.ny.gov/resource/acw9-uyeq.json': 'premature_deaths_by_county',
                      'https://health.data.ny.gov/resource/8t6s-vqv5.json': 'unemployment_data_by_county',
                      'https://health.data.ny.gov/resource/du4z-hmkb.json': 'medicaid_patient_visits_by_county',
                      'https://data.ny.gov/resource/qkrk-6v78.json': 'unemployment_avg_duration_by_county',
                      'https://data.ny.gov/resource/ekci-x6aq.json': 'active_construction_by_county',
                      'https://data.ny.gov/resource/mef4-viwt.json': 'ny_state_career_centers',
                      'https://data.ny.gov/resource/f6sn-r72s.json': 'low_income_tax_credits_by_county',
                      'https://data.ny.gov/resource/shc7-xcbw.json': 'employment_wage_data_by_county',
                      'https://data.ny.gov/resource/6k74-dgkb.json': 'overall_employment_data_by_county',
                      'https://data.ny.gov/resource/b7d6-zygf.json': 'long_term_industry_projection_by_county',
                      'https://data.ny.gov/resource/mx4v-8962.json': 'short_term_industry_projection_by_county',
                      'https://data.ny.gov/resource/5hyu-bdh8.json': 'local_unemployment_data_by_county',
                      'https://data.ny.gov/resource/ykyj-hw45.json': 'employment_data_by_race_by_county',
                      'https://data.ny.gov/resource/a5je-8vxp.json': 'suny_data_by_county',
                      'https://data.ny.gov/resource/dwpa-fswx.json': 'swm_data_by_county'}

def get_mysql_engine():
    """
    Connects to local mysql database to cache downloaded data.
    :return: engine
    """
    return create_engine(
        "mysql://root:{}@localhost:3306".format(os.environ["MYSQL_LOCAL_PASS"])
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
    :param client: ClientSession
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
    table_title = client.get_metadata(table_string)['name']
    logger.info("Downloaded table: %s", table_title)
    return {table_title: download_data(client, table_string)}


def main():
    ts = time()
