from pathlib import Path
import pandas as pd

from ..config.db_connection import (
    neon_db_connection,
    local_db_connection
)
from ..config.logging_config import logging_config


airplane_path = Path("data/transform/airplane_data/airplane.csv")

create_table_sql = """
CREATE TABLE IF NOT EXISTS airplane(
    airplane_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    iata_code VARCHAR(10),
    icao_code VARCHAR(10)
)
"""


def airplane_local_load(df):

    logger = logging_config("loading", "airplane")

    logger.info("Connecting to local database...")
    conn = local_db_connection()
    cur = conn.cursor()

    logger.info("Creating airplane table if it does not exist...")
    cur.execute(create_table_sql)

    logger.info("Starting airplane data insertion...")

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO airplane (
                name,
                iata_code,
                icao_code
            )
            VALUES (%s, %s, %s)
            """,
            (
                row["name"],
                row["iata_code"],
                row["icao_code"]
            )
        )

    conn.commit()

    cur.close()
    conn.close()

    logger.info("Airplane data loaded into Local PostgreSQL successfully!")
    print("Airplane data loaded into Local PostgreSQL!")


def airplane_neon_load(df):

    logger = logging_config("loading", "airplane")

    logger.info("Connecting to Neon database...")
    conn = neon_db_connection()
    cur = conn.cursor()

    logger.info("Creating airplane table if it does not exist...")
    cur.execute(create_table_sql)

    logger.info("Starting airplane data insertion...")

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO airplane (
                name,
                iata_code,
                icao_code
            )
            VALUES (%s, %s, %s)
            """,
            (
                row["name"],
                row["iata_code"],
                row["icao_code"]
            )
        )

    conn.commit()

    cur.close()
    conn.close()

    logger.info("Airplane data loaded into Neon successfully!")
    print("Airplane data loaded into Neon!")


def main_airplane_load():

    logger = logging_config("loading", "airplane")

    logger.info("Airplane file checking...")
    print("Airplane file checking...")

    if not airplane_path.exists():

        logger.error("Airplane file not available!")
        print("Airplane file not available!")

        return

    logger.info("Airplane file available.")
    print("Airplane file available.")

    logger.info("Reading airplane file...")
    print("Reading airplane file...")

    df = pd.read_csv(airplane_path)

    logger.info("Airplane file read successfully.")
    print("Airplane file read successfully.")

    logger.info(f"Rows to load: {len(df)}")
    print(f"Rows to load: {len(df)}")

    airplane_local_load(df)

    airplane_neon_load(df)

    logger.info("Airplane loading completed successfully!")
    print("Airplane loading completed successfully!")