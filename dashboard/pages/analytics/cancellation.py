import streamlit as st
from pathlib import Path
import sys


# ============================================================
# PROJECT PATH
# ============================================================

dir = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(dir))


# ============================================================
# IMPORT DATA SERVICE
# ============================================================

from src.airport_data_platform.services.dashborad_data import (
    load_analysis_data
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Cancellation Analysis",
    page_icon="❌",
    layout="wide"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("❌ Cancellation Analysis")

st.caption(
    "Analyze cancelled flights, cancellation rates, "
    "airlines, airports, and cancellation reasons."
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_analysis_data()


# ============================================================
# EXTRACT DATA
# ============================================================

total_flights = data["total_flights"]

cancelled_flights = data["cancelled_flights"]

cancellation_rate = data["cancellation_rate"]

airline_cancellation = data["airline_cancellation"]

airport_cancellation = data["airport_cancellation"]

cancellation_reason = data["cancellation_reason"]


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Cancellation Overview")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        label="Total Flights",
        value=f"{total_flights:,}"
    )


with col2:

    st.metric(
        label="Cancelled Flights",
        value=f"{cancelled_flights:,}"
    )


with col3:

    st.metric(
        label="Cancellation Rate",
        value=f"{cancellation_rate:.2f}%"
    )


# ============================================================
# AIRLINE CANCELLATION
# ============================================================

st.divider()

st.subheader("✈️ Airline Cancellation Performance")

st.dataframe(
    airline_cancellation,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# AIRLINE CANCELLATION CHART
# ============================================================

st.subheader("📈 Cancellation Rate by Airline")

st.bar_chart(
    airline_cancellation
    .set_index("airline")["cancellation_rate"]
)


# ============================================================
# AIRPORT CANCELLATION
# ============================================================

st.divider()

st.subheader("🛫 Airport Cancellation Performance")

st.dataframe(
    airport_cancellation,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# AIRPORT CANCELLATION CHART
# ============================================================

st.subheader("📈 Cancellation Rate by Airport")

st.bar_chart(
    airport_cancellation
    .set_index("departure_airport")["cancellation_rate"]
)


# ============================================================
# CANCELLATION REASONS
# ============================================================

st.divider()

st.subheader("⚠️ Cancellation Reasons")

st.dataframe(
    cancellation_reason,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CANCELLATION REASON CHART
# ============================================================

st.subheader("📊 Flights by Cancellation Reason")

st.bar_chart(
    cancellation_reason
    .set_index("cancellation_reason")["cancelled_flights"]
)
