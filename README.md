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
| 5 | Data Platforms (Bruin) | 🔄 In Progress | [Link](./homework/05-data-platforms-bruin/) |
| 6 | Batch Processing (PySpark) | 📝 Notes Added | [Link](./learn/05-batch-pyspark/) |
| 7 | Streaming (Kafka/PyFlink) | ⏳ Pending | - |
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
│   ├── 05-data-platforms-bruin/  # Module 5: Bruin
│   └── 05-batch-pyspark/         # PySpark homework (bonus)
│
├── learn/                       # Learning notes & materials
│   ├── 01-docker-sql-terraform/
│   ├── 02-workflow-orchestration/
│   ├── 03-data-warehouse/
│   ├── 04-analytics-engineering/
│   ├── 05-batch-pyspark/         # PySpark notes
│   └── 06-data-platform-bruin/   # Bruin notes
│
├── docs/                        # Session documentation (gitignored)
│   └── 2026-02-24-module-5-bruin.md
│
└── .venv/                       # Virtual environment (uv)
```

---

## 🛠️ Tech Stack & Tools

| Category | Tools |
|----------|-------|
| **Infrastructure** | Google Cloud Platform (GCP) |
| **Orchestration** | Kestra, Bruin |
| **Data Platform** | Bruin (unified data pipeline) |
| **Batch Processing** | PySpark, Apache Spark |
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

### Module 5: Data Platforms (Bruin) 🔄
- Unified data pipeline framework
- Data ingestion with ingestr
- SQL/Python transformation
- Data quality checks
- Pipeline orchestration
- **Status**: In Progress

### Module 6: Batch Processing (PySpark) 📝
- Spark architecture and fundamentals
- PySpark DataFrame operations
- Batch processing patterns
- Spark UI for monitoring
- **Status**: Notes Added (bonus learning)

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
cd learn/05-batch-pyspark
source .venv/bin/activate
python homework5.py
```

---

## 📚 Learning Resources

- **Course**: [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- **Community**: [DataTalks.Club](https://datatalks.club/)
- **Bruin Docs**: [https://getbruin.com/docs](https://getbruin.com/docs)
- **Kestra Docs**: [https://kestra.io/docs](https://kestra.io/docs)

---

## 👨‍💻 Author

**Rayhan Ananda Resky**
- DE Zoomcamp 2026 Cohort
- Focus: Building robust and scalable data pipelines
- Learning: Data Engineering, Data Platforms, Distributed Systems

---

*Note: This repository is intended for educational purposes and documenting progress within the DataTalks.Club community.*
