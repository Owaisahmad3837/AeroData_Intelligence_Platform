from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.validation.weather import weather_validation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_weather_validation(tmp_path):
    logger = log("Unit Test/Validation", "weather_log_validation")

    logger.info("Starting weather validation test.")

    input_file = tmp_path / "weather.parquet"
    good_file = tmp_path / "good/weather.parquet"
    bad_file = tmp_path / "bad/weather.parquet"

    logger.info(f"Temporary input file: {input_file}")
    logger.info(f"Temporary good output file: {good_file}")
    logger.info(f"Temporary bad output file: {bad_file}")

    good_file.parent.mkdir(parents=True, exist_ok=True)
    bad_file.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Temporary output folders created.")

    test_data = pd.DataFrame({
        "valid_time": [
            "2024-01-01 23:00:00",
            "2024-01-02 23:00:00",
            "2024-01-03 23:00:00",
            "2024-01-04 23:00:00"
        ],
        "latitude": [33.6, 34.0, 31.5, 40.7],
        "longitude": [73.1, 73.2, 74.3, -74.0],
        "airport_id": [1, 2, 3, 4],
        "airport_latitude": [33.6, 34.0, 31.5, 40.7],
        "airport_longitude": [73.1, 73.2, 74.3, -74.0],
        "u10": [1.0, 2.0, 3.0, 4.0],
        "v10": [1.0, 2.0, 3.0, 4.0],
        "d2m": [270.0, 271.0, 272.0, 273.0],
        "t2m": [280.0, 281.0, 282.0, 283.0],
        "msl": [101000, 101100, 101200, 101300],
        "sp": [100000, 100100, 100200, 100300],
        "tcc": [0.2, 0.4, 0.6, 0.8],
        "number": [1, 2, 3, 4],
        "accum_tp": [0.0, 1.0, 2.0, 3.0],
        "accum_number": [1, 2, 3, 4],
        "max_fg10": [5.0, 6.0, 7.0, 8.0],
        "max_number": [1, 2, 3, 4],
    })

    logger.info(f"Test dataset created with {len(test_data)} rows.")

    test_data.to_parquet(input_file, index=False)

    logger.info("Test dataset saved successfully.")

    with (
        patch(
            "src.airport_data_platform.validation.weather.weather_file",
            input_file
        ),
        patch(
            "src.airport_data_platform.validation.weather.output_good_file",
            good_file
        ),
        patch(
            "src.airport_data_platform.validation.weather.output_bad_file",
            bad_file
        ),
    ):
        logger.info("Production paths patched successfully.")
        logger.info("Running weather validation.")

        weather_validation()

        logger.info("Weather validation completed.")

    assert good_file.exists()
    logger.info("Good output file exists.")

    assert bad_file.exists()
    logger.info("Bad output file exists.")

    good_data = pd.read_parquet(good_file)
    bad_data = pd.read_parquet(bad_file)

    logger.info(f"Good rows: {len(good_data)}")
    logger.info(f"Bad rows: {len(bad_data)}")

    assert len(good_data) == 4
    assert len(bad_data) == 0

    logger.info("Weather validation test passed successfully.")