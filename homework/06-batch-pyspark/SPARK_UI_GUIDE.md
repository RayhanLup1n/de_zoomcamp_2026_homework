# Panduan Membaca Spark UI

**Panduan ini untuk membantu kamu memahami Spark UI** dengan bahasa yang mudah dipahami.

---

## ⚠️ PENTING: Spark UI vs Kestra UI

Sebelum mulai, pahami dulu perbedaan mendasar:

| Aspek | Kestra UI | Spark UI |
|--------|-----------|----------|
| **Purpose** | Orkestrasi workflow | Monitoring job execution |
| **Desain** | User-friendly, banyak penjelasan | Minimalis, teknikal |
| **Job Info** | Ada deskripsi manual, nama custom | Otomatis dari action, generic |
| **Level** | High-level (workflow) | Low-level (task execution) |

**Kenapa Spark UI tidak jelas seperti Kestra?**
- Spark UI **otomatis** berdasarkan action yang dipanggil (`count()`, `show()`, dll)
- Tidak ada mekanisme untuk menambahkan deskripsi manual
- Nama job otomatis seperti "collect at Homework6.py:123"
- Ini sifat bawaan Spark, bukan bug!

---

## 📋 Apa itu Spark UI?

**Spark UI** adalah dashboard monitoring bawaan dari Spark yang menunjukkan:
- ✅ Job apa yang sedang/sudah berjalan
- ✅ Bagaimana job dipecah menjadi stages dan tasks
- ✅ Resource usage (memory, CPU)
- ✅ Execution time dan performance metrics

**Analogi:**
- **Kestra UI** = Orkestrator workflow (seperti project manager)
- **Spark UI** = Monitoring saat job berjalan (seperti task manager untuk distributed computing)

---

## 🌐 Cara Mengakses Spark UI

### 1. Jalankan Script Spark
```bash
# Jalankan homework script
cd /mnt/b/DE_Zoomcamp/builder_rayhanAnanda/homework/06-batch-pyspark
uv run python homework6.py
```

### 2. Buka Browser
Saat script berjalan, buka:
```
http://localhost:4040
```

### 3. Penting!
- **Jangan stop script** (jangan tekan Ctrl+C) saat mau lihat UI
- Script akan **keep session alive** sampai kamu tekan Ctrl+C
- UI akan hilang kalau script berhenti

---

## 📊 Tab-Tab di Spark UI

### 1. Jobs Tab (Tab Utama)

**URL:** `http://localhost:4040/jobs/`

**Apa yang ditampilkan:**
- Semua job yang telah dijalankan
- Status job (SUCCEEDED, FAILED, RUNNING)
- Duration (berapa lama job berjalan)
- Tasks yang dijalankan

**Cara baca:**
```
Job Name                 | Status     | Duration | Tasks
-------------------------|------------|----------|------
count at Homework6.py:82 | SUCCEEDED  | 2.1s     | 4/4
show at Homework6.py:88   | SUCCEEDED  | 0.3s     | 4/4
write at Homework6.py:39  | SUCCEEDED  | 1.5s     | 4/4
```

**Penjelasan kolom:**
- **Job Name**: Nama job otomatis (berdasarkan action yang dipakai)
  - Format: `count at Homework6.py:line_number`
  - Ini artinya: Action `count()` dipanggil di line 82
- **Status**: SUCCEEDED (sukses), FAILED (gagal), RUNNING (sedang berjalan)
- **Duration**: Berapa lama job selesai (semakin kecil semakin baik)
- **Tasks**: Jumlah task yang selesai (misal 4/4 berarti semua selesai)

**Apa artinya?**
- Setiap `action` di PySpark (`count()`, `show()`, `write()`) membuat 1 job
- Job yang sukses = tanda code kamu berjalan dengan benar

