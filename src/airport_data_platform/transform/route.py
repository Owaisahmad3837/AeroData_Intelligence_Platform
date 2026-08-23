import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config


Route_path=Path("data/validation/good/route_data/routes.csv")
output_path=Path("data/transform/route_data/routes.csv")


def route_transformation():
  logger=logging_config("transform","route")
  print("Staring")
  logger.info("starting...")
  logger.info(f"look file Route:{Route_path}...")
  print(f"look file Route:{Route_path}...")
  if not Route_path.exists():
    logger.info("file not avabile so first check it ..... ")
    print("file not avabile so first check it .....")
    return

  logger.info(f"checking output folder if not exist so create first...")
  print(f"checking output folder if not exist so create first...")
  output_path.parent.mkdir(parents=True, exist_ok=True)

  logger.info(f"Read file Route:{Route_path}...")
  print(f"Read file Route:{Route_path}...")
  df=pd.read_csv(Route_path)
  logger.info(f"file reading complete")
  print(f"file reading complete")

  df = df.rename(columns={
        "Airline": "airline_code",
        "Airline ID": "airline_id",
        "Source airport": "source_airport_code",
        "Source airport ID": "source_airport_id",
        "Destination airport": "destination_airport_code",
        "Destination airport ID": "destination_airport_id",
        "Codeshare": "codeshare",
        "Stops": "stops",
        "Equipment": "equipment"
    })

  df["airline_code"] = (
    df["airline_code"]
    .str.strip()
    .str.upper()
)

  df["source_airport_code"] = (
    df["source_airport_code"]
    .str.strip()
    .str.upper()
)

  df["destination_airport_code"] = (
    df["destination_airport_code"]
    .str.strip()
    .str.upper()
)

  df["airline_id"] = pd.to_numeric(
    df["airline_id"], errors="coerce"
).astype("Int64")

  df["source_airport_id"] = pd.to_numeric(
    df["source_airport_id"], errors="coerce"
).astype("Int64")

  df["destination_airport_id"] = pd.to_numeric(
    df["destination_airport_id"], errors="coerce"
).astype("Int64")

  df["stops"] = pd.to_numeric(
    df["stops"], errors="coerce"
).astype("Int64")

  df["codeshare"] = (
    df["codeshare"]
    .fillna("")
    .str.strip()
    .str.upper()
    .map({
        "Y": True,
        "N": False
    })
)

  df["equipment"] = (
    df["equipment"]
    .fillna("")
    .str.strip()
    .str.upper()
)




  logger.info("Apply busness rule")
  print("Apply busness rule")
  logger.info(f"start file saving location: {output_path}...")  
  print(f"complete file save location: {output_path}...")
  df.to_csv(output_path,index=False)
  logger.info(f"complete file save location: {output_path}...")
  print(f"complete file save location: {output_path}...")
