from ..config.db_connection import  neon_db_connection,local_db_connection
import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config

route_path=Path("data/transform/route_data/routes.csv")

columns = [
    "airline_code",
    "airline_id",
    "source_airport_code",
    "source_airport_id",
    "destination_airport_code",
    "destination_airport_id",
    "codeshare",
    "stops",
    "equipment"
]


Route_table = """
CREATE TABLE IF NOT EXISTS route (
    route_id SERIAL PRIMARY KEY,
    airline_code VARCHAR(10),
    airline_id INTEGER,
    source_airport_code VARCHAR(10),
    source_airport_id INTEGER,
    destination_airport_code VARCHAR(10),
    destination_airport_id INTEGER,
    codeshare BOOLEAN,
    stops INTEGER,
    equipment VARCHAR(100),

    UNIQUE (
        airline_code,
        source_airport_code,
        destination_airport_code,
        equipment
    )
);
"""

query=f"""
insert into route(
{",".join(columns)}
)values({",".join(["%s"]*len(columns))}
)
"""


def Route_local_load(df):

    logger = logging_config("loading", "Route")

    logger.info("Connecting to local database...")
    conn = local_db_connection()
    cur = conn.cursor()

    logger.info("Creating Route table if it does not exist...")
    cur.execute(Route_table)

    logger.info("Starting Route data insertion...")


    for index, row in df[columns].iterrows():
    
         try:
            values = tuple(
                None if pd.isna(value) else value
                for value in row
            )
    
            cur.execute(query, values)
    
         except Exception as e:
            print("\n❌ ERROR ON ROW:", index)
            print(row)
            print("\nVALUES:")
            print(values)
            print("\nERROR:")
            print(e)
    
            conn.rollback()
            raise

    conn.commit()

    cur.close()
    conn.close()

    logger.info("Route data loaded into Local PostgreSQL successfully!")
    print("Route data loaded into Local PostgreSQL!")


def Route_neon_load(df):

    logger = logging_config("loading", "Route")

    logger.info("Connecting to Neon database...")
    conn = neon_db_connection()
    cur = conn.cursor()

    logger.info("Creating Route table if it does not exist...")
    cur.execute(Route_table)
    

    logger.info("Starting Route data insertion...")


    for index, row in df[columns].iterrows():

     try:
        values = tuple(
            None if pd.isna(value) else value
            for value in row
        )

        cur.execute(query, values)

     except Exception as e:
        print("\n❌ ERROR ON ROW:", index)
        print(row)
        print("\nVALUES:")
        print(values)
        print("\nERROR:")
        print(e)

        conn.rollback()
        raise



    
    conn.commit()

    cur.close()
    conn.close()

    logger.info("Route data loaded into Neon successfully!")
    print("Route data loaded into Neon!")


def main_Route_load():

    logger = logging_config("loading", "Route")

    logger.info("Route file checking...")
    print("Route file checking...")

    if not route_path.exists():

        logger.error("Route file not available!")
        print("Route file not available!")

        return

    logger.info("Route file available.")
    print("Route file available.")

    logger.info("Reading Route file...")
    print("Reading Route file...")

    df = pd.read_csv(route_path)
    df = df.where(pd.notna(df), None)

    logger.info("Route file read successfully.")
    print("Route file read successfully.")

    logger.info(f"Rows to load: {len(df)}")
    print(f"Rows to load: {len(df)}")

    Route_local_load(df)

    Route_neon_load(df)

    logger.info("Route loading completed successfully!")
    print("Route loading completed successfully!")