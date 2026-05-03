#!/bin/bash

# Indonesia Weather Analytics - Clean Script
# Removes all containers, volumes, and data

set -e

echo "========================================="
echo "  Cleaning Indonesia Weather Project"
echo "========================================="
echo ""

# Stop and remove containers + volumes
echo "Stopping containers and removing volumes..."
docker compose down -v
echo "✓ Containers and volumes removed"
echo ""

# Remove data files
echo "Removing data files..."
rm -f data/capstone.duckdb data/capstone.duckdb.wal
echo "✓ Data files removed"

echo ""
echo "========================================="
echo "  Clean Complete!"
echo "========================================="
echo ""
echo "To restart: make setup"
echo ""
