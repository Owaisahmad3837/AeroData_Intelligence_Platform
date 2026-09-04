from src.airport_data_platform.config.logging_config import logging_config as log

from src.airport_data_platform.ingestion.main_ingestion import main_ingestion
from src.airport_data_platform.validation.main_validation import main_validation
from src.airport_data_platform.transform.main_transform import main_transform
from src.airport_data_platform.load.main_load import main_load


def main():

    logger = log("main", "main_pipeline")

    logger.info("Starting the main pipeline...")
    print("Starting the main pipeline...")

    # Ingestion
    logger.info("Starting data ingestion...")
    print("Starting data ingestion...")

    main_ingestion()

    logger.info("Data ingestion completed successfully!")
    print("Data ingestion completed successfully!")

    # Validation
    logger.info("Starting data validation...")
    print("Starting data validation...")

    main_validation()

    logger.info("Data validation completed successfully!")
    print("Data validation completed successfully!")

    # Transformation
    logger.info("Starting data transformation...")
    print("Starting data transformation...")

    main_transform()

    logger.info("Data transformation completed successfully!")
    print("Data transformation completed successfully!")

    # Loading
    logger.info("Starting data loading...")
    print("Starting data loading...")

    main_load()

    logger.info("Data loading completed successfully!")
    print("Data loading completed successfully!")

    # Completed
    logger.info("Main pipeline completed successfully!")
    print("Main pipeline completed successfully!")


if __name__ == "__main__":
    main()