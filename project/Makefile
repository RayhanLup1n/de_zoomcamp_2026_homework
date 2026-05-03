.PHONY: setup ingest transform serve down clean help

help: ## Show available commands
	@echo "Indonesia Weather Analytics - Available Commands:"
	@echo ""
	@echo "  make setup      Full setup: ingest + transform + start dashboard"
	@echo "  make ingest     Fetch weather data from Open-Meteo API"
	@echo "  make transform  Run dbt transformations and tests"
	@echo "  make serve      Start dashboard and orchestration services"
	@echo "  make down       Stop all services"
	@echo "  make clean      Full cleanup (remove volumes and data)"
	@echo ""

setup: ingest transform serve ## Full pipeline: ingest -> transform -> start dashboard

ingest: ## Fetch weather data from Open-Meteo API -> DuckDB
	@echo "Fetching weather data from Open-Meteo API..."
	@echo "   Cities: Jakarta, Surabaya, Denpasar, Medan, Makassar"
	@echo "   This takes about 1-2 minutes (no API key needed)"
	docker compose --profile ingest up --build ingestion
	@echo "Ingestion complete!"

transform: ## Run dbt transformations (staging -> core -> analytics) and tests
	@echo "Running dbt transformations..."
	docker compose --profile transform run --build dbt sh -c "cd /app/dbt && dbt run --profiles-dir . --project-dir . && dbt test --profiles-dir . --project-dir ."
	@echo "Transformations complete!"

serve: ## Start dashboard (port 8501) and Kestra (port 8080)
	@echo "Starting services..."
	docker compose up -d --build
	@echo ""
	@echo "Services started!"
	@echo "   Dashboard:  http://localhost:8501"
	@echo "   Kestra UI:  http://localhost:8080"

down: ## Stop all services
	docker compose down

clean: ## Full cleanup (remove volumes, data, and containers)
	docker compose down -v
	rm -f data/capstone.duckdb
	@echo "Cleanup complete!"
