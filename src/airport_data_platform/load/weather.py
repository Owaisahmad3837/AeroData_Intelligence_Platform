from ..config.db_connection import neon_db_connection, local_db_connection

import pandas as pd
from pathlib import Path
from psycopg2.extras import execute_values

from ..config.logging_config import logging_config


weather_path = Path("data/transform/weather_data/weather.parquet")


columns = [
    "weather_time",
    "wind_u10",
    "wind_v10",
    "dewpoint_c",
    "temperature_c",
    "sea_level_pressure_hpa",
    "surface_pressure_hpa",
    "cloud_cover_pct",
    "ensemble_number",
    "latitude",
    "longitude",
    "experiment_version",
    "airport_id",
    "airport_latitude",
    "airport_longitude",
    "accum_valid_time",
    "precipitation_mm",
    "accum_ensemble_number",
    "accum_experiment_version",
    "max_valid_time",
    "max_wind_gust",
    "max_ensemble_number",
    "max_experiment_version"
]


weather_table = """
CREATE TABLE IF NOT EXISTS weather (

    weather_id SERIAL PRIMARY KEY,

    weather_time TIMESTAMP,

    wind_u10 DOUBLE PRECISION,
    wind_v10 DOUBLE PRECISION,
    dewpoint_c DOUBLE PRECISION,
    temperature_c DOUBLE PRECISION,

    sea_level_pressure_hpa DOUBLE PRECISION,
    surface_pressure_hpa DOUBLE PRECISION,
    cloud_cover_pct DOUBLE PRECISION,

    ensemble_number INTEGER,

    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    experiment_version VARCHAR(20),

    airport_id INTEGER,

    airport_latitude DOUBLE PRECISION,
    airport_longitude DOUBLE PRECISION,

    accum_valid_time TIMESTAMP,
    precipitation_mm DOUBLE PRECISION,

    accum_ensemble_number INTEGER,
    accum_experiment_version VARCHAR(20),

    max_valid_time TIMESTAMP,
    max_wind_gust DOUBLE PRECISION,

    max_ensemble_number INTEGER,
    max_experiment_version VARCHAR(20)

);
"""


query = f"""
INSERT INTO weather (
    {",".join(columns)}
)
VALUES %s
"""


def weather_local_load(df):

    logger = logging_config("loading", "weather")

    logger.info("Connecting to local database...")
    print("Connecting to local database...")

    conn = local_db_connection()
    cur = conn.cursor()

    logger.info("Creating weather table...")
    print("Creating weather table...")

    cur.execute(weather_table)

    logger.info("Preparing weather data...")
    print(f"Preparing {len(df)} rows...")

    values = [
        tuple(
            None if pd.isna(value) else value
            for value in row
        )
        for _, row in df[columns].iterrows()
    ]

    print("Starting fast weather insertion...")

    execute_values(
        cur,
        query,
        values,
        page_size=5000
    )

    conn.commit()

    cur.close()
    conn.close()

    logger.info(
        "Weather data loaded into Local PostgreSQL successfully!"
    )

    print("Weather data loaded into Local PostgreSQL!")


def weather_neon_load(df):

    logger = logging_config("loading", "weather")

    logger.info("Connecting to Neon database...")
    print("Connecting to Neon database...")

    conn = neon_db_connection()
    cur = conn.cursor()

    logger.info("Creating weather table...")
    cur.execute(weather_table)

    print(f"Preparing {len(df)} rows...")

    values = [
        tuple(
            None if pd.isna(value) else value
            for value in row
        )
        for _, row in df[columns].iterrows()
    ]

    print("Starting weather insertion into Neon...")

    execute_values(
        cur,
        query,
        values,
        page_size=5000
    )

    conn.commit()

    cur.close()
    conn.close()

    logger.info(
        "Weather data loaded into Neon successfully!"
    )

    print("Weather data loaded into Neon!")


def main_weather_load():

    logger = logging_config("loading", "weather")

    logger.info("Weather file checking...")
    print("Weather file checking...")

    if not weather_path.exists():

        logger.error("Weather file not available!")
        print("Weather file not available!")

        return

    logger.info("Weather file available.")
    print("Weather file available.")

    logger.info("Reading weather file...")
    print("Reading weather file...")

    df = pd.read_parquet(weather_path)

    logger.info("Weather file read successfully.")
    print("Weather file read successfully.")

    logger.info(f"Rows to load: {len(df)}")
    print(f"Rows to load: {len(df)}")

    weather_local_load(df)

    # weather_neon_load(df)

    logger.info("Weather loading completed successfully!")
    print("Weather loading completed successfully!")