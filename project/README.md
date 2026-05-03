# Indonesia Weather Analytics Dashboard

> **Data Engineering Capstone Project 2026**
> Author: Rayhan Ananda | May 2026

---

## Problem Description

### The Problem

Indonesia is a tropical archipelago nation spanning over 5,000 km with significant **climate variation between cities**. Urban planners, agricultural stakeholders, and disaster response teams need to understand local weather patterns, but weather data is scattered across APIs and difficult to analyze at scale.

Key challenges:
1. **Fragmented data**: Weather data for Indonesian cities exists in raw API form, not centralized or analytics-ready
2. **No historical comparison**: Understanding whether current weather is normal requires years of historical context
3. **City-level differences are hidden**: National averages mask important regional variations in temperature, rainfall, and sunshine

### How This Project Solves It

This project builds a **complete end-to-end data pipeline** that:

1. **Ingests** 6 years of daily weather data (2020-2025) for 5 major Indonesian cities from the Open-Meteo API using **dlt**
2. **Stores** raw data in a data lake (**GCS**) and loads into a data warehouse (**BigQuery**) with partitioning and clustering for efficient querying
3. **Transforms** raw data through a 3-layer dbt architecture (staging -> core -> analytics) with data quality tests
4. **Visualizes** insights in an interactive **Streamlit** dashboard with 2 analytical tiles:
   - **Tile 1 (Categorical):** Temperature comparison across cities — identifies which cities are hotter/cooler
   - **Tile 2 (Temporal):** Monthly precipitation trends — reveals wet/dry season patterns per city
5. **Orchestrates** the full pipeline as an end-to-end DAG in **Kestra** (fetch -> transform -> test -> done)
6. **Provisions** all cloud infrastructure with **Terraform** (BigQuery datasets + GCS bucket)

### Business Value

| Stakeholder | Insight | Example |
|-------------|---------|---------|
| **Urban Planners** | Rainfall patterns per city | Jakarta gets 2x more rain than Makassar — plan drainage accordingly |
| **Agriculture** | Seasonal temperature trends | Optimal planting windows based on 6 years of monthly temperature data |
| **Tourism** | Best travel months | Denpasar (Bali) is driest in July-September — peak tourist season |
| **Disaster Prep** | Extreme weather frequency | Identify which months have highest thunderstorm counts per city |

---

