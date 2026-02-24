# Module 5: Data Platforms with Bruin - Homework

## Overview

Module ini membahas tentang **Data Platforms** menggunakan **Bruin** - unified data pipeline framework yang menggabungkan data ingestion, transformation, orchestration, dan data quality dalam satu tool.

### Apa itu Bruin?

Bruin adalah open-source tool yang menggabungkan:
- **Data ingestion** - 100+ connectors via ingestr
- **Data transformation** - SQL, Python, R
- **Data orchestration** - Scheduling & dependency management
- **Data quality** - Built-in checks & validation
- **Metadata management** - Lineage & documentation

**Analogi:** "Airbyte + Airflow + dbt + Great Expectations dalam satu tool"

---

## Summary Answers

| No | Pertanyaan | Jawaban |
|----|------------|---------|
| 1 | Bruin Pipeline Structure | `.bruin.yml` and `pipeline.yml` (assets can be anywhere) |
| 2 | Materialization Strategy | `time_interval` - incremental based on a time column |
| 3 | Override Variables | `bruin run --var 'taxi_types=["yellow"]'` |
| 4 | Run with Dependencies | `bruin run --select ingestion.trips+` |
| 5 | Quality Check for NULL | `name: not_null` |
| 6 | Lineage Command | `bruin lineage` |
| 7 | First-Time Run Flag | `--full-refresh` |

---

## Project Structure

```
project/
├── .bruin.yml              # Environments & connections (REQUIRED)
├── pipeline.yml            # Pipeline definition (REQUIRED)
└── assets/                 # Asset files
    ├── ingestion/          # Layer 1: Data ingestion
    ├── staging/            # Layer 2: Cleaning & transformation
    └── reports/            # Layer 3: Aggregation & analytics
```

---

## Question 1: Bruin Pipeline Structure

### Task Explanation

Bruin project membutuhkan file/directory tertentu agar bisa berjalan. Pertanyaan ini menanyakan komponen **wajib** (required) dalam Bruin project.

### Query Function

**Required Files:**
- `.bruin.yml` - Environment & connection configuration (di root directory)
- `pipeline.yml` - Pipeline name, schedule, variables (di `pipeline/` atau root)
- `assets/` - Folder berisi asset files (SQL, Python, YAML)

**Breakdown:**
1. **`.bruin.yml`**: Menyimpan konfigurasi environment (dev, staging, prod) dan connections ke database/API. Harus ada di root directory dan **gitignored**.
2. **`pipeline.yml`**: Menyimpan pipeline configuration seperti name, schedule, start_date, default_connections, dan variables.
3. **`assets/`**: Folder berisi file-file asset. Bisa ditaruh di mana saja selama terdeteksi oleh git.

**Multiple Choice Options:**
- `bruin.yml` and `assets/`
- `.bruin.yml` and `pipeline.yml` (assets can be anywhere)
- `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`
- `pipeline.yml` and `assets/` only

**Answer:** **`.bruin.yml` and `pipeline.yml` (assets can be anywhere)**

**Reason:**
- `.bruin.yml` wajib ada di root untuk environment & connections
- `pipeline.yml` wajib ada untuk pipeline configuration
- `assets/` bisa ditaruh di mana saja (default: next to `pipeline.yml`)

---

## Question 2: Materialization Strategies

### Task Explanation

NYC taxi data diorganisir berdasarkan `pickup_datetime`. Pertanyaan ini menanyakan materialization strategy terbaik untuk incremental processing dengan delete+insert per time period.

### Query Function

**Materialization Configuration:**
```yaml
materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
```

**Breakdown:**
1. **`type: table`**: Simpan hasil sebagai table (bukan view)
2. **`strategy: time_interval`**: Incremental processing berdasarkan rentang waktu
3. **`incremental_key: pickup_datetime`**: Kolom yang digunakan untuk menentukan window waktu

