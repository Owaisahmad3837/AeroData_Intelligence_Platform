import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def local_db_connection():

  # db_password = os.getenv("local_db_password")
  conn=psycopg2.connect(
    host="localhost",
    database="Airport_data_platform",
    user="owais",
    password="owais7383",
    port="5432"
  )

  print("Local Database connect Scuessfully!")

  return conn

def neon_db_connection():
  neon=os.getenv("NEON_DATABASE_URL")
  conn=psycopg2.connect(neon)

  print("Neon Database connect Scuessfully!")

  return conn