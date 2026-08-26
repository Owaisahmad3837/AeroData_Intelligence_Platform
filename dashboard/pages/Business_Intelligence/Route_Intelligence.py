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
    page_title="Route Intelligence",
    page_icon="🛣️",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🛣️ Route Intelligence")

st.caption(
    "Route traffic, reliability and operational risk"
)

st.divider()


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = local_db_connection()


# ============================================================
# 1. TOTAL ROUTES
# ============================================================

query_total_routes = """

SELECT
    COUNT(DISTINCT (
        origin_airport_code,
        destination_airport_code
    )) AS total_routes

FROM flight

WHERE
    origin_airport_code IS NOT NULL
    AND destination_airport_code IS NOT NULL

"""

df_total_routes = pd.read_sql(
    query_total_routes,
    conn
)

total_routes = int(
    df_total_routes.iloc[0]["total_routes"]
)


# ============================================================
# 2. TOTAL FLIGHTS
# ============================================================

query_total_flights = """

SELECT
    COUNT(flight_id) AS total_flights

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
# 4. BUSIEST ROUTE
# ============================================================

query_busiest_route = """

SELECT

    origin_airport_code,
    destination_airport_code,

    COUNT(*) AS total_flights

FROM flight

WHERE
    origin_airport_code IS NOT NULL
    AND destination_airport_code IS NOT NULL

GROUP BY
    origin_airport_code,
    destination_airport_code

ORDER BY
    total_flights DESC

LIMIT 1

"""

df_busiest_route = pd.read_sql(
    query_busiest_route,
    conn
)

busiest_route = (
    df_busiest_route.iloc[0]["origin_airport_code"]
    + " → "
    + df_busiest_route.iloc[0]["destination_airport_code"]
)


# ============================================================
# 5. WORST ROUTE
# ============================================================
# Minimum 100 flights prevents tiny routes
# from dominating the ranking.

query_worst_route = """

SELECT

    origin_airport_code,
    destination_airport_code,

    COUNT(*) AS total_flights,

    AVG(arr_delay) AS avg_delay

FROM flight

WHERE
    arr_delay IS NOT NULL
    AND origin_airport_code IS NOT NULL
    AND destination_airport_code IS NOT NULL

GROUP BY
    origin_airport_code,
    destination_airport_code

HAVING COUNT(*) >= 100

ORDER BY
    avg_delay DESC

LIMIT 1

"""

df_worst_route = pd.read_sql(
    query_worst_route,
    conn
)

worst_route = (
    df_worst_route.iloc[0]["origin_airport_code"]
    + " → "
    + df_worst_route.iloc[0]["destination_airport_code"]
)


# ============================================================
# 6. BUSIEST ROUTES
# ============================================================

query_busiest_routes = """

SELECT

    origin_airport_code,
    destination_airport_code,

    COUNT(*) AS total_flights

FROM flight

WHERE
    origin_airport_code IS NOT NULL
    AND destination_airport_code IS NOT NULL

GROUP BY
    origin_airport_code,
    destination_airport_code

ORDER BY
    total_flights DESC

LIMIT 10

"""

df_busiest_routes = pd.read_sql(
    query_busiest_routes,
    conn
)

df_busiest_routes["route"] = (
    df_busiest_routes["origin_airport_code"]
    + " → "
    + df_busiest_routes["destination_airport_code"]
)


# ============================================================
# 7. ROUTE PERFORMANCE
# ============================================================

query_route_performance = """

SELECT

    origin_airport_code,
    destination_airport_code,

    COUNT(*) AS total_flights,

    AVG(arr_delay) AS avg_delay

FROM flight

WHERE
    arr_delay IS NOT NULL
    AND origin_airport_code IS NOT NULL
    AND destination_airport_code IS NOT NULL

GROUP BY
    origin_airport_code,
    destination_airport_code

HAVING COUNT(*) >= 100

ORDER BY
    avg_delay DESC

LIMIT 10

"""

df_route_performance = pd.read_sql(
    query_route_performance,
    conn
)

df_route_performance["route"] = (
    df_route_performance["origin_airport_code"]
    + " → "
    + df_route_performance["destination_airport_code"]
)


# ============================================================
# 8. ON-TIME % BY ROUTE
# ============================================================

query_route_on_time = """

SELECT

    origin_airport_code,
    destination_airport_code,

    COUNT(*) AS total_flights,

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

WHERE
    origin_airport_code IS NOT NULL
    AND destination_airport_code IS NOT NULL

GROUP BY
    origin_airport_code,
    destination_airport_code

HAVING
    COUNT(
        CASE
            WHEN arr_delay IS NOT NULL THEN 1
        END
    ) >= 100

ORDER BY
    on_time DESC

LIMIT 10

"""

df_route_on_time = pd.read_sql(
    query_route_on_time,
    conn
)

df_route_on_time["route"] = (
    df_route_on_time["origin_airport_code"]
    + " → "
    + df_route_on_time["destination_airport_code"]
)


# ============================================================
# 9. CANCELLATION RATE BY ROUTE
# ============================================================

query_route_cancellation = """

SELECT

    origin_airport_code,
    destination_airport_code,

    COUNT(*) AS total_flights,

    COUNT(
        CASE
            WHEN cancelled = true THEN 1
        END
    ) * 100.0

    / NULLIF(COUNT(*), 0) AS cancellation_rate

