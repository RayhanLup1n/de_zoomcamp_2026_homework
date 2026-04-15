"""
NYC Taxi Ingestion Main Script

This script runs the dlt pipeline to ingest NYC taxi data
into DuckDB database.
"""

import os
import logging
import dlt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import source
from ingestion.source import nyc_taxi_source


def get_env_list(env_var, default=None):
    """Parse environment variable into list."""
    if env_var not in os.environ:
        return default if default is not None else []

    value = os.environ[env_var]
    return [item.strip() for item in value.split(",")]


def main():
    """Main entry point for ingestion pipeline."""
    # Get configuration from environment
    duckdb_path = os.environ.get("DUCKDB_PATH", "./data/capstone.duckdb")
    project_id = os.environ.get("GCP_PROJECT_ID")
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    # Check both potential variables for credential path
    credentials_path = os.environ.get("LOCAL_GCP_CREDENTIALS") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    # Determine destination
    logger.debug(f"Checking for GCP config: Project={project_id}, Path={credentials_path}")
    if project_id and credentials_path and os.path.exists(credentials_path):
        logger.info("Destination set to BIGQUERY (using Project: %s)", project_id)
        
        # Load credentials from JSON file explicitly
        import json
        with open(credentials_path, 'r') as f:
            credentials_dict = json.load(f)
            
        destination = dlt.destinations.bigquery(
            credentials=credentials_dict,
            location="US"
        )
        # Use GCS as staging for faster loads to BigQuery
        if bucket_name:
            staging = dlt.destinations.filesystem(
                f"gs://{bucket_name}",
                credentials=credentials_dict
            )
            logger.info("Using GCS STAGING: gs://%s", bucket_name)
        else:
            staging = None
            logger.warning("No GCS_BUCKET_NAME found. Using direct BigQuery load (slower).")
    else:
        logger.info("Destination set to DUCKDB")
        destination = dlt.destinations.duckdb(credentials=duckdb_path)
        staging = None

    # Convert string years to integers
    years_str = os.environ.get("YEARS", "2024")
    years = [int(y.strip()) for y in years_str.split(",")]

    taxi_types = get_env_list("TAXI_TYPES", ["green"])

    logger.info("=" * 60)
    logger.info("NYC Taxi Ingestion Pipeline")
    logger.info("=" * 60)
    logger.info("Years: %s", years)
    logger.info("Taxi Types: %s", taxi_types)

    source = nyc_taxi_source(years=years, taxi_types=taxi_types)

    # Initialize dlt pipeline
    pipeline = dlt.pipeline(
        pipeline_name="nyc_taxi_ingestion",
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
    logger.info("")
    print("Success! Ingestion completed.")


if __name__ == "__main__":
    main()
