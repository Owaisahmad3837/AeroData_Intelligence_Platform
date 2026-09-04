from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.transform.airline import airline_transformation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_airline_transformation(tmp_path):
    logger = log("Unit Test/Transform", "airline_transformation")
    logger.info("Starting airline transformation test.")

    input_file = tmp_path / "airlines.csv"
    output_file = tmp_path / "airlines.csv"

    test_data = pd.DataFrame({
        "Airline ID": [1, 2, 3],
        "Name": [" Airline One ", "Airline Two", "Airline Three"],
        "Alias": ["-", "-", "-"],
        "IATA": ["AA", "UA", "PK"],
        "ICAO": ["AAA", "BBB", "CCC"],
        "Callsign": ["ONE", "TWO", "THREE"],
        "Country": ["USA", "USA", "Pakistan"],
        "Active": ["Y", "N", "Y"],
    })

    test_data.to_csv(input_file, index=False)
    logger.info("Test dataset created.")

    with (
        patch(
            "src.airport_data_platform.transform.airline.Airline_path",
            input_file
        ),
        patch(
            "src.airport_data_platform.transform.airline.output_path",
            output_file
        ),
    ):
        airline_transformation()

    assert output_file.exists()

    result = pd.read_csv(output_file)

    assert "airline_id" in result.columns
    assert "airline_name" in result.columns
    assert "active" in result.columns
    assert "Alias" not in result.columns
    assert result.loc[0, "airline_name"] == " Airline One "

    logger.info(f"Output rows: {len(result)}")
    logger.info("Airline transformation test passed successfully.")