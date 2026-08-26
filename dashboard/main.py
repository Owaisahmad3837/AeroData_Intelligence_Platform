import streamlit as st
from pathlib import Path
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT_DIR))



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SkyHub Airport Data Platform",
    page_icon="✈️",
    layout="wide"
)


# ============================================================
# NAVIGATION
# ============================================================

from src.airport_data_platform.services.dashborad_data import load_flight_operation_data

load_flight_operation_data()

from navigation import create_navigation


pg = create_navigation()

pg.run()