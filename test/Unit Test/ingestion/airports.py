from pathlib import Path
from unittest.mock import patch
import sys
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.ingestion.airports import download_airport_data
from src.airport_data_platform.config.logging_config import logging_config as log


def test_download_airport_data(tmp_path):
  logger=log("Unit Test","airport_log")

  logger.info("Starting testing.....")
  logger.info("Create temporary folder.")

  test_folder_path = tmp_path / "data/raw/airport_test_data"
  logger.info(f"Temporary folder created at: {test_folder_path}")

  logger.info("Patching Path to use temporary folder.")
  with (
    patch("src.airport_data_platform.ingestion.airports.Path") as mock_path,
    patch("src.airport_data_platform.ingestion.airports.sp.run") as mock_run,
):
    mock_path.return_value=test_folder_path
    logger.info("Calling download_airport_data function.")
    download_airport_data()
    logger.info("download_airport_data function executed successfully.")
    logger.info("Checking if the temporary folder exists.")
    assert test_folder_path.exists()
    
    logger.info("Checking kaggle command.")
    mock_run.assert_called_once()


