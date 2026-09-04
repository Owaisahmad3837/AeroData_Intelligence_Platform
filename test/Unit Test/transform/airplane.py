from pathlib import Path
from unittest.mock import patch
import sys
from airport_data_platform.transform.airplane import airplane_transformation
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.transform.airplane import airplane_transformation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_airplane_transformation(tmp_path):
    logger = log("Unit Test/Transform", "airplane_transformation")
    logger.info("Starting airplane transformation test.")

    input_file = tmp_path / "airplane.csv"
    output_file = tmp_path / "airplane.csv"

    test_data = pd.DataFrame({
        "Name": [" Boeing 737 ", "Airbus A320", " Boeing 777 "],
        "IATA code": [" 737 ", "a320", " 777 "],
        "ICAO code": [" b737 ", "a320", " b77w "],
    })

    test_data.to_csv(input_file, index=False)
    logger.info("Test dataset created.")

    with (
        patch(
            "src.airport_data_platform.transform.airplane.Airplane_path",
            input_file
        ),
        patch(
            "src.airport_data_platform.transform.airplane.output_path",
            output_file
        ),
    ):
        airplane_transformation()

    assert output_file.exists()

    result = pd.read_csv(output_file)

    assert "name" in result.columns
    assert "iata_code" in result.columns
    assert "icao_code" in result.columns
    assert result.loc[0, "name"] == "Boeing 737"
    assert result.loc[1, "iata_code"] == "A320"
    assert result.loc[0, "icao_code"] == "B737"

    logger.info(f"Output rows: {len(result)}")
    logger.info("Airplane transformation test passed successfully.")