# DengueGuard AI

A transparent, hackathon-ready MVP for dengue surveillance exploration and weather-scenario risk assessment, initially focused on Chattogram, Bangladesh.

> **Important:** The bundled records are **Synthetic Demo Data**. The included scenario estimator is a deterministic, illustrative heuristic—not a trained or validated epidemiological model. No model accuracy is reported. It must not be used for clinical or public-health operational decisions.

## MVP capabilities

- Responsive multi-page React + TypeScript dashboard.
- Historical monthly trend and weather charts (synthetic demonstration series).
- Interactive weather scenario simulator with baseline comparison, uncertainty band, factor contributions, and recommendations.
- Bangladesh/Chattogram-focused interactive Leaflet map. District markers show synthetic demonstration risk indices, not official observations.
- Alert center, prevention guidance, source registry, CSV import and validation.
- FastAPI service with typed request/response models and SQLite persistence for uploaded records.
- Optional Random Forest training script with chronological holdout and baseline comparison. Training runs only when a user supplies a real, appropriately aligned dataset.

## Architecture

```text
React + TypeScript + Vite
  ├── dashboard / analytics / simulator / map / alerts / guidance
  ├── predictionService.ts (isolated API adapter + offline fallback)
  └── Leaflet + OpenStreetMap tiles / Recharts
             │ HTTP
             ▼
FastAPI
  ├── /api/dashboard, /historical-data, /regions, /predict, /simulate
  ├── /api/risk-map, /alerts, /data/upload, /model/metrics
  └── SQLite (development uploads)
             │
             ▼
Pandas / NumPy / scikit-learn training pipeline
```

## Run locally

### 1. Backend (Python 3.10+)

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open API documentation at http://localhost:8000/docs.

### 2. Frontend (Node 18+)

In another terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open the Vite URL (normally http://localhost:5173). Set `VITE_API_BASE_URL=http://localhost:8000` to connect to FastAPI. If the API is unavailable, the UI falls back to the clearly labeled offline demo service.

### 3. Offline demo

No paid API keys are required. The frontend's offline demo mode uses local synthetic records. The Leaflet basemap uses OpenStreetMap tiles and therefore requires internet access; the rest of the dashboard and simulator work offline. If tiles are unavailable, markers and the surrounding UI remain available.

## Data contract for CSV upload

Required columns (case-insensitive):

| Column | Type | Unit / format |
|---|---|---|
| date | ISO date or parseable date | Daily or monthly; one consistent frequency per file |
| location | text | District/city/area name |
| dengue_cases | non-negative integer | Reported cases in the period |
| rainfall_mm | number | Millimetres accumulated over the period |
| temperature_c | number | Mean 2 m air temperature in °C |
| humidity_pct | number | Mean relative humidity, 0–100% |

Missing weather values are retained as missing and must be imputed only inside a training fold. Missing case counts are rejected. Duplicate date-location rows are rejected. Negative cases/rainfall and impossible humidity values are rejected. Do not combine daily and monthly rows in one file. CSV uploads are stored in SQLite for development; production should use authenticated object storage and a governed database.

## Real-data integration status

| Source | Status in this MVP | Notes |
|---|---|---|
| Bangladesh DGHS Dengue Dynamic Dashboard | **Documented / manual import** | Official dashboard is linked in the UI. No unsupported scraping or API access is assumed. Verify export terms and definitions before ingestion. |
| Bangladesh Meteorological Department (BMD) | **Planned connector** | Obtain authorized station observations / data-sharing access; station quality control and station-to-district aggregation are required. |
| NASA POWER | **Planned connector** | Public meteorological and solar data API; use for gridded weather covariates, not as a substitute for local station validation. |
| Open-Meteo Historical Weather | **Documented / optional public connector** | ERA5 / ERA5-Land reanalysis provides historical estimates, not direct station observations. Review attribution and terms for intended use. |
| Open-Meteo Forecast | **Planned connector** | Forecast covariates should be stored with issue time and lead time to avoid leakage. |

Links:
- DGHS: https://dashboard.dghs.gov.bd/pages/heoc_dengue_v1.php
- BMD: https://bmd.gov.bd/
- NASA POWER: https://power.larc.nasa.gov/
- Open-Meteo historical API: https://open-meteo.com/en/docs/historical-weather-api
- Open-Meteo forecast API: https://open-meteo.com/en/docs

## Model development protocol

1. Acquire an authorized, documented dengue time series with stable geographic identifiers and case definitions.
2. Align weekly or monthly case counts to weather periods; record reporting delays and revisions.
3. Add lagged weather variables, seasonal terms, historical case lags, and population denominators where available.
4. Split chronologically. Never randomly split time-series rows.
5. Fit preprocessing and imputation on training data only.
6. Compare a seasonal-naive / lagged baseline with Random Forest (and optionally XGBoost).
7. Report MAE, RMSE and WAPE (only where denominator is non-zero), plus per-region and horizon performance.
8. Construct uncertainty intervals from held-out residual quantiles or rolling-origin conformal residuals. Check empirical coverage.
9. Only enable `model_status=validated` after independent review, reproducible training, and documented validation. The current MVP does not enable this status.

The training script in `ml/train_model.py` expects a real CSV with the columns in `ml/README.md`. It prints metrics and saves a model artifact only after successful training. Do not use the bundled synthetic demo CSV to claim predictive performance.

## Risk classification

The demo simulator produces a relative risk index (0–100) from scenario departures from a clearly stated reference weather profile. Default display bands are configurable in `frontend/src/config.ts`:
- Low: 0–24
- Moderate: 25–49
- High: 50–74
- Critical: 75–100

These are **prototype UI bands**, not validated epidemiological thresholds. Production thresholds must be calibrated against population-adjusted incidence, local historical baselines, health-system capacity, and public-health stakeholder input. Raw counts must not be compared directly across differently sized populations.

## Security and production hardening

- Add authentication/authorization and audit logs before exposing uploads or sensitive records.
- Add upload size limits, malware scanning, schema versioning, and rate limits.
- Use HTTPS, managed secrets, backups, migrations, and PostgreSQL in production.
- Do not upload personally identifiable patient data. This MVP expects aggregate counts only.
- Notification routes are alert-ready only; no email/SMS delivery provider is connected.

## Team presentation suggestion

- **Member 1 — Data & public health:** source provenance, data dictionary, CSV validation, surveillance limitations.
- **Member 2 — ML & evaluation:** temporal feature engineering, baseline comparison, chronological evaluation, uncertainty.
- **Member 3 — Product & engineering:** React UI, FastAPI contracts, map, simulator, deployment and demo flow.

## License / attribution

OpenStreetMap map tiles are provided by OpenStreetMap contributors. The application code is provided for hackathon prototyping; review each upstream data provider's license and terms before redistribution or operational use.
