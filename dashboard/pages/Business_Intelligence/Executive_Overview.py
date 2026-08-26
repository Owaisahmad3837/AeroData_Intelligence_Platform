import streamlit as st
import pandas as pd
import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR))


from src.airport_data_platform.config.db_connection import local_db_connection


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Executive Overview")

st.caption(
    "High-level airport flight performance and operational intelligence."
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = local_db_connection()


# ============================================================
# 1. TOTAL FLIGHTS
# ============================================================

query_total_flights = """
SELECT
    COUNT(*) AS total_flights
FROM flight
"""

df_total_flights = pd.read_sql(
    query_total_flights,
    conn
)

total_flights = int(
    df_total_flights.iloc[0]["total_flights"]
)


# ============================================================
# 2. ON-TIME PERFORMANCE
# ============================================================

query_on_time = """
SELECT
    COUNT(
        CASE
            WHEN arr_delay <= 0 THEN 1
        END
    ) * 100.0
    / NULLIF(COUNT(*), 0) AS on_time_percent

FROM flight
WHERE arr_delay IS NOT NULL
"""

df_on_time = pd.read_sql(
    query_on_time,
    conn
)

on_time_percent = float(
    df_on_time.iloc[0]["on_time_percent"]
)


# ============================================================
# 3. AVERAGE ARRIVAL DELAY
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
# 4. CANCELLED FLIGHTS
# ============================================================

query_cancelled = """
SELECT
    COUNT(
        CASE
            WHEN cancelled = TRUE THEN 1
        END
    ) AS cancelled_flights

FROM flight
"""

df_cancelled = pd.read_sql(
    query_cancelled,
    conn
)

cancelled_flights = int(
    df_cancelled.iloc[0]["cancelled_flights"]
)


# ============================================================
# 5. TOTAL AIRPORTS
# ============================================================

query_airports = """
SELECT
    COUNT(*) AS total_airports
FROM airport
"""

df_airports = pd.read_sql(
    query_airports,
    conn
)

total_airports = int(
    df_airports.iloc[0]["total_airports"]
)


# ============================================================
# 6. TOTAL AIRLINES
# ============================================================

query_airlines = """
SELECT
    COUNT(*) AS total_airlines
FROM airline
"""

df_airlines_count = pd.read_sql(
    query_airlines,
    conn
)

total_airlines = int(
    df_airlines_count.iloc[0]["total_airlines"]
)


# ============================================================
# 7. FLIGHTS BY MONTH
# ============================================================

query_flights_month = """
SELECT
    month,
    COUNT(*) AS total_flights

FROM flight

GROUP BY month

ORDER BY month
"""

df_month = pd.read_sql(
    query_flights_month,
    conn
)


# ============================================================
# 8. CANCELLATION RATE BY MONTH
# ============================================================

query_cancellation_rate = """
SELECT

    month,

    COUNT(
        CASE
            WHEN cancelled = TRUE THEN 1
        END
    ) * 100.0
    / NULLIF(COUNT(*), 0) AS cancellation_rate

FROM flight

GROUP BY month

ORDER BY month
"""

df_cancellation = pd.read_sql(
    query_cancellation_rate,
    conn
)


# ============================================================
# 9. AIRLINE PERFORMANCE
# ============================================================

query_airline_performance = """
SELECT

    a.airline_name,

    COUNT(f.flight_id) AS total_flights,

    ROUND(
        AVG(f.arr_delay)::numeric,
        2
    ) AS avg_delay,

    ROUND(
        (
            COUNT(
                CASE
                    WHEN f.arr_delay <= 0 THEN 1
                END
            ) * 100.0
            / NULLIF(
                COUNT(
                    CASE
                        WHEN f.arr_delay IS NOT NULL THEN 1
                    END
                ),
                0
            )
        )::numeric,
        2
    ) AS on_time_percent

FROM flight f

JOIN airline a
    ON f.operating_carrier = a.iata_code

GROUP BY a.airline_name

ORDER BY on_time_percent DESC
"""

df_airline_performance = pd.read_sql(
    query_airline_performance,
    conn
)


# ============================================================
# 10. WORST ROUTES
# ============================================================

query_worst_routes = """
SELECT

    origin_airport_code,
    destination_airport_code,

    COUNT(*) AS total_flights,

    ROUND(
        AVG(arr_delay)::numeric,
        2
    ) AS avg_delay

FROM flight

WHERE arr_delay IS NOT NULL

GROUP BY
    origin_airport_code,
    destination_airport_code

HAVING COUNT(*) >= 10

ORDER BY avg_delay DESC

LIMIT 10
"""

df_routes = pd.read_sql(
    query_worst_routes,
    conn
)


# ============================================================
# CREATE ROUTE LABEL
# ============================================================

if not df_routes.empty:

    df_routes["route"] = (
        df_routes["origin_airport_code"]
        + " → "
        + df_routes["destination_airport_code"]
    )


# ============================================================
# 11. WEATHER OVERVIEW
# ============================================================

query_weather = """
SELECT

    airport_id,

    ROUND(
        AVG(temperature_c)::numeric,
        2
    ) AS avg_temperature,

    ROUND(
        AVG(
            SQRT(
                POWER(wind_u10, 2)
                + POWER(wind_v10, 2)
            )
        )::numeric,
        2
    ) AS avg_wind_speed,

    ROUND(
        AVG(precipitation_mm)::numeric,
        2
    ) AS avg_precipitation,

    ROUND(
        AVG(cloud_cover_pct)::numeric,
        2
    ) AS avg_cloud_cover

FROM weather

GROUP BY airport_id

ORDER BY avg_precipitation DESC

LIMIT 10
"""

df_weather = pd.read_sql(
    query_weather,
    conn
)


# ============================================================
# KPI SECTION
# ============================================================

st.divider()

st.subheader("🎯 Key Performance Indicators")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "✈️ Total Flights",
        f"{total_flights:,}"
    )


