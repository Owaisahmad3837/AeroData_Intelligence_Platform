import streamlit as st

from pathlib import Path
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[3]

sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# DATA SERVICE
# ============================================================

from src.airport_data_platform.services.dashborad_data import load_flight_operation_data


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Weather & Flight Impact",
    page_icon="🌦️",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🌦️ Weather & Flight Impact")

st.caption(
    "Analyze how weather conditions affect flight operations, "
    "delays, cancellations, and airport performance."
)

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

data = load_flight_operation_data()


flight_in_bad_weather_count = data[
    "flight_in_bad_weather_count"
]

flight_bad_weather_avg_delay = data[
    "flight_bad_weather_avg_delay"
]

cancelled_flight_bad_weather = data[
    "cancelled_flight_bad_weather"
]

weather_distribution = data[
    "weather_dustribution"
]

weather_vs_flight = data[
    "weather_vs_flight"
]

delay_by_weather = data[
    "delay_by_weather"
]

cancellation_rate_by_weather = data[
    "cancellation_rate_by_weather"
]

airport_effect = data[
    "airport_effect"
]


# ============================================================
# SECTION 1 — WEATHER IMPACT KPIs
# ============================================================

st.subheader("🌦️ Weather Impact Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "✈️ Flights in Bad Weather",
        f"{int(flight_in_bad_weather_count):,}"
    )

with col2:
    st.metric(
        "⏱️ Avg Delay in Bad Weather",
        f"{float(flight_bad_weather_avg_delay):.1f} min"
    )

with col3:
    st.metric(
        "❌ Cancelled in Bad Weather",
        f"{int(cancelled_flight_bad_weather):,}"
    )

st.divider()


# ============================================================
# SECTION 2 — WEATHER DISTRIBUTION
# ============================================================

st.subheader("🌦️ Weather Conditions")

st.caption(
    "Distribution of weather conditions across the available "
    "weather observations."
)

st.dataframe(
    weather_distribution,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SECTION 3 — WEATHER VS FLIGHTS
# ============================================================

st.subheader("✈️ Flights by Weather Condition")

st.caption(
    "Compare the number of flights operating under each "
    "weather condition."
)

st.dataframe(
    weather_vs_flight,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SECTION 4 — DELAY IMPACT
# ============================================================

st.subheader("⏱️ Delay Impact by Weather")

st.caption(
    "Analyze average flight delay under different weather "
    "conditions."
)

st.dataframe(
    delay_by_weather,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SECTION 5 — CANCELLATION IMPACT
# ============================================================

st.subheader("❌ Cancellation Rate by Weather")

st.caption(
    "Compare flight cancellation rates across weather "
    "conditions."
)

st.dataframe(
    cancellation_rate_by_weather,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SECTION 6 — AIRPORT IMPACT
# ============================================================

st.subheader("🛫 Airport Weather Impact")

st.caption(
    "Identify airports experiencing the greatest operational "
    "impact during adverse weather."
)

st.dataframe(
    airport_effect,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SkyHub Airport Data Platform • Weather & Flight Intelligence"
)
