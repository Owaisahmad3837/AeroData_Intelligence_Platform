from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.validation.airplane import airplane_validation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_airplane_validation(tmp_path):
    logger=log("Unit Test","airplane_log_validation")


    logger.info("Starting testing.....")
    logger.info("Create temporary folder.")
    input_file = tmp_path / "airplanes.csv"
    good_file = tmp_path / "good/airplanes.csv"
    bad_file = tmp_path / "bad/airplanes.csv"


    logger.info("Create dataFrame.")
    test_data = pd.DataFrame({
    "Airline ID": [1, 2, 3, 4],
    "Name": ["Air One", "Air Two", None, "Air Four"],
    "IATA code": ["AA", "BB", "CC", None],
    "ICAO code": ["AAA", "BBB", "CCC", "DDD"]
})

    logger.info("read dataFrame.")
    test_data.to_csv(input_file, index=False)

    logger.info("Patching Path to use temporary folder.")
    with (
        patch(
            "src.airport_data_platform.validation.airplane.airplane_file",
            input_file
        ),
        patch(
            "src.airport_data_platform.validation.airplane.output_good_file",
            good_file
        ),
        patch(
            "src.airport_data_platform.validation.airplane.output_bad_file",
            bad_file
        ),
    ):
        logger.info("Calling download_airplane_data function.")
        airplane_validation()
        
    logger.info("airplane_validation function executed successfully.")
    logger.info("Checking if the good and bad files exist.")

    assert good_file.exists()
    logger.info("Checking if the bad file exists.")
    assert bad_file.exists()


    logger.info("Reading good and bad files.")
    good_data = pd.read_csv(good_file)
    logger.info("Reading bad files.")
    bad_data = pd.read_csv(bad_file)

    assert len(good_data) == 2
    assert len(bad_data) == 2