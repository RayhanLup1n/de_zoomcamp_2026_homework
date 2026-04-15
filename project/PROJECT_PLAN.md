# Data Engineering Capstone Project - 2026

> **Project Title:** NYC Taxi Analytics Dashboard
> **Author:** Rayhan Ananda
> **Deadline:** April 21, 2026
> **Start Date:** April 12, 2026
> **Status:** Planning Phase

---

## Executive Summary

This project builds an end-to-end data pipeline to analyze NYC taxi trips from 2024-2025, providing insights into ride patterns, payment trends, and spatial distribution across different boroughs. The pipeline processes multiple taxi types (Yellow & Green) across two years, transforming raw trip data into analytics-ready insights accessible via an interactive dashboard.

### Business Problem

NYC TLC (Taxi & Limousine Commission) generates massive amounts of trip data daily. Traditional analysis methods are time-consuming and don't provide real-time insights. This project aims to:

1. **Centralize Data:** Aggregate taxi data from multiple sources (Yellow & Green cabs)
2. **Automate Processing:** Build a repeatable pipeline for monthly data updates
3. **Enable Analytics:** Provide self-service analytics for:
   - Trip patterns by time of day, day of week, month
   - Payment method preferences
   - Fare trends over time
   - Geographic distribution across boroughs

### Target Audience

- NYC urban planners (for transportation planning)
- Taxi fleet managers (for demand forecasting)
- Data science teams (for ML model inputs)
- General public (via public dashboard)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA PIPELINE                                │
└─────────────────────────────────────────────────────────────────────┘

                            ┌──────────┐
                            │  Source  │
                            │          │
                            │ NYC TLC  │
                            │   GCS    │
                            └────┬─────┘
                                 │
                                 ↓
                    ┌────────────────────────┐
                    │      Ingestion          │
                    │                         │
                    │  dlt                   │
                    │  • Source definition   │
                    │  • Schema inference    │
                    │  • Incremental load   │
                    └──────┬─────────────────┘
                           │
                           ↓
                    ┌────────────────────────┐
                    │    Data Lake (Local)   │
                    │                         │
                    │  DuckDB                │
                    │  • raw.green_tripdata  │
                    │  • raw.yellow_tripdata │
                    └──────┬─────────────────┘
                           │
                           ↓
                    ┌────────────────────────┐
                    │   Orchestration         │
                    │                         │
                    │  Kestra                │
                    │  • Schedule triggers    │
                    │  • DAG execution        │
                    └──────┬─────────────────┘
                           │
                           ↓
                    ┌────────────────────────┐
                    │   Transformation        │
                    │                         │
                    │  dbt                   │
                    │  • staging layer       │
                    │  • marts layer         │
                    │  • data tests          │
                    └──────┬─────────────────┘
                           │
                           ↓
                    ┌────────────────────────┐
                    │   Data Warehouse       │
                    │                         │
                    │  DuckDB                │
                    │  • analytics.*         │
                    └──────┬─────────────────┘
                           │
                           ↓
                    ┌────────────────────────┐
                    │      Dashboard         │
                    │                         │
                    │  Streamlit             │
                    │  • Categorical charts  │
                    │  • Temporal analysis   │
                    │  • Filters             │
                    └────────────────────────┘
```

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Containerization** | Docker | Latest | Environment consistency |
| **Orchestration** | Docker Compose | 3.8+ | Multi-container deployment |
| **Ingestion** | dlt | 1.0+ | ETL pipeline, schema inference |
| **Data Lake** | DuckDB | Latest | Local OLAP database |
| **Orchestration** | Kestra | Latest | Workflow scheduling |
| **Transformation** | dbt | 1.7+ | SQL-based transformations |
| **Dashboard** | Streamlit | Latest | Interactive web dashboard |
| **Language** | Python | 3.11+ | Primary language |
| **Package Manager** | uv | Latest | Fast Python dependency manager |

### Why This Stack?

1. **Cost-Effective:** All tools have free tiers/local versions
2. **Learning-Aligned:** Matches tools from DE Zoomcamp
3. **Cloud-Ready:** Can deploy to GCP with minimal changes
4. **Developer-Friendly:** Python-first, great documentation
5. **Portable:** Docker makes it easy to share & reproduce

---

## Data Strategy

### Dataset Details

**Source:** NYC Taxi & Limousine Commission (TLC)
**URL:** `https://nyc-tlc.s3.amazonaws.com/trip/data/`
**Format:** Parquet (compressed columnar)
**Data Range:** January 2024 - December 2025 (24 months total)

