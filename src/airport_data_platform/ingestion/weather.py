
import time
from pathlib import Path

import pandas as pd
import requests

from ..config.logging_config import logging_config as log


OPEN_METEO_URL = (
    "https://archive-api.open-meteo.com/v1/archive"
)

AIRPORT_DATA = Path(
    "data/raw/airport_data/airports.csv"
)

OUTPUT_DIR = Path(
    "data/raw/weather_data"
)

OUTPUT_FILE = OUTPUT_DIR / "weather.csv"

START_DATE = "2024-01-01"
END_DATE = "2025-01-01"


HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "rain",
    "weather_code",
    "cloud_cover",
    "wind_speed_10m",
    "wind_direction_10m",
    "visibility",
]


def download_weather_data():

    print("========== Downloading Weather Data ==========")

    logger = log(
        "ingestion",
        "weather_data"
    )

    # --------------------------------------------------
    # 1. Check airport CSV
    # --------------------------------------------------

    print("Checking airport CSV...")

    if not AIRPORT_DATA.exists():

        logger.error(
            "Airport CSV file not found."
        )

        print(
            "Airport CSV file not found."
        )

        return

    logger.info(
        "Airport CSV file found."
    )

    # --------------------------------------------------
    # 2. Read airport CSV
    # --------------------------------------------------

    airport_csv_df = pd.read_csv(
        AIRPORT_DATA
    )

    logger.info(
        f"Loaded {len(airport_csv_df)} airports."
    )

    print(
        f"Loaded {len(airport_csv_df)} airports."
    )

    # --------------------------------------------------
    # 3. Create output directory
    # --------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        f"Weather output directory: "
        f"{OUTPUT_DIR.resolve()}"
    )

    # --------------------------------------------------
    # 4. Start processing airports
    # --------------------------------------------------

    print(
        "Downloading weather data..."
    )

    for index, airport in airport_csv_df.iterrows():

        airport_id = airport["Airport ID"]
        latitude = airport["Latitude"]
        longitude = airport["Longitude"]
        airport_name = airport["Name"]

        print(
            f"[{index + 1}/{len(airport_csv_df)}] "
            f"{airport_name} (ID: {airport_id})"
        )

        logger.info(
            f"Starting airport {airport_id}: "
            f"{airport_name}"
        )

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": START_DATE,
            "end_date": END_DATE,
            "hourly": ",".join(
                HOURLY_VARIABLES
            ),
            "timezone": "auto",
        }

        # --------------------------------------------------
        # 5. Request with retry
        # --------------------------------------------------

        max_retries = 5

        for attempt in range(max_retries):

            try:

                response = requests.get(
                    OPEN_METEO_URL,
                    params=params,
                    timeout=60
                )

                # Rate limit
                if response.status_code == 429:

                    wait_time = 30 * (attempt + 1)

                    logger.warning(
                        f"Rate limit reached for "
                        f"airport {airport_id}. "
                        f"Waiting {wait_time} seconds..."
                    )

                    print(
                        f"Rate limit reached. "
                        f"Waiting {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                # Other HTTP errors
                response.raise_for_status()

                # Success
                data = response.json()

                break

            except requests.RequestException as e:

                logger.error(
                    f"Request failed for "
                    f"airport {airport_id}: {e}"
                )

                if attempt == max_retries - 1:

                    print(
                        f"Skipping airport "
                        f"{airport_id}."
                    )

                    data = None

                    break

                wait_time = 10 * (attempt + 1)

                print(
                    f"Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

        # --------------------------------------------------
        # 6. Check API response
        # --------------------------------------------------

        if data is None:

            continue

        if "hourly" not in data:

            logger.error(
                f"No hourly data for "
                f"airport {airport_id}."
            )

            logger.error(
                f"API response: {data}"
            )

            print(
                f"No hourly data for "
                f"airport {airport_id}. Skipping."
            )

            continue

        # --------------------------------------------------
        # 7. Convert hourly data to DataFrame
        # --------------------------------------------------

        weather_data = pd.DataFrame(
            data["hourly"]
        )

        if weather_data.empty:

            logger.warning(
                f"Empty weather data for "
                f"airport {airport_id}."
            )

            continue

        # --------------------------------------------------
        # 8. Add airport information
        # --------------------------------------------------

        weather_data["airport_id"] = airport_id

        weather_data["Latitude"] = latitude

        weather_data["Longitude"] = longitude

        weather_data["Airport Name"] = airport_name

        # --------------------------------------------------
        # 9. Save immediately
        # --------------------------------------------------

        weather_data.to_csv(
            OUTPUT_FILE,
            mode="a",
            header=not OUTPUT_FILE.exists(),
            index=False
        )

        # --------------------------------------------------
        # 10. Success message
        # --------------------------------------------------

        logger.info(
            f"Airport {airport_id} "
            f"{airport_name} "
            f"downloaded and saved successfully."
        )

        print(
            f"Weather data for airport "
            f"{airport_name} "
            f"(ID: {airport_id}) "
            f"downloaded and saved successfully."
        )

        # --------------------------------------------------
        # 11. Small delay
        # --------------------------------------------------

        time.sleep(2)

    # --------------------------------------------------
    # 12. Final check
    # --------------------------------------------------

    if OUTPUT_FILE.exists():

        file_size = OUTPUT_FILE.stat().st_size

        logger.info(
            f"Weather CSV created successfully: "
            f"{OUTPUT_FILE.resolve()}"
        )

        print()
        print(
            "========== Weather Download Completed =========="
        )

        print(
            f"CSV file saved successfully:"
        )

        print(
            OUTPUT_FILE.resolve()
        )

        print(
            f"File size: {file_size / 1024 / 1024:.2f} MB"
        )

    else:

        logger.error(
            "Weather CSV file was not created."
        )

        print(
            "ERROR: Weather CSV file was not created."
        )


if __name__ == "__main__":
    download_weather_data()
