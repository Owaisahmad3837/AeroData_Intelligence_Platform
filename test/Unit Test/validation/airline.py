from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.validation.airline import airline_validation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_airline_validation(tmp_path):
    logger=log("Unit Test","airline_log_validation")


    logger.info("Starting testing.....")
    logger.info("Create temporary folder.")
    input_file = tmp_path / "airlines.csv"
    good_file = tmp_path / "good/airlines.csv"
    bad_file = tmp_path / "bad/airlines.csv"


    logger.info("Create dataFrame.")
    test_data = pd.DataFrame({
        "Airline ID": [1, 2, -3, 4],
        "Name": ["Air One", "Air Two", "Air Three", "Air Four"],
        "IATA": ["AA", "BB", "CC", "DD"],
        "ICAO": ["AAA", "BBB", "CCC", "DDD"],
        "Active": ["Y", "N", "Y", "X"]
    })

    logger.info("read dataFrame.")
    test_data.to_csv(input_file, index=False)

    logger.info("Patching Path to use temporary folder.")
    with (
        patch(
            "src.airport_data_platform.validation.airline.airline_file",
            input_file
        ),
        patch(
            "src.airport_data_platform.validation.airline.output_good_file",
            good_file
        ),
        patch(
            "src.airport_data_platform.validation.airline.output_bad_file",
            bad_file
        ),
    ):
        logger.info("Calling download_airplane_data function.")
        airline_validation()
        
    logger.info("airline_validation function executed successfully.")
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