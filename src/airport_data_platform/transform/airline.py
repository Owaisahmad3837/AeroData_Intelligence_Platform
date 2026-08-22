import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config


Airline_path=Path("data/validation/good/airline_data/airlines.csv")
output_path=Path("data/transform/airline_data/airlines.csv")


def airline_transformation():
  logger=logging_config("transform","airline")
  print("Staring")
  logger.info("starting...")
  logger.info(f"look file Airline:{Airline_path}...")
  print(f"look file Airline:{Airline_path}...")
  if not Airline_path.exists():
    logger.info("file not avabile so first check it ..... ")
    print("file not avabile so first check it .....")
    return

  logger.info(f"checking output folder if not exist so create first...")
  print(f"checking output folder if not exist so create first...")
  output_path.parent.mkdir(parents=True, exist_ok=True)

  logger.info(f"Read file Airline:{Airline_path}...")
  print(f"Read file Airline:{Airline_path}...")
  df=pd.read_csv(Airline_path)
  logger.info(f"file reading complete")
  print(f"file reading complete")

  
  df=df.rename(columns={
    "Airline ID":"airline_id",
    "Name":"airline_name",
    "IATA":"iata_code",
    "ICAO":"icao_code",
    "Callsign":"callsign",
    "Country":"country",
    "Active":"active"
  })
  df=df.drop(columns=["Alias"])

  df["active"]=df["active"].map(
    {
      "Y":True,
      "N":False
    }
  )


  logger.info("Apply busness rule")
  print("Apply busness rule")
  logger.info(f"start file saving location: {output_path}...")  
  print(f"complete file save location: {output_path}...")
  df.to_csv(output_path,index=False)
  logger.info(f"complete file save location: {output_path}...")
  print(f"complete file save location: {output_path}...")
