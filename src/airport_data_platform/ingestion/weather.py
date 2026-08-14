from pathlib import Path

import cdsapi

from ..config.logging_config import logging_config as log


dataset = "reanalysis-era5-single-levels"


def download_weather_data():
    logging = log("ingestion", "weather_data")

    # ---------------------------------------------------------
    # 1. Check/Create data folder
    # ---------------------------------------------------------

    logging.info("Checking weather data folder.")

    make_dir = Path("data/raw/weather_data")

    if make_dir.exists():
        logging.info("Weather data folder exists.")
    else:
        logging.info("Weather data folder does not exist. Creating it.")

        make_dir.mkdir(parents=True, exist_ok=True)

        logging.info("Weather data folder created successfully.")

    # ---------------------------------------------------------
    # 2. ERA5 request
    # ---------------------------------------------------------

    request = {
        "product_type": ["reanalysis"],

        "variable": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_dewpoint_temperature",
            "2m_temperature",
            "mean_sea_level_pressure",
            "surface_pressure",
            "total_precipitation",
            "total_cloud_cover"
        ],

        "year": ["2024"],

        "month": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12"
        ],

        "day": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30", "31"
        ],

        "time": ["23:00"],

        "data_format": "netcdf",

        "download_format": "zip",

        "area": [90, -180, -90, 180]
    }

    # ---------------------------------------------------------
    # 3. Download weather data
    # ---------------------------------------------------------

    file_path = make_dir / "era5_2024_23utc.zip"

    try:
        logging.info("Connecting to Copernicus CDS...")

        client = cdsapi.Client()

        logging.info("Connected to Copernicus CDS successfully.")

        logging.info("Starting ERA5 weather data download.")
        logging.info(f"Dataset: {dataset}")
        logging.info(f"Output file: {file_path}")

        client.retrieve(
            dataset,
            request,
            str(file_path)
        )

        logging.info("Weather data downloaded successfully.")
        logging.info(f"Weather data saved to: {file_path}")

        print(f"Weather data downloaded successfully: {file_path}")

    except Exception as e:
        logging.error(f"Error occurred while downloading weather data: {e}")

        print(f"Weather data download failed: {e}")