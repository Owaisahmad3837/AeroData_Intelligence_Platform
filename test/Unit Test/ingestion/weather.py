from pathlib import Path
from unittest.mock import patch
import sys
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.ingestion.weather import download_weather_data
from src.airport_data_platform.config.logging_config import logging_config as log


def test_download_weather_data(tmp_path):
  logger=log("Unit Test/Ingestion","weather_log")

  logger.info("Starting testing.....")

  logger.info("Create temporary folder.")
  test_folder_path = tmp_path / "data/raw/airline_test_data"
  logger.info(f"Temporary folder created at: {test_folder_path}")

  logger.info("Patching Path to use temporary folder.")
  with (
    patch("src.airport_data_platform.ingestion.weather.Path") as mock_path,
    patch("src.airport_data_platform.ingestion.weather.cdsapi.Client") as mock_cdsapi,
):
    mock_path.return_value=test_folder_path
    logger.info("Calling download_weather_data function.")
    download_weather_data()
    logger.info("download_weather_data function executed successfully.")
    logger.info("Checking if the temporary folder exists.")
    assert test_folder_path.exists()
    
    logger.info("Checking kaggle command.")
    mock_cdsapi.assert_called_once()

