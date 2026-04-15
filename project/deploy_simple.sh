#!/bin/bash
# Deploy to Cloud Run - Simple Version

echo "🚀 NYC Taxi Dashboard - Cloud Run Deployment"
echo "==============================================="
echo ""

# Configuration
PROJECT_ID="de-zoomcamp-2026-484615"
SERVICE_NAME="nyc-taxi-dashboard"
REGION="us-central1"

cd "$(dirname "$0")"

echo "📦 Step 1: Building Docker image..."
docker build -t "${SERVICE_NAME}:latest" --platform linux/amd64 . || {
    echo "❌ Docker build failed!"
    exit 1
}
echo "✅ Docker image built"

echo ""
echo "☁️  Step 2: Deploying via gcloud Docker container..."
echo "   This will take 5-10 minutes..."
echo ""

# Create a temporary script to run inside gcloud container
cat > /tmp/deploy_in_gcloud.sh << 'GCLOUDSCRIPT'
#!/bin/bash
set -e

echo "🔐 Authenticating..."
gcloud auth activate-service-account --key-file=/workspace/de-zoomcamp-2026-484615-35de71278b22.json
gcloud config set project de-zoomcamp-2026-484615

echo "🏷️  Preparing image..."
docker tag nyc-taxi-dashboard:latest gcr.io/de-zoomcamp-2026-484615/nyc-taxi-dashboard:latest

echo "📤 Pushing to GCR..."
gcloud auth configure-docker gcr.io --quiet
docker push gcr.io/de-zoomcamp-2026-484615/nyc-taxi-dashboard:latest

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy nyc-taxi-dashboard \
  --image gcr.io/de-zoomcamp-2026-484615/nyc-taxi-dashboard:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DUCKDB_PATH=/app/data/capstone.duckdb,GCP_PROJECT_ID=de-zoomcamp-2026-484615" \
  --memory=1Gi \
  --cpu=1 \
  --concurrency=80 \
  --max-instances=2 \
  --min-instances=0 \
  --timeout=300s \
  --quiet

echo "✅ Deployment complete!"

SERVICE_URL=$(gcloud run services describe nyc-taxi-dashboard --region=us-central1 --format='value(status.url)' --quiet)
echo "$SERVICE_URL" > /workspace/service_url.txt

echo "🌐 Dashboard URL: $SERVICE_URL"
GCLOUDSCRIPT

chmod +x /tmp/deploy_in_gcloud.sh

# Run gcloud container with the script
docker run --rm -it \
  -v "$(pwd):/workspace" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp/deploy_in_gcloud.sh:/deploy.sh \
  -w /workspace \
  google/cloud-sdk:latest \
  bash /deploy.sh

# Check if deployment was successful
if [ -f service_url.txt ]; then
    SERVICE_URL=$(cat service_url.txt)
    rm service_url.txt

    echo ""
    echo "========================================"
    echo "🎉 DEPLOYMENT SUCCESSFUL!"
    echo "========================================"
    echo ""
    echo "🌐 Dashboard URL:"
    echo "   $SERVICE_URL"
    echo ""
    echo "📊 GCP Console:"
    echo "   https://console.cloud.google.com/run/detail/us-central1/nyc-taxi-dashboard"
    echo ""
    echo "✅ Your dashboard is now live!"
    echo "========================================"
else
    echo ""
    echo "⚠️  Deployment status unclear."
    echo "    Please check GCP Console:"
    echo "    https://console.cloud.google.com/run"
    echo ""
fi

echo ""
echo "✅ Deployment process complete!"
