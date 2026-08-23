from ..config.db_connection import local_db_connection, neon_db_connection

from pathlib import Path

from ..config.logging_config import logging_config


# ============================================================
# FLIGHT CSV PATH
# ============================================================

Flight_path = Path(
    "data/transform/flight_data/flight.csv"
)


# ============================================================
# COLUMNS
# ============================================================

columns = [
    "year",
    "month",
    "day_of_month",
    "day_of_week",
    "flight_date",
    "operating_carrier",
    "flight_number",
    "origin_airport_code",
    "origin_city",
    "origin_state",
    "destination_airport_code",
    "destination_city",
    "destination_state",
    "crs_dep_time",
    "dep_time",
    "dep_delay",
    "taxi_out",
    "wheels_off",
    "wheels_on",
    "taxi_in",
    "crs_arr_time",
    "arr_time",
    "arr_delay",
    "cancelled",
    "cancellation_code",
    "diverted",
    "crs_elapsed_time",
    "actual_elapsed_time",
    "air_time",
    "distance",
    "carrier_delay",
    "weather_delay",
    "nas_delay",
    "security_delay",
    "late_aircraft_delay"
]


# ============================================================
# FLIGHT TABLE
# ============================================================

flight_table = """
CREATE TABLE IF NOT EXISTS flight (

    flight_id SERIAL PRIMARY KEY,

    year INTEGER,
    month INTEGER,
    day_of_month INTEGER,
    day_of_week INTEGER,

    flight_date DATE,

    operating_carrier VARCHAR(50),
    flight_number INTEGER,

    origin_airport_code VARCHAR(20),
    origin_city VARCHAR(100),
    origin_state VARCHAR(50),

    destination_airport_code VARCHAR(120),
    destination_city VARCHAR(100),
    destination_state VARCHAR(50),

    crs_dep_time INTEGER,
    dep_time INTEGER,

    dep_delay NUMERIC(10,2),

    taxi_out INTEGER,

    wheels_off INTEGER,
    wheels_on INTEGER,

    taxi_in INTEGER,

    crs_arr_time INTEGER,
    arr_time INTEGER,

    arr_delay NUMERIC(10,2),

    cancelled BOOLEAN,

    cancellation_code VARCHAR(50),

    diverted BOOLEAN,

    crs_elapsed_time INTEGER,
    actual_elapsed_time INTEGER,

    air_time INTEGER,

    distance INTEGER,

    carrier_delay NUMERIC(10,2),
    weather_delay NUMERIC(10,2),
    nas_delay NUMERIC(10,2),
    security_delay NUMERIC(10,2),
    late_aircraft_delay NUMERIC(10,2)
);
"""


# ============================================================
# POSTGRESQL COPY QUERY
# ============================================================

copy_query = f"""
COPY flight ({",".join(columns)})
FROM STDIN
WITH (
    FORMAT CSV,
    HEADER TRUE,
    NULL ''
)
"""


# ============================================================
# FAST LOCAL LOAD
# ============================================================

