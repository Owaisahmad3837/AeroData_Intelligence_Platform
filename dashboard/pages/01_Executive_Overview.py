import streamlit as st
import pandas as pd
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
# Add project root to Python path
sys.path.insert(0, str(ROOT_DIR))

from src.airport_data_platform.config.db_connection import local_db_connection

st.set_page_config(
  page_title="Executive Overview",
  page_icon="📊",
  layout="wide"
)


st.title("Executive Overview")
st.write(
    "High-level airport flight performance and operational metrics."
)


conn=local_db_connection()

query="""
select count(*) as total_flight ,avg(arr_delay) as delay_flight ,count(*) filter(where cancelled = true)as cancelled from flight
"""

df=pd.read_sql(query,conn)

Total_flight=int(df.iloc[0]["total_flight"])
delay_flight=float(df.iloc[0]["delay_flight"])
cancelled=int(df.iloc[0]["cancelled"])

col1,col2,col3=st.columns(3)

with col1:
  st.metric("Total Flight",f"{Total_flight:,}")


with col2:
  st.metric("Total Delay",f"{delay_flight:%}")


with col3:
  st.metric("Total cancelled",f"{cancelled:,}")


  monthly_query = """
SELECT
    month,
    COUNT(*) AS total_flights
FROM flight
GROUP BY month
ORDER BY month
"""

monthly_df = pd.read_sql(monthly_query, conn)

st.subheader("Flights by Month")

st.bar_chart(
    monthly_df.set_index("month")["total_flights"]
)