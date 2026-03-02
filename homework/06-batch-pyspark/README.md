# Module 6: Batch Processing with PySpark - Homework

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

## Summary Jawaban

| No | Jawaban | File Detail |
|----|---------|------------|
| 1 | `4.1.1` | [answer_question_1.md](answer_question_1.md) |
| 2 | **25MB** | [answer_question_2.md](answer_question_2.md) |
| 3 | **162,604** | [answer_question_3.md](answer_question_3.md) |
| 4 | **90.6** | [answer_question_4.md](answer_question_4.md) |
| 5 | **4040** | [answer_question_5.md](answer_question_5.md) |
| 6 | **Governor's Island/Ellis Island/Liberty Island** | [answer_question_6.md](answer_question_6.md) |

---

## Detail Jawaban

Lihat file individual untuk penjelasan lengkap setiap pertanyaan:

1. [Question 1: Install Spark and PySpark](answer_question_1.md)
2. [Question 2: Yellow November 2025 - Repartition](answer_question_2.md)
3. [Question 3: Count Records on November 15th](answer_question_3.md)
4. [Question 4: Longest Trip Duration](answer_question_4.md)
5. [Question 5: Spark UI Port](answer_question_5.md)
6. [Question 6: Least Frequent Pickup Location Zone](answer_question_6.md)

---

## Resources

| Resource | Link |
|----------|------|
| **Submit** | https://courses.datatalks.club/de-zoomcamp-2026/homework/hw6 |
| **Script** | `homework6_nov2025.py` |
| **Data source** | NYC Taxi & Limousine Commission |
| **Module materials** | `data-engineering-zoomcamp/06-batch/` |

---

## Key Takeaways

1. **Spark DataFrame** = Distributed version of Pandas
2. **Repartition** = Mengontrol jumlah file output (penting untuk optimasi)
3. **Spark UI** = Tool untuk monitoring dan debugging (port 4040)
4. **Transformations** (lazy) vs **Actions** (eager) dalam Spark
5. **JOIN di Spark** = Mirip SQL tapi untuk data skala besar
6. **Spark 4.x**: Gunakan `unix_timestamp()` untuk TIMESTAMP_NTZ, bukan `cast("long")`