### Data Sources

| Dataset | Description | Records/Month | Size/Month |
|---------|-------------|----------------|------------|
| `green_tripdata` | Green taxi (boroughs outside Manhattan) | ~1.5M | ~150MB |
| `yellow_tripdata` | Yellow taxi (Manhattan) | ~2.5M | ~250MB |

**Total Estimated Size:** ~9GB (24 months × 2 types × ~200MB avg)

### Data Schema

**Common Fields (both Green & Yellow):**

| Field | Type | Description |
|-------|------|-------------|
| `VendorID` | int | Vendor identifier |
| `lpep_pickup_datetime` / `tpep_pickup_datetime` | timestamp | Pickup time |
| `lpep_dropoff_datetime` / `tpep_dropoff_datetime` | timestamp | Dropoff time |
| `passenger_count` | int | Number of passengers |
| `trip_distance` | float | Trip distance in miles |
| `RatecodeID` | int | Rate code |
| `store_and_fwd_flag` | string | Store and forward flag |
| `PULocationID` | int | Pickup location ID |
| `DOLocationID` | int | Dropoff location ID |
| `payment_type` | int | Payment type (1=Credit, 2=Cash, etc.) |
| `fare_amount` | float | Base fare amount |
| `extra` | float | Extra charges |
| `mta_tax` | float | MTA tax |
| `tip_amount` | float | Tip amount |
| `tolls_amount` | float | Tolls amount |
| `improvement_surcharge` | float | Improvement surcharge |
| `total_amount` | float | Total amount charged |
| `congestion_surcharge` | float | Congestion surcharge |
| `Airport_fee` | float | Airport fee |

**Additional Lookup Data:**

- `taxi_zone_lookup.csv` - Maps LocationID to Zone, Borough, Service Zone

### Data Quality Considerations

**Known Issues:**
1. **Missing values:** Some trips have missing passenger counts
2. **Negative amounts:** Refunds may show negative values
3. **Outliers:** Very long trips (>4 hours) or very short trips (<1 minute)
4. **Future dates:** Some test data may have pickup after dropoff

**Handling Strategy:**
- Filter: `trip_distance > 0` and `trip_distance < 100`
- Filter: `duration > 60` and `duration < 14400` (1 min to 4 hours)
- Filter: `fare_amount >= 0`
- Filter: `passenger_count >= 0` and `passenger_count <= 10`

---

## Project Structure

