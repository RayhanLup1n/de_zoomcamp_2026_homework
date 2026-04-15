# NYC Taxi Analytics Dashboard — Data Engineering Capstone Project 2026

> **Author:** Rayhan Ananda
> **Date:** April 2026
> **Status:** Complete — Ready for Review

---

## Overview

This project builds an end-to-end data pipeline to analyze NYC taxi trips from 2024–2025, providing insights into ride patterns, payment trends, and trip distributions.

### Problem Statement

NYC Taxi & Limousine Commission (TLC) generates massive amounts of trip data daily. Traditional analysis methods are time-consuming and don't provide real-time insights. This project aims to:

1. **Centralize Data:** Aggregate taxi data from multiple sources (Green & Yellow cabs)
2. **Automate Processing:** Build a repeatable pipeline for monthly data updates
3. **Enable Analytics:** Provide self-service analytics for trip patterns, payment preferences, and fare trends

### Business Value

- **Urban Planners:** Optimize transportation infrastructure using trip patterns
- **Fleet Managers:** Forecast demand and optimize operations
- **Data Scientists:** Access clean, structured data for ML models

---

## Architecture

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Ingestion** | dlt | Extract, normalize, load taxi data |
| **Data Lake** | DuckDB | Local OLAP database |
| **Orchestration** | Kestra | Workflow scheduling |
| **Transformation** | dbt | SQL-based transformations (staging → core → analytics) |
| **Dashboard** | Streamlit + Plotly | Interactive web analytics |
| **Deployment** | Docker Compose | Multi-container orchestration |

### Data Flow

```
NYC TLC (Parquet files)
    ↓
dlt (Ingestion)
    ↓
DuckDB (raw.green_tripdata, raw.yellow_tripdata)
    ↓
Kestra (Orchestration)
    ↓
dbt (staging → core → analytics)
    ↓
DuckDB (analytics.fct_trips, analytics.trips_payment_type, analytics.trips_by_hour)
    ↓
Streamlit (Dashboard)
```

---

## Dataset

### Source: NYC Taxi & Limousine Commission

| Property | Details |
|----------|---------|
| **Data Range** | January 2024 – December 2025 (2 years) |
| **Taxi Types** | Green (outer boroughs) and Yellow (Manhattan) |
| **Format** | Parquet (compressed columnar) |
| **Total Size** | ~9GB (48 files × ~200MB each) |

### Current Data Status

> **Note:** Only **Green taxi** data (2024–2025) has been fully loaded. Yellow taxi ingestion was halted due to CloudFront rate limiting on the NYC TLC data source.
>
> The dashboard fully supports both taxi types — Yellow taxi data will populate automatically once ingested.

| Taxi Type | Status | Records |
|-----------|--------|---------|
| Green 2024 | ✅ Loaded | ~612K trips |
| Green 2025 | ✅ Loaded | ~554K trips |
| Yellow 2024 | ⏳ Pending | Rate-limited by CloudFront |
| Yellow 2025 | ⏳ Pending | Rate-limited by CloudFront |

### Key Fields

- `pickup_datetime` / `dropoff_datetime` — Trip timestamps
- `trip_distance` — Distance in miles
- `payment_type` — Payment method (Credit Card, Cash, etc.)
- `fare_amount`, `tip_amount`, `total_amount` — Financial fields
- `PULocationID` / `DOLocationID` — Pickup/dropoff location IDs

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### 1. Start Services

```bash
cd builder_rayhanAnanda/project

# Create environment file
cp .env.example .env

# Start core services (Kestra + Dashboard)
docker compose up -d

# Dashboard will be available at http://localhost:8501
# Kestra UI will be available at http://localhost:8080
```

> **Default `docker compose up`** starts only the dashboard, Kestra, and PostgreSQL.
> Ingestion and dbt are opt-in via profiles (see below).

### 2. Run Ingestion (Optional — data already included)

```bash
# Run ingestion manually (downloads ~9GB of data)
docker compose --profile ingest up ingestion

# ⚠️ This downloads large files and may take 30-60 minutes
```

### 3. Run dbt Transformations (Optional — already built)

```bash
# Run dbt transformations
docker compose --profile transform run dbt dbt run --project-dir /app/dbt --profiles-dir /app/dbt

# Run dbt tests
docker compose --profile transform run dbt dbt test --project-dir /app/dbt --profiles-dir /app/dbt
```

### 4. Stop Services

```bash
# Stop services (preserve data)
docker compose down

# Stop services + remove volumes (full reset)
docker compose down -v
```

---

## Dashboard

### Key Metrics

| Metric | Description |
|--------|-------------|
| **Total Trips** | Number of taxi trips in selected period |
| **Total Revenue** | Sum of fare + tips + tolls |
| **Avg Distance** | Average trip distance in miles |
| **Avg Fare** | Average fare per trip |
| **Avg Tip** | Average tip per trip |

