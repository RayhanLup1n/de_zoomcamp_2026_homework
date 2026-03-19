"""
DE Zoomcamp 2026 - Module 6: Batch Processing (PySpark)
Homework 6 Solution - November 2025 Data
"""

import pyspark
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, unix_timestamp, asc, desc

# ==============================================================================
# QUESTION 1: Create Spark Session and check version
# ==============================================================================
print("=" * 70)
print("QUESTION 1: Spark Version")
print("=" * 70)

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("DEZoomcamp_Homework6_Nov2025") \
    .config("spark.ui.port", "4040") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()

# Set log level to ERROR to reduce noise
spark.sparkContext.setLogLevel("ERROR")

print(f"✅ Spark version: {spark.version}")
print(f"✅ PySpark version: {pyspark.__version__}")
print(f"🔥 Spark UI: http://localhost:4041 (port 4040 sudah dipakai)")
print()

# ==============================================================================
# QUESTION 2: Read November 2025 data, repartition to 4, save to parquet
# ==============================================================================
print("=" * 70)
print("QUESTION 2: Repartition to 4 partitions")
print("=" * 70)

df_yellow = spark.read.parquet("yellow_tripdata_2025-11.parquet")

print(f"Original partitions: {df_yellow.rdd.getNumPartitions()}")
print(f"Total records: {df_yellow.count():,}")

# Repartition to 4 and save
df_yellow.repartition(4).write.mode("overwrite").parquet("yellow_nov_2025_repartitioned")
print("Saved to 'yellow_nov_2025_repartitioned/' with 4 partitions")

# Check file sizes
import os
import glob

parquet_files = glob.glob("yellow_nov_2025_repartitioned/*.parquet")
total_size = 0
print("\nFile sizes:")
for f in parquet_files:
    size_mb = os.path.getsize(f) / (1024 * 1024)
    total_size += size_mb
    print(f"  {os.path.basename(f)}: {size_mb:.2f} MB")

avg_size = total_size / len(parquet_files) if parquet_files else 0
print(f"\nAverage file size: {avg_size:.2f} MB")
print()

# ==============================================================================
# QUESTION 3: Count records on November 15th
# ==============================================================================
print("=" * 70)
print("QUESTION 3: Count trips on November 15th")
print("=" * 70)

# Re-read the original data
print("   Loading data...")
df_yellow = spark.read.parquet("yellow_tripdata_2025-11.parquet")

# Register temp view for better job names
df_yellow.createOrReplaceTempView("yellow_trips")

# Filter for November 15th with explicit job naming
print("   Filtering for November 15th...")
df_nov_15 = spark.sql("""
    SELECT COUNT(*) as trip_count
    FROM yellow_trips
    WHERE tpep_pickup_datetime LIKE '2025-11-15%'
""")

count_nov_15 = df_nov_15.collect()[0]["trip_count"]
print(f"   ✅ Number of trips on November 15th: {count_nov_15:,}")
print()

# ==============================================================================
# QUESTION 4: Longest trip in hours
# ==============================================================================
print("=" * 70)
print("QUESTION 4: Longest trip duration (in hours)")
print("=" * 70)

# Calculate duration in hours using unix_timestamp
df_yellow = df_yellow.withColumn(
    "duration_hours",
    (unix_timestamp(col("tpep_dropoff_datetime")) - unix_timestamp(col("tpep_pickup_datetime"))) / 3600
)

# Find the longest trip
longest_trip = df_yellow.agg({"duration_hours": "max"}).collect()[0][0]
print(f"Longest trip duration: {longest_trip:.2f} hours")
print()

# ==============================================================================
# QUESTION 5: Spark UI Port
# ==============================================================================
print("=" * 70)
print("QUESTION 5: Spark UI Port")
print("=" * 70)
print("Spark UI runs on port: 4040")
print("Access it at: http://localhost:4040")
print()

# ==============================================================================
# QUESTION 6: Least frequent pickup location zone
# ==============================================================================
print("=" * 70)
print("QUESTION 6: Least frequent pickup location zone")
print("=" * 70)

# Load zone lookup data
print("   Loading zone lookup data...")
df_zones = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("taxi_zone_lookup.csv")

# Create temp views with explicit names
df_zones.createOrReplaceTempView("zones_lookup")
df_yellow.createOrReplaceTempView("yellow_trips")