**⚠️ TIDAK ADA DESKRIPSI MANUAL!**
- Kamu TIDAK bisa menambahkan deskripsi ke job di Spark UI
- Job name selalu otomatis dari nama action dan line number
- Kalau mau tau apa job ini doing, lihat kode di line number tersebut!

---

### 💡 CARA NAVIGASI YANG BENAR

**❌ SALAH:**
- Klik pada judul job name
- Klik pada link di deskripsi

**✅ BENAR:**
1. Buka Jobs Tab
2. Cari job yang mau dilihat detailnya
3. **KLIK pada ID Job** (misal: `job-0`, `job-1`, dll)
4. Lihat detail job termasuk:
   - SQL query (kalau job dari SQL)
   - Stages breakdown
   - Task details
5. Klik "Stages" atau "SQL" untuk lihat lebih detail

**Contoh:**
```
Jobs Tab:
ID   | Job Name                    | Status
------|-----------------------------|-------
job-0 | count at Homework6.py:82   | SUCCEEDED  ← Klik ID job-0
job-1 | show at Homework6.py:88     | SUCCEEDED
job-2 | write at Homework6.py:39   | SUCCEEDED
```

Klik pada `job-0`, bukan pada "count at Homework6.py:82"

---

### 2. Stages Tab

**URL:** `http://localhost:4040/stages/`

**Apa yang ditampilkan:**
- Breakdown job menjadi stages
- Detail execution per stage
- Task metrics (input, output, shuffle)

**Konsep Job vs Stage vs Task:**
```
JOB (Action: count())
  ├─ STAGE 1: filter + select (map side)
  │   ├─ TASK 1 (partition 0)
  │   ├─ TASK 2 (partition 1)
  │   ├─ TASK 3 (partition 2)
  │   └─ TASK 4 (partition 3)
  └─ STAGE 2: aggregate (reduce side, after shuffle)
      ├─ TASK 1
      ├─ TASK 2
      ├─ TASK 3
      └─ TASK 4
```

**Penjelasan:**
- **Job**: 1 action (misalnya `count()`)
- **Stage**: Bagian job yang dijalankan secara parallel
  - Stage boundary = shuffle operation (join, groupBy, repartition)
- **Task**: Unit kerja smallest di Spark (per partition)

**Cara baca:**
- Jumlah stages = seberapa komplek job kamu
- Lebih banyak stages = lebih banyak shuffle = lebih lambat
- Duration per stage = mana yang paling lambat (bottleneck)

---

### 3. Storage Tab

**URL:** `http://localhost:4040/storage/`

**Apa yang ditampilkan:**
- Data yang di-cache di memory
- Fraction cached (berapa persen)
- Size in memory/disk
- Number of partitions

**Apa itu Cache?**
```python
df.cache()  # Simpan DataFrame di memory
```

**Cara baca:**
```
Cached Table   | Fraction | Size in Memory | Size in Disk | Partitions
---------------|----------|----------------|--------------|----------
taxi_trips     | 100%     | 85.5 MB        | 0 B          | 4
```

**Penjelasan:**
- **Cached Table**: Nama DataFrame yang di-cache
- **Fraction**: Berapa persen data yang tersimpan di memory
- **Size in Memory**: Ukuran data di memory (semakin besar semakin banyak memory dipakai)
- **Partitions**: Jumlah partisi data yang di-cache

**Apa artinya?**
- Kalau `Fraction < 100%` = tidak semua data muat di memory
- Kalau `Size in Disk > 0` = data overflow ke disk (lebih lambat)
- Cache bagus untuk data yang sering dipakai berulang

---

### 4. SQL Tab

**URL:** `http://localhost:4040/SQL/`

**Apa yang ditampilkan:**
- Query execution plan (DAG - Directed Acyclic Graph)
- Cara Spark meng-optimalkan query kamu
- Visual breakdown dari query

**Cara baca:**
Klik pada job yang menggunakan SQL, maka akan muncul:

