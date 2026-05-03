#!/bin/bash

# Indonesia Weather Analytics - Setup Script
# Creates .env file and data directory

set -e

echo "========================================="
echo "  Indonesia Weather Analytics Setup"
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
touch data/.gitkeep
echo "✓ data directory ready"

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  make ingest      # Fetch weather data from Open-Meteo API"
echo "  make transform   # Run dbt transformations"
echo "  make serve       # Start dashboard + Kestra"
echo ""
echo "Or run everything at once:"
echo "  make setup"
echo ""