# SQL query to find least frequent pickup zone with explicit job naming
print("   Finding least frequent pickup zone...")
result = spark.sql("""
    SELECT z.Zone, COUNT(*) as trip_count
    FROM yellow_trips y
    JOIN zones_lookup z ON y.PULocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY trip_count ASC
    LIMIT 5
""")

print("   Top 5 LEAST frequent pickup zones:")
result.show()

# Get the least frequent
least_frequent = spark.sql("""
    SELECT z.Zone, COUNT(*) as trip_count
    FROM yellow_trips y
    JOIN zones_lookup z ON y.PULocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY trip_count ASC
    LIMIT 1
""").collect()[0]

print(f"\n   ✅ Least frequent pickup zone: '{least_frequent[0]}' with {least_frequent[1]} trips")
print()

# ==============================================================================
# SUMMARY
# ==============================================================================
print("=" * 70)
print("SUMMARY ANSWERS")
print("=" * 70)
print(f"Q1 - Spark Version: {spark.version}")
print(f"Q2 - Avg file size after repartition(4): {avg_size:.0f} MB")
print(f"Q3 - Trips on Nov 15: {count_nov_15:,}")
print(f"Q4 - Longest trip: {int(longest_trip)} hours")
print(f"Q5 - Spark UI Port: 4040")
print(f"Q6 - Least frequent pickup zone: {least_frequent[0]}")
print("=" * 70)

# ==============================================================================
# KEEP SESSION ALIVE FOR UI
# ==============================================================================
print("\n" + "=" * 70)
print("🔥 SPARK UI AKTIF - BUKA BROWSER ANDA!")
print("=" * 70)
print(f"""
🌐 Buka di browser: http://localhost:4041

📸 TAB-TAB YANG WAJIB DILIHAT:

1️⃣  JOBS TAB (http://localhost:4041/jobs/)
   └─ Ini halaman UTAMA yang perlu dilihat
   └─ Menunjukkan 7 jobs yang sudah dijalankan:
      • count at ... (Q3 - Count trips on Nov 15)
      • show at ... (Q6 - Show least frequent zones)
      • count at ... (Q6 - Get least frequent zone)
      • write at ... (Q2 - Write repartitioned data)
      • count at ... (Q2 - Count records)
      • count at ... (Q1 - Check version - dummy)
   └─ ⚠️  KLIK pada job ID, JANGAN klik di judul!

2️⃣  SQL TAB (http://localhost:4041/SQL/)
   └─ Menunjukkan 3 SQL queries yang dijalankan
   └─ Query 1: SELECT COUNT(*) FROM yellow_trips WHERE ...
   └─ Query 2: SELECT z.Zone, COUNT(*) FROM yellow_trips JOIN ...
   └─ Query 3: SELECT z.Zone, COUNT(*) FROM yellow_trips JOIN ...

3️⃣  STAGES TAB (http://localhost:4041/stages/)
   └─ Detail breakdown job menjadi stages
   └─ Setiap job bisa punya 1-2 stages
   └─ Stage 1: scan + filter (map side)
   └─ Stage 2: aggregate (reduce side, after shuffle)

💡 CARA NAVIGASI YANG BENAR:
   1. Buka Jobs Tab → Lihat semua job
   2. Klik pada ID job (misal: job-0) untuk lihat detail
   3. Di detail job, klik "Stages" untuk breakdown
   4. Kembali ke Jobs Tab untuk lihat job lain

❌ JANGAN KLIK:
   • Jangan klik judul job (navigasi bisa aneh)
   • Jangan klik link di description
   ✅ KLIK ID job atau tombol detail

💡 TIPS SCREENSHOT:
   • Gunakan dark mode di browser
   • Zoom out (Ctrl+-) untuk lihat lebih banyak info
   • Capture metrics penting: Duration, Tasks, Memory
   • Full screen browser (F11) untuk capture maksimal

🛑 Tekan Ctrl+C untuk stop Spark session
""")
print("=" * 70)

# Keep session alive so you can view UI
try:
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        if counter % 30 == 0:
            print(f"   ⏱️  Session aktif... ({counter}s elapsed)")
except KeyboardInterrupt:
    print("\n\n" + "=" * 70)
    print("🛑 STOPPING SPARK SESSION")
    print("=" * 70)
    spark.stop()
    print("✅ Spark session stopped!")
    print("\n🎉 Homework completed!")
    print("📚 Baca SPARK_UI_GUIDE.md untuk memahami UI lebih detail!")