**Multiple Choice Options:**
- `append` - always add new rows
- `replace` - truncate and rebuild entirely
- `time_interval` - incremental based on a time column
- `view` - create a virtual table only

**Answer:** **`time_interval` - incremental based on a time column**

**Reason:**
- `time_interval` dirancang khusus untuk time-series data
- Strategy ini akan delete data dalam rentang waktu yang diproses, lalu insert data baru
- Cocok untuk NYC taxi data yang diorganisir berdasarkan `pickup_datetime`
- Hindari duplikasi untuk rerun di tanggal yang sama

**Strategy Comparison:**

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `append` | Selalu tambah row baru | Log data, never delete |
| `replace` | Truncate + rebuild seluruh table | Full refresh |
| `time_interval` | Delete + insert per time window | Time-series data |
| `view` | Virtual table saja | Aggregation layer |

---

## Question 3: Pipeline Variables

### Task Explanation

Pipeline variables digunakan untuk parameterize pipeline. Pertanyaan ini menanyakan cara override variable `taxi_types` saat run.

### Query Function

**Variable Definition (pipeline.yml):**
```yaml
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

**Override Command:**
```bash
bruin run . --var 'taxi_types=["yellow"]'
```

**Breakdown:**
1. **`--var`**: Flag untuk override variable
2. **`'taxi_types=["yellow"]'`**: Format JSON array sebagai string value

**Multiple Choice Options:**
- `bruin run --taxi-types yellow`
- `bruin run --var taxi_types=yellow`
- `bruin run --var 'taxi_types=["yellow"]'`
- `bruin run --set taxi_types=["yellow"]`

**Answer:** **`bruin run --var 'taxi_types=["yellow"]'`**

**Reason:**
- Format yang benar adalah `--var 'key=value'`
- Value harus dalam format JSON karena `taxi_types` didefinisikan sebagai array
- Single quotes diperlukan agar shell tidak menginterpretasi bracket

**Usage in Assets:**

SQL:
```sql
WHERE taxi_type IN {{ var.taxi_types }}
```

Python:
```python
import os, json
vars = json.loads(os.environ.get("BRUIN_VARS", "{}"))
taxi_types = vars.get("taxi_types", [])
```

---

## Question 4: Running with Dependencies

### Task Explanation

Setelah memodifikasi `ingestion/trips.py`, kita ingin menjalankannya beserta semua downstream assets. Pertanyaan ini menanyakan command yang tepat.

### Query Function

**Command:**
```bash
bruin run --select ingestion.trips+
```

**Breakdown:**
1. **`--select`**: Flag untuk memilih asset tertentu
2. **`ingestion.trips`**: Nama asset (dot notation)
3. **`+`**: Include semua downstream dependencies

**Multiple Choice Options:**
- `bruin run ingestion.trips --all`
- `bruin run ingestion/trips.py --downstream`
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+`

**Answer:** **`bruin run --select ingestion.trips+`**

**Reason:**
- `--select` dengan notation `+` adalah cara resmi untuk run asset + downstream
- `ingestion.trips` menggunakan dot notation (asset path dengan titik)
- `+` berarti include semua downstream dependencies

**Dependency Graph Example:**
```
ingestion.payment_lookup
    ↓
ingestion.trips
    ↓
staging.trips
    ↓
reports.trips_report
```

Jika run `bruin run --select ingestion.trips+`, semua asset dari `ingestion.trips` ke bawah akan dijalankan.

---

## Question 5: Quality Checks

### Task Explanation

Data quality check penting untuk memastikan integritas data. Pertanyaan ini menanyakan check yang tepat untuk memastikan kolom tidak memiliki NULL values.

### Query Function

**Column Definition:**
```sql
columns:
  - name: pickup_datetime
    type: timestamp
    primary_key: true
    checks:
      - name: not_null
```

**Breakdown:**
1. **`name: pickup_datetime`**: Nama kolom
2. **`type: timestamp`**: Tipe data
3. **`checks`**: Array of quality checks
4. **`name: not_null`**: Check untuk memastikan tidak ada NULL values

