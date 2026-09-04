import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config

route_file=Path("data/raw/route_data/routes.csv")
output_good_file=Path("data/validation/good/route_data/routes.csv")
output_bad_file=Path("data/validation/bad/route_data/routes.csv")

required_columns = [
    "Airline ID",
    "Source airport",
    "Destination airport",
    "Codeshare",
    "Equipment"
 ]


def route_validation():
  log=logging_config("validation","route")

  log.info("checking route file csv...")
  print("checking route file csv... ")

  if not route_file.exists():
      print("No csv route file")
      log.warning("no csv route file exist first check it")
      return
  
  output_good_file.parent.mkdir(parents=True, exist_ok=True)
  output_bad_file.parent.mkdir(parents=True, exist_ok=True)
  print(f"File is avabile and location is {route_file}.Now start reading...")
  log.info(f"File is avabile and location is {route_file}.Now start reading...")
  df=pd.read_csv(route_file)
  print("reading full file.")
  log.info("reading full file.")

  numeric_columns = [
    "Airline ID",
    "Source airport ID",
    "Destination airport ID",
    "Stops"
]

  for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

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
    | (df["Airline"].astype(str).str.strip() == "")
    | (df["Airline ID"].notna() & (df["Airline ID"] <= 0))
    | (df["Source airport"].notna() & (df["Source airport"].astype(str).str.strip() == ""))
    | (df["Source airport ID"] <= 0)
    | (df["Destination airport"].notna() & (df["Destination airport"].astype(str).str.strip() == ""))
    | (df["Destination airport ID"] <= 0)
    | (
        df["Codeshare"].notna()
        & ~df["Codeshare"].astype(str).str.match(r"^Y$", na=False)
    )
    | (df["Stops"] < 0)
    | (df["Equipment"].notna() & (df["Equipment"].astype(str).str.strip() == ""))
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
  print("route validation complete.")
  print(f"Total rows: {len(df)}")
  print(f"Good rows: {len(good_data)}")
  print(f"Bad rows: {len(bad_data)}")
  
  log.info("route validation complete.")
  log.info(f"Total rows: {len(df)}")
  log.info(f"Good rows: {len(good_data)}")
  log.info(f"Bad rows: {len(bad_data)}")