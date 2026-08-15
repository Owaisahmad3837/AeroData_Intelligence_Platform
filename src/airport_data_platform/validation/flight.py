import pandas as pd
from pathlib import Path

from ..config.logging_config import logging_config as log

validation_folder = Path("data/validation")
validation_good_data_folder = Path("data/validation/good/flight_data")
validation_bad_data_folder = Path("data/validation/bad/flight_data")
flight_raw_data = Path("data/raw/flight_data/flight_data_2024.csv")
output_good_data = Path("data/validation/good/flight_data/flight_data.csv")
output_bad_data = Path("data/validation/bad/flight_data/flight_data.csv")


required_columns = [
    "fl_date",
    "op_unique_carrier",
    "op_carrier_fl_num",
    "origin",
    "dest",
    "crs_dep_time",
    "crs_arr_time",
    "cancelled",
    "diverted"
]

def flight_validation():

    logger = log("validation", "flight_validation")
    logger.info("Checking flight.csv file...")
    if not flight_raw_data.exists():
        print("Flight raw file not available.")
        logger.error(
            f"Flight raw file not available: {flight_raw_data}"
        )
        return


    print("Flight raw file available.")
    logger.info("Flight raw file available.")
    validation_folder.mkdir(parents=True,exist_ok=True)
    validation_good_data_folder.mkdir(parents=True,exist_ok=True)
    validation_bad_data_folder.mkdir(parents=True,exist_ok=True)
    logger.info("Validation folders checked OR created.")

    print("Reading flight CSV...")
    logger.info("Reading flight CSV...")
    df = pd.read_csv(flight_raw_data)
    print("Flight CSV read.")
    logger.info("Flight CSV read.")


    missing_columns = [column
        for column in required_columns
        if column not in df.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        logger.error(
            f"Missing columns: {missing_columns}"
        )

        return


    print("Checking bad data...")
    logger.info("Checking bad data...")


    bad_mask = (

        df[required_columns]
        .isnull()
        .any(axis=1)


        | ~df["month"].between(1, 12)

        | ~df["day_of_month"].between(1, 31)

        | ~df["day_of_week"].between(1, 7)

        | (df["distance"] < 0)

        | ~df["cancelled"].isin([0, 1])

        | ~df["diverted"].isin([0, 1])

        | (df["origin"] == df["dest"])

        | (df["taxi_out"] < 0)

        | (df["taxi_in"] < 0)

        | (df["air_time"] < 0)

        | (df["crs_elapsed_time"] < 0)

        | (df["actual_elapsed_time"] < 0)
    )

    bad = df[bad_mask]

    print("Checking good data...")
    logger.info("Checking good data...")

    good = df[~bad_mask]

    print("Saving good data...")
    logger.info("Saving good data...")
    good.to_csv(
        output_good_data,
        index=False
    )
    print("Saving bad data...")
    logger.info("Saving bad data...")
    bad.to_csv(
        output_bad_data,
        index=False
    )
    print()
    print("Flight validation complete.")
    print(f"Total rows: {len(df)}")
    print(f"Good rows: {len(good)}")
    print(f"Bad rows: {len(bad)}")

    logger.info("Flight validation complete.")
    logger.info(f"Total rows: {len(df)}")
    logger.info(f"Good rows: {len(good)}")
    logger.info(f"Bad rows: {len(bad)}")



