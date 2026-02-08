## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- **0 MB for the External Table and 155.12 MB for the Materialized Table**
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

**Queries:**
```sql
-- External Table
SELECT COUNT(DISTINCT(PULocationID)) FROM `de-zoomcamp-2026-484615.nytaxi.external_yellow_tripdata_homework`;

-- Materialized Table
SELECT COUNT(DISTINCT(PULocationID)) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`;
```

**Answer:** `0 MB for the External Table and 155.12 MB for the Materialized Table`

**Explanation:** BigQuery estimates 0 MB for External Tables because it doesn't scan the external data until execution to provide an estimate. For internal (materialized) tables, BigQuery uses pre-calculated metadata.