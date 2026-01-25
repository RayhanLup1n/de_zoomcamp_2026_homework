import os
import pandas as pd
from sqlalchemy import create_engine
from time import time
import click

@click.command()
@click.option('--user', default='root')
@click.option('--password', default='root')
@click.option('--host', default='localhost')
@click.option('--port', default=5432)
@click.option('--db', default='green_tripdata')
@click.option('--table', default='green_taxi_trips')
@click.option('--url', help='url of the parquet file')
@click.option('--zones_url', default='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv')
def main(user, password, host, port, db, table, url, zones_url):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # 1. Ingest Zones
    print("Downloading and ingesting zones...")
    df_zones = pd.read_csv(zones_url)
    df_zones.to_sql(name='zones', con=engine, if_exists='replace')

    # 2. Ingest Green Taxi Data (Parquet)
    parquet_name = 'data.parquet'
    print(f"Downloading taxi data from {url}...")
    os.system(f"wget {url} -O {parquet_name}")
    
    print("Reading and ingesting taxi data...")
    df = pd.read_parquet(parquet_name)
    
    # Mengirim data ke SQL
    df.to_sql(name=table, con=engine, if_exists='replace', chunksize=100000)
    print("Finished ingesting data.")

if __name__ == '__main__':
    main()