"""
Indonesia Weather Ingestion Main Script

Runs the dlt pipeline to ingest weather data from Open-Meteo API
into DuckDB (local) or BigQuery (cloud).

Usage:
    python -m ingestion.main

Environment Variables:
    DUCKDB_PATH          - Path to DuckDB file (default: ./data/capstone.duckdb)
    START_DATE           - Start date for data fetch (default: 2020-01-01)
    END_DATE             - End date for data fetch (default: 2025-12-31)
    GCP_PROJECT_ID       - GCP project ID (enables BigQuery mode)
    GCS_BUCKET_NAME      - GCS bucket for staging (optional, speeds up BigQuery loads)
    GOOGLE_APPLICATION_CREDENTIALS - Path to GCP service account JSON
"""

import os
import logging
import dlt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Import source
from ingestion.source import weather_source


def main():
    """Main entry point for ingestion pipeline."""
    # Configuration from environment
    duckdb_path = os.environ.get("DUCKDB_PATH", "./data/capstone.duckdb")
    project_id = os.environ.get("GCP_PROJECT_ID")
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    start_date = os.environ.get("START_DATE", "2020-01-01")
    end_date = os.environ.get("END_DATE", "2025-12-31")

    # Determine destination: BigQuery (cloud) or DuckDB (local)
    if project_id and credentials_path and os.path.exists(credentials_path):
        logger.info("Destination: BIGQUERY (Project: %s)", project_id)

        import json

        with open(credentials_path, "r") as f:
            credentials_dict = json.load(f)

        destination = dlt.destinations.bigquery(
            credentials=credentials_dict,
            location="US",
        )

        # Use GCS staging for faster BigQuery loads
        if bucket_name:
            staging = dlt.destinations.filesystem(
                f"gs://{bucket_name}",
                credentials=credentials_dict,
            )
            logger.info("Staging: GCS gs://%s", bucket_name)
        else:
            staging = None
            logger.warning("No GCS_BUCKET_NAME set. Using direct BigQuery load.")
    else:
        logger.info("Destination: DUCKDB (%s)", duckdb_path)

        # Ensure data directory exists
        os.makedirs(os.path.dirname(duckdb_path) or ".", exist_ok=True)

        destination = dlt.destinations.duckdb(credentials=duckdb_path)
        staging = None

    logger.info("=" * 60)
    logger.info("Indonesia Weather Ingestion Pipeline")
    logger.info("=" * 60)
    logger.info("Date range: %s to %s", start_date, end_date)
    logger.info("Cities: Jakarta, Surabaya, Denpasar, Medan, Makassar")

    # Create source
    source = weather_source(start_date=start_date, end_date=end_date)

    # Initialize dlt pipeline
    pipeline = dlt.pipeline(
        pipeline_name="indonesia_weather",
        destination=destination,
        staging=staging,
        dataset_name="raw",
    )

    logger.info("")
    logger.info("Starting ingestion...")
    logger.info("")

    # Run pipeline
    load_info = pipeline.run(source)

    logger.info("")
    logger.info("=" * 60)
    logger.info("Ingestion Complete!")
    logger.info("=" * 60)
    logger.info(str(load_info))
    print("Success! Ingestion completed.")


if __name__ == "__main__":
    main()