with col2:

    st.metric(
        "🟢 On-Time %",
        f"{on_time_percent:.1f}%"
    )


with col3:

    st.metric(
        "⏱️ Avg Delay",
        f"{avg_delay:.1f} min"
    )


col4, col5, col6 = st.columns(3)


with col4:

    st.metric(
        "❌ Cancelled",
        f"{cancelled_flights:,}"
    )


with col5:

    st.metric(
        "🛄 Airports",
        f"{total_airports:,}"
    )


with col6:

    st.metric(
        "🛫 Airlines",
        f"{total_airlines:,}"
    )


# ============================================================
# FLIGHT VOLUME TREND
# ============================================================

st.divider()

st.subheader("📈 Flight Volume Trend")


st.line_chart(
    df_month.set_index("month")["total_flights"],
    use_container_width=True
)


# ============================================================
# PERFORMANCE OVERVIEW
# ============================================================

st.divider()

st.subheader("📊 Performance Overview")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# AIRLINE PERFORMANCE
# ------------------------------------------------------------

with col1:

    st.markdown("### 🛫 Airline Performance")

    if not df_airline_performance.empty:

        chart_data = (
            df_airline_performance
            .set_index("airline_name")["on_time_percent"]
        )

        st.bar_chart(
            chart_data,
            use_container_width=True
        )

    else:

        st.info("No airline performance data available.")


# ------------------------------------------------------------
# AIRPORT / CANCELLATION PERFORMANCE
# ------------------------------------------------------------

with col2:

    st.markdown("### ❌ Cancellation Rate")

    st.bar_chart(
        df_cancellation.set_index("month")[
            "cancellation_rate"
        ],
        use_container_width=True
    )


# ============================================================
# OPERATIONAL RISKS
# ============================================================

st.divider()

st.subheader("⚠️ Operational Risks")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# WORST ROUTES
# ------------------------------------------------------------

with col1:

    st.markdown("### 🛣️ Worst Routes")

    if not df_routes.empty:

        st.bar_chart(
            df_routes.set_index("route")["avg_delay"],
            use_container_width=True
        )

    else:

        st.info("No route data available.")


