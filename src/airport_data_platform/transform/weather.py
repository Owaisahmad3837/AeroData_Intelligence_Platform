import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config


Weather_path=Path("data/validation/good/weather_data/weather.parquet")
output_path=Path("data/transform/weather_data/weather.parquet")


def weather_transformation():
  logger=logging_config("transform","weather")
  print("Staring")
  logger.info("starting...")
  logger.info(f"look file Weather:{Weather_path}...")
  print(f"look file Weather:{Weather_path}...")
  if not Weather_path.exists():
    logger.info("file not avabile so first check it ..... ")
    print("file not avabile so first check it .....")
    return

  logger.info(f"checking output folder if not exist so create first...")
  print(f"checking output folder if not exist so create first...")
  output_path.parent.mkdir(parents=True, exist_ok=True)

  logger.info(f"Read file Weather:{Weather_path}...")
  print(f"Read file Weather:{Weather_path}...")
  df=pd.read_parquet(Weather_path)
  logger.info(f"file reading complete")
  print(f"file reading complete")

  df = df.rename(columns={
    "valid_time": "weather_time",
    "u10": "wind_u10",
    "v10": "wind_v10",
    "d2m": "dewpoint_c",
    "t2m": "temperature_c",
    "msl": "sea_level_pressure_hpa",
    "sp": "surface_pressure_hpa",
    "tcc": "cloud_cover_pct",
    "number": "ensemble_number",
    "latitude": "latitude",
    "longitude": "longitude",
    "expver": "experiment_version",
    "airport_id": "airport_id",
    "airport_latitude": "airport_latitude",
    "airport_longitude": "airport_longitude",
    "accum_valid_time": "accum_valid_time",
    "accum_tp": "precipitation_mm",
    "accum_number": "accum_ensemble_number",
    "accum_expver": "accum_experiment_version",
    "max_valid_time": "max_valid_time",
    "max_fg10": "max_wind_gust",
    "max_number": "max_ensemble_number",
    "max_expver": "max_experiment_version"
})


  numeric_columns = [
    "wind_u10",
    "wind_v10",
    "temperature_c",
    "dewpoint_c",
    "sea_level_pressure_hpa",
    "surface_pressure_hpa",
    "cloud_cover_pct",
    "ensemble_number",
    "latitude",
    "longitude",
    "airport_id",
    "airport_latitude",
    "airport_longitude",
    "precipitation_mm",
    "accum_ensemble_number",
    "max_wind_gust",
    "max_ensemble_number"
]

  for column in numeric_columns:
    df[column] = pd.to_numeric(df[column])

  df["weather_time"]=pd.to_datetime(df["weather_time"])
  df["accum_valid_time"] = pd.to_datetime(df["accum_valid_time"])
  df["max_valid_time"] = pd.to_datetime(df["max_valid_time"])

  df["temperature_c"] = df["temperature_c"] - 273.15
  df["dewpoint_c"] = df["dewpoint_c"] - 273.15

  df["sea_level_pressure_hpa"] = df["sea_level_pressure_hpa"] / 100
  df["surface_pressure_hpa"] = df["surface_pressure_hpa"] / 100

  df["cloud_cover_pct"] = df["cloud_cover_pct"] * 100

  df["precipitation_mm"] = df["precipitation_mm"] * 1000

  

  logger.info("Apply busness rule")
  print("Apply busness rule")
  logger.info(f"start file saving location: {output_path}...")  
  print(f"complete file save location: {output_path}...")
  df.to_parquet(output_path,index=False)
  logger.info(f"complete file save location: {output_path}...")
  print(f"complete file save location: {output_path}...")
