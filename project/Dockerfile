FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY dashboard/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy dashboard code
COPY dashboard/ /app/dashboard/

# Environment
ENV PYTHONUNBUFFERED=1

# Cloud Run uses PORT env var (default 8080)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8080/_stcore/health || exit 1

# Run Streamlit on Cloud Run port
CMD ["streamlit", "run", "dashboard/app.py", \
     "--server.port=8080", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
