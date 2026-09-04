from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


from src.airport_data_platform.load.airline import main_airline_load
from src.airport_data_platform.load.flight import main_flight_load
from src.airport_data_platform.load.airport import main_airport_load
from src.airport_data_platform.load.airplane import main_airplane_load
from src.airport_data_platform.load.weather import main_weather_load
from src.airport_data_platform.config.logging_config import logging_config as log




def main_load():
    logger = log("loading", "main_load")

    logger.info("Starting data loading process...")

    print("Starting data loading process...")
    logger.info("Loading data airline ...")
    main_airline_load()
    logger.info("Loading data airplane ...")
    main_airplane_load()
    logger.info("Loading data airport ...")
    main_airport_load()
    logger.info("Loading data flight ...")
    main_flight_load()
    logger.info("Loading data weather ...")
    main_weather_load()

    logger.info("Data loading process completed successfully!")
    print("Data loading process completed successfully!")


if __name__ == "__main__":
    main_load()