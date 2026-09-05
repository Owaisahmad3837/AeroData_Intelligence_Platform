# ✈️ AeroData Intelligence Platform

<p align="center">
  <img src="./docs/images/airport-data-platform-banner.png"
       alt="AeroData Intelligence Platform"
       width="100%">
</p>

<h1 align="center">AeroData Intelligence Platform</h1>

<p align="center">
  <strong>End-to-End ETL • Data Engineering • Airport Operations • Business Intelligence</strong>
</p>

<p align="center">
  Extract → Validate → Transform → Load → Analyze
</p>

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-Local%20%2B%20Neon-4169E1?logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-Analytics-FF4B4B?logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/Power%20BI-Business%20Intelligence-F2C811?logo=powerbi&logoColor=black">
  <img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white">
  <img src="https://img.shields.io/badge/ETL-End--to--End-success">
  <img src="https://img.shields.io/badge/License-MIT-green">
</p>

<p align="center">
  <a href="#-project-overview">Overview</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-etl-pipeline">ETL Pipeline</a> •
  <a href="#-analytics">Analytics</a> •
  <a href="#-testing">Testing</a> •
  <a href="#-installation">Installation</a>
</p>

---

# 🎬 Project Demo

<p align="center">
  <a href="https://youtu.be/VIDEO_ID">
    <img src="./docs/images/demo-thumbnail.png"
         alt="AeroData Intelligence Platform Demo"
         width="850">
  </a>
</p>

### ▶️ Watch the Complete Project Walkthrough

