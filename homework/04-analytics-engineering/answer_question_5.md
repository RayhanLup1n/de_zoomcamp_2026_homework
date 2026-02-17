# Module 4 Homework - Question 5

## Question: Green Taxi Trip Counts (October 2019)

Using the `fct_monthly_zone_revenue` table, what is the **total number of trips** (`total_monthly_trips`) for **Green** taxis in **October 2019**?

### Options:
- A) 500,234
- B) 350,891
- C) 384,624
- D) 421,509

---

### Answer: C

**Query:**
```sql
SELECT
    SUM(total_monthly_trips) as total_trips,
    COUNT(DISTINCT pickup_zone) as active_zones
FROM prod.fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND revenue_month = '2019-10-01'
```

**Result:**
| Metric | Value |
|--------|-------|
| Total trips | 384,624 |
| Active zones | 252 |

**Reasoning:**
- Green taxis completed 384,624 trips in October 2019
- The trips were distributed across 252 pickup zones
- October 2019 had a full month of Green taxi data (all zones active)

