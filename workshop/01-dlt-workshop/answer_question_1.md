# Question 1

## Task Explanation

Find the start date and end date of the NYC Yellow Taxi dataset loaded from the API.

### Query

```sql
SELECT
    MIN(trip_pickup_date_time) as min_date,
    MAX(trip_pickup_date_time) as max_date
FROM nyc_taxi.trips
```

**Breakdown:**
1. **MIN()**: Finds the earliest (oldest) pickup date in the dataset
2. **MAX()**: Finds the latest (most recent) pickup date in the dataset
3. **trip_pickup_date_time**: Column containing the pickup timestamp (dlt converts from PascalCase to snake_case)

**Multiple Choice Options:**
- 2009-01-01 to 2009-01-31
- 2009-06-01 to 2009-07-01
- 2024-01-01 to 2024-02-01
- 2024-06-01 to 2024-07-01

**Answer:** 2009-06-01 to 2009-07-01

**Reason:** The dataset contains taxi trip data from June 1, 2009 18:33:00 to July 1, 2009 06:58:00. This matches the second option.
