from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.transform.airport import airport_transformation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_airport_transformation(tmp_path):
    logger = log("Unit Test/Transform", "airport_transformation")
    logger.info("Starting airport transformation test.")

    input_file = tmp_path / "airports.csv"
    output_file = tmp_path / "airports.csv"

    test_data = pd.DataFrame({
        "Airport ID": [1, 2, 3],
        "Name": [" Airport One ", "Airport Two", "Airport Three"],
        "City": [" Islamabad ", " Lahore ", " Karachi "],
        "Country": ["Pakistan*", "Pakistan", "Pakistan*"],
        "IATA": [" isb ", "lhe", "khi"],
        "ICAO": [" opis ", "opla", "opkc"],
        "Latitude": ["33.6844", "31.5204", "24.8607"],
        "Longitude": ["73.0479", "74.3587", "67.0011"],
        "Altitude": ["5400", "700", "30"],
        "Timezone": [" 5 ", "5", "5"],
        "DST": ["N", "Y", "U"],
        "Tz database time zone": ["Asia/Karachi", "Asia/Karachi", "Asia/Karachi"],
        "Type": [" Airport ", "AIRPORT", "Airport"],
        "Source": ["OurAirports*", "OurAirports", "OurAirports*"],
    })

    test_data.to_csv(input_file, index=False)
    logger.info("Test dataset created.")

    with (
        patch(
            "src.airport_data_platform.transform.airport.Airport_path",
            input_file
        ),
        patch(
            "src.airport_data_platform.transform.airport.output_path",
            output_file
        ),
    ):
        airport_transformation()

    assert output_file.exists()

    result = pd.read_csv(output_file)

    assert "airport_id" in result.columns
    assert "airport_type" in result.columns
    assert result.loc[0, "name"] == "Airport One"
    assert result.loc[0, "country"] == "Pakistan"
    assert result.loc[0, "iata_code"] == "ISB"
    assert result.loc[0, "icao_code"] == "OPIS"
    assert result.loc[0, "latitude"] == 33.6844
    assert result.loc[0, "dst"] == False
    assert result.loc[1, "dst"] == True

    logger.info(f"Output rows: {len(result)}")
    logger.info("Airport transformation test passed successfully.")