#!/bin/bash

# Indonesia Weather Analytics - Pipeline Runner
# Runs the complete data pipeline via Docker Compose

set -e

echo "========================================="
echo "  Indonesia Weather Analytics Pipeline"
echo "========================================="
echo ""

# Step 1: Ingestion
echo "Step 1: Fetching weather data from Open-Meteo API..."
echo "   Cities: Jakarta, Surabaya, Denpasar, Medan, Makassar"
echo "   This takes about 1-2 minutes (no API key needed)"
docker compose --profile ingest up --build ingestion
echo "✓ Ingestion complete"
echo ""

# Step 2: Transformation
echo "Step 2: Running dbt transformations (staging → core → analytics)..."
docker compose --profile transform run --build dbt \
  sh -c "cd /app/dbt && dbt run --profiles-dir . --project-dir ."
echo "✓ Transformations complete"
echo ""

# Step 3: Tests
echo "Step 3: Running dbt tests..."
docker compose --profile transform run dbt \
  sh -c "cd /app/dbt && dbt test --profiles-dir . --project-dir ."
echo "✓ Tests complete"
echo ""

# Step 4: Start services
echo "Step 4: Starting dashboard and Kestra..."
docker compose up -d --build
echo "✓ Services started"
echo ""

echo "========================================="
echo "  Pipeline Complete!"
echo "========================================="
echo ""
echo "  Dashboard:  http://localhost:8501"
echo "  Kestra UI:  http://localhost:8080"
echo ""