**[🎥 AeroData Intelligence Platform — Full Demo](https://youtu.be/VIDEO_ID)**

The video demonstrates the complete journey of the platform:

```text
External Data Sources
        ↓
Data Extraction
        ↓
Raw Data
        ↓
Data Validation
        ↓
       ┌───────────────┐
       │               │
      GOOD            BAD
       │               │
       ↓               ↓
Transformation      Rejected Data
       │
       ↓
Processed Data
       ↓
PostgreSQL
 ┌─────┴─────┐
 ↓           ↓
Local       Neon
PostgreSQL  PostgreSQL
 └─────┬─────┘
       ↓
   Analytics
 ┌─────┴─────┐
 ↓           ↓
Streamlit   Power BI
````

---

# 📌 Project Overview

**Airport Data Platform** is a complete **end-to-end data engineering and analytics platform** designed for airport operations analysis.

The project demonstrates the complete lifecycle of data — starting from external data sources and ending with interactive operational and business intelligence dashboards.

Instead of directly loading downloaded files into a database, the platform follows a structured ETL workflow:

> **Extract → Store Raw Data → Validate → Separate Good/Bad Data → Transform → Store Processed Data → Load into PostgreSQL → Analyze**

The platform brings together **six airport-related data domains**:

| # | Data Domain   | Purpose                                     |
| - | ------------- | ------------------------------------------- |
| 1 | ✈️ Flights    | Flight operations, delays and cancellations |
| 2 | 🏢 Airports   | Airport information and intelligence        |
| 3 | 🛫 Airlines   | Airline performance analysis                |
| 4 | 🛩️ Airplanes | Aircraft analysis                           |
| 5 | 🛣️ Routes    | Route intelligence                          |
| 6 | 🌦️ Weather   | Weather and flight relationship analysis    |

The final data is made available through **two analytical platforms**:

* 🟥 **Streamlit** — interactive operational analytics
* 🟨 **Power BI** — business intelligence and reporting

The platform also includes:

* Data validation
* Good/bad data separation
* CSV processing
* NetCDF processing
* Parquet processing
* Local PostgreSQL
* Neon PostgreSQL
* Structured logging
* Unit testing
* End-to-end testing
* Modular Python architecture

---

# 🎯 What Problem Does This Project Solve?

Airport operations generate different types of information from different sources.

Flight information, airport information, airline information, aircraft information, routes, and weather data do not naturally exist as one clean analytical dataset.

This project creates a pipeline that brings these different sources together into a structured analytical platform.

The idea is simple:

```text
Raw Data
   ↓
Reliable Data
   ↓
Structured Data
   ↓
Database
   ↓
Analytics
   ↓
Business Insights
```

The project therefore focuses not only on visualization, but on the **entire data journey before visualization**.

---

# 🏗️ Platform Architecture

<p align="center">
  <img src="./docs/images/architecture.png"
       alt="Airport Data Platform Architecture"
       width="950">
</p>

The platform is organized into separate layers.

```text
┌───────────────────────────────────────────────────────────┐
│                    EXTERNAL SOURCES                       │
│                                                           │
│                 Kaggle / Web Sources                      │
└────────────────────────────┬──────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────┐
│                     INGESTION                             │
│                                                           │
│          Download / Extract / Collect Raw Data            │
└────────────────────────────┬──────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────┐
│                      DATA/RAW                             │
│                                                           │
│ Flights • Airports • Airlines • Airplanes • Routes       │
│ Weather NetCDF                                             │
└────────────────────────────┬──────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────┐
│                     VALIDATION                            │
│                                                           │
│                 Data Quality Checks                        │
└───────────────────────┬───────────────┬───────────────────┘
                        │               │
                     VALID           INVALID
                        │               │
                        ▼               ▼
                 validation/good   validation/bad
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│                    TRANSFORMATION                         │
│                                                           │
│ Cleaning • Formatting • Structuring • Conversion          │
└────────────────────────────┬──────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────┐
│                 PROCESSED / TRANSFORM                      │
│                                                           │
│                 Analytics-ready datasets                   │
└────────────────────────────┬──────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────┐
│                         LOAD                              │
│                                                           │
│                    PostgreSQL Layer                        │
└──────────────────────┬──────────────────┬─────────────────┘
                       │                  │
                       ▼                  ▼
                Local PostgreSQL    Neon PostgreSQL
                       │                  │
                       └────────┬─────────┘
                                ▼
┌───────────────────────────────────────────────────────────┐
│                       ANALYTICS                           │
│                                                           │
│              Streamlit + Power BI                         │
└───────────────────────────────────────────────────────────┘
```

---

# 🔄 End-to-End ETL Pipeline

## 1️⃣ Extract — Data Ingestion

The first stage of the platform is **data ingestion**.

The project obtains airport-related datasets from external sources such as **Kaggle and web sources**.

The six primary datasets are:

```text
Airlines
Airplanes
Airports
Flights
Routes
Weather
```

The ingestion layer contains dedicated Python modules for the different data domains.

```text
src/airport_data_platform/ingestion/
```

The purpose of this layer is to move external/source data into the platform while keeping the original data separate from later processing.

---

# 📥 Raw Data Layer

After ingestion, source files are stored in:

```text
data/raw/
```

The raw layer contains the original datasets before transformation.

Example:

```text
data/raw/
├── airline_data/
│   └── airlines.csv
│
├── airplane_data/
│   └── airplanes.csv
│
├── airport_data/
│   └── airports.csv
│
├── flight_data/
│   └── flight_data_2024.csv
│
├── route_data/
│   └── routes.csv
│
└── weather_data/
    ├── weather_accum_2024.nc
    ├── weather_instant_2024.nc
    └── weather_max_2024.nc
```

Keeping raw data separate is important because it preserves the source layer independently from transformation logic.

---

# 2️⃣ Validate — Data Quality Layer

The extracted data is not immediately loaded into the database.

Before transformation, it passes through a dedicated validation layer.

```text
data/raw/
     │
     ▼
 VALIDATION
     │
     ├───────────────┐
     ▼               ▼
   GOOD             BAD
     │               │
     ▼               ▼
Continue          Isolate
Pipeline          Problematic Data
```

Validated data is stored under:

```text
data/validation/good/
```

Problematic data is separated under:

```text
data/validation/bad/
```

This provides a clear separation between data that can continue through the pipeline and data that requires attention.

---

# 🟢 Good Data

Valid datasets continue through the ETL pipeline.

```text
data/validation/good/
```

Example:

```text
good/
├── airline_data/
├── airplane_data/
├── airport_data/
├── flight_data/
├── route_data/
└── weather_data/
```

---

# 🔴 Bad Data

Data that fails validation is isolated rather than silently entering the next stage.

```text
data/validation/bad/
```

This provides visibility into data-quality problems and prevents invalid data from automatically flowing through the entire pipeline.

---

# 3️⃣ Transform — Data Transformation

Once data passes validation, it enters the transformation layer.

```text
validation/good/
        │
        ▼
   TRANSFORMATION
        │
        ▼
 data/transform/
```

The transformation layer contains separate modules for:

* Airlines
* Airplanes
* Airports
* Flights
* Routes
* Weather

Source code:

```text
src/airport_data_platform/transform/
```

The goal of this stage is to prepare the validated data for database loading and analytics.

---

# 🌦️ Weather Data Engineering

One of the distinctive parts of this project is the weather pipeline.

Unlike the other datasets, the raw weather data is provided as **NetCDF (`.nc`) files**.

There are three source files:

```text
weather_accum_2024.nc
weather_instant_2024.nc
weather_max_2024.nc
```

The platform processes the three weather files and produces a consolidated Parquet dataset.

```text
weather_accum_2024.nc
          │
          │
weather_instant_2024.nc
          ├──────────────► Weather Processing
          │                       │
weather_max_2024.nc               │
                                  ▼
                         final_weather_2024.parquet
```

The processed weather dataset is stored under:

```text
data/processed/weather_data_2024/
└── final_weather_2024.parquet
```

This part of the project demonstrates working with:

```text
NetCDF → Python Processing → Parquet
```

rather than only processing traditional CSV files.

---

# 4️⃣ Load — Database Layer

After validation and transformation, the data is loaded into PostgreSQL.

The platform supports **two PostgreSQL environments**.

```text
                    PostgreSQL
                       │
              ┌────────┴────────┐
              ▼                 ▼
        Local PostgreSQL    Neon PostgreSQL
          Development           Cloud
```

## 🖥️ Local PostgreSQL

The local PostgreSQL database provides a development and testing environment.

It allows the complete pipeline to be executed locally.

---

## ☁️ Neon PostgreSQL

The project also supports **Neon PostgreSQL** for cloud-based database storage.

Database configuration is managed through environment variables.

```text
.env
```

This avoids hardcoding database credentials into Python source files.

---

# 🗃️ Database Domains

The database layer handles the six primary airport domains:

```text
✈️ Flights
🏢 Airports
🛫 Airlines
🛩️ Airplanes
🛣️ Routes
🌦️ Weather
```

These datasets become the foundation for the analytical layer.

---

# 📊 Analytics Layer

The platform provides two major analytical interfaces.

```text
                    PostgreSQL
                         │
               ┌─────────┴─────────┐
               ▼                   ▼
          🟥 Streamlit         🟨 Power BI
          Interactive          Business
          Analytics           Intelligence
```

---

# 🟥 Streamlit Analytics

The project includes a dedicated Streamlit dashboard.

```text
dashboard/
├── main.py
├── navigation.py
└── pages/
```

The dashboard is organized into multiple analytical areas.

## 📈 Analytics

```text
Cancellation Analysis
Delay Analysis
```

These pages focus on understanding flight disruptions and operational performance.

---

## 🧠 Business Intelligence

```text
Executive Overview
Airline Performance
Airport Intelligence
Route Intelligence
```

These pages provide higher-level business and operational insights.

---

## ⚙️ Operations

```text
Airplane Analysis
Flight Operations
Weather vs Flight
```

These pages focus on operational analysis and relationships between flight activity, aircraft, and weather conditions.

---

## 🖥️ Streamlit Dashboard

<p align="center">
  <img src="https://github.com/user-attachments/assets/7d516455-7e52-4c07-9967-3f136c1077d9" width="300"/>
  <img src="https://github.com/user-attachments/assets/faf87aa1-0808-45a4-9826-adcce76c7d94" width="300"/>
  <img src="https://github.com/user-attachments/assets/2349b00c-429e-48f0-ab4a-dbd0a0ba4505" width="300"/>
  <img src="https://github.com/user-attachments/assets/0d1cf606-62e0-4cfd-b96d-caa04478f1da" width="300"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/4e241763-0b41-47de-9ae5-5448f9e84310" width="300"/>
  <img src="https://github.com/user-attachments/assets/5f3ed0aa-3abb-424e-8c4d-1b9d6ff075ff" width="300"/>
  <img src="https://github.com/user-attachments/assets/db87a233-564c-49ff-ae1f-062b0335bb1e" width="300"/>
  <img src="https://github.com/user-attachments/assets/b255c5cf-6865-4c30-a11e-5eb34ebcce09" width="300"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/c6fb3491-22c3-4b08-a106-623160306d62" width="300"/>
  <img src="https://github.com/user-attachments/assets/e24bb31a-d6a5-4aad-b113-23f9a0a02ccd" width="300"/>
</p>

---

# 🟨 Power BI Analytics

The platform also includes a Power BI report for business intelligence and reporting.

```text
powerbi/
└── Airport_data_platform_2.pbix.zip
```

Power BI provides another analytical interface over the processed airport data.

<p align="center">
  <img src="./docs/images/powerbi-dashboard.png"
       alt="Power BI Dashboard"
       width="950">
</p>

---

# 🧪 Testing Strategy

Testing is treated as part of the data platform rather than something added at the end.

The project contains:

```text
Unit Tests
     +
End-to-End Tests
```

---

# 🔬 Unit Testing

Unit tests are organized according to ETL stages.

```text
test/
└── Unit Test/
    ├── ingestion/
    ├── transform/
    └── validation/
```

The purpose is to test individual components and transformations independently.

---

# 🔄 End-to-End Testing

The project also includes dedicated end-to-end tests.

```text
test/
└── End to End Test/
    ├── Airline_end_to_end.py
    ├── Airplane_end_to_end.py
    ├── Airports_end_to_end.py
    ├── flight_end_to_end.py
    └── route_end_to_end.py
```

End-to-end tests help verify complete data flows across multiple pipeline stages.

---

# 📝 Logging & Observability

The project contains a dedicated logging structure.

```text
logs/
├── data_profile/
├── End to End Test/
├── ingestion/
├── loading/
├── main/
├── Streamlit_log/
├── transform/
├── Unit Test/
└── validation/
```

Logs are separated by purpose and pipeline stage.

This makes it easier to investigate:

* Data ingestion
* Validation
* Transformation
* Database loading
* Pipeline execution
* Unit tests
* End-to-end tests
* Streamlit execution

---

# 📋 Logging Architecture

```text
                Pipeline
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
   Ingestion   Transform     Load
       │           │           │
       └───────────┼───────────┘
                   │
                   ▼
                 logs/
                   │
       ┌───────────┼────────────┐
       ▼           ▼            ▼
 Validation      Tests      Dashboard
```

The logs provide an execution trail that can be used during development, debugging, and testing.

---

# 🧰 Data Profiling

The project also contains:

```text
tools/data_profile.py
```

This provides a dedicated location for data profiling functionality.

Data profiling is useful for understanding the structure and quality of incoming datasets before or during pipeline processing.

---

# 🧱 Project Structure

```text
Airport-Data-Platform/
├── .env
├── .gitattributes
├── .gitignore
├── check.py
├── main.py
├── README.md
├── requirements.txt
├── dashboard/
│   ├── main.py
│   ├── navigation.py
│   └── pages/
│       ├── Home.py
│       ├── analytic/
│       │   ├── canellation.py
│       │   └── delay_analysis.py
│       ├── Business_intellenginece/
│       │   ├── Airline_performacne.py
│       │   ├── airport_intelligence.py
│       │   ├── Excuitive_overview.py
│       │   └── Route_intelliegnce.py
│       └── Operation/
│           ├── airplane_analysus.py
│           ├── flight_operation.py
│           └── weather vs flight .py
├── data/
│   ├── processed/
│   │   └── weather_data_2024/
│   │       └── final_weather_2024.parquet
│   ├── raw/
│   │   ├── airline_data/
│   │   │   └── airlines.csv
│   │   ├── airplane_data/
│   │   │   ├── .~lock.airplanes.csv#
│   │   │   └── airplanes.csv
│   │   ├── airport_data/
│   │   │   └── airports.csv
│   │   ├── flight_data/
│   │   │   └── flight_data_2024.csv
│   │   ├── route_data/
│   │   │   └── routes.csv
│   │   └── weather_data/
│   │       ├── weather_accum_2024.nc
│   │       ├── weather_instant_2024.nc
│   │       └── weather_max_2024.nc
│   ├── transform/
│   │   ├── airline_data/
│   │   │   └── airlines.csv
│   │   ├── airplane_data/
│   │   │   ├── .~lock.airplanes.csv#
│   │   │   └── airplanes.csv
│   │   ├── airport_data/
│   │   │   └── airports.csv
│   │   ├── flight_data/
│   │   │   └── flight_data_2024.csv
│   │   ├── route_data/
│   │   │   └── routes.csv
│   │   └── weather_data/
│   │       └── weather.parquet
│   └── validation/
│       ├── bad/
│       │   ├── airline_data/
│       │   │   └── file.csv
│       │   ├── airplane_data/
│       │   ├── airports_data/
│       │   ├── flight_data/
│       │   ├── route_data/
│       │   └── weather_data/
│       └── good/
│           ├── airline_data/
│           │   └── airlines.csv
│           ├── airplane_data/
│           │   ├── .~lock.airplanes.csv#
│           │   └── airplanes.csv
│           ├── airport_data/
│           │   └── airports.csv
│           ├── flight_data/
│           │   └── flight_data_2024.csv
│           ├── route_data/
│           │   └── routes.csv
│           └── weather_data/
│               └── weather.parquet
├── logs/
│   ├── data_profile/
│   │   └── data_profile.log
│   ├── End to End Test/
│   │   ├── airline_e2e_log.log
│   │   ├── airplane_e2e_log.log
│   │   ├── airport_e2e_log.log
│   │   └── route_e2e_log.log
│   ├── ingestion/
│   │   ├── airline_data.log
│   │   ├── airplane_data.log
│   │   ├── airport_data.log
│   │   ├── flight_data.log
│   │   ├── main_ingestion_log.log
│   │   ├── route_data.log
│   │   ├── weather_data_nc_to_parquet.log
│   │   └── weather_data.log
│   ├── loading/
│   │   ├── airline.log
│   │   ├── airplane.log
│   │   ├── airport.log
│   │   ├── flight.log
│   │   ├── main_load.log
│   │   ├── Route.log
│   │   └── weather.log
│   ├── main/
│   │   └── main_pipeline.log
│   ├── Streamlit_log/
│   │   ├── home_page.log
│   │   └── main_page.log
│   ├── transform/
│   │   ├── airline.log
│   │   ├── airplane.log
│   │   ├── airport.log
│   │   ├── flight.log
│   │   ├── main_transform_log.log
│   │   ├── route.log
│   │   └── weather.log
│   ├── Unit Test/
│   │   ├── Ingestion/
│   │   │   ├── airline_log.log
│   │   │   ├── airplane_log.log
│   │   │   ├── airport_log.log
│   │   │   ├── flight_log.log
│   │   │   ├── route_log.log
│   │   │   └── weather_log.log
│   │   ├── Transform/
│   │   │   ├── airline_transformation.log
│   │   │   ├── airplane_transformation.log
│   │   │   ├── airport_transformation.log
│   │   │   ├── route_transformation.log
│   │   │   └── weather_transformation.log
│   │   └── Validation/
│   │       ├── airline_log_validation.log
│   │       ├── airplane_log_validation.log
│   │       ├── airport_log_validation.log
│   │       ├── flight_log_validation.log
│   │       ├── route_log_validation.log
│   │       └── weather_log_validation.log
│   └── validation/
│       ├── airlines.log
│       ├── airplanes.log
│       ├── airports.log
│       ├── flight_validation.log
│       ├── route.log
│       └── weather.log
├── powerbi/
│   └── Airport_data_platform_2.pbix.zip
├── src/
│   └── airport_data_platform/
│       ├── __init__.py
│       ├── __pycache__/
│       ├── config/
│       │   ├── __init__.py
│       │   ├── db_connection.py
│       │   ├── logging_config.py
│       │   └── __pycache__/
│       ├── ingestion/
│       │   ├── airlines.py
│       │   ├── airplanes.py
│       │   ├── airports.py
│       │   ├── flights.py
│       │   ├── main_ingestion.py
│       │   ├── routes.py
│       │   ├── tempCodeRunnerFile.py
│       │   ├── weather_nc_to_parquet.py
│       │   ├── weather.py
│       │   └── __pycache__/
│       ├── load/
│       │   ├── airline.py
│       │   ├── airplane.py
│       │   ├── airport.py
│       │   ├── flight.py
│       │   ├── main_load.py
│       │   ├── route.py
│       │   ├── weather.py
│       │   └── __pycache__/
│       ├── Query/
│       │   ├── Analysis_query.py
│       │   ├── Operation_Query.py
│       │   └── __pycache__/
│       ├── services/
│       │   ├── dashborad_data.py
│       │   ├── tempCodeRunnerFile.py
│       │   └── __pycache__/
│       ├── transform/
│       │   ├── airline.py
│       │   ├── airplane.py
│       │   ├── airport.py
│       │   ├── flight.py
│       │   ├── main_transform.py
│       │   ├── route.py
│       │   ├── weather.py
│       │   └── __pycache__/
│       └── validation/
│           ├── airline.py
│           ├── airplane.py
│           ├── airport.py
│           ├── flight.py
│           ├── main_validation.py
│           ├── route.py
│           ├── tempCodeRunnerFile.py
│           ├── weather.py
│           └── __pycache__/
├── test/
│   ├── End to End Test/
│   │   ├── Airline_end_to_end.py
│   │   ├── Airplane_end_to_end.py
│   │   ├── Airports_end_to_end.py
│   │   ├── flight_end_to_end.py
│   │   ├── route_end_to_end.py
│   │   ├── tempCodeRunnerFile.py
│   │   └── __pycache__/
│   └── Unit Test/
│       ├── ingestion/
│       │   ├── airline.py
│       │   ├── airplanes.py
│       │   ├── airports.py
│       │   ├── flight.py
│       │   ├── routes.py
│       │   ├── tempCodeRunnerFile.py
│       │   ├── weather.py
│       │   └── __pycache__/
│       ├── transform/
│       │   ├── airlines.py
│       │   ├── airplane.py
│       │   ├── airports.py
│       │   ├── routes.py
│       │   ├── weather.py
│       │   └── __pycache__/
│       └── validation/
│           ├── airline.py
│           ├── airplanes.py
│           ├── airport.py
│           ├── flight.py
│           ├── route.py
│           ├── weather.py
│           └── __pycache__/
├── tools/
│   └── data_profile.py
└── venv/
```

---

# 🔗 Data Flow

The complete platform can be summarized as:

```text
                         SOURCE
                           │
                           ▼
                 Kaggle / Web Sources
                           │
                           ▼
                     INGESTION
                           │
                           ▼
                       data/raw
                           │
                           ▼
                      VALIDATION
                     /           \
                    /             \
                 GOOD             BAD
                  │                │
                  ▼                ▼
             TRANSFORM         Isolated
                  │
                  ▼
             data/transform
                  │
                  ▼
                LOAD
                  │
          ┌───────┴───────┐
          ▼               ▼
       Local             Neon
     PostgreSQL       PostgreSQL
          │               │
          └───────┬───────┘
                  ▼
              ANALYTICS
             /         \
            ▼           ▼
       Streamlit      Power BI
```

---

# 🧩 Technology Stack

## Programming

* Python 3.9+
* Pandas
* PyArrow
* Xarray
* SQLAlchemy
* Psycopg

## Data Engineering

* ETL architecture
* CSV processing
* NetCDF processing
* Parquet
* Data validation
* Data transformation
* Database loading

## Databases

* PostgreSQL
* Local PostgreSQL
* Neon PostgreSQL

## Analytics

* Streamlit
* Power BI
* SQL

## Testing

* Pytest
* Unit testing
* End-to-end testing

## Engineering

* Python logging
* Environment variables
* Modular architecture
* Git/GitHub

---

# 🖥️ Development Environment

The project was developed and tested across multiple environments.

```text
Windows 11
     +
Linux
     +
VirtualBox Virtual Machines
```

Working across Windows and Linux environments provided practical experience with different development environments and execution workflows.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Owaisahmad3837/Airport-Data-Platform-.git

cd Airport-Data-Platform-
```

---

## 2. Create a Virtual Environment

### Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```powershell
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

The project uses environment variables for configuration.

Create/configure your:

```text
.env
```

The configuration can contain the required database connection information for:

```text
Local PostgreSQL
+
Neon PostgreSQL
```

### ⚠️ Security

Never commit:

```text
Passwords
API Keys
Database Credentials
Secret Tokens
```

to GitHub.

Add sensitive files to `.gitignore`.

---

# ▶️ Running the ETL Pipeline

The complete ETL process is orchestrated through:

```text
main.py
```

Run:

```bash
python main.py
```

The pipeline follows the overall lifecycle:

```text
Extract
   ↓
Validate
   ↓
Transform
   ↓
Load
```

---

# 📊 Running the Streamlit Dashboard

After the ETL pipeline has completed:

```bash
streamlit run dashboard/main.py
```

The Streamlit application provides the interactive analytical layer.

---

# 📈 Opening the Power BI Report

The Power BI report is located at:

```text
powerbi/Airport_data_platform_2.pbix.zip
```

Extract the ZIP archive and open the `.pbix` file with Power BI Desktop.

---

# 🧪 Running Tests

Run the complete test suite with:

```bash
pytest -v
```

You can also run individual test groups.

### Unit Tests

```bash
pytest "test/Unit Test" -v
```

### End-to-End Tests

```bash
pytest "test/End to End Test" -v
```

---

# 📊 Example Pipeline Execution

A complete execution looks conceptually like:

```text
$ python main.py

========================================
     AIRPORT DATA PLATFORM
========================================

[1] Data Ingestion
        ↓
[2] Data Validation
        ↓
[3] Data Transformation
        ↓
[4] Database Loading
        ↓
[5] Pipeline Completed

========================================
          ETL COMPLETE
========================================
```

---

# 📈 Analytics Capabilities

The platform is designed to support analysis such as:

### ✈️ Flight Operations

* Flight activity
* Operational performance
* Delays
* Cancellations

### 🛫 Airline Performance

* Airline-level operational metrics
* Comparative performance
* Flight activity

### 🏢 Airport Intelligence

* Airport-level activity
* Airport comparisons
* Operational indicators

### 🛣️ Route Intelligence

* Route activity
* Origin/destination analysis
* Route-level comparisons

### 🛩️ Aircraft Analysis

* Aircraft-level information
* Aircraft activity
* Operational analysis

### 🌦️ Weather Analysis

* Weather data processing
* Weather vs flight analysis
* Relationship between weather conditions and operations

---

# 📸 Project Gallery

A visual walkthrough of the **Airport Data Platform** — showcasing the complete journey from data ingestion and validation to database loading, analytics, logging, and testing.



---

## 🔄 Complete ETL Pipeline

<p align="center">
  <img src="https://github.com/user-attachments/assets/0ab0ec08-88a0-42f5-b233-b3682e7de755" width="300"/>
  <img src="https://github.com/user-attachments/assets/3a15d298-534a-41f0-b995-f3c412d35f14" width="300"/>
  <img src="https://github.com/user-attachments/assets/9233e8ac-4b48-41a8-8106-a0072946c0ee" width="300"/>
  <img src="https://github.com/user-attachments/assets/6110d98d-a587-4e6a-a8ee-7532175d315c" width="300"/>
</p>

---

## 🗄️ Database

### ⚙️ Database Loading

<p align="center">
  <img src="https://github.com/user-attachments/assets/b3e1e81f-6b7f-4bfe-90a8-62d588b27032" width="300"/>
  <img src="https://github.com/user-attachments/assets/00b8d884-3b27-4080-bcfd-5aa0d6712e7f" width="300"/>
  <img src="https://github.com/user-attachments/assets/2ea7b690-d382-40ed-a295-4ccb998c187d" width="300"/>
  <img src="https://github.com/user-attachments/assets/c4f25cbb-104a-4db7-9934-02c924e2a390" width="300"/>
</p>

### 🖥️ Local PostgreSQL

<p align="center">
  <img src="https://github.com/user-attachments/assets/4db25967-ebcb-4890-885a-fa997c299f09" width="300"/>
  <img src="https://github.com/user-attachments/assets/7d2fb062-90af-4b7b-b48b-ed73c8a46ca8" width="300"/>
  <img src="https://github.com/user-attachments/assets/271ae35d-71c2-4cff-8881-c449bb004174" width="300"/>
  <img src="https://github.com/user-attachments/assets/60fb3fbd-0970-4514-b348-8b9c0d91957b" width="300"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3c48c453-8093-4440-92e6-4966d4b01f26" width="300"/>
</p>

### ☁️ Neon PostgreSQL

<p align="center">
  <img src="https://github.com/user-attachments/assets/0691fc79-1699-4e5c-9feb-1136862d4248" width="300"/>
  <img src="https://github.com/user-attachments/assets/7cc4f36b-74c3-410a-9a38-d39eea7a9d02" width="300"/>
  <img src="https://github.com/user-attachments/assets/6d6beeb0-e3b6-429d-9e44-bdcd18ba86c0" width="300"/>
</p>

---

## ✅ Data Validation

<p align="center">
  <img src="https://github.com/user-attachments/assets/5e0a4e43-ea04-4e3b-9137-70cf47368c48" width="300"/>
  <img src="https://github.com/user-attachments/assets/c73d3c97-ff9e-4a2c-b0ad-a034a973d46b" width="300"/>
  <img src="https://github.com/user-attachments/assets/98ce1d4f-c797-4a47-8a2c-b469946ccdee" width="300"/>
  <img src="https://github.com/user-attachments/assets/43581c12-f7b5-4566-be55-4d961885be26" width="300"/>
</p>

---

## 📝 Pipeline Logging

<p align="center">
  <img src="https://github.com/user-attachments/assets/75d6cca3-d325-4e5a-8365-62a30faa9969" width="300"/>
  <img src="https://github.com/user-attachments/assets/1c1602fd-214b-47ba-bc9b-94893db0d635" width="300"/>
</p>

> Extensive logging is maintained across ingestion, validation, transformation, loading, testing, and dashboard execution.

---

## 🧪 Testing

<p align="center">
  <img src="https://github.com/user-attachments/assets/402f2ec3-9efa-45be-a193-20091af39423" width="300"/>
  <img src="https://github.com/user-attachments/assets/10781b82-dab1-4fed-bca9-b5e73ef83a45" width="300"/>
</p>

---

## 📊 Analytics & Intelligence

<p align="center">
  <img src="https://github.com/user-attachments/assets/7d516455-7e52-4c07-9967-3f136c1077d9" width="300"/>
  <img src="https://github.com/user-attachments/assets/faf87aa1-0808-45a4-9826-adcce76c7d94" width="300"/>
  <img src="https://github.com/user-attachments/assets/2349b00c-429e-48f0-ab4a-dbd0a0ba4505" width="300"/>
  <img src="https://github.com/user-attachments/assets/0d1cf606-62e0-4cfd-b96d-caa04478f1da" width="300"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/4e241763-0b41-47de-9ae5-5448f9e84310" width="300"/>
  <img src="https://github.com/user-attachments/assets/5f3ed0aa-3abb-424e-8c4d-1b9d6ff075ff" width="300"/>
  <img src="https://github.com/user-attachments/assets/db87a233-564c-49ff-ae1f-062b0335bb1e" width="300"/>
  <img src="https://github.com/user-attachments/assets/b255c5cf-6865-4c30-a11e-5eb34ebcce09" width="300"/>
</p>

---

## 🏗️ End-to-End Architecture

<p align="center">

**Data Sources**

⬇️

**Raw Data**

⬇️

**Validation**

🟢 Good Data &nbsp;&nbsp; 🔴 Bad Data

⬇️

**Transformation**

⬇️

**PostgreSQL**

🖥️ Local &nbsp;&nbsp; ☁️ Neon

⬇️

**Analytics**

📊 Streamlit &nbsp;&nbsp; 📈 Power BI

</p>

---

## ✈️ From Data to Airport Intelligence

<p align="center">

**Extract → Validate → Transform → Load → Analyze**

</p>

<p align="center">

Raw Sources  
↓  
Validated Data  
↓  
Clean & Transformed Datasets  
↓  
PostgreSQL  
↓  
Business Intelligence  
↓  
Airport Insights

</p>

---

<p align="center">

### ✈️ Airport Data Platform

**From Raw Data → Validated Data → Transformed Data → PostgreSQL → Analytics**

Built with ❤️ using Python • PostgreSQL • Streamlit • Power BI

</p>
### ✈️ Airport Data Platform

**From Raw Data → Validated Data → Transformed Data → PostgreSQL → Analytics**

</p>

---

# 💡 Why This Project Matters

This project was intentionally built as more than a dashboard.

A dashboard is only the final layer.

The difficult part is ensuring that the data reaching the dashboard has passed through a reliable and traceable process.

This platform therefore focuses on:

```text
Where does the data come from?
          ↓
How is it collected?
          ↓
Where is raw data stored?
          ↓
How is data validated?
          ↓
What happens to invalid data?
          ↓
How is valid data transformed?
          ↓
How is weather data converted?
          ↓
Where is processed data stored?
          ↓
How is it loaded into PostgreSQL?
          ↓
How can the pipeline be tested?
          ↓
How can failures be investigated?
          ↓
How can the final data be analyzed?
```

This complete lifecycle is the core idea behind the project.

---

# 📚 What I Learned

Building this project provided practical experience across multiple areas of software and data engineering.

## Data Engineering

* Designing an end-to-end ETL pipeline
* Data ingestion
* Data validation
* Data transformation
* Database loading
* Handling multiple data formats
* Working with NetCDF
* Converting NetCDF to Parquet

## Python Engineering

* Modular project structure
* Separation of concerns
* Reusable functions
* Configuration management
* Environment variables
* Logging

## Database Engineering

* PostgreSQL
* Local database environments
* Cloud PostgreSQL with Neon
* Database connectivity
* SQL-based analytical workflows

## Testing

* Unit testing
* End-to-end testing
* Pipeline verification
* Test logging

## Analytics

* Streamlit dashboards
* Power BI reports
* Operational analysis
* Business intelligence
* Data-driven visualization

---

# 🚀 Future Roadmap

This project is designed to continue evolving.

Future improvements may include:

* [ ] More airport datasets
* [ ] More weather sources
* [ ] Additional years of data
* [ ] Automated data ingestion
* [ ] Scheduled ETL execution
* [ ] Real-time airport data
* [ ] Real-time weather integration
* [ ] Advanced data-quality monitoring
* [ ] More automated tests
* [ ] CI/CD integration
* [ ] Docker deployment
* [ ] Cloud deployment
* [ ] Data orchestration
* [ ] Advanced SQL analytics
* [ ] Predictive analytics
* [ ] Machine learning models
* [ ] Delay prediction
* [ ] Cancellation prediction
* [ ] More Power BI dashboards
* [ ] More Streamlit pages

---

# 🗺️ Long-Term Vision

The long-term goal is to evolve the project from a learning-oriented ETL platform into a more complete airport data ecosystem.

```text
                    AIRPORT DATA PLATFORM
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   Data Sources          Data Platform        Analytics
        │                    │                    │
   ┌────┴────┐         ┌─────┴─────┐       ┌─────┴─────┐
   │         │         │           │       │           │
 Kaggle    APIs      ETL       Database  Streamlit   Power BI
   │         │         │           │       │           │
   └────┬────┘         └─────┬─────┘       └─────┬─────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                     Airport Intelligence
```

---

# 🌟 Project Highlights

| Capability               | Implementation                                          |
| ------------------------ | ------------------------------------------------------- |
| 🔄 ETL                   | End-to-End Extract → Validate → Transform → Load        |
| 📥 Ingestion             | Kaggle / Web-based sources                              |
| 🗂️ Raw Layer            | Dedicated `data/raw/` structure                         |
| 🧪 Validation            | Good / Bad data separation                              |
| 🔧 Transformation        | Modular Python transformation layer                     |
| 🌦️ Weather              | 3 NetCDF files → consolidated Parquet                   |
| 🗄️ Database             | Local PostgreSQL + Neon PostgreSQL                      |
| 📊 Analytics             | Streamlit                                               |
| 📈 Business Intelligence | Power BI                                                |
| 🧪 Testing               | Unit + End-to-End                                       |
| 📝 Logging               | Pipeline-wide logging                                   |
| 🛩️ Domains              | Flights, Airports, Airlines, Airplanes, Routes, Weather |
| 🐍 Language              | Python                                                  |
| 🖥️ Environments         | Windows 11 + Linux + VirtualBox                         |

---

# 🏆 What Makes This Project Different?

The main focus of this project is the **complete data lifecycle**.

Many analytics projects begin with:

```text
Clean CSV
   ↓
Dashboard
```

This project begins much earlier:

```text
External Source
      ↓
Data Extraction
      ↓
Raw Data
      ↓
Validation
      ↓
Good / Bad Separation
      ↓
Transformation
      ↓
NetCDF Processing
      ↓
Parquet
      ↓
PostgreSQL
      ↓
Testing
      ↓
Logging
      ↓
Streamlit
      ↓
Power BI
```

The objective is to demonstrate the engineering work that happens **before the final chart appears on the screen**.

---

# 🎥 Full Walkthrough

The project video covers the complete platform from beginning to end.

### The walkthrough includes:

```text
01. Project Architecture
02. Data Sources
03. Data Ingestion
04. Raw Data Layer
05. Data Validation
06. Good / Bad Data
07. Data Transformation
08. Weather NetCDF Processing
09. Parquet Output
10. PostgreSQL Loading
11. Local Database
12. Neon Database
13. Logging
14. Unit Testing
15. End-to-End Testing
16. Streamlit Dashboard
17. Power BI Analytics
18. Future Improvements
```

<p align="center">
  <a href="https://youtu.be/VIDEO_ID">
    <img src="./docs/images/demo-thumbnail.png"
         alt="Watch Airport Data Platform Demo"
         width="800">
  </a>
</p>

---

# 👨‍💻 Author

## Owais Ahmad

**Software Engineer | Data Engineering & Analytics Enthusiast**

Pakistan 🇵🇰

This project represents a practical learning journey through:

```text
Python
   ↓
Data Engineering
   ↓
ETL
   ↓
Databases
   ↓
Testing
   ↓
Analytics
   ↓
Business Intelligence
```

---

# ⭐ Support the Project

If you find this project useful, educational, or interesting:

⭐ **Star the repository**

🍴 **Fork the project**

🐛 **Open an issue**

💡 **Suggest an improvement**

🤝 **Contribute**

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

<p align="center">

# ✈️ Airport Data Platform

### From Raw Data to Airport Intelligence

**Extract • Validate • Transform • Load • Analyze**

Built with ❤️ using Python • PostgreSQL • Streamlit • Power BI

</p>
```
