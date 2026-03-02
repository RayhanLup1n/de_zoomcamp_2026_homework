# Workshop: DLT (Data Loading Tool) - Homework

## Overview

This workshop covers building a data ingestion pipeline using **dlt (Data Loading Tool)** with AI assistance. dlt is a Python library for loading data from various sources (APIs, databases, files) to destinations (DuckDB, BigQuery, Postgres, etc.) with minimal code.

**Key Concepts Learned:**
- REST API data source with pagination
- dlt source and resource decorators
- Loading data to DuckDB
- Inspecting data using dlt Dashboard and DuckDB queries

## Pipeline Implementation

### taxi_pipeline.py

```python
import dlt
import requests


@dlt.source(name="nyc_taxi")
def nyc_taxi_source():
    """NYC Taxi data source from the API."""
    return trips


@dlt.resource(write_disposition="replace")
def trips():
    """Fetch all trips from the NYC Taxi API with pagination."""
    base_url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    page = 1

    while True:
        response = requests.get(f"{base_url}?page={page}")
        data = response.json()

        # Stop when empty page is returned
        if not data:
            break

        print(f"Fetched page {page}: {len(data)} records")
        yield data

        page += 1


# Create the pipeline
pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="nyc_taxi",
)


if __name__ == "__main__":
    load_info = pipeline.run(nyc_taxi_source())
    print("Load completed!", load_info)
```

### How to Run

```bash
# Install dependencies
uv pip install "dlt[duckdb]"

# Run the pipeline
uv run python taxi_pipeline.py

# View pipeline dashboard
dlt pipeline taxi_pipeline show
```

## Answer Summary

| No | Question | Answer | File |
|----|----------|--------|------|
| 1 | Start and end date of dataset | 2009-06-01 to 2009-07-01 | [answer_question_1.md](answer_question_1.md) |
| 2 | Proportion of credit card payments | 26.66% | [answer_question_2.md](answer_question_2.md) |
| 3 | Total tips generated | $6,063.41 | [answer_question_3.md](answer_question_3.md) |

## Dataset Statistics

| Property | Value |
|----------|-------|
| Total Records | 10,000 trips |
| Date Range | 2009-06-01 to 2009-07-01 |
| Payment Distribution | CASH (72.35%), Credit (26.66%), Other (1%) |
| Total Tips | $6,063.41 |
| Database File | `taxi_pipeline.duckdb` |

## Resources

| Resource | Link |
|----------|------|
| Submit Homework | [courses.datatalks.club](https://courses.datatalks.club/de-zoomcamp-2026/homework/dlt) |
| Workshop README | [cohorts/2026/workshops/dlt](../../../data-engineering-zoomcamp/cohorts/2026/workshops/dlt) |
| dlt Documentation | [dlthub.com/docs](https://dlthub.com/docs) |
| dlt Dashboard Guide | [dlthub.com/docs/dashboard](https://dlthub.com/docs/general-usage/dashboard) |
