# Module 7: Streaming (Kafka/PyFlink) - Homework

## Overview
Module ini membahas tentang streaming data processing menggunakan Kafka (Redpanda) dan PyFlink. Streaming adalah teknik untuk memproses data secara real-time saat data tersebut dihasilkan, berbeda dengan batch processing yang memproses data dalam chunk tertentu.

**Konsep utama yang dipelajari:**
- **Kafka/Redpanda**: Distributed streaming platform untuk publish-subscribe messages
- **Kafka Producer**: Mengirim data ke Kafka topic
- **Kafka Consumer**: Membaca data dari Kafka topic
- **PyFlink**: Stream processing framework berbasis Apache Flink untuk Python
- **Windowing**: Membagi data stream menjadi window berdasarkan waktu
  - Tumbling window: Fixed-size, non-overlapping windows
  - Session window: Dynamic windows based on activity gaps
- **Watermark**: Mekanisme untuk menangani late data dalam event time processing
- **Event Time**: Waktu ketika event terjadi (bukan waktu diproses)

## Summary Jawaban
| No | Jawaban | File Detail |
|----|---------|------------|
| 1 | v25.3.9 | [answer_question_1.md](answer_question_1.md) |
| 2 | 60 seconds | [answer_question_2.md](answer_question_2.md) |
| 3 | 7506 | [answer_question_3.md](answer_question_3.md) |
| 4 | 75 | [answer_question_4.md](answer_question_4.md) |
| 5 | 51 | [answer_question_5.md](answer_question_5.md) |
| 6 | 2025-10-30 16:00:00 | [answer_question_6.md](answer_question_6.md) |

## Detail Jawaban

### [Question 1: Redpanda Version](answer_question_1.md)
Menentukan versi Redpanda yang berjalan di container menggunakan command `rpk version`.

### [Question 2: Sending Data to Redpanda](answer_question_2.md)
Membuat Kafka producer untuk mengirim data green taxi trip dari file parquet ke topic `green-trips` dan mengukur waktu yang dibutuhkan.

**Files:**
- `producer_green_taxi.py` - Script producer untuk mengirim data ke Kafka

### [Question 3: Consumer - Trip Distance](answer_question_3.md)
Membuat Kafka consumer untuk membaca semua message dari topic `green-trips` dan menghitung jumlah trip dengan `trip_distance` > 5.0 km.

**Files:**
- `consumer_green_taxi.py` - Script consumer untuk membaca dan menghitung data

### [Question 4: Tumbling Window - Pickup Location](answer_question_4.md)
Membuat Flink job dengan 5-minute tumbling window untuk menghitung trip per `PULocationID` dan menemukan location dengan trip terbanyak dalam satu window.

**Files:**
- `flink_job_tumbling_window.py` - Flink job untuk tumbling window aggregation

**Setup:**
```bash
# Create PostgreSQL table
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
CREATE TABLE trips_per_location_5min (
    window_start TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT,
    PRIMARY KEY (window_start, PULocationID)
);"

# Run Flink job
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/flink_job_tumbling_window.py

# Query results
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
SELECT PULocationID, num_trips
FROM trips_per_location_5min
ORDER BY num_trips DESC
LIMIT 3;"
```

### [Question 5: Session Window - Longest Streak](answer_question_5.md)
Membuat Flink job dengan session window (5-minute gap) untuk menemukan session terpanjang (trip terbanyak dalam satu session) per `PULocationID`.

**Files:**
- `flink_job_session_window.py` - Flink job untuk session window aggregation

**Setup:**
```bash
# Create PostgreSQL table
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
CREATE TABLE session_window_results (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    PULocationID INT,
    session_id STRING,
    num_trips BIGINT,
    PRIMARY KEY (window_start, PULocationID)
);"

# Run Flink job
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/flink_job_session_window.py

# Query results
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
SELECT PULocationID, num_trips, window_start, window_end
FROM session_window_results
ORDER BY num_trips DESC
LIMIT 1;"
```

### [Question 6: Tumbling Window - Largest Tip](answer_question_6.md)
Membuat Flink job dengan 1-hour tumbling window untuk menghitung total tip amount per jam dan menemukan jam dengan total tip tertinggi.

**Files:**
- `flink_job_hourly_tips.py` - Flink job untuk hourly tip aggregation

**Setup:**
```bash
# Create PostgreSQL table
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
CREATE TABLE hourly_tip_totals (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    total_tip DOUBLE,
    PRIMARY KEY (window_start)
);"

# Run Flink job
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/flink_job_hourly_tips.py

# Query results
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
SELECT window_start, total_tip
FROM hourly_tip_totals
ORDER BY total_tip DESC
LIMIT 1;"
```

## Resources

| Resource | Link |
|----------|------|
| Submit Homework | https://courses.datatalks.club/de-zoomcamp-2026/homework/hw7 |
| Module Materials | /mnt/b/DE_Zoomcamp/data-engineering-zoomcamp/07-streaming/ |
| Workshop Materials | /mnt/b/DE_Zoomcamp/data-engineering-zoomcamp/07-streaming/workshop/ |

## Tech Stack

### Infrastructure
- **Docker**: Containerization untuk menjalankan semua services
- **Redpanda**: Kafka-compatible streaming platform (drop-in replacement untuk Kafka)
- **PostgreSQL**: Database untuk menyimpan hasil aggregation

### Python Libraries
- **kafka-python**: Kafka producer dan consumer client untuk Python
- **pandas**: Data manipulation dan parquet file reading
- **PyFlink**: Stream processing framework dari Apache Flink untuk Python

### Data Format
- **Parquet**: Columnar storage format untuk input data
- **JSON**: Format message untuk Kafka topic

## Key Concepts Applied

### 1. Kafka Producer Pattern
```python
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)
producer.send('topic', value=message)
producer.flush()  # Ensure all messages sent
```

### 2. Kafka Consumer Pattern
```python
consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # Start from beginning
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
```

### 3. Flink Source Table with Kafka
```sql
CREATE TABLE source (
    event_timestamp AS TO_TIMESTAMP(timestamp_col, 'yyyy-MM-dd HH:mm:ss'),
    WATERMARK for event_timestamp as event_timestamp - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'topic-name',
    'format' = 'json'
);
```

### 4. Flink Windowing
- **Tumbling Window**: Fixed-size windows yang tidak overlap
```sql
TUMBLE(TABLE source, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTES)
```

- **Session Window**: Dynamic windows berdasarkan activity gaps
```sql
SESSION(event_timestamp, INTERVAL '5' MINUTES)
```

### 5. Flink Aggregation with Window
```sql
INSERT INTO sink_table
SELECT
    window_start,
    key_column,
    COUNT(*) AS num_events,
    SUM(metric) AS total_metric
FROM TABLE(TUMBLE(...))
GROUP BY window_start, key_column;
```

## Important Notes

### Parallelism
Flink jobs harus menggunakan `env.set_parallelism(1)` karena:
- Topic `green-trips` hanya memiliki 1 partition
- Parallelism > 1 akan menyebabkan idle consumer subtasks
- Watermark tidak akan advance dengan subtasks yang idle

### Watermark
Watermark digunakan untuk:
- Menangani out-of-order events
- Menentukan kapan window harus ditutup
- Interval watermark memberikan toleransi untuk late data

### Event Time vs Processing Time
- **Event Time**: Waktu ketika event sebenarnya terjadi
- **Processing Time**: Waktu ketika event diproses oleh system
- Stream processing sebaiknya menggunakan event time untuk accuracy
