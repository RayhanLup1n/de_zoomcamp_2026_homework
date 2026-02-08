## (Bonus: Not worth points) Question 9:
Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

**Query:**
```sql
SELECT COUNT(*) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`;
```

**Estimate:** `0 bytes`

**Reasoning:** 
BigQuery stores the total row count of native (materialized) tables in its metadata. When executing a simple `COUNT(*)` without filters, BigQuery pulls this value directly from metadata instead of scanning the data columns, resulting in 0 bytes processed.