```
Query 1: SELECT COUNT(*) FROM taxi_trips

Logical Plan:
   Aggregate [COUNT(*)] ───► Final result
   └── Scan taxi_trips    ───► Read data

Physical Plan:
   *HashAggregate ───► Grouping
   └── *Scan parquet ───► Read from file
```

**Apa artinya?**
- Spark akan optimalkan query kamu secara otomatis
- `*` = operator yang akan dijalankan di cluster
- Spark bisa push-down filter ke storage layer (lebih cepat)

**Visual DAG (Directed Acyclic Graph):**
```
[Scan] → [Filter] → [Project] → [Aggregate] → [Result]
```
- Setiap kotak = operator
- Arrow = data flow
- Spark akan cari cara tercepat untuk jalankan query ini

---

### 5. Executors Tab

**URL:** `http://localhost:4040/executors/`

**Apa yang ditampilkan:**
- Resource usage per executor
- Active tasks, completed tasks, failed tasks
- Memory usage

**Cara baca:**
```
ID   | Active Tasks | Completed Tasks | Failed Tasks | Memory Used | Disk Used
-----|--------------|-----------------|--------------|-------------|----------
0    | 0            | 12              | 0             | 1.2 GB      | 0 B
1    | 0            | 12              | 0             | 1.2 GB      | 0 B
2    | 0            | 12              | 0             | 1.2 GB      | 0 B
3    | 0            | 12              | 0             | 1.2 GB      | 0 B
```

**Penjelasan:**
- **ID**: Executor ID (setiap executor = 1 worker process)
- **Active Tasks**: Task yang sedang berjalan saat ini
- **Completed Tasks**: Task yang sudah selesai
- **Failed Tasks**: Task yang gagal (harus 0)
- **Memory Used**: Memory yang dipakai executor
- **Disk Used**: Disk yang dipakai untuk shuffle data

**Apa artinya?**
- `Failed Tasks > 0` = ada masalah (out of memory, data skew, dll)
- `Memory Used` dekat limit = mungkin OOM (out of memory)
- `Disk Used > 0` = shuffle data overflow ke disk (lebih lambat)

---

### 6. Environment Tab

**URL:** `http://localhost:4040/environment/`

**Apa yang ditampilkan:**
- Spark configuration
- Runtime information
- Java version, Scala version
- System properties

**Yang penting:**
- `spark.master`: `local[*]` = local mode
- `spark.app.name`: Nama aplikasi Spark kamu
- `spark.executor.memory`: Memory per executor
- `spark.driver.memory`: Memory untuk driver
- `spark.sql.shuffle.partitions`: Default partitions untuk shuffle

**Apa artinya?**
- Kalau `spark.master = local[*]` = berjalan di single machine
- Kalau `spark.master = yarn` = berjalan di cluster Hadoop
- Config ini bisa di-set saat create SparkSession

---

## 🎯 Perbandingan: Kestra UI vs Spark UI

| Fitur | Kestra UI | Spark UI |
|--------|-----------|----------|
| **Purpose** | Orkestrasi workflow | Monitoring job execution |
| **View** | DAG workflow | Job, Stage, Task breakdown |
| **Timeline** | Schedule & triggers | Real-time execution |
| **Metrics** | Success/failure rate | Resource usage, latency |
| **Level** | High-level (workflow) | Low-level (task execution) |
| **Use case** | Schedule & retry jobs | Debug & optimize performance |

**Analogi:**
- **Kestra UI** = Project Manager (manage overall workflow)
- **Spark UI** = Task Manager (monitor detailed execution)

---

## 💡 Tips Membaca Spark UI

### 1. Identifikasi Bottleneck
- Lihat **Stages Tab**
- Cari stage dengan duration terlama
- Itu adalah bottleneck code kamu

### 2. Cek Data Skew
- Lihat **Stages Tab**
- Klik stage → lihat "Tasks"
- Kalau ada task yang jauh lebih lama = data skew

### 3. Optimize Memory
- Lihat **Storage Tab**
- Kalau fraction < 100%, increase memory
- Kalau disk used > 0, reduce partitions or increase memory

