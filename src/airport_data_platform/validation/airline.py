import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config

airline_file=Path("data/raw/airline_data/airlines.csv")
output_good_file = Path("data/validation/good/airline_data/airlines.csv")
output_bad_file = Path("data/validation/bad/airline_data/airlines.csv")

required_columns=[
  "Airline ID",
  "Name"
]


def airline_validation():

  logger=logging_config("validation","airlines")

  logger.info("checking airport file csv...")
  print("checking airport file csv... ")

  if not airline_file.exists():
    print("No csv airline file")
    logger.warning("no csv airline file exist first check it")
    return

  output_good_file.parent.mkdir(parents=True, exist_ok=True)
  output_bad_file.parent.mkdir(parents=True, exist_ok=True)
  print(f"File is avabile and location is {airline_file}.Now start reading...")
  logger.info(f"File is avabile and location is {airline_file}.Now start reading...")
  df=pd.read_csv(airline_file)
  print("reading full file.")
  logger.info("reading full file.")

  missing_column=[
    column
    for column in required_columns
    if column not in df.columns
  ]
  if missing_column:
    print(f"Missing column:{missing_column}")
    logger.error(f"Missing column:{missing_column}")
    return

  bad_mask = (
    df[required_columns].isnull().any(axis=1)
    | (df["Airline ID"] <= 0)
    | df["Airline ID"].duplicated(keep=False)
    | (df["IATA"].notna() & df["IATA"].duplicated(keep=False))
    | (df["ICAO"].notna() & df["ICAO"].duplicated(keep=False))
    | (df["IATA"].notna() & (df["IATA"].str.len() != 2))
    | (df["ICAO"].notna() & (df["ICAO"].str.len() != 3))
    | (df["Active"].notna() & ~df["Active"].isin(["Y", "N"]))
)

  bad_data = df[bad_mask]
  good_data = df[~bad_mask]

  print("Saving good data...")
  logger.info("Saving good data...")
  good_data.to_csv(
          output_good_file,
          index=False
      )
  print("Saving bad data...")
  logger.info("Saving bad data...")
  bad_data.to_csv(
          output_bad_file,
          index=False
      )
  print()
  print("airline validation complete.")
  print(f"Total rows: {len(df)}")
  print(f"Good rows: {len(good_data)}")
  print(f"Bad rows: {len(bad_data)}")
  
  logger.info("airline validation complete.")
  logger.info(f"Total rows: {len(df)}")
  logger.info(f"Good rows: {len(good_data)}")
  logger.info(f"Bad rows: {len(bad_data)}")
  


  
