# ============================================================
# FLIGHT OPERATIONS QUERIES
# ============================================================


# ------------------------------------------------------------
# 1. TOTAL FLIGHTS
# ------------------------------------------------------------

TOTAL_FLIGHTS = """
SELECT
    COUNT(flight_id) AS total_flights
FROM flight
"""


# ------------------------------------------------------------
# 2. ON-TIME PERFORMANCE %
# ------------------------------------------------------------

ON_TIME_PERFORMANCE = """
SELECT
    COUNT(
        CASE
            WHEN arr_delay <= 0 THEN 1
        END
    ) * 100.0
    / NULLIF(
        COUNT(*),
        0
    ) AS on_time_percent
FROM flight
"""


# ------------------------------------------------------------
# 3. CANCELLATION %
# ------------------------------------------------------------

CANCELLATION_RATE = """
SELECT
    COUNT(
        CASE
            WHEN cancelled = TRUE THEN 1
        END
    ) * 100.0
    / NULLIF(
        COUNT(*),
        0
    ) AS cancellation_percent
FROM flight
"""


# ------------------------------------------------------------
# 4. AVERAGE DELAY
# ------------------------------------------------------------

AVERAGE_DELAY = """
SELECT
    AVG(arr_delay) AS avg_delay
FROM flight
WHERE arr_delay IS NOT NULL
"""


# ------------------------------------------------------------
# 5. DELAYED FLIGHTS %
# ------------------------------------------------------------

DELAYED_PERCENT = """
SELECT
    COUNT(
        CASE
            WHEN arr_delay > 0 THEN 1
        END
    ) * 100.0
    / NULLIF(
        COUNT(
            CASE
                WHEN arr_delay IS NOT NULL THEN 1
            END
        ),
        0
    ) AS delayed_percent
FROM flight
"""


# ------------------------------------------------------------
# 6. FLIGHT VOLUME BY DATE
# ------------------------------------------------------------

FLIGHT_VOLUME = """
SELECT
    flight_date,
    COUNT(*) AS total_flights
FROM flight
GROUP BY flight_date
ORDER BY flight_date
"""


# ------------------------------------------------------------
# 7. FLIGHT STATUS
# ------------------------------------------------------------

FLIGHT_STATUS = """
SELECT
    CASE
        WHEN cancelled = TRUE
            THEN 'Cancelled'

        WHEN arr_delay > 0
            THEN 'Delayed'

        ELSE 'On-Time'
    END AS flight_status,

    COUNT(*) AS total_flights

FROM flight

GROUP BY flight_status

ORDER BY total_flights DESC
"""


# ------------------------------------------------------------
# 8. DELAY BY DAY
# ------------------------------------------------------------

DELAY_BY_DAY = """
SELECT
    flight_date,
    AVG(arr_delay) AS avg_delay
FROM flight
WHERE arr_delay IS NOT NULL
GROUP BY flight_date
ORDER BY flight_date
"""


# ------------------------------------------------------------
# 9. MOST DELAYED FLIGHTS
# ------------------------------------------------------------

MOST_DELAYED_FLIGHTS = """
SELECT
    flight_id,
    operating_carrier,
    origin_airport_code,
    destination_airport_code,
    arr_delay
FROM flight
WHERE arr_delay IS NOT NULL
ORDER BY arr_delay DESC
LIMIT 10
"""





# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# ..........................................................................
# ..........................................................................
# ..........................................................................
# ..........................................................................
# ||||||||||||||||||||||||...................|||||||||||||||||||||||||||||||
#......................... Flight and Weather...............................
#......................... Flight and Weather...............................
#......................... Flight and Weather...............................
# ||||||||||||||||||||||||...................|||||||||||||||||||||||||||||||
# ..........................................................................
# ..........................................................................
# ..........................................................................
# ..........................................................................
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||






query_flight_in_bad_weather_count="""
select count(*) as bad_flight_weather
from flight f join weather w on f.flight_number=w.airport_id and date(f.flight_date)=date(w.weather_time)
where  w.precipitation_mm>10
or max_wind_gust >15
   or cloud_cover_pct>90;
"""





query_flight_bad_weather_avg_delay="""
SELECT
    COUNT(*) AS bad_flights,
    AVG(f.arr_delay) AS avg_delay

FROM flight f

JOIN weather w
    ON f.flight_number = w.airport_id
    AND DATE(f.flight_date) = DATE(w.weather_time)

WHERE
    (
        w.precipitation_mm > 10
        OR w.max_wind_gust > 15
        OR w.cloud_cover_pct > 90
    );

"""


query_cancelled_flight_bad_weather="""
SELECT
    COUNT(*) AS bad_flights,
    count(*) filter(where f.cancelled=true) AS cancelled

FROM flight f

JOIN weather w
    ON f.flight_number = w.airport_id
    AND DATE(f.flight_date) = DATE(w.weather_time)

WHERE
    (
        w.precipitation_mm > 10
        OR w.max_wind_gust > 15
        OR w.cloud_cover_pct > 90
    );

"""


