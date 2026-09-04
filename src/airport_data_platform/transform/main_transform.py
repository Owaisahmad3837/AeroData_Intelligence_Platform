from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))



from src.airport_data_platform.transform.airline import airline_transformation
from src.airport_data_platform.transform.airplane import airplane_transformation
from src.airport_data_platform.transform.airport import airport_transformation
from src.airport_data_platform.transform.flight import flight_transformation
from src.airport_data_platform.transform.route import route_transformation
from src.airport_data_platform.transform.weather import weather_transformation
from src.airport_data_platform.config.logging_config import logging_config as log



def main_transform():
    logger = log("transform", "main_transform_log")
    logger.info("Starting main transformation process.")
    logger.info("Transforming airline data...")
    airline_transformation()
    logger.info("Transforming airplane data...")
    airplane_transformation()
    logger.info("Transforming airport data...")
    airport_transformation()
    logger.info("Transforming flight data...")
    flight_transformation()
    logger.info("Transforming route data...")
    route_transformation()
    logger.info("Transforming weather data...")
    weather_transformation()        
    logger.info("Main transformation process completed successfully.")


if __name__ == "__main__":
    main_transform()