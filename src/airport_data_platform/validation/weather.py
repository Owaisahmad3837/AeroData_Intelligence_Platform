import pandas as pd
from pathlib import Path
from ..config.logging_config import logging_config

weather_file=Path("data/processed/weather_data_2024/final_weather_2024.parquet")
output_good_file=Path("data/validation/good/weather_data/weather.parquet")
output_bad_file=Path("data/validation/bad/weather_data/weather.parquet")

required_columns = [
 'valid_time',
 "latitude",
 "longitude",
 "airport_id",
 "airport_latitude",
 "airport_longitude"

]


def weather_validation():
  log=logging_config("validation","weather")

  log.info("checking weather file ...")
  print("checking weather file ... ")

  if not weather_file.exists():
      print("No weather file")
      log.warning("no csv weather file exist first check it")
      return
  
  output_good_file.parent.mkdir(parents=True, exist_ok=True)
  output_bad_file.parent.mkdir(parents=True, exist_ok=True)
  print(f"File is avabile and location is {weather_file}.Now start reading...")
  log.info(f"File is avabile and location is {weather_file}.Now start reading...")
  df=pd.read_parquet(weather_file)
  print("reading full file.")
  log.info("reading full file.")

  numeric_columns = [
        "u10",
        "v10",
        "d2m",
        "t2m",
        "msl",
        "sp",
        "tcc",
        "number",
        "latitude",
        "longitude",
        "airport_id",
        "airport_latitude",
        "airport_longitude",
        "accum_tp",
        "accum_number",
        "max_fg10",
        "max_number"
    ]

  for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )


  missing_column=[
    column
    for column in required_columns
    if column not in df.columns
  ]
  if missing_column:
    print(f"Missing column:{missing_column}")
    log.error(f"Missing column:{missing_column}")
    return

  bad_mask = (

        # Required columns cannot be NULL
        df[required_columns]
        .isnull()
        .any(axis=1)

        |

        # Latitude
        (
            ~df["latitude"].between(
                -90,
                90
            )
        )

        |

        # Longitude
        (
            ~df["longitude"].between(
                -180,
                180
            )
        )

        |

        # Airport latitude
        (
            ~df["airport_latitude"].between(
                -90,
                90
            )
        )

        |

        # Airport longitude
        (
            ~df["airport_longitude"].between(
                -180,
                180
            )
        )

        |

        # Airport ID must be positive
        (
            df["airport_id"] <= 0
        )

        |

        # Total cloud cover: 0 to 1
        (
            df["tcc"].notna()
            &
            ~df["tcc"].between(
                0,
                1
            )
        )

        |

        # Accumulated precipitation cannot be negative
        (
            df["accum_tp"].notna()
            &
            (df["accum_tp"] < 0)
        )

        |

        # Maximum wind gust cannot be negative
        (
            df["max_fg10"].notna()
            &
            (df["max_fg10"] < 0)
        )

        |

        # Surface pressure must be positive
        (
            df["sp"].notna()
            &
            (df["sp"] <= 0)
        )

        |

        # Mean sea-level pressure must be positive
        (
            df["msl"].notna()
            &
            (df["msl"] <= 0)
        )
    )

  bad_data = df[bad_mask]
  good_data = df[~bad_mask]

  print("Saving good data...")
  log.info("Saving good data...")
  good_data.to_parquet(
    output_good_file,
    index=False
)
  print("Saving bad data...")
  log.info("Saving bad data...")
  bad_data.to_parquet(
    output_bad_file,
    index=False
)
  print()
  print("weather validation complete.")
  print(f"Total rows: {len(df)}")
  print(f"Good rows: {len(good_data)}")
  print(f"Bad rows: {len(bad_data)}")
  
  log.info("weather validation complete.")
  log.info(f"Total rows: {len(df)}")
  log.info(f"Good rows: {len(good_data)}")
  log.info(f"Bad rows: {len(bad_data)}")