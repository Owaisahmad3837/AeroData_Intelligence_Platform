# DELAY ANALYSIS QUERIES

# 1. Total Flights
query_total_flights = """
SELECT COUNT(*) AS total_flights
FROM flight;
"""


# 2. Delayed Flights
query_delayed_flights = """
SELECT COUNT(*) AS delayed_flights
FROM flight
WHERE delay_minutes > 0;
"""


# 3. Delay Rate
query_delay_rate = """
SELECT
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE delay_minutes > 0)
        / NULLIF(COUNT(*), 0),
        2
    ) AS delay_rate
FROM flight;
"""


# 4. Average Delay
query_avg_delay = """
SELECT
    ROUND(AVG(delay_minutes), 2) AS avg_delay
FROM flight
WHERE delay_minutes > 0;
"""


# 5. Airline Performance
query_airline_performance = """
SELECT
    airline,
    COUNT(*) AS total_flights,
    COUNT(*) FILTER (
        WHERE delay_minutes > 0
    ) AS delayed_flights,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE delay_minutes > 0
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS delay_rate,
    ROUND(
        AVG(delay_minutes) FILTER (
            WHERE delay_minutes > 0
        ),
        2
    ) AS avg_delay
FROM flight
GROUP BY airline
ORDER BY delay_rate DESC;
"""


# 6. Airport Performance
query_airport_performance = """
SELECT
    departure_airport,
    COUNT(*) AS total_flights,
    COUNT(*) FILTER (
        WHERE delay_minutes > 0
    ) AS delayed_flights,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE delay_minutes > 0
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS delay_rate,
    ROUND(
        AVG(delay_minutes) FILTER (
            WHERE delay_minutes > 0
        ),
        2
    ) AS avg_delay
FROM flight
GROUP BY departure_airport
ORDER BY delay_rate DESC;
"""