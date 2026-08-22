from src.airport_data_platform.transform.airline import airline_transformation

from src.airport_data_platform.transform.airplane import airplane_transformation

from src.airport_data_platform.transform.airport import airport_transformation
from src.airport_data_platform.transform.route import route_transformation

from src.airport_data_platform.transform.flight import flight_transformation

from src.airport_data_platform.transform.weather import weather_transformation


def main():
    print("Starting transformation pipeline...")

    print("1. Transforming airline data...")
    airline_transformation()

    print("2. Transforming airplane data...")
    airplane_transformation()

    print("3. Transforming airport data...")
    airport_transformation()

    print("4. Transforming route data...")
    route_transformation()

    print("5. Transforming flight data...")
    flight_transformation()

    print("6. Transforming weather data...")
    weather_transformation()

    print("Transformation pipeline completed!")

if __name__ == "__main__":
    main()

