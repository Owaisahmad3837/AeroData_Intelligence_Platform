from ..config.logging_config import logging_config

import xarray as xr
import pandas as pd
from pathlib import Path


def weather_nc_to_parquet():

    logging = logging_config(
        "ingestion",
        "weather_data_nc_to_parquet"
    )

    # Paths
    airport_data_path = Path(
        "data/raw/airport_data/airports.csv"
    )

    weather_data_path = Path(
        "data/raw/weather_data"
    )

    output_path = Path(
        "data/processed/weather_data_2024/final_weather_2024.parquet"
    )


    # Read airport data
    print(f"Reading airport data from {airport_data_path}")

    read_airport_data = pd.read_csv(
        airport_data_path
    )

    print("Reading complete...")


    # Read weather data
    print("Reading weather_accum...")

    read_weather_accum = xr.open_dataset(
        weather_data_path / "weather_accum_2024.nc"
    )

    print("Reading weather_instant...")

    read_weather_instant = xr.open_dataset(
        weather_data_path / "weather_instant_2024.nc"
    )

    print("Reading weather_max...")

    read_weather_max = xr.open_dataset(
        weather_data_path / "weather_max_2024.nc"
    )

    print("Reading weather data complete...")


    # Store data for all airports
    all_weather_data = []


    # Process each airport
    for _, airport in read_airport_data.iterrows():

        airport_id = airport["Airport ID"]
        latitude = airport["Latitude"]
        longitude = airport["Longitude"]


        # Find nearest weather point
        accum_point = read_weather_accum.sel(
            latitude=latitude,
            longitude=longitude,
            method="nearest"
        )

        instant_point = read_weather_instant.sel(
            latitude=latitude,
            longitude=longitude,
            method="nearest"
        )

        max_point = read_weather_max.sel(
            latitude=latitude,
            longitude=longitude,
            method="nearest"
        )


        # Convert to pandas
        accum = (
            accum_point
            .to_dataframe()
            .reset_index()
        )

        instant = (
            instant_point
            .to_dataframe()
            .reset_index()
        )

        maximum = (
            max_point
            .to_dataframe()
            .reset_index()
        )


        # Add airport information
        instant["airport_id"] = airport_id
        instant["airport_latitude"] = latitude
        instant["airport_longitude"] = longitude


        # Add accumulated variables
        for column in accum.columns:

            if column not in [
                "time",
                "latitude",
                "longitude"
            ]:

                instant["accum_" + column] = (
                    accum[column].values
                )


        # Add maximum variables
        for column in maximum.columns:

            if column not in [
                "time",
                "latitude",
                "longitude"
            ]:

                instant["max_" + column] = (
                    maximum[column].values
                )


        # Store this airport's data
        all_weather_data.append(
            instant
        )


    # Combine all airports
    final_weather = pd.concat(
        all_weather_data,
        ignore_index=True
    )


    # Create output folder
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # Save Parquet
    final_weather.to_parquet(
        output_path,
        index=False
    )


    print("Weather extraction completed!")
    print("Total rows:", len(final_weather))
    print("Output file:", output_path)


# Run the function
weather_nc_to_parquet()