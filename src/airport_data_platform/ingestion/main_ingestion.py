from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.ingestion.airlines import download_airline_data
from src.airport_data_platform.ingestion.airplanes import download_airplane_data
from src.airport_data_platform.ingestion.airports import download_airport_data
from src.airport_data_platform.ingestion.flights import download_flight_data
from src.airport_data_platform.ingestion.routes import download_route_data
from src.airport_data_platform.ingestion.weather import download_weather_data
from src.airport_data_platform.config.logging_config import logging_config as log



def main_ingestion():
    logger = log("ingestion", "main_ingestion_log")
    logger.info("Starting main ingestion process.")
    logger.info("Downloading airline data...")
    download_airline_data()
    logger.info("Downloading airplane data...")
    download_airplane_data()
    logger.info("Downloading airport data...")
    download_airport_data()
    logger.info("Downloading flight data...")
    download_flight_data()
    logger.info("Downloading route data...")
    download_route_data()
    logger.info("Downloading weather data...")
    download_weather_data()
    logger.info("Main ingestion process completed successfully.")

if __name__ == "__main__":
    main_ingestion()


