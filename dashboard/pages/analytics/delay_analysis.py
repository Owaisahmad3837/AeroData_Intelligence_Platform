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
    page_title="Delay Analysis",
    page_icon="✈️",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("✈️ Delay Analysis")

st.caption(
    "Show Delay Analysis"
)


# ============================================================
# LOAD CACHED DATA
# ============================================================

data = load_flight_operation_data()


# ============================================================
# DATA
# ============================================================

total_flights = data["total_flights"]
