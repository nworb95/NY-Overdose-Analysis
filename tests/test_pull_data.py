from src.pull_socrata_data import pull_socrata_data
from models.ny_public_data import ParoleData
from config import TEST_URI, TEST_OVERDOSE_DATA
import json

# TODO do I need to map TableNames to data sources?

def test_main():
    with open(TEST_OVERDOSE_DATA, "r") as f:
        test_name_mapping = json.load(f)
    pull_socrata_data(TEST_URI, test_name_mapping)
