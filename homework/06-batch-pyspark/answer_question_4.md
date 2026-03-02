# Question 4

## Task Explanation

Find the length of the longest trip in the dataset in hours. Calculate the difference between `tpep_dropoff_datetime` and `tpep_pickup_datetime`.

### Query Function

**Query (Python):**
```python
from pyspark.sql.functions import col, unix_timestamp

df = spark.read.parquet("yellow_tripdata_2025-11.parquet")

# Calculate duration in hours using unix_timestamp
df_with_duration = df.withColumn(
    "duration_hours",
    (unix_timestamp(col("tpep_dropoff_datetime")) -
     unix_timestamp(col("tpep_pickup_datetime"))) / 3600
)

# Find the maximum value
longest = df_with_duration.agg({"duration_hours": "max"}).collect()[0][0]
print(f"Longest trip: {longest:.2f} hours")
```

**Breakdown:**
1.  **`unix_timestamp()`**: Converts timestamp to epoch seconds (unix timestamp)
2.  **Difference / 3600**: Converts seconds to hours (3600 seconds = 1 hour)
3.  **`.agg({"duration_hours": "max"})`**: Aggregation to find maximum value

**Multiple Choice Options:**
- 22.7
- 58.2
- 90.6
- 134.5

**Answer:** **90.6**

**Reason:** The longest trip is **90.65 hours**, which is closest to option **90.6**.

> **Note:** In Spark 4.x, use `unix_timestamp()` instead of `cast("long")` for TIMESTAMP_NTZ type.
