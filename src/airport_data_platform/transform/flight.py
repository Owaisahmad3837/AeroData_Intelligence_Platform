import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config


Flight_path=Path("data/validation/good/flight_data/flight_data.csv")
output_path=Path("data/transform/flight_data/flight.csv")

numeric_columns = [
    "year",
    "month",
    "day_of_month",
    "day_of_week",
    "flight_number",
    "dep_delay",
    "taxi_out",
    "wheels_off",
    "wheels_on",
    "taxi_in",
    "arr_delay",
    "crs_elapsed_time",
    "actual_elapsed_time",
    "air_time",
    "distance",
    "carrier_delay",
    "weather_delay",
    "nas_delay",
    "security_delay",
    "late_aircraft_delay"
]

def flight_transformation():
  logger=logging_config("transform","flight")
  print("Staring")
  logger.info("starting...")
  logger.info(f"look file Flight:{Flight_path}...")
  print(f"look file Flight:{Flight_path}...")
  if not Flight_path.exists():
    logger.info("file not avabile so first check it ..... ")
    print("file not avabile so first check it .....")
    return

  logger.info(f"checking output folder if not exist so create first...")
  print(f"checking output folder if not exist so create first...")
  output_path.parent.mkdir(parents=True, exist_ok=True)



  logger.info(f"Read file Flight:{Flight_path}...")
  print(f"Read file Flight:{Flight_path}...")
  df=pd.read_csv(Flight_path)
  logger.info(f"file reading complete")
  print(f"file reading complete")

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

  for column in numeric_columns:
    df[column]=pd.to_numeric(df[column])


  df["origin_airport_code"] = df["origin_airport_code"].str.strip().str.upper()
  df["destination_airport_code"] = df["destination_airport_code"].str.strip().str.upper()
  
  df["operating_carrier"] = df["operating_carrier"].str.strip().str.upper()

  only_str_strip=[
    "origin_city",
    "destination_city",
    "origin_state",
    "destination_state"
  ]

  for column in only_str_strip:
    df[column]=df[column].str.strip()

  logger.info("Apply busness rule")
  print("Apply busness rule")
  logger.info(f"start file saving location: {output_path}...")  
  print(f"complete file save location: {output_path}...")
  df.to_csv(output_path,index=False)
  logger.info(f"complete file save location: {output_path}...")
  print(f"complete file save location: {output_path}...")
