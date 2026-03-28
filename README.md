# Data Engineering Zoomcamp - Homework & Learning

This repository contains my personal journey, exercises, and homework solutions for the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) program.

---

## 🚀 Course Progress

| Module | Topic | Status | Homework |
|--------|-------|--------|----------|
| 1 | Docker, SQL, Terraform & GCP | ✅ Completed | [Link](./homework/01-docker-sql-terraform-gcp-homework/) |
| 2 | Workflow Orchestration (Kestra) | ✅ Completed | [Link](./homework/02-workflow-orchestration-homework/) |
| 3 | Data Warehouse (BigQuery) | ✅ Completed | [Link](./homework/03-data-warehouse/) |
| 4 | Analytics Engineering (dbt) | ✅ Completed | [Link](./homework/04-analytics-engineering/) |
| 5 | Data Platforms (Bruin) | ✅ Completed | [Link](./homework/05-data-platforms-bruin/) |
| 6 | Batch Processing (PySpark) | ✅ Completed | [Link](./homework/06-batch-pyspark/) |
| 7 | Streaming (Kafka/PyFlink) | ✅ Completed | [Link](./homework/07-streaming/) |
| WS | Workshop 1: DLT Ingestion | ✅ Completed | [Link](./workshop/01-dlt-workshop/) |
| 8-9 | Projects | ⏳ Pending | - |

---

## 📁 Repository Structure

```
builder_rayhanAnanda/
|
├── homework/                    # Official homework solutions
│   ├── 01-docker-sql-terraform-gcp-homework/
│   ├── 02-workflow-orchestration-homework/
│   ├── 03-data-warehouse/
│   ├── 04-analytics-engineering/
│   ├── 05-data-platforms-bruin/
│   ├── 06-batch-pyspark/
│   └── 07-streaming/             # Kafka/PyFlink streaming
│
├── workshop/                    # Workshop solutions
│   └── 01-dlt-workshop/         # DLT Ingestion Workshop
│
├── learn/                       # Learning notes & materials
│   ├── 01-docker-sql-terraform/
│   ├── 02-workflow-orchestration/
│   ├── 03-data-warehouse/
│   ├── 04-analytics-engineering/
│   ├── 05-batch-pyspark/
│   └── 06-data-platform-bruin/
│
├── docs/                        # Session documentation
│   ├── overview.md
│   ├── 2026-02-24-module-5-bruin.md
│   ├── 2026-03-02-module-6-pyspark.md
│   ├── 2026-03-02-workshop-dlt.md
│   └── module_07_streaming_homework.md
│
└── .venv/                       # Virtual environment (uv)
```

---

## 🛠️ Tech Stack & Tools

