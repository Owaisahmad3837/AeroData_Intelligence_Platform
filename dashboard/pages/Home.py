from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from src.airport_data_platform.config.logging_config import logging_config




logger=logging_config("Streamlit_log","main_page")
logger.info("start")

logger.info("set_page_config...")
st.set_page_config(
  page_title="Skyhub Airport Data Platform",
  page_icon="✈️",
  layout="wide"
)

st.title("✈️Skyhub Airport Data Platform")
st.subheader("This is Airport Operation & Flight Intelligence")

st.markdown(
  " ### Monitor • Analyze • Understand • Improve  "
)

st.divider()


logger.info("Platfrom Status")

st.subheader("Platfrom Status")

col1,col2=st.columns(2)

with col1:
  st.metric(
    "Database",
    "🟢 Connected"
  )

with col2:
  st.metric(
    "ETL Pipline",
    "🟢 Healthy"
  )


logger.info("Data Coverage")

st.subheader("Data Coverage")

col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Aavabile","🛫 Airlines" )

with col4:
    st.metric("Aavabile","✈️ Aircraft")

with col5:
    st.metric("Aavabile","🛄 Airports")


col6, col7, col8 = st.columns(3)

with col6:
    st.metric("Aavabile","🛬 Flights")

with col7:
    st.metric("Aavabile","🗺️ Routes")

with col8:
    st.metric("Aavabile","🌤️ Weather")





logger.info("Explore the Platfrom")

st.subheader("Explore the Platfrom")


col9,col10=st.columns(2)

with col9:
  st.button(
    "📊 Executive Overview"
  )


with col10:
  st.button(
    "🛬 Flight Operation"
  )

col11,col12=st.columns(2)

with col11:
  st.button(
    "🛫 Airport Intelligence"
  )

with col12:
  st.button(
    "🛣️ Route Intelligence"
  )



logger.info("Technology stack")

st.subheader("Technology stack")

st.write(
    "🐍 Python  •  🐼 Pandas  •  🔢 NumPy  •  🗄️ PostgreSQL"
)

st.write(
    "☁️ Neon  •  🧮 SQL  •  📦 CSV / Parquet  •  🧪 Pytest"
)

st.write(
    "📝 Logging  •  🖥️ Streamlit  •  📊 Power BI  •  📓 Jupyter"
)

st.write(
    "🔧 Git / GitHub"
)


st.divider()

st.caption(
    "SkyHub Airport Data Platform • Airport Operations & Flight Intelligence"
)

logger.info("Main complete")
