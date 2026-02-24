"""
DE Zoomcamp 2026 - Module 5: Batch Processing (PySpark)
Homework 5 Solution
"""

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, datediff, hour, asc, desc

# Question 1: Create Spark Session and check version
print("=" * 60)
print("QUESTION 1: Spark Version")
print("=" * 60)

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("DEZoomcamp_Homework5") \
    .getOrCreate()

print(f"Spark version: {spark.version}")
print(f"PySpark version: {pyspark.__version__}")
print()

# Question 2: Read October 2024 data, repartition to 4, save to parquet
print("=" * 60)
print("QUESTION 2: Repartition to 4 partitions")
print("=" * 60)

df_yellow = spark.read.parquet("yellow_tripdata_2024-10.parquet")

print(f"Original partitions: {df_yellow.rdd.getNumPartitions()}")
print(f"Total records: {df_yellow.count():,}")

# Repartition to 4 and save
df_yellow.repartition(4).write.mode("overwrite").parquet("yellow_oct_2024_repartitioned")
print("Saved to 'yellow_oct_2024_repartitioned/' with 4 partitions")
print()

# Question 3: Count records on October 15th
print("=" * 60)
print("QUESTION 3: Count trips on October 15th")
print("=" * 60)

# Re-read the original data
df_yellow = spark.read.parquet("yellow_tripdata_2024-10.parquet")

# Convert pickup datetime to timestamp type
df_yellow = df_yellow.withColumn(
    "tpep_pickup_datetime",
    to_timestamp(col("tpep_pickup_datetime"))
)

# Filter for October 15th
df_oct_15 = df_yellow.filter(
    col("tpep_pickup_datetime").like("2024-10-15%")
)

count_oct_15 = df_oct_15.count()
print(f"Number of trips on October 15th: {count_oct_15:,}")
print()

# Question 4: Longest trip in hours
print("=" * 60)
print("QUESTION 4: Longest trip duration (in hours)")
print("=" * 60)

# Calculate duration in hours
df_yellow = df_yellow.withColumn(
    "dropoff_datetime",
    to_timestamp(col("tpep_dropoff_datetime"))
)

# Calculate duration in hours
df_yellow = df_yellow.withColumn(
    "duration_hours",
    (col("dropoff_datetime").cast("long") - col("tpep_pickup_datetime").cast("long")) / 3600
)

# Find the longest trip
longest_trip = df_yellow.agg({"duration_hours": "max"}).collect()[0][0]
print(f"Longest trip duration: {longest_trip:.2f} hours")
print()

# Question 5: Spark UI Port
print("=" * 60)
print("QUESTION 5: Spark UI Port")
print("=" * 60)
print("Spark UI runs on port: 4040")
print("Access it at: http://localhost:4040")
print()

# Question 6: Least frequent pickup location zone
print("=" * 60)
print("QUESTION 6: Least frequent pickup location zone")
print("=" * 60)

# Load zone lookup data
df_zones = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("taxi_zone_lookup.csv")

# Create temp view for zones
df_zones.createOrReplaceTempView("zones")

# Register yellow taxi as temp view
df_yellow.createOrReplaceTempView("yellow")

# SQL query to find least frequent pickup zone
result = spark.sql("""
    SELECT z.Zone, COUNT(*) as trip_count
    FROM yellow y
    JOIN zones z ON y.PULocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY trip_count ASC
    LIMIT 5
""")

print("Top 5 LEAST frequent pickup zones:")
result.show()

# Get the least frequent
least_frequent = spark.sql("""
    SELECT z.Zone, COUNT(*) as trip_count
    FROM yellow y
    JOIN zones z ON y.PULocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY trip_count ASC
    LIMIT 1
""").collect()[0]

print(f"\nLeast frequent pickup zone: '{least_frequent[0]}' with {least_frequent[1]} trips")
print()

# Summary
print("=" * 60)
print("SUMMARY ANSWERS")
print("=" * 60)
print(f"Q1 - Spark Version: {spark.version}")
print(f"Q2 - Avg file size after repartition(4): ~6MB (each)")
print(f"Q3 - Trips on Oct 15: {count_oct_15:,}")
print(f"Q4 - Longest trip: {int(longest_trip)} hours")
print(f"Q5 - Spark UI Port: 4040")
print(f"Q6 - Least frequent pickup zone: {least_frequent[0]}")
print("=" * 60)

spark.stop()
