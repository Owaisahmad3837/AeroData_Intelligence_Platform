import pandas as pd
import streamlit as st
from pathlib import Path
import sys
dir=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(dir))


from src.airport_data_platform.config.db_connection import (
    local_db_connection
)

from src.airport_data_platform.Query.Operation_Query import (
    TOTAL_FLIGHTS,
    ON_TIME_PERFORMANCE,
    CANCELLATION_RATE,
    AVERAGE_DELAY,
    DELAYED_PERCENT,
    FLIGHT_VOLUME,
    FLIGHT_STATUS,
    DELAY_BY_DAY,
    MOST_DELAYED_FLIGHTS,
    # .....flight vs weather.....
    query_flight_in_bad_weather_count,
    query_flight_bad_weather_avg_delay,
    query_cancelled_flight_bad_weather,
    query_weather_dustribution,
    query_weather_vs_flight,
    query_delay_by_weather,
    query_cancellation_rate_by_weather,
    query_airport_effect,

    # Aircraft
    
   total_aircraft,
    total_aircraft_types,
    total_iata_codes,
    total_icao_codes,
    aircraft_type_list

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


    # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    
    # --------------------------------------------------------
    #                   weather vs FLIGHTS
    # --------------------------------------------------------

    # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,



    data["flight_in_bad_weather_count"] = pd.read_sql(
    query_flight_in_bad_weather_count,
    conn).iloc[0]["bad_flight_weather"]

    data["flight_bad_weather_avg_delay"] = pd.read_sql(
    query_flight_bad_weather_avg_delay,
    conn).iloc[0]["avg_delay"]

    data["cancelled_flight_bad_weather"] = pd.read_sql(
    query_cancelled_flight_bad_weather,
    conn).iloc[0]["cancelled"]
                #   ,,,,,,,,,,,,
    
    data["weather_dustribution"] = pd.read_sql(
                query_weather_dustribution,
                conn
            )
         # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    
    data["weather_vs_flight"] = pd.read_sql(
                query_weather_vs_flight,
                conn
            )
         # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    
    data["delay_by_weather"] = pd.read_sql(
                query_delay_by_weather,
                conn
            )
         # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    
    data["cancellation_rate_by_weather"] = pd.read_sql(
                query_cancellation_rate_by_weather,
                conn
            )
         # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    
    data["airport_effect"] = pd.read_sql(
                    query_airport_effect,
                    conn
                )
             # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
        
    
    # ................................
    # ........................
    # ..................
    # 
    # 
    data["total_aircraft"] = pd.read_sql(
        total_aircraft,
        conn
    ).iloc[0]["total_aircraft"]

    #..........................aircraft.....................................

    data["total_aircraft_types"] = pd.read_sql(
    total_aircraft_types,
    conn
).iloc[0]["total_aircraft_types"]

    data["total_iata_codes"] = pd.read_sql(
    total_iata_codes,
    conn
).iloc[0]["total_iata_codes"]

    data["total_icao_codes"] = pd.read_sql(
    total_icao_codes,
    conn
).iloc[0]["total_icao_codes"]

    data["aircraft_type_list"] = pd.read_sql(
    aircraft_type_list,
    conn
)

    conn.close()

    return data



import streamlit as st
import pandas as pd

from src.airport_data_platform.Query.Analysis_query import (
    query_total_flights,
    query_delayed_flights,
    query_delay_rate,
    query_avg_delay,
    query_airline_performance,
    query_airport_performance,
      query_cancelled_flights,
    query_cancellation_rate,
    query_airline_cancellation,
    query_airport_cancellation,
    query_cancellation_reason
)

@st.cache_data
def load_analysis_data():

    conn = local_db_connection()

    data = {}

    total_flights_df = pd.read_sql(
        query_total_flights,
        conn
    )
    data["total_flights"] = total_flights_df.iloc[0, 0]

    delayed_flights_df = pd.read_sql(
        query_delayed_flights,
        conn
    )
    data["delayed_flights"] = delayed_flights_df.iloc[0, 0]

    delay_rate_df = pd.read_sql(
        query_delay_rate,
        conn
    )
    data["delay_rate"] = delay_rate_df.iloc[0, 0]

    avg_delay_df = pd.read_sql(
        query_avg_delay,
        conn
    )
    data["avg_delay"] = avg_delay_df.iloc[0, 0]

    data["airline_performance"] = pd.read_sql(
        query_airline_performance,
        conn
    )

    data["airport_performance"] = pd.read_sql(
        query_airport_performance,
        conn
    )

    total_flights_df = pd.read_sql(
        query_total_flights,
        conn
    )

    data["total_flights"] = total_flights_df.iloc[0, 0]


    # --------------------------------------------------------
    # 2. Cancelled Flights
    # --------------------------------------------------------

    cancelled_flights_df = pd.read_sql(
        query_cancelled_flights,
        conn
    )

    data["cancelled_flights"] = cancelled_flights_df.iloc[0, 0]


    # --------------------------------------------------------
    # 3. Cancellation Rate
    # --------------------------------------------------------

    cancellation_rate_df = pd.read_sql(
        query_cancellation_rate,
        conn
    )

    data["cancellation_rate"] = cancellation_rate_df.iloc[0, 0]


    # --------------------------------------------------------
    # 4. Airline Cancellation
    # --------------------------------------------------------

    data["airline_cancellation"] = pd.read_sql(
        query_airline_cancellation,
        conn
    )


    # --------------------------------------------------------
    # 5. Airport Cancellation
    # --------------------------------------------------------

    data["airport_cancellation"] = pd.read_sql(
        query_airport_cancellation,
        conn
    )


    # --------------------------------------------------------
    # 6. Cancellation Reasons
    # --------------------------------------------------------

    data["cancellation_reason"] = pd.read_sql(
        query_cancellation_reason,
        conn
    )

    conn.close()

    return data

