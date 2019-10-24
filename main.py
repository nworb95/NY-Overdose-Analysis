from src.seed_database import seed_database
import logging

__author__ = "Emma Brown"
__version__ = "0.1.0"
__license__ = "MIT"

logging.basicConfig(
    filemode="w",
    filename="/var/app/logs/database.log",
    format="%(asctime)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)


def main():
    seed_database()


if __name__ == "__main__":
    logging.info("Seeding database!")
    main()
    logging.info("Finished!")