query_weather_dustribution="""
SELECT
    CASE
        WHEN precipitation_mm > 10
          OR max_wind_gust > 15
          OR cloud_cover_pct > 90
        THEN 'Bad Weather'

        WHEN precipitation_mm > 2
          OR max_wind_gust > 8
          OR cloud_cover_pct > 70
        THEN 'Moderate Weather'

        ELSE 'Normal Weather'
    END AS weather_condition,
 count(*) as total_records
FROM weather
group by weather_condition
;
"""


query_weather_vs_flight="""
SELECT
    CASE
        WHEN w.precipitation_mm > 10
          OR w.max_wind_gust > 15
          OR w.cloud_cover_pct > 90
        THEN 'Bad Weather'

        WHEN w.precipitation_mm > 2
          OR w.max_wind_gust > 8
          OR w.cloud_cover_pct > 70
        THEN 'Moderate Weather'

        ELSE 'Normal Weather'
    END AS weather_condition,
    count(f.flight_id)as flight_total 
FROM weather w join flight f on  f.flight_number = w.airport_id
    AND DATE(f.flight_date) = DATE(w.weather_time)

group by weather_condition
;
"""





query_delay_by_weather="""
SELECT
    CASE
        WHEN w.precipitation_mm > 10
          OR w.max_wind_gust > 15
          OR w.cloud_cover_pct > 90
        THEN 'Bad Weather'

        WHEN w.precipitation_mm > 2
          OR w.max_wind_gust > 8
          OR w.cloud_cover_pct > 70
        THEN 'Moderate Weather'

        ELSE 'Normal Weather'
    END AS weather_condition,
   COUNT(CASE WHEN f.arr_delay > 0 THEN 1 END) * 100.0
/ NULLIF(COUNT(*), 0)as avg_delay 
FROM weather w join flight f on  f.flight_number = w.airport_id
    AND DATE(f.flight_date) = DATE(w.weather_time)

group by weather_condition
"""




query_cancellation_rate_by_weather="""
SELECT
    CASE
        WHEN w.precipitation_mm > 10
          OR w.max_wind_gust > 15
          OR w.cloud_cover_pct > 90
        THEN 'Bad Weather'

        WHEN w.precipitation_mm > 2
          OR w.max_wind_gust > 8
          OR w.cloud_cover_pct > 70
        THEN 'Moderate Weather'

        ELSE 'Normal Weather'
    END AS weather_condition,
     COUNT(*) FILTER (
        WHERE f.cancelled = TRUE ) * 100.0
/ NULLIF(COUNT(*), 0)as avg_delay 
FROM weather w join flight f on  f.flight_number = w.airport_id
    AND DATE(f.flight_date) = DATE(w.weather_time)

group by weather_condition
"""


query_airport_effect="""
SELECT
    a.name,
    w.airport_id,

    CASE
        WHEN w.precipitation_mm > 10
          OR w.max_wind_gust > 15
          OR w.cloud_cover_pct > 90
        THEN 'Bad Weather'

        WHEN w.precipitation_mm > 2
          OR w.max_wind_gust > 8
          OR w.cloud_cover_pct > 70
        THEN 'Moderate Weather'

        ELSE 'Normal Weather'
    END AS weather_condition

FROM airport a
JOIN weather w
    ON a.airport_id = w.airport_id

LIMIT 10;
"""













# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# ..........................................................................
# ..........................................................................
# ..........................................................................
# ..........................................................................
# ||||||||||||||||||||||||...................|||||||||||||||||||||||||||||||
#......................... ------------------...............................
#....................... 🛩️ Fleet / Aircraft Analysis.......................
#......................... ------------------...............................
# ||||||||||||||||||||||||...................|||||||||||||||||||||||||||||||
# ..........................................................................
# ..........................................................................
# ..........................................................................
# ..........................................................................
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||







#..........................fleet_kpi.....................................

total_aircraft = """SELECT COUNT(*) AS total_aircraft
FROM airplane;"""


#..........................aircraft_kpi.....................................

total_aircraft_types = """SELECT
    COUNT(*) AS total_aircraft_types
FROM airplane;"""

total_iata_codes = """SELECT
    COUNT(DISTINCT iata_code) AS total_iata_codes
FROM airplane
WHERE iata_code IS NOT NULL;"""

total_icao_codes = """SELECT
    COUNT(DISTINCT icao_code) AS total_icao_codes
FROM airplane
WHERE icao_code IS NOT NULL;"""

#..........................aircraft_reference.....................................

aircraft_type_list = """SELECT
    name,
    iata_code,
    icao_code
FROM airplane
ORDER BY name;"""