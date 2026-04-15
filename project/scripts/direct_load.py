"""
Direct Data Loader - Load NYC Taxi Data directly into DuckDB

Bypasses dlt to avoid pyarrow timezone issues on Windows.
Uses DuckDB's native parquet reader which handles timezones internally.

Usage:
    python scripts/direct_load.py                    # Load all missing data
    python scripts/direct_load.py --type yellow --year 2024  # Load specific batch
    python scripts/direct_load.py --status            # Check what's loaded
"""

import os
import sys
import argparse
import logging
import duckdb

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUCKDB_PATH = os.path.join(PROJECT_ROOT, "data", "capstone.duckdb")

# NYC TLC base URL
NYC_TLC_BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

# Full data matrix
ALL_YEARS = [2024, 2025]
ALL_TAXI_TYPES = ["green", "yellow"]


def check_loaded_data(con=None):
    """Check which taxi_type + year combos are already in DuckDB."""
    close_con = False
    if con is None:
        if not os.path.exists(DUCKDB_PATH):
            logger.info("DuckDB file not found. No data loaded yet.")
            return set()
        con = duckdb.connect(DUCKDB_PATH, read_only=True)
        close_con = True

    try:
        # Check if table exists
        tables = con.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='raw'"
        ).fetchall()
        table_names = [t[0] for t in tables]

        if "trips_resource" not in table_names:
            print("\n  No trips_resource table found yet.")
            return set()

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
        print(f"  {'Taxi Type':<12} {'Year':<8} {'Months':<18} {'Rows':>12}")
        print("-" * 65)

        for row in result:
            taxi_type, year, months, rows = row
            loaded.add((taxi_type, year))
            status = f"COMPLETE (12/12)" if months == 12 else f"PARTIAL ({months}/12)"
            print(f"  {taxi_type:<12} {year:<8} {status:<18} {rows:>12,}")

        # Show missing
        print("-" * 65)
        missing = []
        for taxi_type in ALL_TAXI_TYPES:
            for year in ALL_YEARS:
                if (taxi_type, year) not in loaded:
                    missing.append((taxi_type, year))
                    print(f"  {taxi_type:<12} {year:<8} {'MISSING':<18} {'---':>12}")

        total = con.execute("SELECT COUNT(*) FROM raw.trips_resource").fetchone()[0]
        print("-" * 65)
        print(f"  {'TOTAL':<12} {'':<8} {'':<18} {total:>12,}")
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
        if close_con:
            con.close()


