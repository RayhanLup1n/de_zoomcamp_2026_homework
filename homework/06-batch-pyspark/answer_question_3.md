# Question 3

## Task Explanation

Count the number of taxi trips that occurred on November 15th, 2025. Filter based on `tpep_pickup_datetime`.

### Query Function

**Query (Python):**
```python
from pyspark.sql.functions import col

df = spark.read.parquet("yellow_tripdata_2025-11.parquet")

df.filter(col("tpep_pickup_datetime").like("2025-11-15%")) \
  .count()
```

**Breakdown:**
1.  **`col("tpep_pickup_datetime")`**: Creates a column reference
2.  **`.like("2025-11-15%")`**: Pattern matching for date (`%` is wildcard)
3.  **`.count()`**: Counts the number of rows after filtering

**Multiple Choice Options:**
- 62,610
- 102,340
- 162,604
- 225,768

**Answer:** **162,604**

**Reason:** Filtering for date `2025-11-15` results in **162,604 trips**.
