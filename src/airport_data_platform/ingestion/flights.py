from pathlib import Path
import subprocess 
from ..config.logging_config import logging_config 
import logging


def  download_flight_data():
  logging=logging_config("ingestion","flight_data")


  logging.info("Checking data folder.")
  make_dir=Path("data/raw/flight_data")
  data_file = make_dir / "flight_data_2024.csv"
  if data_file.exists():

        logging.info(
            "Flight data already exists. Skipping download."
        )

        print(
            "Flight data already exists. Skipping download."
        )

        return

    # Create folder if it doesn't exist
  if make_dir.exists():
      logging.info("Data folder exists.")
  else:
    logging.info("Data folder does not exist. Creating it.")
    make_dir.mkdir(parents=True, exist_ok=True)

  try:
    logging.info("Downloading flight data from Kaggle.")

    subprocess.run(
    [
      "kaggle",
      "datasets",
      "download",
      "-d",
      "hrishitpatil/flight-data-2024",
      "-f",
      "flight_data_2024.csv",
      "-p",
      str(make_dir),

              ],
      check=True,
  )
    logging.info("Flight data downloaded successfully.")
    print("Flight data downloaded successfully.")
  except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while downloading flight data: {e}")
        print("Error occurred while downloading flight data. Check logs for details.")

if __name__ == "__main__":
    download_flight_data()