# ------------------------------------------------------------
# WEATHER IMPACT
# ------------------------------------------------------------

with col2:

    st.markdown("### 🌦️ Weather Impact")

    if not df_weather.empty:

        weather_chart = (
            df_weather
            .set_index("airport_id")["avg_precipitation"]
        )

        st.bar_chart(
            weather_chart,
            use_container_width=True
        )

    else:

        st.info("No weather data available.")


# ============================================================
# TOP INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Top Insights")


col1, col2, col3, col4 = st.columns(4)


# ------------------------------------------------------------
# BEST AIRLINE
# ------------------------------------------------------------

with col1:

    if not df_airline_performance.empty:

        best_airline = (
            df_airline_performance
            .sort_values(
                "on_time_percent",
                ascending=False
            )
            .iloc[0]
        )

        st.metric(
            "🏆 Best Airline",
            best_airline["airline_name"],
            f"{best_airline['on_time_percent']:.1f}%"
        )

    else:

        st.metric(
            "🏆 Best Airline",
            "N/A"
        )


# ------------------------------------------------------------
# HIGHEST TRAFFIC AIRPORT
# ------------------------------------------------------------

query_top_airport = """
SELECT

    origin_airport_code AS airport,
    COUNT(*) AS total_flights

FROM flight

GROUP BY origin_airport_code

ORDER BY total_flights DESC

LIMIT 1
"""

df_top_airport = pd.read_sql(
    query_top_airport,
    conn
)


with col2:

    if not df_top_airport.empty:

        top_airport = df_top_airport.iloc[0]

        st.metric(
            "✈️ Highest Traffic Airport",
            top_airport["airport"],
            f"{int(top_airport['total_flights']):,} flights"
        )

    else:

        st.metric(
            "✈️ Highest Traffic Airport",
            "N/A"
        )


# ------------------------------------------------------------
# WORST ROUTE
# ------------------------------------------------------------

with col3:

    if not df_routes.empty:

        worst_route = df_routes.iloc[0]

        st.metric(
            "⚠️ Worst Route",
            worst_route["route"],
            f"{worst_route['avg_delay']:.1f} min delay"
        )

    else:

        st.metric(
            "⚠️ Worst Route",
            "N/A"
        )


# ------------------------------------------------------------
# WEATHER INSIGHT
# ------------------------------------------------------------

with col4:

    if not df_weather.empty:

        worst_weather = df_weather.iloc[0]

        st.metric(
            "🌦️ Highest Rainfall",
            f"Airport {int(worst_weather['airport_id'])}",
            f"{worst_weather['avg_precipitation']:.1f} mm"
        )

    else:

        st.metric(
            "🌦️ Highest Rainfall",
            "N/A"
        )


# ============================================================
# DETAILED AIRLINE TABLE
# ============================================================

st.divider()

st.subheader("🛫 Airline Performance Details")


if not df_airline_performance.empty:

    display_airlines = df_airline_performance.copy()

    display_airlines["total_flights"] = (
        display_airlines["total_flights"]
        .map(lambda x: f"{int(x):,}")
    )

    display_airlines["avg_delay"] = (
        display_airlines["avg_delay"]
        .map(lambda x: f"{float(x):.1f} min")
    )

    display_airlines["on_time_percent"] = (
        display_airlines["on_time_percent"]
        .map(lambda x: f"{float(x):.1f}%")
    )

    display_airlines.columns = [
        "Airline",
        "Flights",
        "Avg Delay",
        "On-Time %"
    ]

    st.dataframe(
        display_airlines,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# WEATHER DETAILS
# ============================================================

st.divider()

st.subheader("🌦️ Weather Overview")


if not df_weather.empty:

    display_weather = df_weather.copy()

    display_weather.columns = [
        "Airport ID",
        "Avg Temperature °C",
        "Avg Wind",
        "Avg Precipitation mm",
        "Avg Cloud Cover %"
    ]

    st.dataframe(
        display_weather,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()