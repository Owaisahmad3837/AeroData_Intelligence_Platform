import streamlit as st

from pathlib import Path
import sys


# ==========================================
# PROJECT PATH
# ==========================================

dir = Path(__file__).resolve().parents[3]

sys.path.insert(0, str(dir))


# ==========================================
# IMPORT DATA SERVICE
# ==========================================

from src.airport_data_platform.services.dashborad_data import (
    load_analysis_data
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Delay Analysis",
    page_icon="✈️",
    layout="wide"
)


# ==========================================
# PAGE HEADER
# ==========================================

st.title("✈️ Delay Analysis")

st.caption(
    "Analyze flight delays, airline performance, and airport performance."
)


# ==========================================
# LOAD DATA
# ==========================================

data = load_analysis_data()

total_flights = data["total_flights"]
delayed_flights = data["delayed_flights"]
delay_rate = data["delay_rate"]
avg_delay = data["avg_delay"]

airline_performance = data["airline_performance"]
airport_performance = data["airport_performance"]


# ==========================================
# KPI CARDS
# ==========================================

st.subheader("📊 Delay Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        label="Total Flights",
        value=f"{total_flights:,}"
    )


with col2:
    st.metric(
        label="Delayed Flights",
        value=f"{delayed_flights:,}"
    )


with col3:
    st.metric(
        label="Delay Rate",
        value=f"{delay_rate:.2f}%"
    )


with col4:
    st.metric(
        label="Average Delay",
        value=f"{avg_delay:.2f} min"
    )


# ==========================================
# AIRLINE PERFORMANCE
# ==========================================

st.divider()

st.subheader("✈️ Airline Performance")

st.dataframe(
    airline_performance,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# AIRLINE DELAY RATE CHART
# ==========================================

st.subheader("📈 Airline Delay Rate")

st.bar_chart(
    airline_performance
    .set_index("airline")["delay_rate"]
)


# ==========================================
# AIRPORT PERFORMANCE
# ==========================================

st.divider()

st.subheader("🛫 Airport Performance")

st.dataframe(
    airport_performance,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# AIRPORT DELAY RATE CHART
# ==========================================

st.subheader("📈 Airport Delay Rate")

st.bar_chart(
    airport_performance
    .set_index("origin_airport_code")["delay_rate"]
)