```
builder_rayhanAnanda/
└── project/                          # Capstone project root
    ├── README.md                     # ⭐ Project overview (graded)
    ├── PROJECT_PLAN.md               # This file
    ├── .env.example                  # Environment template
    ├── docker-compose.yml            # ⭐ Single deployment command
    ├── docker/
    │   ├── Dockerfile.ingestion      # dlt container
    │   ├── Dockerfile.dbt            # dbt container
    │   └── Dockerfile.dashboard      # Streamlit container
    ├── ingestion/
    │   ├── __init__.py
    │   ├── source.py                 # dlt source definition
    │   ├── main.py                   # Ingestion entry point
    │   └── taxi_lookup.csv           # Zone lookup data
    ├── kestra/
    │   └── flows/
    │       └── main_flow.yml         # Orchestration flow
    ├── dbt/
    │   ├── dbt_project.yml           # dbt configuration
    │   ├── profiles.yml              # Database profiles
    │   ├── models/
    │   │   ├── staging/
    │   │   │   ├── stg_green_trips.sql
    │   │   │   └── stg_yellow_trips.sql
    │   │   ├── marts/
    │   │   │   ├── core/
    │   │   │   │   ├── dim_locations.sql
    │   │   │   │   ├── fct_trips.sql
    │   │   │   │   └── agg_trips_by_date.sql
    │   │   │   └── analytics/
    │   │   │       ├── trips_payment_type.sql
    │   │   │       ├── trips_by_hour.sql
    │   │   │       └── trips_by_month.sql
    │   │   └── tests/
    │   │       └── generic/
    │   │           └── data_quality.yml
    │   └── seeds/
    │       └── taxi_zone_lookup.csv
    ├── dashboard/
    │   ├── app.py                     # Streamlit main app
    │   ├── pages/
    │   │   ├── 1_Overview.py
    │   │   └── 2_Analytics.py
    │   └── utils.py                  # Utility functions
    ├── data/                         # Persistent data
    │   ├── capstone.duckdb            # Main database
    │   └── taxi_lookup.csv            # Zone lookup
    ├── scripts/
    │   ├── setup.sh                   # One-time setup
    │   ├── run.sh                     # Run pipeline
    │   ├── test.sh                    # Run tests
    │   └── clean.sh                   # Clean everything
    └── tests/
        ├── test_ingestion.py
        └── test_dashboard.py
```

---

## Pipeline Components

### 1. Ingestion (dlt)

**Purpose:** Extract taxi data from NYC TLC, normalize schema, load to DuckDB

**Configuration:**
```python
# ingestion/source.py
@dlt.source(name="nyc_taxi")
def nyc_taxi_source(years: List[int], taxi_types: List[str]):
    """Main source for NYC taxi data."""
    for year in years:
        for taxi_type in taxi_types:
            for month in range(1, 13):
                yield trips_resource(year, month, taxi_type)

@dlt.resource(write_disposition="append")
def trips_resource(year: int, month: int, taxi_type: str):
    """Load a single month of taxi data."""
    url = f"https://nyc-tlc.s3.amazonaws.com/trip/data/{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    return dlt.sources.filesystem.read_parquet(url)
```

**Data Flow:**
```
NYC TLC GCS → dlt → DuckDB.raw.green_tripdata
                  → DuckDB.raw.yellow_tripdata
```

**Quality Checks:**
- Schema inference from first record
- Column name normalization (snake_case)
- Type validation on load
- Row count reporting

---

### 2. Orchestration (Kestra)

**Purpose:** Schedule and coordinate pipeline execution

**Workflow:**
```yaml
# kestra/flows/main_flow.yml
id: nyc_taxi_pipeline
namespace: de_zoomcamp

tasks:
  - id: ingestion
    type: io.kestra.core.tasks.scripts.Bash
    commands:
      - cd /app/ingestion
      - python main.py

  - id: transformation
    type: io.kestra.core.tasks.scripts.Bash
    commands:
      - cd /app/dbt
      - dbt run

  - id: tests
    type: io.kestra.core.tasks.scripts.Bash
    commands:
      - cd /app/dbt
      - dbt test
```

**Triggers:**
- Manual trigger (for initial load)
- Monthly schedule (for updates)
- Data availability trigger (advanced, optional)

---

### 3. Transformation (dbt)

**Purpose:** Clean, standardize, and model data for analytics

**Layer Architecture:**

```
dbt/models/
├── staging/           # Raw data, cleaned & typed
│   ├── stg_green_trips.sql      # Green taxi staging
│   └── stg_yellow_trips.sql     # Yellow taxi staging
│
├── marts/
│   ├── core/                    # Reusable models
│   │   ├── dim_locations.sql     # Location dimension
│   │   ├── fct_trips.sql         # Trip fact table
│   │   └── agg_trips_by_date.sql # Aggregated by date
│   │
│   └── analytics/               # Dashboard-ready
│       ├── trips_payment_type.sql    # Payment type analysis
│       ├── trips_by_hour.sql          # Hourly patterns
│       └── trips_by_month.sql         # Monthly trends
```

