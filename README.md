# Data Engineering Zoomcamp - Homework & Learning

This repository contains my personal journey, exercises, and homework solutions for the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) program.

## 🚀 Repository Structure

This repository is organized into two main sections:

*   **[📁 learn/](./learn/)**: Contains all the learning materials, notes, and exercises followed during the course modules.
    *   Docker, SQL, Terraform, and GCP setup.
    *   Workflow Orchestration with Kestra.
*   **[📁 homework/](./homework/)**: Contains my official solutions to the weekly assignments.
    *   [Module 1 Homework](./homework/01-docker-sql-terraform-gcp-homework/)
    *   [Module 2 Homework](./homework/02-workflow-orchestration-homework/)
    *   [Module 3 Homework](./homework/03-data-warehouse/)


## 🛠️ Tech Stack & Tools

*   **Infrastructure**: Google Cloud Platform (GCP)
*   **Orchestration**: Kestra
*   **IaC**: Terraform
*   **Data Warehouse**: BigQuery
*   **Containerization**: Docker & Docker Compose
*   **Programming**: Python 3.13 (Managed by [uv](https://github.com/astral-sh/uv))
*   **Database**: PostgreSQL
*   **Analytical DB**: DuckDB
*   **Management Tools**: pgAdmin, pgcli

## 📝 Running the Solutions

Each module folder contains specific instructions. In general, to run the environments locally:

### Module 1: Docker & SQL
1.  **Spin up the database environment**:
    ```bash
    cd learn/01-docker-xml
    docker-compose up -d
    ```

### Module 2: Workflow Orchestration (Kestra)
1.  **Spin up Kestra & Postgres**:
    ```bash
    cd learn/02-workflow-orchestration
    docker-compose up -d
    ```
2.  **Access Kestra UI**: Open [http://localhost:8080](http://localhost:8080) in your browser.

### Module 3: Data Warehouse (BigQuery)
1.  **Load data to GCS**:
    ```bash
    cd homework/03-data-warehouse
    uv run load_yellow_taxi_data.py
    ```
2.  **Execute SQL Queries**: Use the queries in `module-3-queries.sql` within the BigQuery Console.


## 👨‍💻 Author

**Rayhan Ananda Resky**
*   DE Zoomcamp 2026 Cohort
*   Focus: Building robust and scalable data pipelines.

---
*Note: This repository is intended for educational purposes and documenting progress within the DataTalks.Club community.*
