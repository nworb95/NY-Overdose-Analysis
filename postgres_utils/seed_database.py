import logging
import os
import re

import pandas as pd
from sodapy import Socrata
import psycopg2

logging.basicConfig(
    filemode="w",
    filename="logs/postgres.log",
    format="%(asctime)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

table_name_mapping = {
    "https://data.ny.gov/resource/jshw-gkgu.json": "union_compensation_claims_by_county",
    "https://data.ny.gov/resource/dwpa-fswx.json": "swm_data_by_county",
    "https://health.data.ny.gov/resource/du4z-hmkb.json": "medicaid_patient_visits_by_county",
    "https://health.data.ny.gov/resource/rv8x-4fm3.json": "inpatient_discharges_by_county",
    "https://health.data.ny.gov/resource/7728-g3f6.json": "dropouts_by_county",
    "https://health.data.ny.gov/resource/sn5m-dv52.json": "opioid_deaths_by_county",
    "https://health.data.ny.gov/resource/acw9-uyeq.json": "premature_deaths_by_county",
    "https://health.data.ny.gov/resource/8t6s-vqv5.json": "unemployment_data_by_county",
    "https://data.ny.gov/resource/qkrk-6v78.json": "unemployment_avg_duration_by_county",
    "https://data.ny.gov/resource/ekci-x6aq.json": "active_construction_by_county",
    "https://data.ny.gov/resource/mef4-viwt.json": "ny_state_career_centers",
    "https://data.ny.gov/resource/f6sn-r72s.json": "low_income_tax_credits_by_county",
    "https://data.ny.gov/resource/shc7-xcbw.json": "employment_wage_data_by_county",
    "https://data.ny.gov/resource/6k74-dgkb.json": "overall_employment_data_by_county",
    "https://data.ny.gov/resource/b7d6-zygf.json": "long_term_industry_projection_by_county",
    "https://data.ny.gov/resource/mx4v-8962.json": "short_term_industry_projection_by_county",
    "https://data.ny.gov/resource/5hyu-bdh8.json": "local_unemployment_data_by_county",
    "https://data.ny.gov/resource/ykyj-hw45.json": "employment_data_by_race_by_county",
    "https://data.ny.gov/resource/a5je-8vxp.json": "suny_data_by_county",
    "https://data.ny.gov/resource/iyf9-ajxg.json": "mined_land_data_by_county",
    "https://data.ny.gov/resource/agpz-6i9d.json": "oil_gas_production_data_by_county",
    "https://data.ny.gov/resource/xgig-n5ch.json": "mental_health_data_by_county",
    "https://data.ny.gov/resource/ybg9-s6bm.json": "juvenile_detention_by_county",
    "https://data.ny.gov/resource/hfc5-3hsu.json": "foster_child_data_by_county",
    "https://data.ny.gov/resource/rikd-mt35.json": "adult_arrest_data_by_county",
    "https://data.ny.gov/resource/nymx-kgkn.json": "jail_population_by_county",
    "https://data.ny.gov/resource/pmxm-gftz.json": "parole_data_by_county",
    "https://data.ny.gov/resource/y7pw-wrny.json": "recidivism_data_by_county",
}


def get_postgres_engine():
    """

    :return:
    """
    return psycopg2.connect(
        database="postgres_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5431",
    )


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


def download_data(dataset, client, table):
    """

    :param name:
    :param client:
    :param table:
    :return:
    """
    offset = 0
    conn = get_postgres_engine()
    while client.get(table, limit=50000, offset=offset):
        data = pd.DataFrame.from_records(get_data(client, table, offset))
        data.to_sql(name=dataset, con=conn, schema="public", if_exists="replace")
        offset += len(data)
        logger.info("Generated %d rows!", offset)
    conn.close()


def get_socrata_clients():
    """

    :return:
    """
    logger.info("Connecting to Socrata clients!")
    return (
        Socrata("data.ny.gov", os.environ["SOCRATA_TOKEN"]),
        Socrata("health.data.ny.gov", os.environ["SOCRATA_TOKEN"]),
    )


def load_data(dataset, url, ny_state_data_client, ny_health_data_client):
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
        logger.info("Using NY Data Socrata client!")
    else:
        client = ny_health_data_client
        logger.info("Using NY Health Data Socrata client!")
    table_description = client.get_metadata(table_string)["name"]
    logger.info("Downloading table: %s", table_description)
    download_data(dataset, client, table_string)


def seed_database():
    """
    Initializes postgres database with freshly scraped Socrata data.
    :return:
    """
    ny_state_data_client, ny_health_data_client = get_socrata_clients()
    for url, name in table_name_mapping.items():
        load_data(name, url, ny_state_data_client, ny_health_data_client)
        logging.info("Uploaded table %s successfully!", name)
    ny_health_data_client.close()
    ny_state_data_client.close()