from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.transform.route import route_transformation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_route_transformation(tmp_path):
    logger = log("Unit Test/Transform", "route_transformation")
    logger.info("Starting route transformation test.")

    input_file = tmp_path / "routes.csv"
    output_file = tmp_path / "routes.csv"

    test_data = pd.DataFrame({
        "Airline": [" aa ", "UA", "pk"],
        "Airline ID": ["1", "2", "3"],
        "Source airport": [" jfk ", "LAX", "isb"],
        "Source airport ID": ["100", "200", "300"],
        "Destination airport": [" lax ", "JFK", "lhe"],
        "Destination airport ID": ["200", "100", "400"],
        "Codeshare": ["Y", "N", "Y"],
        "Stops": ["0", "1", "0"],
        "Equipment": [" 737 ", "A320", "777"],
    })

    test_data.to_csv(input_file, index=False)
    logger.info("Test dataset created.")

    with (
        patch(
            "src.airport_data_platform.transform.route.Route_path",
            input_file
        ),
        patch(
            "src.airport_data_platform.transform.route.output_path",
            output_file
        ),
    ):
        route_transformation()

    assert output_file.exists()

    result = pd.read_csv(output_file)

    assert "airline_code" in result.columns
    assert "airline_id" in result.columns
    assert "source_airport_code" in result.columns
    assert "destination_airport_code" in result.columns
    assert result.loc[0, "airline_code"] == "AA"
    assert result.loc[0, "source_airport_code"] == "JFK"
    assert result.loc[0, "destination_airport_code"] == "LAX"
    assert result.loc[0, "stops"] == 0

    logger.info(f"Output rows: {len(result)}")
    logger.info("Route transformation test passed successfully.")