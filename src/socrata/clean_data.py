# Join with Cornell data here
from src.socrata import NY_DATA_DIR
import os


tables = next(os.walk(NY_DATA_DIR))[1]
