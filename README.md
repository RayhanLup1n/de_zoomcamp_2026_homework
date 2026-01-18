# Data Engineering Zoomcamp - Homework & Learning

This repository contains my personal journey, exercises, and homework solutions for the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) program.

## 🚀 Repository Structure

The focus of this repository is to document the progress of the course modules and provide clear solutions to the weekly homework.

*   **[Module 1: Containerization and Infrastructure as Code](./01-docker-sql-terraform-gcp-homework/)**
    *   Docker & Docker Compose (PostgreSQL, pgAdmin)
    *   SQL Refresher with NYC Taxi Data
    *   Infrastructure as Code with Terraform (GCP)
    *   In-depth Documentation/Q&A for Homework 1

## 🛠️ Tech Stack & Tools

*   **Infrastructure**: Google Cloud Platform (GCP)
*   **IaC**: Terraform
*   **Containerization**: Docker & Docker Compose
*   **Programming**: Python 3.13 (Managed by [uv](https://github.com/astral-sh/uv))
*   **Database**: PostgreSQL
*   **Management Tools**: pgAdmin, pgcli

## 📝 Running the Solutions

Each module folder contains specific instructions. In general, to run the environments locally:

1.  **Clone the repo**:
    ```bash
    git clone <your-repo-url>
    ```
2.  **Spin up the database environment**:
    ```bash
    cd 01-docker-sql-terraform-gcp-homework
    docker-compose up -d
    ```
3.  **Run ingestion tasks**:
    ```bash
    # Using uv for fast execution
    uv run python question_3.py --url <dataset_url>
    ```

## 👨‍💻 Author

**Rayhan Ananda Resky**
*   DE Zoomcamp 2026 Cohort
*   Focus: Building robust and scalable data pipelines.

---
*Note: This repository is intended for educational purposes and documenting progress within the DataTalks.Club community.*
