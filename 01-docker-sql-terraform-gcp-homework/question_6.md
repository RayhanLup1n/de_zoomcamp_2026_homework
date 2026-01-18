## Question 6. Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip? 

Note: it's **tip**, not trip. We need the name of the zone, not the ID.

- JFK Airport
- Yorkville West
- East Harlem North
- LaGuardia Airport

## ANSWER

The correct answer is **[TO BE VERIFIED BY RUNNING QUERY]**

## SQL QUERY

```sql
SELECT 
    zdo."Zone" AS dropoff_zone,
    MAX(t.tip_amount) AS max_tip
FROM 
    green_taxi_trips t
JOIN 
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN 
    zones zdo ON t."DOLocationID" = zdo."LocationID"
WHERE 
    zpu."Zone" = 'East Harlem North'
    AND t.lpep_pickup_datetime >= '2025-11-01' 
    AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY 
    1
ORDER BY 
    max_tip DESC
LIMIT 1;
```

## REASON

1.  We need two joins: one for the **Pickup Zone** (`zpu`) and one for the **Dropoff Zone** (`zdo`).
2.  The filter `zpu."Zone" = 'East Harlem North'` ensures we only look at trips starting from that specific area.
3.  `MAX(t.tip_amount)` finds the single highest tip recorded for each dropoff destination from that starting point.
4.  Sorting by `max_tip DESC` and using `LIMIT 1` gives us the winner.