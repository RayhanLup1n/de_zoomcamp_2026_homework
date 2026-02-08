## Question 5:
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
- **Partition by tpep_dropoff_datetime and Cluster on VendorID**
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

**Strategy:**
Partitioning on the date column (`tpep_dropoff_datetime`) allows BigQuery to skip scanning data from unrequested days. Clustering on `VendorID` sorts the data within those partitions, speeding up ordering and filtering by that column.

**SQL:**
```sql
CREATE OR REPLACE TABLE `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_partitioned_clustered_homework`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID 
AS SELECT * FROM `de-zoomcamp-2026-484615.nytaxi.external_yellow_tripdata_homework`;
```
**Answer:** `Partition by tpep_dropoff_datetime and Cluster on VendorID`
