import streamlit as st
from pathlib import Path
import sys

dir = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(dir))

from src.airport_data_platform.services.dashborad_data import load_flight_operation_data


st.set_page_config(
    page_title="Aircraft Analysis",
    page_icon="🛩️",
    layout="wide"
)


data = load_flight_operation_data()

total_aircraft=data["total_aircraft"]
total_aircraft_types = data["total_aircraft_types"]
total_iata_codes = data["total_iata_codes"]
total_icao_codes = data["total_icao_codes"]
aircraft_type_list = data["aircraft_type_list"]


st.title("🛩️ Aircraft Analysis")
st.caption("Aircraft type and code reference information")
st.divider()

st.subheader("🎯 Aircraft KPIs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🛩️ Aircraft Types",
        f"{int(total_aircraft_types):,}"
    )

with col2:
    st.metric(
        "🔤 IATA Codes",
        f"{int(total_iata_codes):,}"
    )

with col3:
    st.metric(
        "🔠 ICAO Codes",
        f"{int(total_icao_codes):,}"
    )



st.divider()

st.subheader("📋 Aircraft Type Reference")

st.dataframe(
    aircraft_type_list,
    use_container_width=True,
    hide_index=True
)