**Staging Layer:**
- Standardize column names (Green vs Yellow have different prefixes)
- Add metadata (ingest_date, source_file)
- Filter invalid records
- Cast to appropriate types

**Core Layer:**
- Union Green & Yellow trips
- Add computed fields (duration, hour_of_day, day_of_week)
- Join with location lookup
- Create dimension tables

**Analytics Layer:**
- Pre-compute aggregations for dashboard
- Optimize for query performance
- Materialize as tables (not views)

---

### 4. Dashboard (Streamlit)

**Purpose:** Interactive analytics for stakeholders

**Pages:**

#### Page 1: Overview
- **Tile 1 (Categorical):** Payment Type Distribution
  - Bar chart showing % of trips by payment type
  - Filter: Year by Year comparison
  - Insight: Credit card adoption trends

- **Tile 2 (Temporal):** Trip Volume by Hour
  - Line chart showing trip patterns by hour of day
  - Heatmap: Hour × Day of Week
  - Insight: Rush hour patterns

#### Page 2: Analytics
- Fare trends over time
- Average trip duration by borough
- Top pickup/dropoff locations
- Monthly revenue comparison

**Features:**
- Date range picker
- Taxi type filter (Green/Yellow/Both)
- Borough filter
- Export to CSV

---

## Deployment Strategy

### Local Development

**Prerequisites:**
- Docker & Docker Compose
- Git

**Setup:**
```bash
cd builder_rayhanAnanda/project
./scripts/setup.sh          # Initialize containers
docker-compose up -d       # Start all services
```

**Access:**
- Kestra UI: http://localhost:8080
- Dashboard: http://localhost:8501

**Run Pipeline:**
```bash
# Via Kestra UI
# Or via script
./scripts/run.sh
```

**Stop:**
```bash
docker-compose down         # Stop services
docker-compose down -v      # Stop + remove volumes
```

### Production (Optional - GCP Free Tier)

**Services:**
- GCS Storage: Raw parquet files (5GB free)
- BigQuery: Data warehouse (1TB/month free queries)
- Cloud Run: Streamlit dashboard (2M requests/month free)

**Deployment:**
```bash
# Export DuckDB to Parquet
python scripts/export_to_gcs.py

# Create BigQuery resources
terraform apply

# Deploy dashboard
gcloud run deploy dashboard --source .
```

---

## Evaluation Criteria Mapping

| Criteria | Points | Implementation | Status |
|----------|--------|----------------|--------|
| Problem Description | 4 | Comprehensive README with business problem, architecture diagrams | ⏳ TBD |
| Cloud | 4 | Optional GCP deployment (Docker first for development) | ⚠️ Optional |
| Data Ingestion | 4 | dlt with Kestra orchestration, multi-source (Green + Yellow) | ⏳ TBD |
| Data Warehouse | 4 | DuckDB with proper schema (partitioning simulated with date fields) | ⏳ TBD |
| Transformations | 4 | dbt with staging → core → analytics layers | ⏳ TBD |
| Dashboard | 4 | Streamlit with 2 tiles (categorical + temporal) | ⏳ TBD |
| Reproducibility | 4 | Docker Compose, setup scripts, clear README | ⏳ TBD |

**Target Score:** 20/32 (minimum) to 28/32 (with cloud)

---

## Development Timeline (1-Day Sprint)

### Phase 1: Setup (30 min)
- [ ] Create project folder structure
- [ ] Initialize git repo
- [ ] Create docker-compose.yml skeleton
- [ ] Create PROJECT_PLAN.md (this file)

### Phase 2: Ingestion (60 min)
- [ ] Create dlt source for NYC taxi data
- [ ] Implement multi-source (Green + Yellow)
- [ ] Test with 1 month of data first
- [ ] Verify DuckDB schema

