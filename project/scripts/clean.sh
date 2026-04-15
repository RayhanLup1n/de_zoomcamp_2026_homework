#!/bin/bash

# Capstone Project Clean Script
# Removes all containers, volumes, and data

set -e

echo "========================================="
echo "  Cleaning NYC Taxi Analytics Project"
echo "========================================="
echo ""

# Stop and remove containers
echo "Stopping and removing containers..."
docker-compose down

# Remove volumes
echo "Removing volumes..."
docker-compose down -v

# Clear data directory (optional - ask first)
echo ""
read -p "Do you want to remove data/capstone.duckdb? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f data/capstone.duckdb
    echo "✓ Data file removed"
else
    echo "✓ Data file preserved"
fi

echo ""
echo "========================================="
echo "  Clean Complete!"
echo "========================================="
echo ""
echo "To restart: docker-compose up -d"
echo ""