| Category | Tools |
|----------|-------|
| **Infrastructure** | Google Cloud Platform (GCP) |
| **Orchestration** | Kestra, Bruin |
| **Data Ingestion** | dlt, Bruin/ingestr |
| **Batch Processing** | PySpark, Apache Spark |
| **Stream Processing** | Kafka, Redpanda, PyFlink |
| **Data Warehouse** | BigQuery, DuckDB |
| **Transformation** | dbt, SQL |
| **IaC** | Terraform |
| **Containerization** | Docker & Docker Compose |
| **Programming** | Python 3.13 (managed by [uv](https://github.com/astral-sh/uv)) |
| **Database** | PostgreSQL |
| **Management Tools** | pgAdmin, pgcli |

---

## 📝 Module Overviews

### Module 1: Docker, SQL, Terraform & GCP
- Docker containerization fundamentals
- PostgreSQL database operations
- Terraform for infrastructure as code
- Google Cloud Platform setup

### Module 2: Workflow Orchestration (Kestra)
- Kestra fundamentals and configuration
- Workflow definitions and dependencies
- Running data pipelines with Kestra UI

### Module 3: Data Warehouse (BigQuery)
- BigQuery fundamentals
- Data loading from GCS to BigQuery
- SQL queries and aggregations

### Module 4: Analytics Engineering (dbt)
- dbt fundamentals and project structure
- Models, seeds, and tests
- Documentation and lineage

### Module 5: Data Platforms (Bruin)
- Unified data pipeline framework
- Data ingestion with ingestr
- SQL/Python transformation
- Data quality checks
- Pipeline orchestration

### Module 6: Batch Processing (PySpark)
- Spark architecture and fundamentals
- PySpark DataFrame operations
- Batch processing patterns
- Spark UI for monitoring

### Module 7: Streaming (Kafka/PyFlink)
- Kafka/Redpanda fundamentals
- Producer and consumer patterns
- Event streaming and message handling
- PyFlink stream processing
- Windowing (tumbling and session windows)
- Watermark and event time processing
- Real-time aggregations

### Workshop 1: DLT Ingestion
- dlt (Data Loading Tool) fundamentals
- REST API data sources with pagination
- Schema inference and normalization
- DuckDB as local data warehouse
- AI-assisted pipeline building

---

## 🏃 Running the Solutions

### Module 1: Docker & SQL
```bash
cd learn/01-docker-sql-terraform
docker-compose up -d
```

### Module 2: Workflow Orchestration (Kestra)
```bash
cd learn/02-workflow-orchestration
docker-compose up -d
# Access Kestra UI: http://localhost:8080
```

### Module 3: Data Warehouse (BigQuery)
```bash
cd homework/03-data-warehouse
uv run load_yellow_taxi_data.py
```

### Module 5: Data Platforms (Bruin)
```bash
# Install Bruin CLI
curl -LsSf https://getbruin.com/install/cli | sh

# Initialize project
bruin init zoomcamp my-pipeline
cd my-pipeline

# Validate pipeline
bruin validate .

# Run pipeline
bruin run . --full-refresh
```

### Module 6: Batch Processing (PySpark)
```bash
cd learn/06-batch-pyspark
source .venv/bin/activate
python homework6_nov2025.py
```

### Workshop 1: DLT Ingestion
```bash
cd workshop/01-dlt-workshop
uv pip install "dlt[duckdb]"
uv run python taxi_pipeline.py

# View pipeline dashboard
dlt pipeline taxi_pipeline show
```

### Module 7: Streaming (Kafka/PyFlink)
```bash
# Setup infrastructure
cd ../../data-engineering-zoomcamp/07-streaming/workshop/
docker-compose build
docker-compose up -d

# Redpanda UI: http://localhost:8082
# Flink UI: http://localhost:8081
# PostgreSQL: localhost:5432 (user: postgres, password: postgres)

# Check Redpanda version
docker exec -it workshop-redpanda-1 rpk version

# Create Kafka topic
docker exec -it workshop-redpanda-1 rpk topic create green-trips

# Run producer
cd ../../../builder_rayhanAnanda/homework/07-streaming/
python producer_green_taxi.py

# Run consumer
python consumer_green_taxi.py

# Run Flink job (copy job files to workshop/src/job/ first)
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/flink_job_tumbling_window.py

# Query PostgreSQL
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "SELECT * FROM trips_per_location_5min;"
```

---

## 📚 Learning Resources

- **Course**: [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- **Community**: [DataTalks.Club](https://datatalks.club/)
- **Bruin Docs**: [https://getbruin.com/docs](https://getbruin.com/docs)
- **Kestra Docs**: [https://kestra.io/docs](https://kestra.io/docs)
- **dlt Docs**: [https://dlthub.com/docs](https://dlthub.com/docs)
- **Kafka Docs**: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
- **Redpanda Docs**: [https://docs.redpanda.com/](https://docs.redpanda.com/)
- **PyFlink Docs**: [https://nightlies.apache.org/flink/flink-docs-release-1.17/docs/dev/python/table/](https://nightlies.apache.org/flink/flink-docs-release-1.17/docs/dev/python/table/)

---

## 👨‍💻 Author

**Rayhan Ananda Resky**
- DE Zoomcamp 2026 Cohort
- Focus: Building robust and scalable data pipelines
- Learning: Data Engineering, Data Platforms, Distributed Systems

---

*Note: This repository is intended for educational purposes and documenting progress within the DataTalks.Club community.*
