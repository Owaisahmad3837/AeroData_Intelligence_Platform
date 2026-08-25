import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Find project root
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from src.airport_data_platform.config.db_connection import local_db_connection


st.set_page_config(
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Overview")

st.write(
    "High-level airport flight performance and operational metrics."
)


# -----------------------------------
# Database Connection
# -----------------------------------

conn = local_db_connection()


# -----------------------------------
# 1. Total Flights
# -----------------------------------

query_total_flight = """
SELECT COUNT(*) AS total_flight
FROM flight
"""

df_total = pd.read_sql(query_total_flight, conn)

total_flight = int(df_total.iloc[0]["total_flight"])


# -----------------------------------
# 2. On-Time %
# -----------------------------------

query_on_time = """
SELECT
    COUNT(CASE WHEN arr_delay <= 0 THEN 1 END) * 100.0
    / COUNT(*) AS on_time
FROM flight
"""

df_on_time = pd.read_sql(query_on_time, conn)

on_time = float(df_on_time.iloc[0]["on_time"])


# -----------------------------------
# 3. Average Delay
# -----------------------------------

query_avg_delay = """
SELECT AVG(arr_delay) AS avg_delay
FROM flight
WHERE arr_delay IS NOT NULL
"""

df_avg_delay = pd.read_sql(query_avg_delay, conn)

avg_delay = float(df_avg_delay.iloc[0]["avg_delay"])


# -----------------------------------
# 4. Cancellations
# -----------------------------------

query_cancellations = """
SELECT
    COUNT(CASE WHEN cancelled = true THEN 1 END) AS cancelled_flight
FROM flight
"""

df_cancellations = pd.read_sql(query_cancellations, conn)

cancellations = int(
    df_cancellations.iloc[0]["cancelled_flight"]
)


# -----------------------------------
# 5. Flights by Month
# -----------------------------------

query_flight_by_month = """
SELECT
    month,
    COUNT(*) AS total_flights
FROM flight
GROUP BY month
ORDER BY month
"""

df_month = pd.read_sql(query_flight_by_month, conn)


# -----------------------------------
# 6. Cancellation Rate by Month
# -----------------------------------

query_cancellation_rate = """
SELECT
    month,
    COUNT(CASE WHEN cancelled = true THEN 1 END)
    * 100.0 / COUNT(*) AS cancellation_rate
FROM flight
GROUP BY month
ORDER BY month
"""

df_cancellation = pd.read_sql(
    query_cancellation_rate,
    conn
)


# -----------------------------------
# 7. Top Delayed Airlines
# -----------------------------------

query_top_delayed_airlines = """
SELECT
    a.airline_name,
    AVG(f.arr_delay) AS avg_delay
FROM flight f
JOIN airline a
    ON f.operating_carrier = a.iata_code
WHERE f.arr_delay > 0
GROUP BY a.airline_name
ORDER BY avg_delay DESC
LIMIT 10;
"""

df_airlines = pd.read_sql(
    query_top_delayed_airlines,
    conn
)


# -----------------------------------
# 8. Worst Routes
# -----------------------------------

query_worst_routes = """
SELECT
    r.source_airport_code,
    r.destination_airport_code,
    COUNT(*) AS total_flights,
    ROUND(AVG(f.arr_delay), 2) AS avg_arrival_delay
FROM route r
JOIN flight f
    ON r.source_airport_code = f.origin_airport_code
    AND r.destination_airport_code = f.destination_airport_code
WHERE f.arr_delay IS NOT NULL
GROUP BY
    r.source_airport_code,
    r.destination_airport_code
ORDER BY avg_arrival_delay DESC
LIMIT 10
"""

df_routes = pd.read_sql(
    query_worst_routes,
    conn
)


# -----------------------------------
# KPI CARDS
# -----------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Flights",
        f"{total_flight:,}"
    )


with col2:
    st.metric(
        "On-Time %",
        f"{on_time:.1f}%"
    )


with col3:
    st.metric(
        "Avg Delay",
        f"{avg_delay:.1f} min"
    )


with col4:
    st.metric(
        "Cancellations",
        f"{cancellations:,}"
    )


st.divider()


# -----------------------------------
# CHARTS — ROW 1
# -----------------------------------

col5, col6 = st.columns(2)


with col5:

    st.subheader("Flights by Month")

    st.line_chart(
        df_month.set_index("month")["total_flights"]
    )


with col6:

    st.subheader("Cancellation Rate")

    st.bar_chart(
        df_cancellation.set_index("month")["cancellation_rate"]
    )


# -----------------------------------
# CHARTS — ROW 2
# -----------------------------------

col7, col8 = st.columns(2)


with col7:

    st.subheader("Top Delayed Airlines")

    st.bar_chart(
        df_airlines.set_index("airline_name")["avg_delay"]
    )


with col8:

    st.subheader("Worst Routes")

    df_routes["route"] = (
        df_routes["source_airport_code"]
        + " → "
        + df_routes["destination_airport_code"]
    )

    st.bar_chart(
        df_routes.set_index("route")["avg_arrival_delay"]
    )


# Close connection
conn.close()