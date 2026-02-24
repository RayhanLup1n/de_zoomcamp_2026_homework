# Module 5: Batch Processing with PySpark - Homework

## Overview

Module ini membahas tentang **Batch Processing** menggunakan Apache Spark dan PySpark. Spark adalah framework untuk memproses data dalam jumlah besar (Big Data) secara terdistribusi.

### Apa itu Spark?

| Konsep | Analogi |
|--------|---------|
| **Pandas** | Satu orang kerjain sendiri → terbatas memori satu komputer |
| **Spark** | Banyak orang (nodes) kerjain bareng → bisa proses data triliunan baris |

### Komponen Utama Spark

- **Driver**: Program utama yang mengontrol eksekusi
- **Workers**: Node yang menjalankan task
- **Partitions**: Bagian data yang didistribusikan ke workers
- **DataFrame**: Struktur data terdistribusi (mirip Pandas tapi scalable)

---

## Question 1: Install Spark and PySpark

### Task Explanation

Install PySpark dan membuat Spark session untuk mengecek versi Spark yang digunakan.

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

**Query Breakdown:**
1. **`SparkSession.builder`**: Membuat builder untuk konfigurasi Spark session
2. **`.master("local[*]")`**: Menjalankan Spark secara lokal menggunakan semua available cores
3. **`.appName("test")`**: Memberi nama aplikasi (muncul di Spark UI)
4. **`.getOrCreate()`**: Membuat session baru atau menggunakan yang sudah ada

**Answer:** `4.1.1`

**Reason:** Output dari `spark.version` menunjukkan versi Spark yang terinstall.

---

## Question 2: Yellow October 2024 - Repartition

### Task Explanation

Membaca data Yellow Taxi October 2024, lalu melakukan **repartition** menjadi 4 partisi dan menyimpannya kembali dalam format Parquet. Tujuannya untuk melihat ukuran file yang dihasilkan.

### Query Function

**Query (Python):**
```python
df = spark.read.parquet("yellow_tripdata_2024-10.parquet")
df.repartition(4).write.parquet("yellow_oct_2024_repartitioned")
```

**Query Breakdown:**
1. **`spark.read.parquet()`**: Membaca file parquet ke Spark DataFrame
2. **`.repartition(4)`**: Membagi data menjadi 4 partisi (file)
3. **`.write.parquet()`**: Menulis DataFrame ke format parquet

**Multiple Choice Options:**
- 6MB
- 25MB
- 75MB
- 100MB

**Answer:** **25MB**

**Reason:** Setelah repartition ke 4, setiap file parquet berukuran ~23MB. Jawaban paling mendekati adalah **25MB**.

**File size breakdown:**
```
part-00000-*.parquet: 23MB
part-00001-*.parquet: 23MB
part-00002-*.parquet: 23MB
part-00003-*.parquet: 23MB
```

---

## Question 3: Count Records on October 15th

### Task Explanation

Menghitung berapa banyak taxi trips yang terjadi pada tanggal 15 Oktober 2024. Kita perlu filter berdasarkan `tpep_pickup_datetime`.

### Query Function

**Query (Python):**
```python
from pyspark.sql.functions import col

df = spark.read.parquet("yellow_tripdata_2024-10.parquet")

df.filter(col("tpep_pickup_datetime").like("2024-10-15%")) \
  .count()
```

**Query Breakdown:**
1. **`col("tpep_pickup_datetime")`**: Membuat column reference
2. **`.like("2024-10-15%")`**: Pattern matching untuk tanggal ( `%` = wildcard)
3. **`.count()`**: Menghitung jumlah baris setelah filter

**Multiple Choice Options:**
- 85,567
- 105,567
- 125,567
- 145,567

**Answer:** **128,893** (tidak ada di opsi)

**Reason:** Filter tanggal `2024-10-15` menghasilkan **128,893 trips**. Nilai ini berada di antara opsi 125,567 dan 145,567.

---

## Question 4: Longest Trip Duration

### Task Explanation

Mencari trip terpanjang dalam satuan **jam**. Perlu menghitung selisih antara `tpep_dropoff_datetime` dan `tpep_pickup_datetime`.

### Query Function

**Query (Python):**
```python
from pyspark.sql.functions import col

df = spark.read.parquet("yellow_tripdata_2024-10.parquet")

# Convert to timestamp dan hitung durasi dalam jam
df_with_duration = df.withColumn(
    "duration_hours",
    (col("tpep_dropoff_datetime").cast("long") -
     col("tpep_pickup_datetime").cast("long")) / 3600
)

# Cari nilai maksimum
longest = df_with_duration.agg({"duration_hours": "max"}).collect()[0][0]
print(f"Longest trip: {longest:.2f} hours")
```

