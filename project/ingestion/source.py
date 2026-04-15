"""
NYC Taxi Data Source for dlt

All taxi trip data (green & yellow, all months/years) is loaded into
a SINGLE table called `trips_resource` in the `raw` schema.
Metadata columns (_ingest_year, _ingest_month, _ingest_taxi_type)
allow downstream dbt models to filter by taxi type and time period.

Performance: yields pyarrow Tables directly instead of per-row dicts.
This lets dlt skip the slow normalize phase and load data much faster.
"""

import dlt
import logging
import os

logger = logging.getLogger(__name__)

# Fix for pyarrow timezone issues on Windows (only if running locally on Windows)
if os.name == 'nt':
    try:
        import tzdata
        import pyarrow as pa
        # Arrow on Windows looks for tzdata. We'll try to let it find it naturally first
        # or skip if it causes OSError
        os.environ['PYARROW_IGNORE_TZDATA_PATH'] = '0'
    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"PyArrow TZ initialization warning: {e}")

# Base URL for NYC taxi trip data (Parquet format)
NYC_TLC_BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"


@dlt.source(name="nyc_taxi")
def nyc_taxi_source(years=None, taxi_types=None):
    """NYC Taxi data source.

    Yields a single resource that contains ALL trip data.
    Each row is tagged with metadata for filtering.
    """
    if years is None:
        years = [2024]
    if taxi_types is None:
        taxi_types = ["green"]

    yield trips_resource(years=years, taxi_types=taxi_types)


@dlt.resource(
    name="trips_resource",
    write_disposition="append",
)
def trips_resource(years, taxi_types):
    """Load all taxi trip data into a single resource.

    Iterates over all year/month/taxi_type combinations and yields
    pyarrow Tables directly. This is MUCH faster than per-row yield
    because dlt can skip the normalize phase entirely.
    """
    import requests
    import io
    import pyarrow as pa
    import pyarrow.parquet as pq

    for year in years:
        for taxi_type in taxi_types:
            for month in range(1, 13):  # Full year: 12 months
                filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
                url = f"{NYC_TLC_BASE_URL}/{filename}"

                try:
                    logger.info(f"Downloading {filename}...")
                    response = requests.get(url, stream=True, timeout=120)
                    response.raise_for_status()

                    # Read parquet from bytes
                    buffer = io.BytesIO(response.content)
                    table = pq.read_table(buffer)

                    num_rows = table.num_rows

                    # Add metadata columns as new arrow columns
                    table = table.append_column(
                        "_ingest_year",
                        pa.array([year] * num_rows, type=pa.int32())
                    )
                    table = table.append_column(
                        "_ingest_month",
                        pa.array([month] * num_rows, type=pa.int32())
                    )
                    table = table.append_column(
                        "_ingest_taxi_type",
                        pa.array([taxi_type] * num_rows, type=pa.string())
                    )
                    table = table.append_column(
                        "_ingest_file",
                        pa.array([filename] * num_rows, type=pa.string())
                    )

                    # Yield the entire pyarrow Table at once
                    # dlt handles arrow tables natively — no normalize needed
                    yield table

                    logger.info(f"Loaded {num_rows:,} rows from {filename}")

                except requests.exceptions.HTTPError as e:
                    # Some months may not exist yet (e.g., future months)
                    if e.response.status_code == 404:
                        logger.warning(f"File not found (skipping): {filename}")
                    else:
                        logger.error(f"HTTP error for {filename}: {e}")
                except Exception as e:
                    logger.warning(f"Could not load {filename}: {e}")
