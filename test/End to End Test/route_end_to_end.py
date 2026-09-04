import pandas as pd
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.config.logging_config import logging_config as log
from src.airport_data_platform.validation.route import route_validation
from src.airport_data_platform.transform.route import route_transformation


def test_route_e2e(tmp_path, monkeypatch):

    logger = log("End to End Test", "route_e2e_log")

    logger.info("Starting route E2E test")

    # 1. Create small test input
    raw_file = tmp_path / "routes.csv"

    data = pd.DataFrame({
        "Airline": [" EK ", " QR "],
        "Airline ID": [1, 2],
        "Source airport": [" DXB ", " DOH "],
        "Source airport ID": [100, 200],
        "Destination airport": [" LHR ", " DXB "],
        "Destination airport ID": [300, 100],
        "Codeshare": ["Y", "Y"],
        "Stops": [0, 0],
        "Equipment": [" 77W ", " A320 "]
    })

    data.to_csv(raw_file, index=False)

    logger.info("Test route data created")

    # 2. Temporary output files
    good_file = tmp_path / "good_routes.csv"
    bad_file = tmp_path / "bad_routes.csv"
    transformed_file = tmp_path / "transformed_routes.csv"

    # 3. Change paths for test
    monkeypatch.setattr(
        "src.airport_data_platform.validation.route.route_file",
        raw_file
    )

    monkeypatch.setattr(
        "src.airport_data_platform.validation.route.output_good_file",
        good_file
    )

    monkeypatch.setattr(
        "src.airport_data_platform.validation.route.output_bad_file",
        bad_file
    )

    monkeypatch.setattr(
        "src.airport_data_platform.transform.route.Route_path",
        good_file
    )

    monkeypatch.setattr(
        "src.airport_data_platform.transform.route.output_path",
        transformed_file
    )

    # 4. Validation
    logger.info("Running route validation")

    route_validation()

    # Check validation
    assert good_file.exists()
    assert bad_file.exists()

    good = pd.read_csv(good_file)
    bad = pd.read_csv(bad_file)

    assert len(good) == 2
    assert len(bad) == 0

    logger.info("Route validation passed")

    # 5. Transformation
    logger.info("Running route transformation")

    route_transformation()

    assert transformed_file.exists()

    # 6. Check result
    result = pd.read_csv(transformed_file)

    assert len(result) == 2

    assert result.loc[0, "airline_code"] == "EK"
    assert result.loc[0, "source_airport_code"] == "DXB"
    assert result.loc[0, "destination_airport_code"] == "LHR"

    assert result.loc[1, "airline_code"] == "QR"
    assert result.loc[1, "source_airport_code"] == "DOH"
    assert result.loc[1, "destination_airport_code"] == "DXB"

    logger.info("Route transformation passed")
    logger.info("Route E2E test completed successfully")