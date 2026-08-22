from pathlib import Path
import pandas as pd

from ..config.db_connection import (
    neon_db_connection,
    local_db_connection
)
from ..config.logging_config import logging_config


airport_path = Path("data/transform/airport_data/airports.csv")

create_table_sql = """
CREATE TABLE IF NOT EXISTS airport (
    airport_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    iata_code VARCHAR(10),
    icao_code VARCHAR(10),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    altitude INTEGER,
    timezone_offset NUMERIC(4,1),
    dst VARCHAR(10),
    timezone VARCHAR(100),
    airport_type VARCHAR(50),
    source VARCHAR(50)
);
"""


def airport_local_load(df):

    logger = logging_config("loading", "airport")

    logger.info("Connecting to local database...")
    conn = local_db_connection()
    cur = conn.cursor()

    logger.info("Creating airport table if it does not exist...")
    cur.execute(create_table_sql)

    logger.info("Starting airport data insertion...")

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO airport (
                airport_id,
                name,
                city,
                country,
                iata_code,
                icao_code,
                latitude,
                longitude,
                altitude,
                timezone_offset,
                dst,
                timezone,
                airport_type,
                source
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (
                row["airport_id"],
                row["name"],
                row["city"],
                row["country"],
                row["iata_code"],
                row["icao_code"],
                row["latitude"],
                row["longitude"],
                row["altitude"],
                row["timezone_offset"],
                row["dst"],
                row["timezone"],
                row["airport_type"],
                row["source"]
            )
        )

    conn.commit()

    cur.close()
    conn.close()

    logger.info("Airport data loaded into Local PostgreSQL successfully!")
    print("Airport data loaded into Local PostgreSQL!")


def airport_neon_load(df):

    logger = logging_config("loading", "airport")

    logger.info("Connecting to Neon database...")
    conn = neon_db_connection()
    cur = conn.cursor()

    logger.info("Creating airport table if it does not exist...")
    cur.execute(create_table_sql)

    logger.info("Starting airport data insertion...")

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO airport (
                airport_id,
                name,
                city,
                country,
                iata_code,
                icao_code,
                latitude,
                longitude,
                altitude,
                timezone_offset,
                dst,
                timezone,
                airport_type,
                source
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (
                row["airport_id"],
                row["name"],
                row["city"],
                row["country"],
                row["iata_code"],
                row["icao_code"],
                row["latitude"],
                row["longitude"],
                row["altitude"],
                row["timezone_offset"],
                row["dst"],
                row["timezone"],
                row["airport_type"],
                row["source"]
            )
        )

    conn.commit()

    cur.close()
    conn.close()

    logger.info("Airport data loaded into Neon successfully!")
    print("Airport data loaded into Neon!")


def main_airport_load():

    logger = logging_config("loading", "airport")

    logger.info("Airport file checking...")
    print("Airport file checking...")

    if not airport_path.exists():

        logger.error("Airport file not available!")
        print("Airport file not available!")

        return

    logger.info("Airport file available.")
    print("Airport file available.")

    logger.info("Reading airport file...")
    print("Reading airport file...")

    df = pd.read_csv(airport_path)

    logger.info("Airport file read successfully.")
    print("Airport file read successfully.")

    logger.info(f"Rows to load: {len(df)}")
    print(f"Rows to load: {len(df)}")

    airport_local_load(df)

    airport_neon_load(df)

    logger.info("Airport loading completed successfully!")
    print("Airport loading completed successfully!")