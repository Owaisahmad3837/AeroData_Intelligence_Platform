import pandas as pd
from pathlib import Path 
import logging 

airline=Path("../data/raw/airline_data/airlines.csv")
airplane=Path("../data/raw/airplane_data/airplanes.csv")
airport=Path("../data/raw/airport_data/airports.csv")
flight=Path("../data/raw/flight_data/flight_data_2024.csv")
route=Path("../data/raw/route_data/routes.csv")
weather=Path("../data/processed/weather_data/final_weather_2024.parquet")

log_folder = Path("../logs/data_profile")
log_folder.mkdir(parents=True, exist_ok=True)

log_file = log_folder / "data_profile.log"

logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
logger = logging.getLogger("data_profile")


def check_all_data():

 
  logger.info("READ Airline file....")
  print("READ Airline file....")
  df_1=pd.read_csv(airline)
  logger.info("READ Airline file complete")
  

  df_1_column=df_1.columns
  df_1_head=df_1.head()
  df_1_type=df_1.dtypes

  print("column name :")
  print(df_1_column)
  logger.info(f"column names:{df_1_column} ")
  print("")
  print("Head:")
  print(df_1_head)
  logger.info(f"head:{df_1_head} ")
  print("column name :")
  print(df_1_type)
  logger.info(f"Data Types:{df_1_type} ")

# .............airplane............



  logger.info("READ Airline file....")
  print("READ Airplane file....")
  df_2=pd.read_csv(airplane)
  logger.info("READ airplane file complete")
  

  df_2_column=df_2.columns
  df_2_head=df_2.head()
  df_2_type=df_2.dtypes

  print("column name :")
  print(df_2_column)
  logger.info(f"column names:{df_2_column} ")
  print("")
  print("Head:")
  print(df_2_head)
  logger.info(f"head:{df_2_head} ")
  print("column name :")
  print(df_2_type)
  logger.info(f"Data Types:{df_1_type} ")

# ............airport..........

  logger.info("READ Airport file....")
  print("READ Airport file....")
  df_3=pd.read_csv(airport)
  logger.info("READ Airport file complete")
  

  df_3_column=df_3.columns
  df_3_head=df_3.head()
  df_3_type=df_3.dtypes

  print("column name :")
  print(df_3_column)
  logger.info(f"column names:{df_3_column} ")
  print("")
  print("Head:")
  print(df_3_head)
  logger.info(f"head:{df_3_head} ")
  print("column name :")
  print(df_1_type)
  logger.info(f"Data Types:{df_3_type} ")

# ............flight..................
  logger.info("READ Flight file....")
  print("READ Flight file....")
  df_4=pd.read_csv(flight)
  logger.info("READ Flight file complete")
  

  df_4_column=df_4.columns
  df_4_head=df_4.head()
  df_4_type=df_4.dtypes

  print("column name :")
  print(df_4_column)
  logger.info(f"column names:{df_4_column} ")
  print("")
  print("Head:")
  print(df_4_head)
  logger.info(f"head:{df_4_head} ")
  print("column name :")
  print(df_4_type)
  logger.info(f"Data Types:{df_4_type} ")


# ..........route..................
  logger.info("READ Route file....")
  print("READ Route file....")
  df_5=pd.read_csv(route)
  logger.info("READ Route file complete")
  

  df_5_column=df_5.columns
  df_5_head=df_5.head()
  df_5_type=df_5.dtypes

  print("column name :")
  print(df_5_column)
  logger.info(f"column names:{df_5_column} ")
  print("")
  print("Head:")
  print(df_5_head)
  logger.info(f"head:{df_5_head} ")
  print("column name :")
  print(df_5_type)
  logger.info(f"Data Types:{df_5_type} ")

# ....................weather................
  logger.info("READ Weather file....")
  print("READ Weather file....")
  df_6=pd.read_parquet(weather)
  logger.info("READ Weather file complete")
  

  df_6_column=df_6.columns
  df_6_head=df_6.head()
  df_6_type=df_6.dtypes

  print("column name :")
  print(df_6_column)
  logger.info(f"column names:{df_6_column} ")
  print("")
  print("Head:")
  print(df_6_head)
  logger.info(f"head:{df_6_head} ")
  print("column name :")
  print(df_6_type)
  logger.info(f"Data Types:{df_6_type} ")


    
  






check_all_data()
