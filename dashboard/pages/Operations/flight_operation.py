import streamlit as st
from pathlib import Path
import sys
dir=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(dir))


from src.airport_data_platform.services.dashborad_data import (
    load_flight_operation_data
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Flight Operations",
    page_icon="✈️",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("✈️ Flight Operations")

st.caption(
    "Monitor flight volume, operational status, delays and "
    "daily flight performance."
)


# ============================================================
# LOAD CACHED DATA
# ============================================================

data = load_flight_operation_data()


# ============================================================
# DATA
# ============================================================

total_flights = data["total_flights"]

on_time_percent = data["on_time_percent"]

delayed_percent = data["delayed_percent"]

cancellation_percent = data["cancellation_percent"]

average_delay = data["average_delay"]

df_flight_volume = data["flight_volume"]

df_flight_status = data["flight_status"]

df_delay_by_day = data["delay_by_day"]

df_most_delayed = data["most_delayed_flights"]


# ============================================================
# KPI SECTION
# ============================================================

st.divider()

st.subheader("🎯 Flight Operations KPIs")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric(
        label="✈️ Total Flights",
        value=f"{int(total_flights):,}"
    )


with col2:
    st.metric(
        label="🟢 On-Time",
        value=f"{on_time_percent:.1f}%"
    )


with col3:
    st.metric(
        label="🔴 Delayed",
        value=f"{delayed_percent:.1f}%"
    )


with col4:
    st.metric(
        label="❌ Cancelled",
        value=f"{cancellation_percent:.1f}%"
    )


with col5:
    st.metric(
        label="⏱️ Avg Delay",
        value=f"{average_delay:.1f} min"
    )


# ============================================================
# FLIGHT VOLUME
# ============================================================

st.divider()

st.subheader("📈 Flight Volume")

st.caption(
    "Number of flights operated over time."
)

if not df_flight_volume.empty:

    st.line_chart(
        df_flight_volume.set_index(
            "flight_date"
        )["total_flights"],
        use_container_width=True
    )

else:

    st.info("No flight volume data available.")


# ============================================================
# FLIGHT STATUS
# ============================================================

st.divider()

st.subheader("🟢 Flight Status")

st.caption(
    "Distribution of on-time, delayed and cancelled flights."
)

col1, col2 = st.columns([1, 2])


with col1:

    if not df_flight_status.empty:

        st.dataframe(
            df_flight_status,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No flight status data available.")


with col2:

    if not df_flight_status.empty:

        status_chart = (
            df_flight_status
            .set_index("flight_status")["total_flights"]
        )

        st.bar_chart(
            status_chart,
            use_container_width=True
        )

    else:

        st.info("No status chart available.")


# ============================================================
# DELAY ANALYSIS
# ============================================================

st.divider()

st.subheader("⏱️ Delay Analysis")

st.caption(
    "Average arrival delay across flight dates."
)

if not df_delay_by_day.empty:

    st.line_chart(
        df_delay_by_day.set_index(
            "flight_date"
        )["avg_delay"],
        use_container_width=True
    )

else:

    st.info("No delay data available.")


# ============================================================
# MOST DELAYED FLIGHTS
# ============================================================

st.divider()

st.subheader("⚠️ Most Delayed Flights")

st.caption(
    "Top 10 flights with the highest arrival delay."
)

if not df_most_delayed.empty:

    display_delayed = df_most_delayed.copy()

    display_delayed.columns = [
        "Flight ID",
        "Airline",
        "Origin",
        "Destination",
        "Arrival Delay"
    ]

    display_delayed["Arrival Delay"] = (
        display_delayed["Arrival Delay"]
        .round(1)
    )

    st.dataframe(
        display_delayed,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No delayed flight records available."
    )


# ============================================================
# OPERATIONAL SUMMARY
# ============================================================

st.divider()

st.subheader("📋 Operational Summary")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🟢 On-Time Performance",
        f"{on_time_percent:.1f}%"
    )


with col2:

    st.metric(
        "🔴 Delay Rate",
        f"{delayed_percent:.1f}%"
    )


with col3:

    st.metric(
        "❌ Cancellation Rate",
        f"{cancellation_percent:.1f}%"
    )