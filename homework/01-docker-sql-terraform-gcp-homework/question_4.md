## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors). Use the pick up time for your calculations.

- 2025-11-14
- 2025-11-20
- 2025-11-23
- 2025-11-25

## ANSWER

The correct answer is **[TO BE VERIFIED BY RUNNING QUERY]**

## SQL QUERY

```sql
SELECT 
    CAST(lpep_pickup_datetime AS DATE) AS pickup_day, 
    MAX(trip_distance) AS max_distance
FROM 
    green_taxi_trips
WHERE 
    trip_distance < 100
GROUP BY 
    1
ORDER BY 
    max_distance DESC
LIMIT 1;
```

## REASON

1.  `CAST(lpep_pickup_datetime AS DATE)` is used to extract the date part from the timestamp.
2.  `MAX(trip_distance)` finds the largest value in the trip distance column for each group.
3.  `WHERE trip_distance < 100` excludes outliers or potential recording errors.
4.  `GROUP BY 1` groups the results by the pickup day.
5.  `ORDER BY max_distance DESC` sorts the days from the longest trip to the shortest.
6.  `LIMIT 1` retrieves only the day with the single longest trip.