### Tile 1: Payment Type Distribution (Categorical)

Bar chart showing trip count and percentage by payment type (Credit Card, Cash, Other, etc.)

### Tile 2: Hourly Trip Patterns (Temporal)

Dual-axis line chart showing trip count and average fare by hour of day.

### Filters

- **Year:** 2023, 2024, 2025
- **Taxi Type:** Green / Yellow / Both

---

## Project Structure

```
project/
├── README.md                 # This file
├── PROJECT_PLAN.md           # Detailed project plan
├── docker-compose.yml        # Docker Compose (profiles for ingestion/dbt)
├── .env.example              # Environment template
├── docker/
│   ├── Dockerfile.ingestion  # dlt container
│   ├── Dockerfile.dbt        # dbt container
│   └── Dockerfile.dashboard  # Streamlit container
├── ingestion/
│   ├── source.py             # dlt source definition
│   └── main.py               # Ingestion entry point
├── kestra/flows/
│   └── main_flow.yml         # Orchestration workflow
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── staging/          # Raw data cleaning
│       └── analytics/        # Dashboard-ready aggregations
├── dashboard/
│   └── app.py                # Streamlit dashboard
├── data/
│   └── capstone.duckdb       # DuckDB database (~1.2GB)
└── scripts/                  # Utility scripts
```

---

## dbt Transformation Layers

### Staging Layer
- `stg_green_trips` — Standardized Green taxi trips with cleaned column names
- `stg_yellow_trips` — Standardized Yellow taxi trips (pending data)

### Core Layer
- `fct_trips` — Unified fact table (Green + Yellow) with computed fields (duration, trip_hour, trip_year, taxi_type)

### Analytics Layer
- `trips_payment_type` — Pre-aggregated payment type distribution by year/taxi type
- `trips_by_hour` — Pre-aggregated hourly trip patterns by year/taxi type

### dbt Test Results
- 10 of 11 tests passing
- 1 expected warning: `payment_type` NULL values (legitimate data — some trips have no payment type recorded)

---

## Evaluation Criteria

| Criteria | Implementation | Status |
|----------|----------------|--------|
| Problem Description | Comprehensive README with business problem | ✅ |
| Cloud | Local development with Docker | ⏳ Optional |
| Data Ingestion | dlt pipeline with multi-source (Green + Yellow) | ✅ |
| Data Warehouse | DuckDB with layered schema (raw → staging → analytics) | ✅ |
| Transformations | dbt with staging → core → analytics layers | ✅ |
| Dashboard | Streamlit with 2 tiles (categorical + temporal) | ✅ |
| Reproducibility | Docker Compose, clear documentation | ✅ |

---

## Troubleshooting

### Services won't start

```bash
docker compose logs                     # Check all logs
docker compose up --build -d            # Rebuild containers
docker compose restart dashboard        # Restart specific service
```

### DuckDB connection error

```bash
# Ensure data directory and database exist
ls -lh data/capstone.duckdb

# Inspect database tables
python -c "import duckdb; print(duckdb.connect('data/capstone.duckdb').execute('SHOW ALL TABLES').df())"
```

### dbt fails to run

```bash
docker compose --profile transform run dbt dbt debug --project-dir /app/dbt --profiles-dir /app/dbt
```

### Dashboard not loading data

1. Verify DuckDB has data: check `data/capstone.duckdb` exists and is >0 bytes
2. Check dashboard logs: `docker compose logs dashboard`
3. Ensure `DUCKDB_PATH` environment variable is set correctly

### Clean reset

```bash
docker compose down -v        # Stop + remove volumes
rm -rf data/                  # Remove database
docker compose up --build -d  # Rebuild everything
```

---

## Known Limitations

1. **Yellow taxi data not yet loaded** — CloudFront rate limiting prevents bulk download. Green taxi data is fully available for 2024-2025.
2. **Year outliers filtered** — Raw data contains occasional outlier records with years 2008/2009/2026. These are filtered in the dashboard query layer.
3. **Single-node deployment** — DuckDB runs as an embedded database. For production scale, consider migrating to BigQuery or PostgreSQL.

---

## Future Enhancements

- [ ] Deploy to GCP free tier (Cloud Run + BigQuery + GCS)
- [ ] Complete Yellow taxi ingestion (retry with backoff for rate limiting)
- [ ] Add CI/CD pipeline with GitHub Actions
- [ ] Add geographic visualizations (pickup/dropoff heatmaps)
- [ ] Implement monthly trend analysis tile

---

## References

- [NYC TLC Trip Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [dlt Documentation](https://dlthub.com/docs)
- [dbt Documentation](https://docs.getdbt.com)
- [Kestra Documentation](https://kestra.io/docs)
- [DuckDB Documentation](https://duckdb.org/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

---

## License

This project is created for educational purposes as part of the Data Engineering Zoomcamp 2026 program.

---

*Last Updated: April 15, 2026*
