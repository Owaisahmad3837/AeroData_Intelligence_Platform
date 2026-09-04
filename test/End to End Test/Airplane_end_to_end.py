import pandas as pd
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.config.logging_config import logging_config as log
from src.airport_data_platform.validation.airplane import airplane_validation
from src.airport_data_platform.transform.airplane import airplane_transformation


def test_airplane_e2e(tmp_path, monkeypatch):

    logger = log("End to End Test", "airplane_e2e_log")

    logger.info("Starting airplane E2E test")

    # Create test raw data
    raw_file = tmp_path / "airplane.csv"

    data = pd.DataFrame({
        "Name": [
            "Boeing 737",
            "Airbus A320"
        ],
        "IATA code": [
            " 737 ",
            " a320 "
        ],
        "ICAO code": [
            " B737 ",
            " A320 "
        ],
    })

    data.to_csv(raw_file, index=False)

    logger.info("Test airplane data created")

    # Test output files
    good_file = tmp_path / "good_airplane.csv"
    bad_file = tmp_path / "bad_airplane.csv"
    transformed_file = tmp_path / "transformed_airplane.csv"

    # Replace validation paths
    monkeypatch.setattr(
        "src.airport_data_platform.validation.airplane.airplane_file",
        raw_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.validation.airplane.output_good_file",
        good_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.validation.airplane.output_bad_file",
        bad_file,
    )

    # Replace transformation paths
    monkeypatch.setattr(
        "src.airport_data_platform.transform.airplane.Airplane_path",
        good_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.transform.airplane.output_path",
        transformed_file,
    )

    # Run validation
    logger.info("Running airplane validation")

    airplane_validation()

    # Check validation output
    assert good_file.exists()
    assert bad_file.exists()

    good_data = pd.read_csv(good_file)
    bad_data = pd.read_csv(bad_file)

    assert len(good_data) == 2
    assert len(bad_data) == 0

    logger.info("Airplane validation passed")

    # Run transformation
    logger.info("Running airplane transformation")

    airplane_transformation()

    # Check transformation output
    assert transformed_file.exists()

    result = pd.read_csv(transformed_file)

    assert len(result) == 2

    assert result.loc[0, "name"] == "Boeing 737"
    assert result.loc[0, "iata_code"] == "737"
    assert result.loc[0, "icao_code"] == "B737"

    assert result.loc[1, "name"] == "Airbus A320"
    assert result.loc[1, "iata_code"] == "A320"
    assert result.loc[1, "icao_code"] == "A320"

    logger.info("Airplane transformation passed")
    logger.info("Airplane E2E test completed successfully")