import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config


Airport_path=Path("data/validation/good/airports_data/airports.csv")
output_path=Path("data/transform/airport_data/airports.csv")


def airport_transformation():
  logger=logging_config("transform","airport")
  print("Staring")
  logger.info("starting...")
  logger.info(f"look file Airport:{Airport_path}...")
  print(f"look file Airport:{Airport_path}...")
  if not Airport_path.exists():
    logger.info("file not avabile so first check it ..... ")
    print("file not avabile so first check it .....")
    return

  logger.info(f"checking output folder if not exist so create first...")
  print(f"checking output folder if not exist so create first...")
  output_path.parent.mkdir(parents=True, exist_ok=True)

  logger.info(f"Read file Airport:{Airport_path}...")
  print(f"Read file Airport:{Airport_path}...")
  df=pd.read_csv(Airport_path)
  logger.info(f"file reading complete")
  print(f"file reading complete")

  df = df.rename(columns={
    "Airport ID": "airport_id",
    "Name": "name",
    "City": "city",
    "Country": "country",
    "IATA": "iata_code",
    "ICAO": "icao_code",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Altitude": "altitude",
    "Timezone": "timezone_offset",
    "DST": "dst",
    "Tz database time zone": "timezone",
    "Type": "airport_type",
    "Source": "source"
})
  
  print("AFTER RENAME:")
  print(df.columns.tolist())



  df["name"] = df["name"].str.strip()
  df["city"] = df["city"].str.strip()

  df["country"] = df["country"].str.strip().str.strip("*")

  df["iata_code"] = df["iata_code"].str.strip().str.strip("*").str.upper()
  df["icao_code"] = df["icao_code"].str.strip().str.upper()

  df["source"] = df["source"].str.strip().str.strip("*")

# Convert numeric columns
  df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
  df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
  df["altitude"] = pd.to_numeric(df["altitude"], errors="coerce")
  df["timezone_offset"] = pd.to_numeric(df["timezone_offset"], errors="coerce")

# Convert DST
  df["dst"] = df["dst"].map({
    "Y": True,
    "N": False,
    "U": None
})

# Clean text
  df["timezone"] = df["timezone"].str.strip()
  df["airport_type"] = df["airport_type"].str.strip().str.lower()
  
  
  


  logger.info("Apply busness rule")
  print("Apply busness rule")
  logger.info(f"start file saving location: {output_path}...")  
  print(f"complete file save location: {output_path}...")
  df.to_csv(output_path,index=False)
  logger.info(f"complete file save location: {output_path}...")
  print(f"complete file save location: {output_path}...")
