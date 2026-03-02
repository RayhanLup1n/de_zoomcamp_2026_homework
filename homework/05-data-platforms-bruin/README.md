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

## Summary Jawaban

| No | Jawaban | File Detail |
|----|---------|------------|
| 1 | `.bruin.yml` and `pipeline.yml` (assets can be anywhere) | [answer_question_1.md](answer_question_1.md) |
| 2 | `time_interval` - incremental based on a time column | [answer_question_2.md](answer_question_2.md) |
| 3 | `bruin run --var 'taxi_types=["yellow"]'` | [answer_question_3.md](answer_question_3.md) |
| 4 | `bruin run --select ingestion.trips+` | [answer_question_4.md](answer_question_4.md) |
| 5 | `name: not_null` | [answer_question_5.md](answer_question_5.md) |
| 6 | `bruin lineage` | [answer_question_6.md](answer_question_6.md) |
| 7 | `--full-refresh` | [answer_question_7.md](answer_question_7.md) |

---

## Detail Jawaban

Lihat file individual untuk penjelasan lengkap setiap pertanyaan:

1. [Question 1: Bruin Pipeline Structure](answer_question_1.md)
2. [Question 2: Materialization Strategies](answer_question_2.md)
3. [Question 3: Pipeline Variables](answer_question_3.md)
4. [Question 4: Running with Dependencies](answer_question_4.md)
5. [Question 5: Quality Checks](answer_question_5.md)
6. [Question 6: Lineage and Dependencies](answer_question_6.md)
7. [Question 7: First-Time Run](answer_question_7.md)

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

## Resources

| Resource | Link |
|----------|------|
| **Submit** | https://courses.datatalks.club/de-zoomcamp-2026/homework/hw5 |
| **Bruin Docs** | https://getbruin.com/docs |
| **Bruin GitHub** | https://github.com/bruin-data/bruin |
| **Module materials** | `data-engineering-zoomcamp_1/05-data-platforms/` |
