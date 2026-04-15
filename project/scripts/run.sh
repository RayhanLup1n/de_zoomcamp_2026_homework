#!/bin/bash

# Capstone Project Run Script
# Runs the complete data pipeline

set -e

echo "========================================="
echo "  Running NYC Taxi Analytics Pipeline"
echo "========================================="
echo ""

# Step 1: Ingestion
echo "Step 1: Running ingestion (dlt)..."
docker-compose exec ingestion python -m ingestion.main
echo "✓ Ingestion complete"
echo ""

# Step 2: Transformation
echo "Step 2: Running transformations (dbt)..."
docker-compose exec dbt dbt run
echo "✓ Transformations complete"
echo ""

# Step 3: Tests
echo "Step 3: Running tests (dbt test)..."
docker-compose exec dbt dbt test
echo "✓ Tests complete"
echo ""

echo "========================================="
echo "  Pipeline Run Complete!"
echo "========================================="
echo ""
echo "Access dashboard at: http://localhost:8501"
echo ""
