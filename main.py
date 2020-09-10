import logging
from datetime import datetime

from src.socrata.socrata_economic_data import SocrataEconomicData
from src.cornell import CornellPopulationData


__author__ = "Emma Brown"
__version__ = "0.2.0"
__license__ = "MIT"

LOG_FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(
    filemode="w",
    filename=f"logs/{datetime.now().strftime('%Y_%m_%d')}_data_pull.log",
    format=LOG_FORMAT,
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


if __name__ == "__main__":
    logging.info("Pulling Cornell Data!")
    population_data = CornellPopulationData()
    logging.info("Pulling Socrata Data!")
    economic_data = SocrataEconomicData()
