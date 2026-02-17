# Module 4 Homework - Question 3

## Question: Counting Records in `fct_monthly_zone_revenue`

After running your dbt project, query the `fct_monthly_zone_revenue` model.

### What is the count of records in the `fct_monthly_zone_revenue` model?

**Options:**
- A) 12,998
- B) 14,120
- C) 12,184
- D) 15,421

---

### Answer: C

**Reasoning:**
- Query: `SELECT COUNT(*) FROM prod.fct_monthly_zone_revenue`
- Result: **12,184 records**
- The model aggregates trip data by (pickup_zone, revenue_month, service_type)
- Breakdown by service type:
  - Yellow taxi: 6,424 records
  - Green taxi: 5,760 records
- Note: The answer assumes using the production target with full 2019-2020 data, not the dev environment which only has 1 month of data (516 records)

