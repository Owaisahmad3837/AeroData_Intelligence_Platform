import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config


Airplane_path=Path("data/validation/good/airplane_data/airplane.csv")
output_path=Path("data/transform/airplane_data/airplane.csv")


def airplane_transformation():
  logger=logging_config("transform","airplane")
  print("Staring")
  logger.info("starting...")
  logger.info(f"look file Airplane:{Airplane_path}...")
  print(f"look file Airplane:{Airplane_path}...")
  if not Airplane_path.exists():
    logger.info("file not avabile so first check it ..... ")
    print("file not avabile so first check it .....")
    return

  logger.info(f"checking output folder if not exist so create first...")
  print(f"checking output folder if not exist so create first...")
  output_path.parent.mkdir(parents=True, exist_ok=True)

  logger.info(f"Read file Airplane:{Airplane_path}...")
  print(f"Read file Airplane:{Airplane_path}...")
  df=pd.read_csv(Airplane_path)
  logger.info(f"file reading complete")
  print(f"file reading complete")

  
  df = df.rename(columns={
    "Name": "name",
    "IATA code": "iata_code",
    "ICAO code": "icao_code"
})

  df["name"]=df["name"].str.strip()
  df["iata_code"] = df["iata_code"].str.strip().str.upper()
  df["icao_code"] = df["icao_code"].str.strip().str.upper()



  logger.info("Apply busness rule")
  print("Apply busness rule")
  logger.info(f"start file saving location: {output_path}...")  
  print(f"complete file save location: {output_path}...")
  df.to_csv(output_path,index=False)
  logger.info(f"complete file save location: {output_path}...")
  print(f"complete file save location: {output_path}...")
