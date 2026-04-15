#!/bin/bash

# Capstone Project Setup Script
# This script initializes the project environment

set -e

echo "========================================="
echo "  NYC Taxi Analytics Dashboard Setup"
echo "========================================="
echo ""

# Check if .env exists, if not copy from .env.example
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

# Create data directory
echo ""
echo "Creating data directory..."
mkdir -p data
echo "✓ data directory created"

# Download taxi zone lookup if not exists
echo ""
echo "Downloading taxi zone lookup..."
if [ ! -f data/taxi_zone_lookup.csv ]; then
    echo "Downloading from NYC TLC..."
    curl -o data/taxi_zone_lookup.csv https://d37ci6v75uryu3.cloudfront.net/misc/taxi_zone_lookup.csv
    echo "✓ taxi_zone_lookup.csv downloaded"
else
    echo "✓ taxi_zone_lookup.csv already exists"
fi

# Create empty .gitkeep in data directory
touch data/.gitkeep

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Review .env file and adjust if needed"
echo "2. Run: docker-compose up -d"
echo "3. Access Kestra UI: http://localhost:8080"
echo "4. Access Dashboard: http://localhost:8501"
echo ""