**Multiple Choice Options:**
- `name: unique`
- `name: not_null`
- `name: positive`
- `name: accepted_values, value: [not_null]`

**Answer:** **`name: not_null`**

**Reason:**
- `not_null` adalah built-in check untuk memastikan kolom tidak memiliki NULL values
- `unique` untuk memastikan semua nilai unik
- `positive` untuk memastikan nilai > 0
- `accepted_values` untuk memastikan nilai ada dalam list tertentu

**Built-in Checks:**

| Check | Description | Example Use |
|-------|-------------|-------------|
| `not_null` | Tidak boleh NULL | Primary keys, required fields |
| `unique` | Harus unik | ID, email |
| `positive` | Harus > 0 | Amount, count |
| `non_negative` | Harus >= 0 | Quantity, duration |
| `accepted_values` | Harus dalam list | Status, category |

---

## Question 6: Lineage and Dependencies

### Task Explanation

Lineage memvisualisasikan dependency graph antar assets. Pertanyaan ini menanyakan command untuk melihatnya.

### Query Function

**Command:**
```bash
bruin lineage assets/ingestion/trips.py
```

**Breakdown:**
1. **`bruin lineage`**: Command untuk melihat dependency graph
2. **`assets/ingestion/trips.py`**: Path ke asset yang ingin dilihat lineagenya

**Multiple Choice Options:**
- `bruin graph`
- `bruin dependencies`
- `bruin lineage`
- `bruin show`

**Answer:** **`bruin lineage`**

**Reason:**
- `bruin lineage` adalah command resmi untuk melihat dependency graph
- Menampilkan upstream (dependencies) dan downstream (dependents)

**Example Output:**
```
UPSTREAM:
  - ingestion.payment_lookup

DOWNSTREAM:
  - staging.trips
  - reports.trips_report
```

---

## Question 7: First-Time Run

### Task Explanation

Saat pertama kali menjalankan pipeline pada database baru, perlu membuat tabel dari awal. Pertanyaan ini menanyakan flag yang tepat.

### Query Function

**Command:**
```bash
bruin run . --full-refresh
```

**Breakdown:**
1. **`bruin run .`**: Jalankan seluruh pipeline
2. **`--full-refresh`**: Flag untuk create/replace tables from scratch

**Multiple Choice Options:**
- `--create`
- `--init`
- `--full-refresh`
- `--truncate`

**Answer:** **`--full-refresh`**

**Reason:**
- `--full-refresh` akan truncate dan rebuild tables from scratch
- Cocok untuk first-time run atau saat ingin refresh seluruh data

**Common Flags:**

| Flag | Purpose |
|------|---------|
| `--full-refresh` | Create/replace tables from scratch |
| `--only checks` | Run quality checks only |
| `--downstream` | Run asset + downstream |
| `--start-date` | Set start date untuk incremental run |
| `--end-date` | Set end date untuk incremental run |
| `--var` | Override variable |

---

## Resources

- **Submit Link:** https://courses.datatalks.club/de-zoomcamp-2026/homework/hw5
- **Bruin Docs:** https://getbruin.com/docs
- **Bruin GitHub:** https://github.com/bruin-data/bruin
- **Zoomcamp Template:** https://github.com/bruin-data/bruin/tree/main/templates/zoomcamp
- **Module README:** `/mnt/b/DE_Zoomcamp/data-engineering-zoomcamp_1/05-data-platforms/README.md`

---

## Learning Notes

Lihat catatan pembelajaran lengkap di:
`/mnt/b/DE_Zoomcamp/builder_rayhanAnanda/learn/06-data-platform-bruin/notes.md`

---

## Session Documentation

Dokumentasi sesi belajar:
`/mnt/b/DE_Zoomcamp/builder_rayhanAnanda/docs/2026-02-24-module-5-bruin.md`