def load_single_month(con, taxi_type, year, month):
    """Load a single month of taxi data directly via DuckDB's httpfs/parquet reader.

    Maps parquet column names (PascalCase) to dlt-normalized names (snake_case)
    and handles green vs yellow schema differences.
    """
    filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    url = f"{NYC_TLC_BASE_URL}/{filename}"

    logger.info(f"Loading {filename}...")

    try:
        # First, check what columns the parquet file has
        parquet_cols = con.execute(f"""
            SELECT column_name FROM (
                DESCRIBE SELECT * FROM read_parquet('{url}')
            )
        """).fetchall()
        parquet_col_names = [c[0] for c in parquet_cols]

        # Build column mapping: parquet name -> table name
        # dlt normalized PascalCase to snake_case
        col_mapping = {
            "VendorID": "vendor_id",
            "RatecodeID": "ratecode_id",
            "PULocationID": "pu_location_id",
            "DOLocationID": "do_location_id",
        }

        # Build SELECT columns, mapping each parquet col to table col
        select_parts = []
        for pcol in parquet_col_names:
            table_col = col_mapping.get(pcol, pcol)
            if pcol != table_col:
                select_parts.append(f'"{pcol}" AS {table_col}')
            else:
                select_parts.append(f'"{pcol}"')

        # Add metadata columns
        select_parts.append(f"{year} AS _ingest_year")
        select_parts.append(f"{month} AS _ingest_month")
        select_parts.append(f"'{taxi_type}' AS _ingest_taxi_type")
        select_parts.append(f"'{filename}' AS _ingest_file")

        # Get all table columns to know which ones need NULL
        table_cols = con.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_schema = 'raw' AND table_name = 'trips_resource'
            ORDER BY ordinal_position
        """).fetchall()
        table_col_names = [c[0] for c in table_cols]

        # Figure out which table columns are NOT covered by the parquet + metadata
        covered_cols = set()
        for pcol in parquet_col_names:
            covered_cols.add(col_mapping.get(pcol, pcol))
        covered_cols.update(["_ingest_year", "_ingest_month", "_ingest_taxi_type", "_ingest_file"])

        # Add NULLs for missing columns (e.g., green doesn't have tpep_* columns)
        for tcol in table_col_names:
            if tcol not in covered_cols:
                select_parts.append(f"NULL AS {tcol}")

        select_clause = ", ".join(select_parts)

        # Build explicit column list for INSERT
        # Order: covered parquet cols (mapped) + metadata + missing cols
        insert_cols = []
        for pcol in parquet_col_names:
            insert_cols.append(col_mapping.get(pcol, pcol))
        insert_cols.extend(["_ingest_year", "_ingest_month", "_ingest_taxi_type", "_ingest_file"])
        for tcol in table_col_names:
            if tcol not in covered_cols:
                insert_cols.append(tcol)

        insert_col_list = ", ".join(insert_cols)

        sql = f"""
            INSERT INTO raw.trips_resource ({insert_col_list})
            SELECT {select_clause}
            FROM read_parquet('{url}')
        """

        con.execute(sql)

        # Get actual inserted count
        count = con.execute(f"""
            SELECT COUNT(*) FROM raw.trips_resource
            WHERE _ingest_taxi_type = '{taxi_type}'
              AND _ingest_year = {year}
              AND _ingest_month = {month}
        """).fetchone()[0]

        logger.info(f"  Loaded {count:,} rows from {filename}")
        return count

    except Exception as e:
        error_msg = str(e)
        if "HTTP Error" in error_msg or "404" in error_msg or "Could not read" in error_msg:
            logger.warning(f"  File not available (skipping): {filename}")
            return 0
        else:
            logger.error(f"  Error loading {filename}: {e}")
            raise


def ensure_table_exists(con):
    """Create the raw.trips_resource table if it doesn't exist, matching the existing schema."""
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

    # Check if table already exists
    tables = con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='raw' AND table_name='trips_resource'"
    ).fetchall()

    if tables:
        logger.info("Table raw.trips_resource already exists")
        return

    # Create table by reading schema from a small sample
    logger.info("Creating raw.trips_resource table from sample...")
    sample_url = f"{NYC_TLC_BASE_URL}/green_tripdata_2024-01.parquet"

    con.execute(f"""
        CREATE TABLE raw.trips_resource AS
        SELECT
            *,
            CAST(0 AS INTEGER) as _ingest_year,
            CAST(0 AS INTEGER) as _ingest_month,
            CAST('' AS VARCHAR) as _ingest_taxi_type,
            CAST('' AS VARCHAR) as _ingest_file
        FROM read_parquet('{sample_url}')
        LIMIT 0
    """)
    logger.info("Table created successfully")


def load_batch(taxi_type, year):
    """Load all 12 months for a taxi_type + year combo."""
    logger.info("=" * 60)
    logger.info(f"Loading batch: {taxi_type} {year}")
    logger.info("=" * 60)

    con = duckdb.connect(DUCKDB_PATH)

    try:
        # Install and load httpfs for reading from URLs
        con.execute("INSTALL httpfs")
        con.execute("LOAD httpfs")

        ensure_table_exists(con)

        total_rows = 0
        for month in range(1, 13):
            try:
                rows = load_single_month(con, taxi_type, year, month)
                total_rows += rows
            except Exception as e:
                logger.error(f"Failed on month {month}: {e}")
                logger.info("Continuing with next month...")
                continue

        logger.info(f"Batch complete: {taxi_type} {year} — {total_rows:,} total rows")

    finally:
        con.close()

    return total_rows


def main():
    parser = argparse.ArgumentParser(description="Direct NYC Taxi Data Loader")
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
