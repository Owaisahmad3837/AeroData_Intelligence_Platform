import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config

airplane_file=Path("data/raw/airplane_data/airplanes.csv")
output_good_file=Path("data/validation/good/airplane_data/airplane.csv")
output_bad_file=Path("data/validation/bad/airplane_data/airplane.csv")

required_columns = [
    "Name",
    "IATA code",
    "ICAO code"
]


def airplane_validation():
  log=logging_config("validation","airplanes")

  log.info("checking airport file csv...")
  print("checking airport file csv... ")

  if not airplane_file.exists():
      print("No csv airline file")
      log.warning("no csv airline file exist first check it")
      return
  
  output_good_file.parent.mkdir(parents=True, exist_ok=True)
  output_bad_file.parent.mkdir(parents=True, exist_ok=True)
  print(f"File is avabile and location is {airplane_file}.Now start reading...")
  log.info(f"File is avabile and location is {airplane_file}.Now start reading...")
  df=pd.read_csv(airplane_file)
  print("reading full file.")
  log.info("reading full file.")

  missing_column=[
    column
    for column in required_columns
    if column not in df.columns
  ]
  if missing_column:
    print(f"Missing column:{missing_column}")
    log.error(f"Missing column:{missing_column}")
    return

  bad_mask = (
      df[required_columns].isnull().any(axis=1)
  )

  bad_data = df[bad_mask]
  good_data = df[~bad_mask]

  print("Saving good data...")
  log.info("Saving good data...")
  good_data.to_csv(
           output_good_file,
           index=False
      )
  print("Saving bad data...")
  log.info("Saving bad data...")
  bad_data.to_csv(
           output_bad_file,
          index=False
      )
  print()
  print("airplane validation complete.")
  print(f"Total rows: {len(df)}")
  print(f"Good rows: {len(good_data)}")
  print(f"Bad rows: {len(bad_data)}")
  
  log.info("airplane validation complete.")
  log.info(f"Total rows: {len(df)}")
  log.info(f"Good rows: {len(good_data)}")
  log.info(f"Bad rows: {len(bad_data)}")