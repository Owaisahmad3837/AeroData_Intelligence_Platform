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