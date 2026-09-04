import pandas as pd
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.config.logging_config import logging_config as log
from src.airport_data_platform.validation.airline import airline_validation
from src.airport_data_platform.transform.airline import airline_transformation


def test_airline_e2e(tmp_path, monkeypatch):

    logger = log("End to End Test", "airline_e2e_log")

    logger.info("Starting airline E2E test")

    # Create test raw data
    raw_file = tmp_path / "airlines.csv"

    data = pd.DataFrame({
        "Airline ID": [1, 2],
        "Name": ["Emirates", "Qatar Airways"],
        "Alias": ["", ""],
        "IATA": ["EK", "QR"],
        "ICAO": ["UAE", "QTR"],
        "Callsign": ["EMIRATES", "QATARI"],
        "Country": ["United Arab Emirates", "Qatar"],
        "Active": ["Y", "Y"],
    })

    data.to_csv(raw_file, index=False)

    logger.info("Test airline data created")

    # Test output files
    good_file = tmp_path / "good_airlines.csv"
    bad_file = tmp_path / "bad_airlines.csv"
    transformed_file = tmp_path / "transformed_airlines.csv"

    # Replace project paths
    monkeypatch.setattr(
        "src.airport_data_platform.validation.airline.airline_file",
        raw_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.validation.airline.output_good_file",
        good_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.validation.airline.output_bad_file",
        bad_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.transform.airline.Airline_path",
        good_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.transform.airline.output_path",
        transformed_file,
    )

    logger.info("Running airline validation")

    # Run validation
    airline_validation()

    # Check validation
    assert good_file.exists()
    assert bad_file.exists()

    good_data = pd.read_csv(good_file)
    bad_data = pd.read_csv(bad_file)

    assert len(good_data) == 2
    assert len(bad_data) == 0

    logger.info("Airline validation passed")

    # Run transformation
    logger.info("Running airline transformation")

    airline_transformation()

    # Check transformation
    assert transformed_file.exists()

    result = pd.read_csv(transformed_file)

    assert len(result) == 2

    assert result.loc[0, "airline_id"] == 1
    assert result.loc[0, "airline_name"] == "Emirates"
    assert result.loc[0, "iata_code"] == "EK"
    assert result.loc[0, "icao_code"] == "UAE"
    assert result.loc[0, "active"] == True

    logger.info("Airline transformation passed")
    logger.info("Airline E2E test completed successfully")