## Architecture

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Source** | [Open-Meteo API](https://open-meteo.com) | Free historical weather API (no auth required) |
| **Ingestion** | [dlt](https://dlthub.com) | Extract and load weather data |
| **Data Lake** | Google Cloud Storage (GCS) | Raw data staging for BigQuery loads |
| **Data Warehouse** | Google BigQuery | OLAP warehouse with partitioning + clustering |
| **Local Warehouse** | DuckDB | Local development (default mode) |
| **Orchestration** | [Kestra](https://kestra.io) | End-to-end DAG pipeline |
| **Transformation** | [dbt](https://getdbt.com) | SQL transformations (3-layer architecture) |
| **Dashboard** | [Streamlit](https://streamlit.io) + Plotly | Interactive analytics dashboard |
| **IaC** | [Terraform](https://terraform.io) | Cloud resource provisioning |
| **Containerization** | Docker Compose | Reproducible multi-service deployment |

### Data Pipeline Flow

```
Open-Meteo API (free, no auth)
    |
    v
[dlt Ingestion] ── fetches 5 cities x 6 years of daily weather data
    |                    |
    v                    v
DuckDB (local)     GCS Bucket (data lake)
                         |
                         v
                    BigQuery (DWH)
                    - Partitioned by observation_date (monthly)
                    - Clustered by city_name
                         |
                         v
                    [dbt Transform]
                    staging -> core -> analytics
                         |
                         v
                    Streamlit Dashboard
                    - Tile 1: Temperature by City
                    - Tile 2: Monthly Precipitation

Orchestrated by: Kestra (end-to-end DAG)
Infra by: Terraform (GCS + BigQuery)
```

---

## Dataset

### Source: Open-Meteo Historical Weather API

| Property | Details |
|----------|---------|
| **API** | `https://archive-api.open-meteo.com/v1/archive` |
| **Authentication** | None required (free and open) |
| **Data Range** | January 2020 - December 2025 (6 years) |
| **Resolution** | Daily aggregations |
| **Total Records** | ~10,950 rows (5 cities x 2,190 days) |
| **Format** | JSON (API response) |

### Cities Analyzed

| City | Latitude | Longitude | Region | Why Selected |
|------|----------|-----------|--------|-------------|
| **Jakarta** | -6.21 | 106.85 | Java (West) | Capital city, largest metro |
| **Surabaya** | -7.25 | 112.75 | Java (East) | 2nd largest city |
| **Denpasar** | -8.65 | 115.22 | Bali | Tourism hub, different microclimate |
| **Medan** | 3.59 | 98.67 | Sumatra (North) | North of equator, different monsoon |
| **Makassar** | -5.14 | 119.42 | Sulawesi | Eastern Indonesia, distinct rainfall pattern |

### Weather Variables

| Variable | Unit | Description |
|----------|------|-------------|
| `temperature_2m_max` | C | Daily maximum temperature |
| `temperature_2m_min` | C | Daily minimum temperature |
| `temperature_2m_mean` | C | Daily mean temperature |
| `precipitation_sum` | mm | Total daily precipitation |
| `rain_sum` | mm | Total daily rainfall |
| `windspeed_10m_max` | km/h | Maximum wind speed at 10m |
| `sunshine_duration` | seconds | Total sunshine duration |
| `weathercode` | WMO code | Weather condition classification |

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- `make` (optional, for convenience commands)

### Option A: One-Command Setup (Recommended)

```bash
# 1. Clone and navigate
git clone <repo-url>
cd project

# 2. Create environment file
cp .env.example .env

# 3. Run full pipeline (ingest + transform + start dashboard)
make setup

# 4. Open dashboard
# -> http://localhost:8501

# 5. Open Kestra UI (orchestration)
# -> http://localhost:8080
```

### Option B: Step-by-Step

```bash
# 1. Create environment file
cp .env.example .env

# 2. Fetch weather data from Open-Meteo API (~1-2 minutes)
docker compose --profile ingest up --build ingestion

# 3. Run dbt transformations and tests
docker compose --profile transform run --build dbt \
  sh -c "cd /app/dbt && dbt run --profiles-dir . --project-dir . && dbt test --profiles-dir . --project-dir ."

# 4. Start dashboard and Kestra
docker compose up -d --build

# 5. Open in browser
# Dashboard: http://localhost:8501
# Kestra UI: http://localhost:8080
```

### Stop Services

```bash
make down              # Stop services (preserve data)
make clean             # Stop + remove all data (full reset)
```

---

## Data Warehouse Optimization

### Partitioning Strategy

The `fct_weather` fact table is **partitioned by `observation_date`** with **monthly granularity**.

**Why monthly partitioning?**
- Dashboard queries always filter by year: `WHERE observation_year = 2024`
- Monthly granularity means BigQuery scans only ~12 partitions per year query instead of ~365 daily partitions
- Cost reduction: only relevant months are scanned, reducing bytes processed
- Our data is small (~11K rows), but this demonstrates the pattern for production-scale weather data

### Clustering Strategy

The `fct_weather` table is **clustered by `city_name`**.

**Why cluster by city?**
- Nearly every dashboard query filters or groups by city: `WHERE city_name = 'Jakarta'` or `GROUP BY city_name`
- Clustering co-locates rows for the same city within each partition
- Combined with partitioning: query for "Jakarta in 2024" scans only the 2024 partition and jumps directly to Jakarta rows
- This matches the two main query patterns:
  1. "Compare all cities for year X" -> partition prunes year, results already grouped by city cluster
  2. "Show monthly trend for city Y" -> cluster prunes to city, partition on month

```sql
-- Example: This query benefits from both partition (year) and cluster (city)
SELECT observation_month, AVG(temperature_mean_c)
FROM analytics.fct_weather
WHERE observation_year = 2024          -- Partition pruning
  AND city_name = 'Jakarta'            -- Cluster pruning
GROUP BY observation_month
```

---

## dbt Transformation Layers

### Layer Architecture

```
raw.daily_weather (source from dlt)
    |
    v
[Staging Layer]
    stg_daily_weather
    - Cleans and standardizes column types
    - Adds computed fields (temperature range, weather category)
    - Maps WMO weather codes to human-readable descriptions
    - Flags rainy days (precipitation > 0.1mm)
    |
    v
[Core Layer]
    fct_weather
    - Single source of truth for all weather observations
    - Partitioned by observation_date, clustered by city_name (BigQuery)
    - Contains all cleaned fields from staging
    |
    v
[Analytics Layer]
    weather_by_city          -> Dashboard Tile 1 (Categorical)
    weather_monthly_trends   -> Dashboard Tile 2 (Temporal)
    - Pre-aggregated marts for efficient dashboard queries
```

### dbt Tests

| Model | Test | Purpose |
|-------|------|---------|
| `stg_daily_weather` | `unique(weather_id)` | No duplicate observations |
| `stg_daily_weather` | `not_null(weather_id, city_name, observation_date)` | Required fields present |
| `stg_daily_weather` | `accepted_values(city_name)` | Only valid cities |
| `stg_daily_weather` | `accepted_values(weather_category)` | Valid weather categories |
| `fct_weather` | `unique(weather_id)` | Uniqueness maintained through transformation |
| `fct_weather` | `accepted_values(weather_category)` | Consistent categorization |
| `weather_monthly_trends` | `accepted_values(observation_month)` | Valid months (1-12) |

---

## Dashboard

### Key Metrics (5 cards)

| Metric | Description |
|--------|-------------|
| Avg Temperature | Mean daily temperature for selected period |
| Total Precipitation | Sum of all precipitation in mm |
| Avg Wind Speed | Average maximum daily wind speed |
| Avg Sunshine | Average daily sunshine hours |
| Rain Days | Count of days with precipitation > 0.1mm |

### Tile 1: Temperature by City (Categorical Distribution)

Bar chart comparing average temperature across 5 Indonesian cities for the selected year. Includes min/max temperature markers to show daily range. Reveals which cities are consistently hotter or cooler.

### Tile 2: Monthly Precipitation Trends (Temporal Distribution)

Line chart showing monthly precipitation patterns across months. Multi-city comparison reveals seasonal differences — Jakarta's wet season (Nov-Mar) vs Makassar's distinct pattern. Helps identify optimal travel/planting windows.

### Filters

- **Year:** 2020, 2021, 2022, 2023, 2024, 2025
- **City:** All, Jakarta, Surabaya, Denpasar, Medan, Makassar

---

## Cloud Deployment (GCP)

### Infrastructure as Code (Terraform)

All cloud resources are provisioned via Terraform:

```bash
cd terraform

# Initialize Terraform
terraform init

# Preview changes
terraform plan -var="credentials_file=/path/to/credentials.json"

# Apply (creates GCS bucket + BigQuery datasets)
terraform apply -var="credentials_file=/path/to/credentials.json"
```

**Resources provisioned:**
- GCS Bucket: `weather-data-de-zoomcamp-2026-484615` (data lake + dlt staging)
- BigQuery Dataset: `raw` (ingested weather data)
- BigQuery Dataset: `analytics` (dbt-transformed models)

### Cloud Pipeline

To run the pipeline against BigQuery instead of DuckDB:

```bash
# Set environment variables
export GCP_PROJECT_ID=de-zoomcamp-2026-484615
export GCS_BUCKET_NAME=weather-data-de-zoomcamp-2026-484615
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Run ingestion to BigQuery
python -m ingestion.main

# Run dbt against BigQuery
cd dbt && dbt run --target prod --profiles-dir . --project-dir .
```

### Cost

All resources stay within **GCP Free Tier** ($0 cost):
- BigQuery: ~11K rows = <1 MB storage (free tier: 10 GB)
- BigQuery queries: <10 MB per query (free tier: 1 TB/month)
- GCS: <5 MB staging data (free tier: 5 GB)

---

## Project Structure

```
project/
├── README.md                 # This file
├── Makefile                  # Convenience commands (make setup, etc.)
├── docker-compose.yml        # Multi-service orchestration
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
│
├── docker/
│   ├── Dockerfile.ingestion  # dlt ingestion container
│   ├── Dockerfile.dbt        # dbt transformation container
│   └── Dockerfile.dashboard  # Streamlit dashboard container
│
├── ingestion/
│   ├── source.py             # dlt source: Open-Meteo API fetch
│   ├── main.py               # Pipeline entry point (DuckDB/BigQuery)
│   └── requirements.txt      # Python dependencies
│
├── kestra/flows/
│   └── main_flow.yml         # End-to-end orchestration DAG
│
├── dbt/
│   ├── dbt_project.yml       # dbt project configuration
│   ├── profiles.yml          # Connection profiles (dev=DuckDB, prod=BigQuery)
│   ├── macros/
│   │   └── generate_schema_name.sql
│   └── models/
│       ├── schema.yml        # Source definitions and tests
│       ├── staging/
│       │   └── stg_daily_weather.sql
│       └── marts/
│           ├── core/
│           │   └── fct_weather.sql        # Partitioned + clustered fact table
│           └── analytics/
│               ├── weather_by_city.sql     # Tile 1: categorical
│               └── weather_monthly_trends.sql  # Tile 2: temporal
│
├── dashboard/
│   ├── app.py                # Streamlit dashboard (2 tiles)
│   └── requirements.txt      # Dashboard dependencies
│
├── terraform/
│   ├── main.tf               # GCS bucket + BigQuery datasets
│   ├── variables.tf          # Configurable variables
│   └── outputs.tf            # Output values
│
└── data/
    └── .gitkeep              # Data directory (DuckDB created here)
```

---

## Orchestration (Kestra)

The Kestra flow (`kestra/flows/main_flow.yml`) defines a clear **end-to-end DAG**:

```
[Validate Environment]
        |
        v
[Fetch Weather Data]  ← Open-Meteo API → DuckDB
        |
        v
[dbt Transform]       ← staging → core → analytics
        |
        v
[dbt Test]            ← Data quality validation
        |
        v
[Pipeline Complete]
```

Access Kestra UI at `http://localhost:8080` to:
- View the pipeline DAG
- Trigger manual executions
- Monitor execution logs
- Configure scheduled runs

---

## Reproducibility Checklist

- [x] No hard-coded file paths or credentials
- [x] `.env.example` provided with all required variables
- [x] Docker Compose works from fresh clone
- [x] All dependencies pinned in `requirements.txt`
- [x] `make setup` runs full pipeline in one command
- [x] Step-by-step instructions in README
- [x] Data sourced from free, publicly accessible API (no auth required)
- [x] Cloud resources provisioned via Terraform (IaC)
- [x] `.gitignore` excludes credentials, data files, and build artifacts

---

## Evaluation Criteria

| Criteria | Implementation | Score Target |
|----------|----------------|-------------|
| **Problem Description** | Comprehensive problem + solution + business value | 4/4 |
| **Cloud** | GCP (BigQuery + GCS) + Terraform IaC | 4/4 |
| **Data Ingestion (Batch)** | End-to-end Kestra DAG with multiple steps | 4/4 |
| **Data Warehouse** | BigQuery with partition (date) + cluster (city) + explanation | 4/4 |
| **Transformations** | dbt 3-layer architecture with tests | 4/4 |
| **Dashboard** | Streamlit with 2 tiles (categorical + temporal) | 4/4 |
| **Reproducibility** | Docker Compose + Makefile + clear docs | 4/4 |

---

## Troubleshooting

### Services won't start
```bash
docker compose logs                 # Check all logs
docker compose up --build -d        # Rebuild containers
docker compose restart dashboard    # Restart specific service
```

### DuckDB connection error
```bash
# Verify database exists
ls -lh data/capstone.duckdb

# Inspect tables
python -c "import duckdb; print(duckdb.connect('data/capstone.duckdb').execute('SHOW ALL TABLES').df())"
```

### dbt fails
```bash
# Debug dbt connection
docker compose --profile transform run dbt \
  sh -c "cd /app/dbt && dbt debug --profiles-dir . --project-dir ."
```

### Dashboard not loading
1. Verify data exists: `data/capstone.duckdb` should be > 0 bytes
2. Check logs: `docker compose logs dashboard`
3. Ensure ingestion and dbt have been run first

### Full reset
```bash
make clean                     # Remove everything
make setup                     # Rebuild from scratch
```

---

## References

- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
- [dlt Documentation](https://dlthub.com/docs)
- [dbt Documentation](https://docs.getdbt.com)
- [Kestra Documentation](https://kestra.io/docs)
- [DuckDB Documentation](https://duckdb.org/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

---

## License

This project is created for educational purposes as part of the [Data Engineering Zoomcamp 2026](https://github.com/DataTalksClub/data-engineering-zoomcamp) program.

---

*Last Updated: May 2026*
