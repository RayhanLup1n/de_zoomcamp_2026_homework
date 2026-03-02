# Question 2

## Task Explanation

Read the November 2025 Yellow taxi data into a Spark DataFrame, repartition to 4 partitions, and save to parquet. Determine the average size of the resulting parquet files.

### Query Function

**Query (Python):**
```python
df = spark.read.parquet("yellow_tripdata_2025-11.parquet")
df.repartition(4).write.parquet("yellow_nov_2025_repartitioned")
```

**Breakdown:**
1.  **`spark.read.parquet()`**: Reads a parquet file into a Spark DataFrame
2.  **`.repartition(4)`**: Repartitions the data into 4 partitions (files)
3.  **`.write.parquet()`**: Writes the DataFrame to parquet format

**Multiple Choice Options:**
- 6MB
- 25MB
- 75MB
- 100MB

**Answer:** **25MB**

**Reason:** After repartitioning to 4, each parquet file is approximately 24.41 MB. The closest answer is **25MB**.

**File size breakdown:**
```
part-00000-*.parquet: 24.39 MB
part-00001-*.parquet: 24.42 MB
part-00002-*.parquet: 24.42 MB
part-00003-*.parquet: 24.41 MB
```
