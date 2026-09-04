from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.airport_data_platform.config.logging_config import logging_config as log
from src.airport_data_platform.validation.route import route_validation


def test_route_validation(tmp_path):

    logger = log("Unit Test/Validation", "route_log_validation")
    logger.info("Starting route validation testing.....")

    logger.info("Creating temporary folder.")
    input_file = tmp_path / "routes.csv"
    logger.info(f"Temporary input file: {input_file}")
    good_file = tmp_path / "good/route_data/routes.csv"
    bad_file = tmp_path / "bad/route_data/routes.csv"
    logger.info(f"Temporary good output file: {good_file}")
    logger.info(f"Temporary bad output file: {bad_file}")
    logger.info("Creating temporary output folders.")
    good_file.parent.mkdir(parents=True, exist_ok=True)
    bad_file.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Temporary output folders created.")
    logger.info("Creating test dataset.")

    test_data = pd.DataFrame({
        "Airline ID": [1, 2, 3, 4],
        "Airline": ["AA", "UA", "DL", "PK"],
        "Source airport": ["JFK", "LAX", "ORD", "ISB"],
        "Source airport ID": [100, 200, 300, 400],
        "Destination airport": ["LAX", "JFK", "ATL", "LHE"],
        "Destination airport ID": [200, 100, 500, 600],
        "Codeshare": ["Y", "Y", "Y", "Y"],
        "Equipment": ["738", "320", "737", "777"],
        "Stops": [0, 0, 1, 0],
    })

    logger.info(f"Test dataset created with {len(test_data)} rows.")
    logger.info("Saving test dataset to temporary input file.")
    test_data.to_csv(input_file, index=False)
    logger.info("Test dataset saved successfully.")
    logger.info("Patching production file paths.")
    with (
        patch(
            "src.airport_data_platform.validation.route.route_file",
            input_file
        ),
        patch(
            "src.airport_data_platform.validation.route.output_good_file",
            good_file
        ),
        patch(
            "src.airport_data_platform.validation.route.output_bad_file",
            bad_file
        ),
    ):

        logger.info("Production paths patched successfully.")
        logger.info("Running route validation function.")
        route_validation()
        logger.info("Route validation function completed.")
    logger.info("Checking whether output files were created.")
    assert good_file.exists()
    logger.info("Good output file exists.")
    assert bad_file.exists()
    logger.info("Bad output file exists.")
    logger.info("Reading validation results.")
    good_data = pd.read_csv(good_file)
    bad_data = pd.read_csv(bad_file)
    logger.info(f"Good rows: {len(good_data)}")
    logger.info(f"Bad rows: {len(bad_data)}")
    logger.info("Checking validation results.")
    assert len(good_data) == 4
    assert len(bad_data) == 0
    logger.info("Route validation test passed successfully.")