### Phase 3: Transformation (60 min)
- [ ] Setup dbt project
- [ ] Create staging models (stg_green_trips, stg_yellow_trips)
- [ ] Create core models (fct_trips, dim_locations)
- [ ] Create analytics models (for dashboard)
- [ ] Add data tests

### Phase 4: Dashboard (60 min)
- [ ] Create Streamlit app skeleton
- [ ] Implement Tile 1: Payment Type Distribution
- [ ] Implement Tile 2: Hourly Trip Patterns
- [ ] Add filters and interactivity
- [ ] Test with sample data

### Phase 5: Orchestration & Polish (45 min)
- [ ] Create Kestra flow
- [ ] Setup docker-compose integration
- [ ] Write README.md
- [ ] Write setup.sh and run.sh scripts
- [ ] End-to-end test

### Phase 6: Documentation (15 min)
- [ ] Update README with screenshots
- [ ] Document API endpoints
- [ ] Add troubleshooting section

**Total:** 5 hours

---

## Cloud Cost Estimation

### Local Development (Free)
- Docker: Free
- DuckDB: Free (single file)
- All tools: Open source

### Production (GCP Free Tier)
| Service | Usage | Cost (Free Tier) |
|---------|-------|------------------|
| GCS Storage | 9GB data | $0 (5GB free) |
| BigQuery Storage | 5GB | $0 (10GB free) |
| BigQuery Queries | 100GB/month | $0 (1TB free) |
| Cloud Run | Dashboard | $0 (2M requests free) |
| **Total** | | **$0 (within free tier)** |

**Note:** First 12 months GCP has generous free tier. After that, estimated monthly cost: ~$2-5 (light usage)

---

## Next Steps

1. **Approval:** Review this plan and confirm approach
2. **Implementation:** Execute timeline phases sequentially
3. **Testing:** Validate each component before moving to next
4. **Documentation:** Update docs as features are implemented

---

## References

### Dataset Documentation
- [NYC TLC Trip Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Taxi Zone Lookup](https://www.nyc.gov/site/tlc/about/taxi-zone-info.page)

### Tool Documentation
- [dlt Documentation](https://dlthub.com/docs)
- [dbt Documentation](https://docs.getdbt.com)
- [Kestra Documentation](https://kestra.io/docs)
- [DuckDB Documentation](https://duckdb.org/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

### Inspiration Projects
- [NYC Taxi Analysis Examples](https://github.com/topics/nyc-taxi)
- [DE Zoomcamp 2023 Projects](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/projects/cohorts/2023/project.md)

---

## Appendix

### A. Payment Type Codes
| Code | Type | Description |
|------|------|-------------|
| 1 | Credit card | Payment via credit card |
| 2 | Cash | Cash payment |
| 3 | No charge | No charge (dispute) |
| 4 | Dispute | Disputed charge |
| 5 | Unknown | Unknown payment type |
| 6 | Voided | Voided trip |

### B. Rate Code IDs
| Code | Description |
|------|-------------|
| 1 | Standard rate |
| 2 | JFK |
| 3 | Newark |
| 4 | Nassau/Westchester |
| 5 | Negotiated fare |
| 6 | Group ride |

### C. SQL Queries Reference

**Total trips by year:**
```sql
SELECT
    EXTRACT(YEAR FROM pickup_datetime) AS year,
    COUNT(*) AS trip_count
FROM analytics.fct_trips
GROUP BY year
ORDER BY year;
```

**Payment type distribution:**
```sql
SELECT
    payment_type_name,
    COUNT(*) AS trip_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage
FROM analytics.fct_trips
WHERE pickup_datetime BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY payment_type_name
ORDER BY trip_count DESC;
```

**Hourly patterns:**
```sql
SELECT
    EXTRACT(HOUR FROM pickup_datetime) AS hour_of_day,
    COUNT(*) AS trip_count
FROM analytics.fct_trips
WHERE pickup_datetime BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY hour_of_day
ORDER BY hour_of_day;
```

---

*Document Version: 1.0*
*Last Updated: April 12, 2026*