FROM flight

WHERE
    origin_airport_code IS NOT NULL
    AND destination_airport_code IS NOT NULL

GROUP BY
    origin_airport_code,
    destination_airport_code

HAVING COUNT(*) >= 100

ORDER BY
    cancellation_rate DESC

LIMIT 10

"""

df_route_cancellation = pd.read_sql(
    query_route_cancellation,
    conn
)

df_route_cancellation["route"] = (
    df_route_cancellation["origin_airport_code"]
    + " → "
    + df_route_cancellation["destination_airport_code"]
)


# ============================================================
# 10. BEST ROUTES
# ============================================================

query_best_routes = """

SELECT

    origin_airport_code,
    destination_airport_code,

    COUNT(*) AS total_flights,

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
    ) AS on_time,

    AVG(arr_delay) AS avg_delay

FROM flight

WHERE
    arr_delay IS NOT NULL
    AND origin_airport_code IS NOT NULL
    AND destination_airport_code IS NOT NULL

GROUP BY
    origin_airport_code,
    destination_airport_code

HAVING COUNT(*) >= 100

ORDER BY
    on_time DESC

LIMIT 10

"""

df_best_routes = pd.read_sql(
    query_best_routes,
    conn
)

df_best_routes["Route"] = (
    df_best_routes["origin_airport_code"]
    + " → "
    + df_best_routes["destination_airport_code"]
)

df_best_routes = df_best_routes[
    [
        "Route",
        "total_flights",
        "on_time",
        "avg_delay"
    ]
]

df_best_routes.columns = [
    "Route",
    "Flights",
    "On-Time %",
    "Avg Delay"
]


# ============================================================
# 11. WORST ROUTES
# ============================================================

query_worst_routes = """

SELECT

    origin_airport_code,
    destination_airport_code,

    COUNT(*) AS total_flights,

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
    ) AS on_time,

    AVG(arr_delay) AS avg_delay

FROM flight

WHERE
    arr_delay IS NOT NULL
    AND origin_airport_code IS NOT NULL
    AND destination_airport_code IS NOT NULL

GROUP BY
    origin_airport_code,
    destination_airport_code

HAVING COUNT(*) >= 100

ORDER BY
    avg_delay DESC

LIMIT 10

"""

df_worst_routes = pd.read_sql(
    query_worst_routes,
    conn
)

df_worst_routes["Route"] = (
    df_worst_routes["origin_airport_code"]
    + " → "
    + df_worst_routes["destination_airport_code"]
)

df_worst_routes = df_worst_routes[
    [
        "Route",
        "total_flights",
        "on_time",
        "avg_delay"
    ]
]

df_worst_routes.columns = [
    "Route",
    "Flights",
    "On-Time %",
    "Avg Delay"
]


# ============================================================
# ROUTE KPIs
# ============================================================

st.subheader("🎯 Route KPIs")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🛣️ Total Routes",
        f"{total_routes:,}"
    )


with col2:

    st.metric(
        "✈️ Total Flights",
        f"{total_flights:,}"
    )


with col3:

    st.metric(
        "⏱️ Avg Delay",
        f"{avg_delay:.1f} min"
    )


col4, col5 = st.columns(2)


with col4:

    st.metric(
        "🔥 Most Active Route",
        busiest_route
    )


with col5:

    st.metric(
        "⚠️ Worst Route",
        worst_route
    )


# ============================================================
# BUSIEST ROUTES
# ============================================================

st.divider()

st.subheader("📊 Top 10 Routes by Flight Volume")


st.bar_chart(
    df_busiest_routes.set_index(
        "route"
    )["total_flights"]
)


# ============================================================
# ROUTE PERFORMANCE
# ============================================================

st.divider()

st.subheader("📊 Average Delay by Route")


st.bar_chart(
    df_route_performance.set_index(
        "route"
    )["avg_delay"]
)


# ============================================================
# ON-TIME PERFORMANCE
# ============================================================

st.divider()

st.subheader("🟢 On-Time % by Route")


st.bar_chart(
    df_route_on_time.set_index(
        "route"
    )["on_time"]
)


# ============================================================
# CANCELLATIONS
# ============================================================

st.divider()

st.subheader("❌ Cancellation Rate by Route")


st.bar_chart(
    df_route_cancellation.set_index(
        "route"
    )["cancellation_rate"]
)


# ============================================================
# ROUTE RANKING
# ============================================================

st.divider()

st.subheader("🏆 Route Ranking")


col1, col2 = st.columns(2)


# ============================================================
# BEST ROUTES
# ============================================================

with col1:

    st.markdown("### 🏆 Best Routes")

    st.dataframe(
        df_best_routes,
        use_container_width=True,
        hide_index=True,

        column_config={

            "On-Time %": st.column_config.NumberColumn(
                format="%.1f%%"
            ),

            "Avg Delay": st.column_config.NumberColumn(
                format="%.1f min"
            )

        }
    )


# ============================================================
# WORST ROUTES
# ============================================================

with col2:

    st.markdown("### ⚠️ Worst Routes")

    st.dataframe(
        df_worst_routes,
        use_container_width=True,
        hide_index=True,

        column_config={

            "On-Time %": st.column_config.NumberColumn(
                format="%.1f%%"
            ),

            "Avg Delay": st.column_config.NumberColumn(
                format="%.1f min"
            )

        }
    )


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()