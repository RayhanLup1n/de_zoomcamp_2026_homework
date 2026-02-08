## Question 3:
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?

- **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

**Queries:**
```sql
-- Scanning only PULocationID
SELECT PULocationID FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`;

-- Scanning PULocationID and DOLocationID
SELECT PULocationID, DOLocationID FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`;
```

**Answer:** BigQuery is a columnar database... (Option 1)
