/*
  Question Num 1:
  What is count of records for the 2024 Yellow Taxi Data?
*/
SELECT COUNT(*) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`;
-- Answer: 20,332,093


/*
  Question Num 2:
  Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
  What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
*/
-- Querying External Table
SELECT COUNT(DISTINCT(PULocationID)) FROM `de-zoomcamp-2026-484615.nytaxi.external_yellow_tripdata_homework`;

-- Querying Native Table
SELECT COUNT(DISTINCT(PULocationID)) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`;
-- Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table
-- Reason: BigQuery estimates 0 MB for external files as it doesn't scan metadata for estimation. Materialized table uses pre-calculated metadata.


/*
  Question Num 3:
  Why are the estimated number of Bytes different for 1 column vs 2 columns?
*/
-- 1 Column
SELECT PULocationID FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`;

-- 2 Columns
SELECT PULocationID, DOLocationID FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`;
-- Answer: BigQuery is a columnar database and scans only the specified columns.


/*
  Question Num 4:
  How many records have a fare_amount of 0?
*/
SELECT COUNT(*) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`
WHERE fare_amount = 0;
-- Answer: 8,333


/*
  Question Num 5:
  What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID?
*/
CREATE OR REPLACE TABLE `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_partitioned_clustered_homework`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS 
SELECT * FROM `de-zoomcamp-2026-484615.nytaxi.external_yellow_tripdata_homework`;
-- Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID


/*
  Question Num 6:
  Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
*/
-- Regular Table
SELECT DISTINCT(VendorID) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Optimized Table
SELECT DISTINCT(VendorID) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_partitioned_clustered_homework`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
-- Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table


/*
  Question Num 7:
  Where is the data stored in the External Table you created?
*/
-- Answer: GCP Bucket (Google Cloud Storage)


/*
  Question Num 8:
  It is best practice in Big Query to always cluster your data:
*/
-- Answer: False


/*
  Question Num 9 (Bonus):
  Write a SELECT count(*) query FROM the materialized table. How many bytes does it estimate?
*/
SELECT COUNT(*) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`;
-- Answer: 0 bytes.
-- Reason: Retrieved from table metadata.