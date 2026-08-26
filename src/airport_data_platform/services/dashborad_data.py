import pandas as pd
import streamlit as st
from pathlib import Path
import sys
dir=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(dir))


from src.airport_data_platform.config.db_connection import (
    local_db_connection
)

from src.airport_data_platform.Query.Operation.Operation_Query import (
    TOTAL_FLIGHTS,
    ON_TIME_PERFORMANCE,
    CANCELLATION_RATE,
    AVERAGE_DELAY,
    DELAYED_PERCENT,
    FLIGHT_VOLUME,
    FLIGHT_STATUS,
    DELAY_BY_DAY,
    MOST_DELAYED_FLIGHTS,
)


@st.cache_data
def load_flight_operation_data():

    conn = local_db_connection()

    data = {}

    # --------------------------------------------------------
    # 1. TOTAL FLIGHTS
    # --------------------------------------------------------

    data["total_flights"] = pd.read_sql(
        TOTAL_FLIGHTS,
        conn
    ).iloc[0]["total_flights"]


    # --------------------------------------------------------
    # 2. ON-TIME %
    # --------------------------------------------------------

    data["on_time_percent"] = pd.read_sql(
        ON_TIME_PERFORMANCE,
        conn
    ).iloc[0]["on_time_percent"]


    # --------------------------------------------------------
    # 3. CANCELLATION %
    # --------------------------------------------------------

    data["cancellation_percent"] = pd.read_sql(
        CANCELLATION_RATE,
        conn
    ).iloc[0]["cancellation_percent"]


    # --------------------------------------------------------
    # 4. AVERAGE DELAY
    # --------------------------------------------------------

    data["average_delay"] = pd.read_sql(
        AVERAGE_DELAY,
        conn
    ).iloc[0]["avg_delay"]


    # --------------------------------------------------------
    # 5. DELAYED %
    # --------------------------------------------------------

    data["delayed_percent"] = pd.read_sql(
        DELAYED_PERCENT,
        conn
    ).iloc[0]["delayed_percent"]


    # --------------------------------------------------------
    # 6. FLIGHT VOLUME
    # --------------------------------------------------------

    data["flight_volume"] = pd.read_sql(
        FLIGHT_VOLUME,
        conn
    )


    # --------------------------------------------------------
    # 7. FLIGHT STATUS
    # --------------------------------------------------------

    data["flight_status"] = pd.read_sql(
        FLIGHT_STATUS,
        conn
    )


    # --------------------------------------------------------
    # 8. DELAY BY DAY
    # --------------------------------------------------------

    data["delay_by_day"] = pd.read_sql(
        DELAY_BY_DAY,
        conn
    )


    # --------------------------------------------------------
    # 9. MOST DELAYED FLIGHTS
    # --------------------------------------------------------

    data["most_delayed_flights"] = pd.read_sql(
        MOST_DELAYED_FLIGHTS,
        conn
    )


    conn.close()

    return data