"""
Incremental Data Loader - Load NYC Taxi Data in Batches

Solves the OOM issue by loading data one taxi_type + year at a time.
Run this script locally (not in Docker) since DuckDB is file-based.

Usage:
    python scripts/incremental_load.py                    # Load all missing data
    python scripts/incremental_load.py --type yellow --year 2024  # Load specific batch
    python scripts/incremental_load.py --status            # Check what's loaded
"""

import os
import sys
import argparse
import logging

# Add project root to path so we can import ingestion module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import duckdb

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUCKDB_PATH = os.path.join(PROJECT_ROOT, "data", "capstone.duckdb")

# Full data matrix we want loaded
ALL_YEARS = [2024, 2025]
ALL_TAXI_TYPES = ["green", "yellow"]


def check_loaded_data():
    """Check which taxi_type + year combos are already in DuckDB."""
    if not os.path.exists(DUCKDB_PATH):
        logger.info("DuckDB file not found. No data loaded yet.")
        return set()

    con = duckdb.connect(DUCKDB_PATH, read_only=True)
    try:
        result = con.execute("""
            SELECT
                _ingest_taxi_type,
                _ingest_year,
                COUNT(DISTINCT _ingest_month) as months,
                COUNT(*) as total_rows
            FROM raw.trips_resource
            GROUP BY 1, 2
            ORDER BY 1, 2
        """).fetchall()

        loaded = set()
        print("\n" + "=" * 65)
        print("  CURRENT DATA STATUS")
        print("=" * 65)
        print(f"  {'Taxi Type':<12} {'Year':<8} {'Months':<10} {'Rows':>12}")
        print("-" * 65)

        for row in result:
            taxi_type, year, months, rows = row
            loaded.add((taxi_type, year))
            status = "COMPLETE" if months == 12 else f"PARTIAL ({months}/12)"
            print(f"  {taxi_type:<12} {year:<8} {status:<10} {rows:>12,}")

        # Show what's missing
        print("-" * 65)
        missing = []
        for taxi_type in ALL_TAXI_TYPES:
            for year in ALL_YEARS:
                if (taxi_type, year) not in loaded:
                    missing.append((taxi_type, year))
                    print(f"  {taxi_type:<12} {year:<8} {'MISSING':<10} {'---':>12}")

        total = con.execute("SELECT COUNT(*) FROM raw.trips_resource").fetchone()[0]
        print("-" * 65)
        print(f"  {'TOTAL':<12} {'':<8} {'':<10} {total:>12,}")
        print("=" * 65)

        if missing:
            print(f"\n  Missing batches: {len(missing)}")
            for t, y in missing:
                print(f"    - {t} {y}")
        else:
            print("\n  All data loaded!")

        print()
        return loaded

    finally:
        con.close()


def load_batch(taxi_type, year):
    """Load a single taxi_type + year batch into DuckDB via dlt."""
    import dlt
    from ingestion.source import nyc_taxi_source

    logger.info("=" * 60)
    logger.info(f"Loading batch: {taxi_type} {year}")
    logger.info("=" * 60)

    # Set env for dlt
    os.environ["DESTINATION_DUCKDB__CREDENTIALS__DATABASE"] = DUCKDB_PATH

    source = nyc_taxi_source(years=[year], taxi_types=[taxi_type])

    pipeline = dlt.pipeline(
        pipeline_name="nyc_taxi_ingestion",
        destination=dlt.destinations.duckdb(credentials=DUCKDB_PATH),
        dataset_name="raw",
    )

    load_info = pipeline.run(source)

    logger.info(f"Batch complete: {taxi_type} {year}")
    logger.info(f"Load info: {load_info}")

    return load_info


def main():
    parser = argparse.ArgumentParser(description="Incremental NYC Taxi Data Loader")
    parser.add_argument("--status", action="store_true", help="Show current data status")
    parser.add_argument("--type", choices=["green", "yellow"], help="Taxi type to load")
    parser.add_argument("--year", type=int, choices=[2024, 2025], help="Year to load")
    args = parser.parse_args()

    if args.status:
        check_loaded_data()
        return

    # Check current state
    loaded = check_loaded_data()

    if args.type and args.year:
        # Load specific batch
        if (args.type, args.year) in loaded:
            logger.info(f"{args.type} {args.year} already loaded. Skipping.")
            return
        load_batch(args.type, args.year)
    else:
        # Load all missing batches
        for taxi_type in ALL_TAXI_TYPES:
            for year in ALL_YEARS:
                if (taxi_type, year) in loaded:
                    logger.info(f"Skipping {taxi_type} {year} (already loaded)")
                    continue
                load_batch(taxi_type, year)

    # Show final status
    print("\n--- FINAL STATUS ---")
    check_loaded_data()


if __name__ == "__main__":
    main()
