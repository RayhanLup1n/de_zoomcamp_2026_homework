# 🚀 Deployment Guide - NYC Taxi Analytics Dashboard

## Overview

Panduan deployment dashboard ke Google Cloud Run dengan setup billing alerts.

---

## Prerequisites

1. Google Cloud SDK (gcloud CLI) terinstall
2. Project GCP aktif: `de-zoomcamp-2026-484615`
3. Billing alerts sudah setup (Rp100.000 dengan 4 thresholds)

---

## Step 1: Authenticate gcloud

```bash
# Login ke Google Cloud
gcloud auth login

# Set project
gcloud config set project de-zoomcamp-2026-484615

# Verify
gcloud config get-value project
```

---

## Step 2: Build Container Image

```bash
# Navigate to project directory
cd builder_rayhanAnanda/project

# Build image with Cloud Build (recommended)
gcloud builds submit --tag gcr.io/de-zoomcamp-2026-484615/nyc-taxi-dashboard:latest .

# Atau build locally dengan Docker (alternative)
# docker build -t gcr.io/de-zoomcamp-2026-484615/nyc-taxi-dashboard:latest .
# docker push gcr.io/de-zoomcamp-2026-484615/nyc-taxi-dashboard:latest
```

---

## Step 3: Deploy to Cloud Run

```bash
# Deploy dengan environment variables
gcloud run deploy nyc-taxi-dashboard \
  --image gcr.io/de-zoomcamp-2026-484615/nyc-taxi-dashboard:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DUCKDB_PATH=/app/data/capstone.duckdb,GCP_PROJECT_ID=de-zoomcamp-2026-484615" \
  --set-secrets="GOOGLE_APPLICATION_CREDENTIALS=bigquery-credentials:latest" \
  --memory=1Gi \
  --cpu=1 \
  --concurrency=80 \
  --max-instances=2 \
  --min-instances=0
```

**Catatan Penting:**
- `--set-secrets` membutuhkan Secret Manager setup terlebih dahulu (lihat Step 4)
- `--min-instances=0` = cost-free saat idle (cold start ~2-5 detik)
- `--memory=1Gi` = cukup untuk DuckDB in-memory

---

## Step 4: Setup Secret Manager (REQUIRED)

Agar credentials JSON aman, kita perlu simpan di Secret Manager:

```bash
# Create secret untuk GCP credentials
gcloud secrets create bigquery-credentials \
  --replication-policy="automatic" \
  --data-file="de-zoomcamp-2026-484615-35de71278b22.json"

# Grant Cloud Run service account access to secret
gcloud secrets add-iam-policy-binding bigquery-credentials \
  --member="serviceAccount:de-zoomcamp-2026-484615@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

---

## Step 5: Verify Deployment

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe nyc-taxi-dashboard \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

echo "Dashboard URL: $SERVICE_URL"

# Test health endpoint
curl -s "${SERVICE_URL}/_stcore/health"
```

---

## 📊 Monitoring & Cost Control

### View Logs
```bash
# Real-time logs
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=nyc-taxi-dashboard" --format="value(textPayload)"

# Cloud Console
open https://console.cloud.google.com/run/detail/us-central1/nyc-taxi-dashboard/logs
```

### Check Usage & Costs
```bash
# Current month's cost
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID

# Resource usage
gcloud run services list --platform managed
```

---

## 🔒 Security Best Practices

1. ✅ **Credentials di Secret Manager** (tidak di kode/container)
2. ✅ **Unauthenticated access** (dashboard publik, data anonim)
3. ✅ **Minimal permissions** (BigQuery read-only, tidak ada write access)
4. ✅ **Auto-scaling to zero** (min-instances=0, cost-free saat idle)

---

## 🆘 Troubleshooting

### Issue: Container fails to start
```bash
# Check logs
gcloud run services describe nyc-taxi-dashboard --region=us-central1

# Test locally first
docker run -p 8080:8080 gcr.io/de-zoomcamp-2026-484615/nyc-taxi-dashboard:latest
```

### Issue: BigQuery connection failed
```bash
# Verify secret exists
gcloud secrets versions list bigquery-credentials

# Test BigQuery connection locally
export GOOGLE_APPLICATION_CREDENTIALS=de-zoomcamp-2026-484615-35de71278b22.json
python -c "from google.cloud import bigquery; client = bigquery.Client(); print(list(client.list_datasets()))"
```

### Issue: Cold start too slow
```bash
# Set min-instances=1 (surcharge $5-10/bulan tapi zero cold start)
gcloud run services update nyc-taxi-dashboard --min-instances=1 --region=us-central1
```

---

## ✅ Pre-Deployment Checklist

- [ ] `gcloud auth login` sukses
- [ ] Project `de-zoomcamp-2026-484615` aktif
- [ ] Billing alerts setup (Rp100.000 dengan 4 thresholds)
- [ ] Dockerfile dan .gcloudignore sudah benar
- [ ] Secret Manager setup untuk credentials
- [ ] Test build locally: `docker build -t test .`

---

## 🎉 Post-Deployment

Setelah deploy sukses:

1. **Screenshot dashboard** untuk dokumentasi portfolio
2. **Update README.md** dengan live URL
3. **Test semua fitur** (filter, charts, caching)
4. **Share URL** di LinkedIn/portfolio 🚀

---

## 📞 Support Resources

- **GCP Free Tier Docs:** https://cloud.google.com/free
- **Cloud Run Pricing:** https://cloud.google.com/run/pricing
- **Streamlit Cloud (alternative):** https://share.streamlit.io

---

**Ready to deploy?** 🚀

Pilih salah satu:
1. **Deploy sekarang ke Cloud Run** (saya bantu step-by-step)
2. **Deploy ke Streamlit Cloud** (lebih mudah, tapi kurang "production")
3. **Bikin GitHub Actions CI/CD** untuk auto-deploy setiap push

Mau yang mana? 😊
