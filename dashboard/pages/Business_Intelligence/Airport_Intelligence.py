import streamlit as st
from pathlib import Path
import pandas as pd
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[3]

sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# DATABASE
# ============================================================

from src.airport_data_platform.config.db_connection import (
    local_db_connection
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Airport Intelligence",
    page_icon="🛫",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🛫 Airport Intelligence")

st.caption(
    "Airport traffic, delays and operational reliability"
)

st.divider()


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = local_db_connection()


# ============================================================
# 1. TOTAL AIRPORTS
# ============================================================

query_total_airports = """
SELECT
    COUNT(airport_id) AS total_airport
FROM airport
"""

total_airport = pd.read_sql(
    query_total_airports,
    conn
)

total_airport = int(
    total_airport.iloc[0]["total_airport"]
)


# ============================================================
# 2. TOTAL FLIGHTS
# ============================================================

query_total_flight = """
SELECT
    COUNT(flight_id) AS total_flight
FROM flight
"""

total_flight = pd.read_sql(
    query_total_flight,
    conn
)

total_flight = int(
    total_flight.iloc[0]["total_flight"]
)


# ============================================================
# 3. AVERAGE DELAY
# ============================================================

query_avg_delay = """
SELECT
    AVG(arr_delay) AS avg_delay
FROM flight
WHERE arr_delay IS NOT NULL
"""

df_avg_delay = pd.read_sql(
    query_avg_delay,
    conn
)

avg_delay = float(
    df_avg_delay.iloc[0]["avg_delay"]
)


# ============================================================
# 4. BUSIEST AIRPORT
# ============================================================
# Overall traffic = departures + arrivals

query_busiest_airport = """
SELECT
    airport_code,
    COUNT(*) AS total_flights

FROM (

    SELECT
        origin_airport_code AS airport_code
    FROM flight

    UNION ALL

    SELECT
        destination_airport_code AS airport_code
    FROM flight

) AS airport_traffic

GROUP BY airport_code

ORDER BY total_flights DESC

LIMIT 1
"""

df_busiest = pd.read_sql(
    query_busiest_airport,
    conn
)

busiest_airport = df_busiest.iloc[0]["airport_code"]


# ============================================================
# 5. ON-TIME %
# ============================================================

query_on_time = """
SELECT

    COUNT(
        CASE
            WHEN arr_delay <= 0 THEN 1
        END
    ) * 100.0

    / NULLIF(
        COUNT(
            CASE
                WHEN arr_delay IS NOT NULL THEN 1
            END
        ),
        0
    ) AS on_time

FROM flight
"""

df_on_time = pd.read_sql(
    query_on_time,
    conn
)

on_time = float(
    df_on_time.iloc[0]["on_time"]
)


# ============================================================
# 6. BUSIEST AIRPORTS
# ============================================================

query_busiest_airports = """
SELECT

    airport_code,

    COUNT(*) AS total_flights

FROM (

    SELECT
        origin_airport_code AS airport_code
    FROM flight

    UNION ALL

    SELECT
        destination_airport_code AS airport_code
    FROM flight

) AS airport_traffic

GROUP BY airport_code

ORDER BY total_flights DESC

LIMIT 10
"""

df_busiest_airports = pd.read_sql(
    query_busiest_airports,
    conn
)


# ============================================================
# AIRPORT KPIs
# ============================================================

st.subheader("🎯 Airport KPIs")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🛄 Total Airports",
        f"{total_airport:,}"
    )


with col2:

    st.metric(
        "✈️ Total Flights",
        f"{total_flight:,}"
    )


with col3:

    st.metric(
        "⏱️ Avg Delay",
        f"{avg_delay:.1f} min"
    )


col4, col5 = st.columns(2)


with col4:

    st.metric(
        "🏆 Busiest Airport",
        busiest_airport
    )


with col5:

    st.metric(
        "🟢 Avg On-Time",
        f"{on_time:.1f}%"
    )


# ============================================================
# BUSIEST AIRPORTS
# ============================================================

st.divider()

st.subheader("📊 Busiest Airports")


st.bar_chart(
    df_busiest_airports.set_index("airport_code")[
        "total_flights"
    ],
    use_container_width=True
)


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()