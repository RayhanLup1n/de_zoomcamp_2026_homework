## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

- 7,853
- 8,007
- 8,254
- 8,421

## ANSWER

The correct answer is **[TO BE VERIFIED BY RUNNING QUERY]**

## SQL QUERY

```sql
SELECT 
    COUNT(1) 
FROM 
    green_taxi_trips 
WHERE 
    lpep_pickup_datetime >= '2025-11-01' 
    AND lpep_pickup_datetime < '2025-12-01'
    AND trip_distance <= 1;
```

## REASON

We use the `COUNT(1)` function to count the number of rows that satisfy the conditions. 
1.  `lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01'` filters the data for the entire month of November 2025.
2.  `trip_distance <= 1` filters the trips that are 1 mile or less in distance.