from src.pull_data import seed_database
from models.ny_public_data import ParoleData
from config import TEST_URI, TEST_OVERDOSE_DATA
import json

# TODO do I need to map TableNames to data sources?

def test_main():
    with open(TEST_OVERDOSE_DATA, "r") as f:
        test_name_mapping = json.load(f)
    seed_database(TEST_URI, test_name_mapping)
