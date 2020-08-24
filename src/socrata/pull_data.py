import logging
import os
import re
import json
from glob import glob
import pandas as pd
from sodapy import Socrata


def get_dataset_string(json_string: str):
    """

    :param json_string:
    :return:
    """
    return re.search(r"resource/(.*).json", json_string).group(1)


def get_data(client, dataset_string, offset, limit=50000):
    """
    # TODO feed the length of existing json as offset. see how many rows, if rows > limit, paginate
    :param client:
    :param dataset_string:
    :param offset:
    :param limit:
    :return:
    """
    return client.get(dataset_string, limit=limit, offset=offset)


def get_table_length(table_dir):
    json_paths = glob(table_dir + "*.json")
    last_json = max([int(f.lstrip(table_dir).rstrip(".json")) for f in json_paths])
    data = pd.read_json(table_dir + str(last_json) + ".json")
    return len(data) + last_json


def get_all_tables():
    return next(os.walk(NY_DATA_DIR))[1]


def paginate_data(client, table, name):
    """
    :param client:
    :param table:
    :param table_name:
    :return:
    """
    table_dir = f"{NY_DATA_DIR}{name}/"
    if not os.path.exists(table_dir):
        os.mkdir(table_dir)
        offset = 0
    else:
        offset = get_table_length(table_dir)
    client.timeout = 50
    while client.get(table, limit=10000, offset=offset):
        data = pd.DataFrame.from_records(get_data(client, table, offset))
        logging.info(data.head())
        try:
            data.to_json(table_dir + "{}.json".format(offset))
        except Exception as e:
            logging.warning(e)
        offset += len(data)
        logging.info(
            "Downloaded output to {}".format(table_dir + "{}.json".format(offset))
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


ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).rstrip("src/socrata") + "s/"
NY_OVERDOSE_DATA = ROOT_DIR + "src/socrata/assets/ny_sources.json"
NY_DATA_DIR = ROOT_DIR + "data/raw_data/"
OVERDOSE_TABLE_MAPPINGS = (
    {
        "active_construction_by_county": {
            "year": ["construction_completion_date", "construction_start_date"]
        },
        "adult_arrest_data_by_county": {
            "year": "year",
            "population": [
                "total",
                "felony_total",
                "drug_felony",
                "vionet_felony",
                "dwi_felony",
                "other_felony",
                "misdemeanor_total",
                "drug_misd",
                "dwi_misd",
                "property_misd",
                "other_misd",
            ],
        },
        "employment_data_by_race_by_county": {"year": "year"},
        "employment_wage_data_by_county": {
            "year": "year",
            "population": "average_employment",
        },
        "foster_child_data_by_county": {
            "year": "year",
            "population": [
                "adoptive_home",
                "agency_operated_boarding_home",
                "approved_relative_home",
                "foster_boarding_home",
                "group_home",
                "group_residence",
                "institution",
                "supervised_independent_living",
                "other",
                "total_days_in_care",
                "admissions",
                "discharges",
                "children_in_care",
                "number_of_children_served",
                "indicated_cps_reports",
            ],
        },
        "inpatient_discharges_by_county": {"year": "discharge_year"},
        "jail_population_by_county": {
            "year": "year",
            "population": [
                "census_2",
                "boarded_out",
                "boarded_in",
                "census",
                "sentenced",
                "civil",
                "federal",
                "technical_parole_violators",
                "state_readies",
                "other_unsentenced",
            ],
        },
        "juvenile_detention_by_county": {
            "year": "year",
            "population": [
                "secure_non_secure_admissions",
                "non_secure_admissions",
                "secure_non_secure_unique_youth",
                "non_secure_unique_youth",
            ],
        },
        "local_unemployment_data_by_county": {
            "year": "year",
            "month": "month",
            "population": ["laborforce", "employed", "unemployed"],
        },
        "long_term_industry_projection_by_county": {
            "year": ["base_year", "projected_year"]
        },
        "low_income_tax_credits_by_county": {
            "year": "calendar_year",
            "population": "affordable_units",
        },
        "medicaid_patient_visits_by_county": {
            "year": "year",
            "population": [
                "ip_recips",
                "ip_admits",
                "ip_admits",
                "er_recips",
                "er_visits",
            ],
        },
        "mined_land_data_by_county": {
            "year": [],
            "area": [
                "acres_controlled",
                "acres_life_of_mine",
                "acres_affected",
                "acres_reclaimed",
                "acresbb",
                "acresbb_range",
            ],
        },
        "ny_state_career_centers": {},
        "oil_gas_production_data_by_county": {"year": "year"},
        "opioid_deaths_by_county": {
            "year": "year",
            "population": "opioid_poisoning_deaths",
        },
        "overall_employment_data_by_county": {
            "year": "year",
            "population": "current_employment",
        },
        "parole_data_by_county": {"year": "snapshot_year"},
        "recidivism_data_by_county": {"year": "release_year"},
        "short_term_industry_projection_by_county": {
            "year": "period",
            "population": [
                "base_year_employment_estimate",
                "projected_year_employment_estimate",
                "net_change",
            ],
        },
        "swm_data_by_county": {"year": "expiration_date"},
        "unemployment_avg_duration_by_county": {"year": "year"},
        "union_compensation_claims_by_county": {
            "year": ["accident_date", "anrc_date", "assembly_date", "first_appeal_date"]
        },
    },
)