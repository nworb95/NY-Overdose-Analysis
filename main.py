import logging
from src.socrata.pull_data import pull_socrata_data

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


if __name__ == "__main__":
    logging.info("Pulling Socrata Data!")
    pull_socrata_data()

