from pathlib import Path
import subprocess as sp
from ..config.logging_config import logging_config as log

dataset="ahmadrafiee/airports-airlines-planes-and-routes-update-2024"
file_name_in_kaggle="routes.csv"

def download_route_data():
  logging=log("ingestion","route_data")

  logging.info("Checking data folder.")
  make_dir=Path("data/raw/route_data")
  if make_dir.exists():
    logging.info("Data folder exists.")
  else:
    logging.info("Data folder does not exist. Creating it.")
    make_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Data folder created successfully.")

    try:
      logging.info("Downloading route data from Kaggle...")

      sp.run(
        ["kaggle","datasets","download","-d",dataset,"-f",file_name_in_kaggle,"-p",str(make_dir)],
        check=True,
      )
      logging.info("Route data downloaded successfully.")

    except sp.CalledProcessError as e:
        logging.error(f"Error occurred while downloading route data: {e}")