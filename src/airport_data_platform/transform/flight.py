import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config


Flight_path = Path("data/validation/good/flight_data/flight_data.csv")
output_path = Path("data/transform/flight_data/flight.csv")


integer_columns = [
    "year",
    "month",
    "day_of_month",
    "day_of_week",
    "flight_number",
    "crs_dep_time",
    "dep_time",
    "taxi_out",
    "wheels_off",
    "wheels_on",
    "taxi_in",
    "crs_arr_time",
    "arr_time",
    "crs_elapsed_time",
    "actual_elapsed_time",
    "air_time",
    "distance"
]

decimal_columns = [
    "dep_delay",
    "arr_delay",
    "carrier_delay",
    "weather_delay",
    "nas_delay",
    "security_delay",
    "late_aircraft_delay"
]


def clean_chunk(df):

    df = df.rename(columns={
        "fl_date": "flight_date",
        "op_unique_carrier": "operating_carrier",
        "op_carrier_fl_num": "flight_number",
        "origin": "origin_airport_code",
        "origin_city_name": "origin_city",
        "origin_state_nm": "origin_state",
        "dest": "destination_airport_code",
        "dest_city_name": "destination_city",
        "dest_state_nm": "destination_state"
    })

    # Integer columns
    for column in integer_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).astype("Int64")

    # Decimal columns
    for column in decimal_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Clean airport codes
    for column in [
        "origin_airport_code",
        "destination_airport_code"
    ]:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.upper()
        )

    # Clean carrier
    df["operating_carrier"] = (
        df["operating_carrier"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # Clean city/state
    for column in [
        "origin_city",
        "destination_city",
        "origin_state",
        "destination_state"
    ]:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df


def flight_transformation():

    logger = logging_config("transform", "flight")

    print("Starting flight transformation...")

    if not Flight_path.exists():
        print("Flight file not available!")
        return

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Remove old transformed file
    if output_path.exists():
        output_path.unlink()
        print("Old transformed file removed.")

    first_chunk = True
    total_rows = 0

    print("Starting chunk processing...")

    for chunk in pd.read_csv(
        Flight_path,
        chunksize=50000,
        low_memory=False
    ):

        chunk = clean_chunk(chunk)

        chunk.to_csv(
            output_path,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        total_rows += len(chunk)

        print(f"Processed {total_rows} rows...")

        first_chunk = False

    print("Flight transformation completed!")
    print(f"Total rows: {total_rows}")
    print(f"Output: {output_path}")

    logger.info("Flight transformation completed successfully!")