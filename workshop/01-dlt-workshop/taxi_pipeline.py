import dlt
import requests
import duckdb


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
    # Load data from the source
    load_info = pipeline.run(nyc_taxi_source())

    print("\nLoad completed!")
    print(load_info)

    # Print summary
    print("\n" + "="*50)
    print("Pipeline Summary")
    print("="*50)

    # Query DuckDB for summary using the correct database file
    con = duckdb.connect("taxi_pipeline.duckdb")

    # Check tables
    tables = con.execute("SHOW TABLES").fetchall()
    print(f"\nTables created: {[t[0] for t in tables]}")

    # Get row count
    count = con.execute("SELECT COUNT(*) FROM nyc_taxi.trips").fetchone()[0]
    print(f"Total records loaded: {count}")

    # Get date range (dlt converts to snake_case)
    date_range = con.execute("""
        SELECT
            MIN(trip_pickup_date_time) as min_date,
            MAX(trip_pickup_date_time) as max_date
        FROM nyc_taxi.trips
    """).fetchone()
    print(f"Date range: {date_range[0]} to {date_range[1]}")