def flight_local_load():

    logger = logging_config(
        "loading",
        "flight"
    )

    print("Connecting to Local PostgreSQL...")

    conn = local_db_connection()
    cur = conn.cursor()

    try:

        # ----------------------------------------------------
        # CREATE TABLE
        # ----------------------------------------------------

        print("Checking flight table...")

        cur.execute(flight_table)

        conn.commit()

        print("Flight table ready.")


        # ----------------------------------------------------
        # OPTIONAL SPEED OPTIMIZATION
        # ----------------------------------------------------

        cur.execute(
            "SET synchronous_commit = OFF;"
        )


        # ----------------------------------------------------
        # CHECK FILE
        # ----------------------------------------------------

        if not Flight_path.exists():

            raise FileNotFoundError(
                f"Flight file not found: {Flight_path}"
            )


        file_size_gb = (
            Flight_path.stat().st_size
            / (1024 ** 3)
        )

        print(
            f"Flight file size: "
            f"{file_size_gb:.2f} GB"
        )


        # ----------------------------------------------------
        # START COPY
        # ----------------------------------------------------

        print(
            "\nStarting FAST PostgreSQL COPY..."
        )

        print(
            "Please wait... PostgreSQL is "
            "loading the CSV directly."
        )


        with open(
            Flight_path,
            "r",
            encoding="utf-8",
            newline=""
        ) as csv_file:

            cur.copy_expert(
                copy_query,
                csv_file,
                size=1024 * 1024
            )


        # ----------------------------------------------------
        # COMMIT
        # ----------------------------------------------------

        conn.commit()


        print(
            "\n======================================"
        )

        print(
            "Flight data loaded successfully!"
        )

        print(
            "======================================"
        )

        logger.info(
            "Flight data loaded successfully "
            "using PostgreSQL COPY."
        )


        # ----------------------------------------------------
        # CHECK ROW COUNT
        # ----------------------------------------------------

        cur.execute(
            "SELECT COUNT(*) FROM flight;"
        )

        total_rows = cur.fetchone()[0]

        print(
            f"Total rows in flight table: "
            f"{total_rows:,}"
        )


    except Exception as e:

        conn.rollback()

        logger.error(
            f"Flight loading failed: {e}"
        )

        print(
            "\n======================================"
        )

        print(
            f"ERROR: {e}"
        )

        print(
            "======================================"
        )

        raise


    finally:

        cur.close()
        conn.close()

        print(
            "Local PostgreSQL connection closed."
        )


# ============================================================
# FAST NEON LOAD
# ============================================================

def flight_neon_load():

    logger = logging_config(
        "loading",
        "flight"
    )

    print("Connecting to Neon...")

    conn = neon_db_connection()
    cur = conn.cursor()

    try:

        # ----------------------------------------------------
        # CREATE TABLE
        # ----------------------------------------------------

        print("Checking flight table...")

        cur.execute(flight_table)

        conn.commit()

        print("Flight table ready.")


        # ----------------------------------------------------
        # START COPY
        # ----------------------------------------------------

        print(
            "\nStarting FAST Neon COPY..."
        )

        with open(
            Flight_path,
            "r",
            encoding="utf-8",
            newline=""
        ) as csv_file:

            cur.copy_expert(
                copy_query,
                csv_file,
                size=1024 * 1024
            )


        # ----------------------------------------------------
        # COMMIT
        # ----------------------------------------------------

        conn.commit()


        print(
            "\n======================================"
        )

        print(
            "Flight data loaded into Neon!"
        )

        print(
            "======================================"
        )


        # ----------------------------------------------------
        # CHECK ROW COUNT
        # ----------------------------------------------------

        cur.execute(
            "SELECT COUNT(*) FROM flight;"
        )

        total_rows = cur.fetchone()[0]

        print(
            f"Total rows in Neon: "
            f"{total_rows:,}"
        )

        logger.info(
            "Flight data loaded into Neon "
            "using PostgreSQL COPY."
        )


    except Exception as e:

        conn.rollback()

        logger.error(
            f"Neon flight loading failed: {e}"
        )

        print(
            f"\nERROR: {e}"
        )

        raise


    finally:

        cur.close()
        conn.close()

        print(
            "Neon connection closed."
        )


# ============================================================
# MAIN
# ============================================================

def main_flight_load():

    logger = logging_config(
        "loading",
        "flight"
    )

    print(
        "Flight file checking..."
    )


    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if not Flight_path.exists():

        print(
            "Flight file not available!"
        )

        logger.error(
            "Flight file not available!"
        )

        return


    print(
        "Flight file available."
    )


    # --------------------------------------------------------
    # FILE SIZE
    # --------------------------------------------------------

    file_size_gb = (
        Flight_path.stat().st_size
        / (1024 ** 3)
    )

    print(
        f"Flight CSV size: "
        f"{file_size_gb:.2f} GB"
    )


    print(
        "\nStarting FAST local loading..."
    )


    # ========================================================
    # LOCAL POSTGRESQL
    # ========================================================

    flight_local_load()


    # ========================================================
    # NEON
    # ========================================================

    # اگر Neon میں بھی load کرنا ہو تو uncomment کریں:
    #
    # flight_neon_load()


    print(
        "\nFlight loading process completed!"
    )

    logger.info(
        "Flight loading process completed."
    )