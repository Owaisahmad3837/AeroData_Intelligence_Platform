# ==========================================
# DELAY ANALYSIS QUERIES
# ==========================================


# 1. Total Flights

query_total_flights = """
SELECT
    COUNT(*) AS total_flights
FROM flight;
"""


# 2. Delayed Flights

query_delayed_flights = """
SELECT
    COUNT(*) AS delayed_flights
FROM flight
WHERE arr_delay > 0;
"""


# 3. Delay Rate

query_delay_rate = """
SELECT
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE arr_delay > 0
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS delay_rate
FROM flight;
"""


# 4. Average Delay

query_avg_delay = """
SELECT
    ROUND(
        AVG(arr_delay),
        2
    ) AS avg_delay
FROM flight
WHERE arr_delay > 0;
"""


# 5. Airline Performance



query_airline_performance = """
SELECT
    operating_carrier AS airline,

    COUNT(*) AS total_flights,

    COUNT(*) FILTER (
        WHERE arr_delay > 0
    ) AS delayed_flights,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE arr_delay > 0
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS delay_rate,

    ROUND(
        AVG(arr_delay) FILTER (
            WHERE arr_delay > 0
        ),
        2
    ) AS avg_delay

FROM flight

GROUP BY operating_carrier

ORDER BY delay_rate DESC;
"""







# 6. Airport Performance

query_airport_performance = """
SELECT
    origin_airport_code,
    COUNT(*) AS total_flights,
    COUNT(*) FILTER (
        WHERE arr_delay > 0
    ) AS delayed_flights,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE arr_delay > 0
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS delay_rate,
    ROUND(
        AVG(arr_delay) FILTER (
            WHERE arr_delay > 0
        ),
        2
    ) AS avg_delay
FROM flight
GROUP BY origin_airport_code
ORDER BY delay_rate DESC;
"""




# ..................


# ============================================================
# CANCELLATION ANALYSIS QUERIES
# ============================================================

# 1. Total Flights
query_cancellation_total_flights = """
SELECT
    COUNT(*) AS total_flights
FROM flight;
"""


# 2. Total Cancelled Flights
query_cancelled_flights = """
SELECT
    COUNT(*) AS cancelled_flights
FROM flight
WHERE cancelled = TRUE;
"""


# 3. Cancellation Rate
query_cancellation_rate = """
SELECT
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE cancelled = TRUE
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS cancellation_rate
FROM flight;
"""


# 4. Cancellation by Airline
query_airline_cancellation = """
SELECT
    a.airline_name AS airline,

    COUNT(*) AS total_flights,

    COUNT(*) FILTER (
        WHERE f.cancelled = TRUE
    ) AS cancelled_flights,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE f.cancelled = TRUE
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS cancellation_rate

FROM flight f

JOIN airline a
    ON f.operating_carrier = a.iata_code

GROUP BY a.airline_name

ORDER BY cancellation_rate DESC;
"""


# 5. Cancellation by Airport
query_airport_cancellation = """
SELECT
    a.name AS departure_airport,
    a.iata_code,

    COUNT(*) AS total_flights,

    COUNT(*) FILTER (
        WHERE f.cancelled = TRUE
    ) AS cancelled_flights,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE f.cancelled = TRUE
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS cancellation_rate

FROM flight f

JOIN airport a
    ON f.origin_airport_code = a.iata_code

GROUP BY
    a.name,
    a.iata_code

ORDER BY cancellation_rate DESC;
"""


# 6. Cancellation Reasons
query_cancellation_reason = """
SELECT
    cancellation_code AS cancellation_reason,

    COUNT(*) AS cancelled_flights

FROM flight

WHERE cancelled = TRUE

GROUP BY cancellation_code

ORDER BY cancelled_flights DESC;
"""