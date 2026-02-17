# Module 4 Homework - Question 4

## Question: Best Performing Zone for Green Taxis (2020)

Using the `fct_monthly_zone_revenue` table, find the pickup zone with the **highest total revenue** (`revenue_monthly_total_amount`) for **Green** taxi trips in **2020**.

### Which zone had the highest revenue?

**Options:**
- A) East Harlem North
- B) Morningside Heights
- C) East Harlem South
- D) Washington Heights South

---

### Answer: A

**Query:**
```sql
SELECT
    pickup_zone,
    SUM(revenue_monthly_total_amount) as total_revenue,
    SUM(total_monthly_trips) as total_trips
FROM prod.fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND revenue_month >= '2020-01-01'
  AND revenue_month < '2021-01-01'
GROUP BY pickup_zone
ORDER BY total_revenue DESC
LIMIT 1;
```

**Result:**
| Zone | Revenue | Trips |
|------|---------|-------|
| East Harlem North | $1,817,150.55 | 135,102 |

**Reasoning:**
- East Harlem North generated the highest total revenue ($1,817,150.55) from Green taxi trips in 2020
- It also had the highest number of trips (135,102) among Green taxi zones in 2020
- East Harlem South was the second highest with $1,653,087.61

