from pathlib import Path
import pandas as pd

from ..config.db_connection import (
    neon_db_connection,
    local_db_connection
)
from ..config.logging_config import logging_config


airline_path = Path("data/transform/airline_data/airlines.csv")

create_table_sql = """
CREATE TABLE IF NOT EXISTS airline(
    airline_id integer PRIMARY KEY,
    airline_name VARCHAR(255) NOT NULL,
    iata_code VARCHAR(10),
    icao_code VARCHAR(10),
    callsign  varchar(50),
    country VARCHAR(100), 
    active  BOOLEAN

)
"""


def airline_local_load(df):

    logger = logging_config("loading", "airline")

    logger.info("Connecting to local database...")
    conn = local_db_connection()
    cur = conn.cursor()

    logger.info("Creating airline table if it does not exist...")
    cur.execute(create_table_sql)

    logger.info("Starting airline data insertion...")

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO airline (
                airline_id,airline_name,iata_code,icao_code,callsign,country,active
            )
            VALUES (%s, %s, %s,%s, %s, %s,%s)
            """,
            (
                row["airline_id"],
                row["airline_name"],
                row["iata_code"],
                row["icao_code"],
                row["callsign"],
                row["country"],
                row["active"]
            )
        )

    conn.commit()

    cur.close()
    conn.close()

    logger.info("airline data loaded into Local PostgreSQL successfully!")
    print("airline data loaded into Local PostgreSQL!")


def airline_neon_load(df):

    logger = logging_config("loading", "airline")

    logger.info("Connecting to Neon database...")
    conn = neon_db_connection()
    cur = conn.cursor()

    logger.info("Creating airline table if it does not exist...")
    cur.execute(create_table_sql)

    logger.info("Starting airline data insertion...")

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO airline (
                airline_id,airline_name,iata_code,icao_code,callsign,country,active

            )
            VALUES (%s, %s, %s,%s, %s, %s,%s)
                        """,
                        (
                            row["airline_id"],
                            row["airline_name"],
                            row["iata_code"],
                            row["icao_code"],
                            row["callsign"],
                            row["country"],
                            row["active"]
            )
        )

    conn.commit()

    cur.close()
    conn.close()

    logger.info("airline data loaded into Neon successfully!")
    print("airline data loaded into Neon!")


def main_airline_load():

    logger = logging_config("loading", "airline")

    logger.info("airline file checking...")
    print("airline file checking...")

    if not airline_path.exists():

        logger.error("airline file not available!")
        print("airline file not available!")

        return

    logger.info("airline file available.")
    print("airline file available.")

    logger.info("Reading airline file...")
    print("Reading airline file...")

    df = pd.read_csv(airline_path)

    logger.info("airline file read successfully.")
    print("airline file read successfully.")

    logger.info(f"Rows to load: {len(df)}")
    print(f"Rows to load: {len(df)}")

    airline_local_load(df)

    airline_neon_load(df)

    logger.info("airline loading completed successfully!")
    print("airline loading completed successfully!")