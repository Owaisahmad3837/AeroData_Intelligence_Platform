from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.validation.airport import airport_validation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_airport_validation(tmp_path):
    logger = log("Unit Test/Validation", "airport_log_validation")

    logger.info("Starting testing.....")
    logger.info("Create temporary folder.")

    input_file = tmp_path / "airports.csv"
    good_file = tmp_path / "good/airports.csv"
    bad_file = tmp_path / "bad/airports.csv"

    logger.info("Create dataFrame.")

    test_data = pd.DataFrame({
        "Airport ID": [1, 2, 3, 4],
        "Name": [
            "Islamabad International Airport",
            "Lahore International Airport",
            None,
            "Karachi International Airport"
        ],
        "Country": [
            "Pakistan",
            "Pakistan",
            "Pakistan",
            "Pakistan"
        ],
        "Type": [
            "airport",
            "airport",
            "airport",
            "airport"
        ],
        "IATA": [
            "ISB",
            "LHE",
            "KHI",
            None
        ],
        "ICAO": [
            "OPIS",
            "OPLA",
            "OPKC",
            "OPXX"
        ],
        "Latitude": [
            33.6844,
            31.5204,
            24.8607,
            100
        ],
        "Longitude": [
            73.0479,
            74.3587,
            67.0011,
            68.0000
        ]
    })

    logger.info("Writing dataFrame to temporary CSV.")

    test_data.to_csv(input_file, index=False)

    logger.info("Patching file paths to use temporary files.")

    with (
    patch(
        "src.airport_data_platform.validation.airport.airplane_file",
        input_file
    ),
    patch(
        "src.airport_data_platform.validation.airport.output_good_file",
        good_file
    ),
    patch(
        "src.airport_data_platform.validation.airport.output_bad_file",
        bad_file
    ),
):
        logger.info("Calling airport_validation function.")

        airport_validation()

    logger.info("airport_validation function executed successfully.")

    logger.info("Checking if the good file exists.")

    assert good_file.exists()

    logger.info("Checking if the bad file exists.")

    assert bad_file.exists()

    logger.info("Reading good and bad files.")

    good_data = pd.read_csv(good_file)

    logger.info("Reading bad file.")

    bad_data = pd.read_csv(bad_file)

    assert len(good_data) == 2
    assert len(bad_data) == 2