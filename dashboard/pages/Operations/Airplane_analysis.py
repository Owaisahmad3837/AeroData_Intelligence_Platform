import streamlit as st

from pathlib import Path
import sys

dir = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(dir))

from src.airport_data_platform.services.dashborad_data import (
    load_aircraft_data
)


st.set_page_config(
    page_title="Aircraft Analysis",
    page_icon="🛩️",
    layout="wide"
)


st.title("🛩️ Fleet / Aircraft Analysis")
st.caption("Aircraft usage, performance and reliability")

st.divider()


data = load_aircraft_data()


#..........................fleet_kpi.....................................

st.subheader("🎯 Fleet KPIs")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "🛩️ Total Aircraft",
        f"{int(data['total_aircraft']):,}"
    )


with col2:
    st.metric(
        "🔢 Aircraft Types",
        f"{int(data['total_aircraft_types']):,}"
    )


with col3:

    most_used = data["most_used_aircraft"]

    if not most_used.empty:
        st.metric(
            "🔥 Most Used Aircraft",
            most_used.iloc[0]["aircraft"]
        )
    else:
        st.metric(
            "🔥 Most Used Aircraft",
            "N/A"
        )


with col4:
    st.metric(
        "⏱️ Average Delay",
        f"{float(data['average_aircraft_delay']):.1f} min"
    )


#..........................fleet_composition.....................................

st.divider()

st.subheader("📊 Fleet Composition")

st.bar_chart(
    data["flights_by_aircraft_type"].set_index(
        "aircraft_type"
    )["total_flights"]
)


#..........................aircraft_performance.....................................

st.divider()

st.subheader("📈 Aircraft Performance")

col1, col2 = st.columns(2)


with col1:

    st.markdown("### ⏱️ Average Delay by Aircraft")

    st.bar_chart(
        data["average_delay_by_aircraft"].set_index(
            "aircraft_type"
        )["avg_delay"]
    )


with col2:

    st.markdown("### 🟢 On-Time % by Aircraft")

    st.bar_chart(
        data["on_time_by_aircraft"].set_index(
            "aircraft_type"
        )["on_time_percent"]
    )


st.markdown("### ❌ Cancellation Rate by Aircraft")

st.bar_chart(
    data["cancellation_rate_by_aircraft"].set_index(
        "aircraft_type"
    )["cancellation_rate"]
)


#..........................aircraft_ranking.....................................

st.divider()

st.subheader("🏆 Aircraft Ranking")

col1, col2 = st.columns(2)


with col1:

    st.markdown("### 🏆 Best Performing Aircraft")

    st.dataframe(
        data["best_performing_aircraft"],
        use_container_width=True,
        hide_index=True,
        column_config={
            "on_time_percent": st.column_config.NumberColumn(
                "On-Time %",
                format="%.1f%%"
            )
        }
    )


with col2:

    st.markdown("### ⚠️ Problem Aircraft")

    st.dataframe(
        data["problem_aircraft"],
        use_container_width=True,
        hide_index=True,
        column_config={
            "avg_delay": st.column_config.NumberColumn(
                "Avg Delay",
                format="%.1f min"
            )
        }
    )