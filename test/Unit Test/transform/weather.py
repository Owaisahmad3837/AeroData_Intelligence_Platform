from pathlib import Path
from unittest.mock import patch
import sys
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.airport_data_platform.transform.weather import weather_transformation
from src.airport_data_platform.config.logging_config import logging_config as log


def test_weather_transformation(tmp_path):
    logger = log("Unit Test/Transform", "weather_transformation")
    logger.info("Starting weather transformation test.")

    input_file = tmp_path / "weather.parquet"
    output_file = tmp_path / "weather.parquet"

    test_data = pd.DataFrame({
        "valid_time": ["2024-01-01 23:00:00", "2024-01-02 23:00:00"],
        "u10": [1.0, 2.0],
        "v10": [2.0, 3.0],
        "d2m": [273.15, 283.15],
        "t2m": [283.15, 293.15],
        "msl": [101325, 100000],
        "sp": [100000, 99000],
        "tcc": [0.5, 0.8],
        "number": [1, 2],
        "latitude": [33.6, 31.5],
        "longitude": [73.1, 74.3],
        "expver": [1, 1],
        "airport_id": [1, 2],
        "airport_latitude": [33.6, 31.5],
        "airport_longitude": [73.1, 74.3],
        "accum_valid_time": ["2024-01-01 23:00:00", "2024-01-02 23:00:00"],
        "accum_tp": [0.001, 0.002],
        "accum_number": [1, 2],
        "accum_expver": [1, 1],
        "max_valid_time": ["2024-01-01 23:00:00", "2024-01-02 23:00:00"],
        "max_fg10": [5.0, 6.0],
        "max_number": [1, 2],
        "max_expver": [1, 1],
    })

    test_data.to_parquet(input_file, index=False)
    logger.info("Test dataset created.")

    with (
        patch(
            "src.airport_data_platform.transform.weather.Weather_path",
            input_file
        ),
        patch(
            "src.airport_data_platform.transform.weather.output_path",
            output_file
        ),
    ):
        weather_transformation()

    assert output_file.exists()

    result = pd.read_parquet(output_file)

    assert "weather_time" in result.columns
    assert "temperature_c" in result.columns
    assert "dewpoint_c" in result.columns
    assert "sea_level_pressure_hpa" in result.columns
    assert "cloud_cover_pct" in result.columns

    assert round(result.loc[0, "temperature_c"], 2) == 10.00
    assert round(result.loc[0, "dewpoint_c"], 2) == 0.00
    assert round(result.loc[0, "sea_level_pressure_hpa"], 2) == 1013.25
    assert round(result.loc[0, "cloud_cover_pct"], 2) == 50.00
    assert round(result.loc[0, "precipitation_mm"], 2) == 1.00

    logger.info(f"Output rows: {len(result)}")
    logger.info("Weather transformation test passed successfully.")