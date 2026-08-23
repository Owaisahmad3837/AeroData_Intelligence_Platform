import pandas as pd
from pathlib import Path
route_path=Path("data/transform/route_data/routes.csv")

df = pd.read_csv(route_path)

print("\nRoute ID columns:")
print(df[
    [
        "airline_id",
        "source_airport_id",
        "destination_airport_id",
        "stops"
    ]
].max())

print("\nData types:")
print(df[
    [
        "airline_id",
        "source_airport_id",
        "destination_airport_id",
        "stops"
    ]
].dtypes)