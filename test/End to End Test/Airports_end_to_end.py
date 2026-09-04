import pandas as pd
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.config.logging_config import logging_config as log
from src.airport_data_platform.validation.airport import airport_validation
from src.airport_data_platform.transform.airport import airport_transformation


def test_airport_e2e(tmp_path, monkeypatch):

    logger = log("End to End Test", "airport_e2e_log")

    logger.info("Starting airport E2E test")

    # Create test raw data
    raw_file = tmp_path / "airports.csv"

    data = pd.DataFrame({
        "Airport ID": [1, 2],
        "Name": [
            "Dubai International Airport",
            "Hamad International Airport"
        ],
        "City": ["Dubai", "Doha"],
        "Country": ["United Arab Emirates", "Qatar"],
        "IATA": ["DXB", "DOH"],
        "ICAO": ["OMDB", "OTHH"],
        "Latitude": [25.2532, 25.2731],
        "Longitude": [55.3657, 51.6081],
        "Altitude": [62, 4],
        "Timezone": [4, 3],
        "DST": ["U", "U"],
        "Tz database time zone": [
            "Asia/Dubai",
            "Asia/Qatar"
        ],
        "Type": ["Airport", "Airport"],
        "Source": ["OurAirports", "OurAirports"],
    })

    data.to_csv(raw_file, index=False)

    logger.info("Test airport data created")

    # Test output files
    good_file = tmp_path / "good_airports.csv"
    bad_file = tmp_path / "bad_airports.csv"
    transformed_file = tmp_path / "transformed_airports.csv"

    # Replace validation paths
    monkeypatch.setattr(
        "src.airport_data_platform.validation.airport.airports_file",
        raw_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.validation.airport.output_good_file",
        good_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.validation.airport.output_bad_file",
        bad_file,
    )

    # Replace transformation paths
    monkeypatch.setattr(
        "src.airport_data_platform.transform.airport.Airport_path",
        good_file,
    )

    monkeypatch.setattr(
        "src.airport_data_platform.transform.airport.output_path",
        transformed_file,
    )

    # Run validation
    logger.info("Running airport validation")

    airport_validation()

    # Check validation
    assert good_file.exists()
    assert bad_file.exists()

    good_data = pd.read_csv(good_file)
    bad_data = pd.read_csv(bad_file)

    assert len(good_data) == 2
    assert len(bad_data) == 0

    logger.info("Airport validation passed")

    # Run transformation
    logger.info("Running airport transformation")

    airport_transformation()

    # Check transformation
    assert transformed_file.exists()

    result = pd.read_csv(transformed_file)

    assert len(result) == 2

    # First airport
    assert result.loc[0, "airport_id"] == 1
    assert result.loc[0, "name"] == "Dubai International Airport"
    assert result.loc[0, "city"] == "Dubai"
    assert result.loc[0, "country"] == "United Arab Emirates"
    assert result.loc[0, "iata_code"] == "DXB"
    assert result.loc[0, "icao_code"] == "OMDB"

    # Numeric transformation
    assert result.loc[0, "latitude"] == 25.2532
    assert result.loc[0, "longitude"] == 55.3657
    assert result.loc[0, "altitude"] == 62

    # Transformation
    assert result.loc[0, "airport_type"] == "airport"

    logger.info("Airport transformation passed")
    logger.info("Airport E2E test completed successfully")