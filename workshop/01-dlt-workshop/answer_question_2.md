# Question 2

## Task Explanation

Calculate the proportion (percentage) of trips that are paid with credit card.

### Query

```sql
SELECT
    payment_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM nyc_taxi.trips
GROUP BY payment_type
ORDER BY count DESC
```

**Breakdown:**
1. **payment_type**: Column containing payment method (Credit, CASH, No Charge, Dispute)
2. **COUNT(*)**: Counts the number of trips for each payment type
3. **SUM(COUNT(*)) OVER()**: Window function that calculates total trips across all payment types
4. **ROUND(..., 2)**: Rounds the percentage to 2 decimal places

**Multiple Choice Options:**
- 16.66%
- 26.66%
- 36.66%
- 46.66%

**Answer:** 26.66%

**Reason:** From the query results, 2,666 out of 10,000 trips were paid with credit card, which equals 26.66%.
