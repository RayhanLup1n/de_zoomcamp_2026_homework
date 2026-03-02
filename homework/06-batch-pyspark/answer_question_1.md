# Question 1

## Task Explanation

Install PySpark and create a local spark session to check the Spark version.

### Query Function

**Query (Python):**
```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("test") \
    .getOrCreate()

print(spark.version)
```

**Breakdown:**
1.  **`SparkSession.builder`**: Creates a builder for Spark session configuration
2.  **`.master("local[*]")`**: Runs Spark locally using all available cores
3.  **`.appName("test")`**: Sets the application name (shown in Spark UI)
4.  **`.getOrCreate()`**: Creates a new session or returns an existing one

**Answer:** `4.1.1`

**Reason:** The output of `spark.version` shows the installed Spark version.