**Query Breakdown:**
1. **`.cast("long")`**: Mengkonversi timestamp ke epoch seconds (unix timestamp)
2. **Selisih / 3600**: Mengkonversi detik ke jam (3600 detik = 1 jam)
3. **`.agg({"duration_hours": "max"})`**: Agregasi untuk mencari nilai maksimum

**Multiple Choice Options:**
- 122
- 142
- 162
- 182

**Answer:** **162**

**Reason:** Trip terpanjang adalah **162.62 jam**, yang paling mendekati opsi **162**.

> **Note:** Trip selama ~162 jam kemungkinan adalah data anomali (mungkin taxi lupa mengakhiri trip).

---

## Question 5: Spark UI Port

### Task Explanation

Spark menyediakan **User Interface (UI)** untuk monitoring job, stages, tasks, dan storage. Pertanyaan menanyakan port default dari Spark UI.

### Query Function

Tidak perlu query. Ini adalah pengetahuan tentang Spark.

**Multiple Choice Options:**
- 80
- 443
- 4040
- 8080

**Answer:** **4040**

**Reason:** Spark UI secara default berjalan di **port 4040**. Akses via browser di `http://localhost:4040`.

**Port lain di Spark:**
| Port | Kegunaan |
|------|----------|
| 4040 | Spark UI (application) |
| 7077 | Spark Master (standalone cluster) |
| 8080 | Cluster Manager UI |
| 8081 | Worker UI |

---

## Question 6: Least Frequent Pickup Location Zone

### Task Explanation

Mencari **zone** dengan jumlah pickup **paling sedikit**. Perlu menggabungkan (join) data Yellow Taxi dengan Taxi Zone Lookup.

### Query Function

**Query (SQL):**
```sql
SELECT z.Zone, COUNT(*) as trip_count
FROM yellow y
JOIN zones z ON y.PULocationID = z.LocationID
GROUP BY z.Zone
ORDER BY trip_count ASC
LIMIT 5;
```

**Query (Python):**
```python
# Load zones
df_zones = spark.read \
    .option("header", "true") \
    .csv("taxi_zone_lookup.csv")

df_zones.createOrReplaceTempView("zones")
df_yellow.createOrReplaceTempView("yellow")

result = spark.sql("""
    SELECT z.Zone, COUNT(*) as trip_count
    FROM yellow y
    JOIN zones z ON y.PULocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY trip_count ASC
    LIMIT 1
""")
```

**Query Breakdown:**
1. **`JOIN`**: Menggabungkan dua tabel berdasarkan `LocationID`
2. **`GROUP BY z.Zone`**: Mengelompokkan berdasarkan nama zone
3. **`COUNT(*)`**: Menghitung jumlah trips per zone
4. **`ORDER BY trip_count ASC`**: Mengurutkan dari yang terkecil
5. **`LIMIT 1`**: Mengambil hanya baris pertama (paling sedikit)

**Multiple Choice Options:**
- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay

**Answer:** **Governor's Island/Ellis Island/Liberty Island**

**Reason:** Zone ini hanya memiliki **1 trip** selama Oktober 2024, paling sedikit dari semua zones.

**Top 5 Least Frequent Zones:**
| Zone | Trip Count |
|------|------------|
| Governor's Island/Ellis Island/Liberty Island | 1 |
| Rikers Island | 2 |
| Arden Heights | 2 |
| Jamaica Bay | 3 |
| Green-Wood Cemetery | 3 |

---

## Summary Table

| No | Jawaban | Key Concept |
|----|----------|-------------|
| 1 | 4.1.1 | PySpark version check |
| 2 | 25MB | Repartition mengontrol file size |
| 3 | 128,893 | Filter tanggal dengan `like()` |
| 4 | 162 | Menghitung durasi dari timestamp diff |
| 5 | 4040 | Spark UI default port |
| 6 | Governor's Island... | JOIN + GROUP BY aggregation |

---

## Resources

- **Script lengkap:** `homework5.py`
- **Submit link:** https://courses.datatalks.club/de-zoomcamp-2026/homework/hw5
- **Data source:** NYC Taxi & Limousine Commission

---

## Key Takeaways dari Module 5

1. **Spark DataFrame** = Distributed version of Pandas
2. **Repartition** = Mengontrol jumlah file output (penting untuk optimasi)
3. **Spark UI** = Tool untuk monitoring dan debugging (port 4040)
4. **Transformations** (lazy) vs **Actions** (eager) dalam Spark
5. **JOIN di Spark** = Mirip SQL tapi untuk data skala besar
