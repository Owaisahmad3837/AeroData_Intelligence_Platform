import pandas as pd
from pathlib import Path

Weather_path=Path("data/validation/good/weather_data/weather.parquet")


df=pd.read_parquet(Weather_path)

print(df.columns)
print(df[[
    "u10",
    "v10",
    "d2m",
    "t2m",
    "msl",
    "sp",
    "tcc",
    "accum_tp",
    "max_fg10"
]].head())