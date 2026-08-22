import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config

airplane_file=Path("data/raw/airport_data/airports.csv")
output_good_file=Path("data/validation/good/airports_data/airports.csv")
output_bad_file=Path("data/validation/bad/airports_data/airports.csv")

required_columns = [
   "Airport ID",
   'Name',
   'Country',
   'Type'
]


def airport_validation():
  log=logging_config("validation","airports")

  log.info("checking airports file csv...")
  print("airports airport file csv... ")

  if not airplane_file.exists():
      print("No csv airports file")
      log.warning("no csv airports file exist first check it")
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

  if "IATA" not in df.columns:
    df["IATA"] = pd.NA

  if "ICAO" not in df.columns:
    df["ICAO"] = pd.NA

  bad_mask = (
    df[required_columns].isnull().any(axis=1)
    | (df["Airport ID"] <= 0)
    | (df["Name"].astype(str).str.strip() == "")
    | (df["Country"].astype(str).str.strip() == "")
    | (
        df["IATA"].notna()
        & ~df["IATA"].astype(str).str.match(r"^[A-Z]{3}$", na=False)
    )
    | (
        df["ICAO"].notna()
        & ~df["ICAO"].astype(str).str.match(r"^[A-Z]{4}$", na=False)
    )
    | (
        df["Latitude"].notna()
        & ~df["Latitude"].between(-90, 90)
    )
    | (
        df["Longitude"].notna()
        & ~df["Longitude"].between(-180, 180)
    )
    | df["Airport ID"].duplicated(keep=False)
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
  print("airports validation complete.")
  print(f"Total rows: {len(df)}")
  print(f"Good rows: {len(good_data)}")
  print(f"Bad rows: {len(bad_data)}")
  
  log.info("airports validation complete.")
  log.info(f"Total rows: {len(df)}")
  log.info(f"Good rows: {len(good_data)}")
  log.info(f"Bad rows: {len(bad_data)}")