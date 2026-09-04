from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.validation.flight import flight_validation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_flight_validation(tmp_path):
    logger = log("Unit Test", "flight_log_validation")

    logger.info("Starting flight validation test.")

    input_file = tmp_path / "flight_data_2024.csv"
    good_file = tmp_path / "good/flight_data.csv"
    bad_file = tmp_path / "bad/flight_data.csv"

    logger.info(f"Input file: {input_file}")
    logger.info(f"Good output file: {good_file}")
    logger.info(f"Bad output file: {bad_file}")

    good_file.parent.mkdir(parents=True, exist_ok=True)
    bad_file.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Creating test dataset.")

    test_data = pd.DataFrame({
        "fl_date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        "op_unique_carrier": ["AA", "UA", "DL", "BA"],
        "op_carrier_fl_num": [100, 200, 300, 400],
        "origin": ["JFK", "LAX", "ORD", "ISB"],
        "dest": ["LAX", "JFK", "ATL", "LHE"],
        "crs_dep_time": [800, 900, 1000, 1100],
        "crs_arr_time": [1100, 1200, 1300, 1400],
        "cancelled": [0, 0, 1, 0],
        "diverted": [0, 0, 0, 0],
        "month": [1, 1, 1, 1],
        "day_of_month": [1, 2, 3, 4],
        "day_of_week": [1, 2, 3, 4],
        "distance": [100, 200, 300, 400],
        "taxi_out": [10, 15, 20, 25],
        "taxi_in": [5, 10, 15, 20],
        "air_time": [80, 90, 100, 110],
        "crs_elapsed_time": [120, 130, 140, 150],
        "actual_elapsed_time": [125, 135, 145, 155],
    })

    logger.info(f"Test dataset created with {len(test_data)} rows.")

    test_data.to_csv(input_file, index=False)

    logger.info("Test dataset saved successfully.")

    with (
        patch(
            "src.airport_data_platform.validation.flight.flight_raw_data",
            input_file
        ),
        patch(
            "src.airport_data_platform.validation.flight.output_good_data",
            good_file
        ),
        patch(
            "src.airport_data_platform.validation.flight.output_bad_data",
            bad_file
        ),
    ):
        logger.info("Production paths patched.")

        flight_validation()

        logger.info("Flight validation completed.")

    assert good_file.exists()
    assert bad_file.exists()

    logger.info("Output files created successfully.")

    good_data = pd.read_csv(good_file)
    bad_data = pd.read_csv(bad_file)

    logger.info(f"Good rows: {len(good_data)}")
    logger.info(f"Bad rows: {len(bad_data)}")

    assert len(good_data) == 4
    assert len(bad_data) == 0

    logger.info("Flight validation test passed successfully.")