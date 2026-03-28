import json
from time import time
import pyarrow.parquet as pq
import pandas as pd
from kafka import KafkaProducer

# Configuration
BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC = 'green-trips'
DATA_URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet'
LOCAL_FILE = 'green_tripdata_2025-10.parquet'

# Columns to keep
COLUMNS = [
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount',
    'total_amount'
]


def read_parquet_data(file_path):
    """Read parquet file and return DataFrame with selected columns"""
    df = pd.read_parquet(file_path, columns=COLUMNS)
    return df


def convert_row_to_dict(row):
    """Convert DataFrame row to dictionary with datetime as strings"""
    return {
        'lpep_pickup_datetime': row['lpep_pickup_datetime'].isoformat() if pd.notna(row['lpep_pickup_datetime']) else None,
        'lpep_dropoff_datetime': row['lpep_dropoff_datetime'].isoformat() if pd.notna(row['lpep_dropoff_datetime']) else None,
        'PULocationID': int(row['PULocationID']) if pd.notna(row['PULocationID']) else None,
        'DOLocationID': int(row['DOLocationID']) if pd.notna(row['DOLocationID']) else None,
        'passenger_count': int(row['passenger_count']) if pd.notna(row['passenger_count']) else None,
        'trip_distance': float(row['trip_distance']) if pd.notna(row['trip_distance']) else None,
        'tip_amount': float(row['tip_amount']) if pd.notna(row['tip_amount']) else None,
        'total_amount': float(row['total_amount']) if pd.notna(row['total_amount']) else None,
    }


def main():
    # Download data if not present
    import os
    if not os.path.exists(LOCAL_FILE):
        print(f"Downloading data from {DATA_URL}...")
        import urllib.request
        urllib.request.urlretrieve(DATA_URL, LOCAL_FILE)
        print("Download complete.")

    # Read parquet data
    print("Reading parquet data...")
    df = read_parquet_data(LOCAL_FILE)
    print(f"Total rows: {len(df)}")

    # Create Kafka producer
    print(f"Connecting to Kafka at {BOOTSTRAP_SERVERS}...")
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    # Send data and measure time
    print(f"Sending data to topic '{TOPIC}'...")
    t0 = time()

    for index, row in df.iterrows():
        message = convert_row_to_dict(row)
        producer.send(TOPIC, value=message)

        # Progress indicator
        if (index + 1) % 10000 == 0:
            print(f"Sent {index + 1} messages...")

    # Flush producer
    print("Flushing producer...")
    producer.flush()

    t1 = time()
    elapsed = t1 - t0
    print(f'Took {elapsed:.2f} seconds')
    print(f'Rate: {len(df) / elapsed:.2f} messages/second')

    producer.close()


if __name__ == '__main__':
    main()
