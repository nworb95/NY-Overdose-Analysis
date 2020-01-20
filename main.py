from src.pull_socrata_data import pull_socrata_data
from config import PROD_URI, NY_OVERDOSE_DATA
import logging
import json

__author__ = "Emma Brown"
__version__ = "0.1.0"
__license__ = "MIT"

logging.basicConfig(
    # filemode="w",
    # filename="/var/app/logs/data_pull.log",
    format="%(asctime)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)


def main():
    with open(NY_OVERDOSE_DATA, "r") as f:
        table_name_mapping = json.load(f)
    pull_socrata_data(table_name_mapping)


if __name__ == "__main__":
    logging.info("Seeding database!")
    main()
    logging.info("Finished!")
