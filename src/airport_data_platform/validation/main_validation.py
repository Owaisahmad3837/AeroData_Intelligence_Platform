from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.validation.airline import airline_validation
from src.airport_data_platform.validation.airplane import airplane_validation
from src.airport_data_platform.validation.airport import airport_validation
from src.airport_data_platform.validation.flight import flight_validation
from src.airport_data_platform.validation.route import route_validation
from src.airport_data_platform.validation.weather import weather_validation
from src.airport_data_platform.config.logging_config import logging_config as log



def main_validation():
    logger = log("validation", "main_validation_log")
    logger.info("Starting main validation process.")
    logger.info("Validating airline data...")
    airline_validation()
    logger.info("Validating airplane data...")
    airplane_validation()
    logger.info("Validating airport data...")
    airport_validation()
    logger.info("Validating flight data...")
    flight_validation()
    logger.info("Validating route data...")
    route_validation()
    logger.info("Validating weather data...")
    weather_validation()
    logger.info("Main validation process completed successfully.")

if __name__ == "__main__":
    main_validation()


