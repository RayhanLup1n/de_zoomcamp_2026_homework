## Question 6:
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive).
Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

Choose the answer which most closely matches.

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

**Queries:**
```sql
-- Normal Table
SELECT DISTINCT(VendorID) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Partitioned & Clustered Table
SELECT DISTINCT(VendorID) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_partitioned_clustered_homework`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```

**Answer:** `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`
