import os
from google.cloud import storage
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

project_id = os.getenv("GCP_PROJECT_ID")
bucket_name = os.getenv("GCS_BUCKET_NAME")
credentials_path = os.getenv("LOCAL_GCP_CREDENTIALS")

# Set credentials for the script
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

def create_bucket_if_not_exists():
    storage_client = storage.Client(project=project_id)
    try:
        bucket = storage_client.get_bucket(bucket_name)
        print(f"Bucket {bucket_name} already exists.")
    except Exception:
        print(f"Creating bucket {bucket_name}...")
        bucket = storage_client.create_bucket(bucket_name, location="US")
        print(f"Bucket {bucket_name} created.")

def create_dataset_if_not_exists():
    bq_client = bigquery.Client(project=project_id)
    dataset_id = f"{project_id}.analytics"
    
    try:
        bq_client.get_dataset(dataset_id)
        print(f"Dataset {dataset_id} already exists.")
    except Exception:
        print(f"Creating dataset {dataset_id}...")
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        bq_client.create_dataset(dataset, timeout=30)
        print(f"Dataset {dataset_id} created.")

if __name__ == "__main__":
    if not project_id:
        print("Error: GCP_PROJECT_ID not found in .env")
    else:
        create_bucket_if_not_exists()
        create_dataset_if_not_exists()
        print("GCP Initialization complete.")
