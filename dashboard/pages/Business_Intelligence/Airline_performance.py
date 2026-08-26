import streamlit as st
from pathlib import Path
import sys
import pandas as pd

st.set_page_config(
  page_title="Airline_performance",
  page_icon="✈️",
  layout="wide"
)


st.header("✈️ Airline Performance")
st.write("This is Airline performane Page")

dir=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(dir))


from src.airport_data_platform.config.db_connection import local_db_connection


conn=local_db_connection()



# ...........
query_total_airline="""
select count(*)as total_airline from airline
"""
query_total_airline=pd.read_sql(query_total_airline,conn)
total_airline=int(query_total_airline.iloc[0]["total_airline"])


# ...........
query_total_flight="""
select count(flight_id) as total_flight from flight
"""

query_total_flight=pd.read_sql(query_total_flight,conn)
total_flight=int(query_total_flight.iloc[0]["total_flight"])


# ...........
query_on_time = """
SELECT
    COUNT(CASE WHEN arr_delay <= 0 THEN 1 END) * 100.0
     / NULLIF(COUNT(*), 0) AS on_time
FROM flight
"""

df_on_time = pd.read_sql(query_on_time, conn)

on_time = float(df_on_time.iloc[0]["on_time"])

# ...........
query_cancellations_rate = """
SELECT
    COUNT(CASE WHEN cancelled = true THEN 1 END)*100 / NULLIF(COUNT(*), 0) AS cancelled_flight
FROM flight
"""

df_cancellations_rate = pd.read_sql(query_cancellations_rate, conn)

cancellations_rate = int(
    df_cancellations_rate.iloc[0]["cancelled_flight"]
)

# ...........

query_avg_delay = """
SELECT
    AVG(arr_delay) AS avg_delay
FROM flight
WHERE arr_delay IS NOT NULL
"""

df_avg_delay = pd.read_sql(query_avg_delay, conn)

avg_delay = float(df_avg_delay.iloc[0]["avg_delay"])

# ..................



st.header("✈️ View")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🛫 Total Airlines",
        total_airline
    )

with col2:
    st.metric(
        "✈️ Total Flights",
        f"{total_flight:,}"
    )

with col3:
    st.metric(
        "⏱️ Average Delay",
        f"{avg_delay:.1f} min"
    )

with col4:
    st.metric(
        "🟢 On-Time %",
        f"{on_time:.1f}%"
    )

with col5:
    st.metric(
        "❌ Cancellation Rate",
        f"{cancellations_rate:.1f}%"
    )



# /....................................

query_flights_airline = """
SELECT
    operating_carrier,
    COUNT(*) AS total_flights
FROM flight
GROUP BY operating_carrier
ORDER BY total_flights DESC
"""

df_flights_airline = pd.read_sql(
    query_flights_airline,
    conn
)

st.subheader("📊 Flights by Airline")

st.bar_chart(
    df_flights_airline.set_index("operating_carrier")
)


# ............................

query_on_time_airline = """
SELECT
    operating_carrier,
    COUNT(CASE WHEN arr_delay <= 0 THEN 1 END) * 100.0
        / NULLIF(COUNT(*), 0) AS on_time_percent
FROM flight
GROUP BY operating_carrier
ORDER BY on_time_percent DESC
"""

df_on_time_airline = pd.read_sql(
    query_on_time_airline,
    conn
)

st.subheader("📈 On-Time Performance")

st.bar_chart(
    df_on_time_airline.set_index("operating_carrier")
)


# ........................
best_airlines = df_on_time_airline.head(5)

st.subheader("🏆 Best Airlines")

st.dataframe(
    best_airlines,
    use_container_width=True,
    hide_index=True
)


worst_airlines = (
    df_on_time_airline
    .tail(5)
    .sort_values("on_time_percent")
)

st.subheader("⚠️ Worst Airlines")

st.dataframe(
    worst_airlines,
    use_container_width=True,
    hide_index=True
)