### 4. Check Failed Tasks
- Lihat **Stages Tab** → **Tasks**
- Kalau ada failed tasks, klik untuk lihat error message

### 5. Monitor Shuffle
- Lihat **Stages Tab**
- Cari stages dengan shuffle (ada shuffle read/write)
- Shuffle = expensive operation, minimize kalau bisa

---

## 📸 Screenshot untuk LinkedIn

**Tab-tab yang bagus untuk screenshot:**

### 1. Jobs Tab
- Menunjukkan semua job yang selesai
- Menunjukkan success rate
- Good untuk: "I processed X jobs successfully!"

### 2. Storage Tab
- Menunjukkan data di-cache
- Menunjukkan Spark capability
- Good untuk: "I cached X GB of data in memory!"

### 3. SQL Tab
- Menunjukkan query plan
- Menunjukkan Spark optimization
- Good untuk: "Spark optimized my queries!"

### 4. Stages Tab
- Menunjukkan parallel processing
- Menunjukkan task breakdown
- Good untuk: "Distributed processing in action!"

### 5. Executors Tab
- Menunjukkan resource usage
- Menunjukkan cluster utilization
- Good untuk: "Efficient resource usage!"

---

## ❓ Pertanyaan Umum (FAQ)

### Q: Spark UI tidak bisa diakses?
**A:**
- Pastikan script masih berjalan (jangan stop)
- Cek firewall settings
- Coba port lain: `.config("spark.ui.port", "4041")`
- Port 4040 sudah dipakai, otomatis ke 4041

### Q: UI terlalu banyak info, mana yang penting?
**A:** Fokus pada:
1. **Jobs Tab**: Apakah job sukses?
2. **Stages Tab**: Mana yang paling lama?
3. **Storage Tab**: Apakah cache muat di memory?

### Q: Sama seperti Kestra UI gak?
**A:** SANGAT BERBEDA!
- **Kestra** = Schedule dan manage workflow dengan deskripsi manual
- **Spark** = Monitor execution secara teknikal, otomatis dari action
- Kestra lebih user-friendly, Spark lebih teknikal
- Kestra bisa trigger Spark job, tapi beda fungsi

### Q: Kenapa job name tidak jelas seperti Kestra?
**A:** Ini sifat Spark!
- Kestra: Kamu bisa custom job name dan deskripsi
- Spark: Job name otomatis dari action + line number
- Tidak bisa dikustomisasi
- Spark fokus ke **performance monitoring**, bukan documentation

### Q: Kalau job failed, gimana cek errornya?
**A:**
1. Buka **Jobs Tab**
2. **KLIK ID job** yang failed (bukan judul!)
3. Lihat error message di detail view
4. Buka **Stages Tab** → klik failed stage → cek task details

### Q: Klik job malah ke resource usage?
**A:** Kamu klik di tempat yang salah!
- ❌ Jangan klik di judul job
- ✅ Klik pada ID job (job-0, job-1, dll)
- ID biasanya ada di kolom paling kiri

### Q: Logs terlalu banyak, bisa dikurangi?
**A:** Sudah saya fix di script! Sekarang:
- Logs dikurangi ke ERROR level saja
- WARNING dan INFO di-hide
- Output lebih bersih

---

## 🚀 Next Steps

1. ✅ Jalankan `homework6.py`
2. ✅ Buka Spark UI di `http://localhost:4040`
3. ✅ Eksplorasi setiap tab
4. ✅ Baca metrics dan pahami artinya
5. ✅ Capture screenshot untuk LinkedIn
6. ✅ Coba optimalkan code berdasarkan metrics

---

**Happy Monitoring! 📊**

Ingat: Spark UI adalah tool untuk **debug dan optimize** performance, bukan sekadar untuk "lihat-lihat". Semakin sering kamu cek, semakin mengerti cara kerja Spark!
