# Question 3

## Task Explanation

Calculate the total amount of money generated in tips from all taxi trips.

### Query

```sql
SELECT ROUND(SUM(tip_amt), 2) as total_tips
FROM nyc_taxi.trips
```

**Breakdown:**
1. **SUM()**: Aggregates (adds up) all values in the tip_amt column
2. **tip_amt**: Column containing the tip amount for each trip (dlt converts from Tip_Amt to snake_case)
3. **ROUND(..., 2)**: Rounds the result to 2 decimal places for currency format

**Multiple Choice Options:**
- $4,063.41
- $6,063.41
- $8,063.41
- $10,063.41

**Answer:** $6,063.41

**Reason:** The SUM of tip_amt across all 10,000 records equals $6,063.41.
