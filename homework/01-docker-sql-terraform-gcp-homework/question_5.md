## Question 5. Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

- East Harlem North
- East Harlem South
- Morningside Heights
- Forest Hills

## ANSWER

The correct answer is **[TO BE VERIFIED BY RUNNING QUERY]**

## SQL QUERY

```sql
SELECT 
    z."Zone", 
    SUM(t.total_amount) AS total_amount_sum
FROM 
    green_taxi_trips t
JOIN 
    zones z ON t."PULocationID" = z."LocationID"
WHERE 
    CAST(t.lpep_pickup_datetime AS DATE) = '2025-11-18'
GROUP BY 
    1
ORDER BY 
    total_amount_sum DESC
LIMIT 1;
```

## REASON

1.  We **JOIN** the taxi trips table with the zones table using `PULocationID` and `LocationID` to get the zone names.
2.  `WHERE CAST(t.lpep_pickup_datetime AS DATE) = '2025-11-18'` filters only for the specific requested day.
3.  `SUM(t.total_amount)` calculates the total revenue per zone.
4.  `GROUP BY 1` groups the sums by the zone name.
5.  `ORDER BY total_amount_sum DESC` sorts the result to put the zone with the highest amount at the top.