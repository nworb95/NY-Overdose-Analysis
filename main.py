from postgres_utils.seed_database import seed_database, logger

__author__ = "Emma Brown"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    seed_database()


if __name__ == "__main__":
    logger.info("Seeding database!")
    main()
    logger.info("Finished!")
