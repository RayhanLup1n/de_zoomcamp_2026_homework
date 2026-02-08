## Question 4:
How many records have a fare_amount of 0?
- 128,210
- 546,578
- 20,188,016
- **8,333**

**Query:**
```sql
SELECT COUNT(*) FROM `de-zoomcamp-2026-484615.nytaxi.yellow_tripdata_2024_homework`
WHERE fare_amount = 0;
```
**Answer:** `8,333`
