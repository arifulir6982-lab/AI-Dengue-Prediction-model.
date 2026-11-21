import os, io, csv, sqlite3
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ScenarioIn, PredictionOut, UploadSummary
from .predictor import simulate

BASE = Path(__file__).resolve().parents[1]
DB = os.getenv("DATABASE_URL", "sqlite:///./dengueguard.db").replace("sqlite:///","")
if not Path(DB).is_absolute(): DB = str(BASE / DB)
conn = sqlite3.connect(DB)
conn.execute("CREATE TABLE IF NOT EXISTS imported_records (id INTEGER PRIMARY KEY, date TEXT, location TEXT, dengue_cases INTEGER, rainfall_mm REAL, temperature_c REAL, humidity_pct REAL, imported_at TEXT)")
conn.commit(); conn.close()

app = FastAPI(title="DengueGuard AI API", version="1.0.0", description="Hackathon MVP API. Demo predictions are synthetic heuristic simulations, not validated forecasts.")
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health(): return {"status":"ok","mode":"synthetic_demo","model_status":"not_trained"}

@app.get("/api/dashboard")
def dashboard():
    return {"mode":"synthetic_demo","historical_demo_cases":1029,"featured_location":"Chattogram","baseline_cases":118,"risk_level":"High","risk_index":63,"model_status":"not_trained","metrics":None}

@app.get("/api/historical-data")
def historical():
    path = BASE / "data" / "synthetic_demo_monthly.csv"
    with path.open(encoding="utf-8") as f: return {"mode":"synthetic_demo","rows":list(csv.DictReader(f))}

@app.get("/api/regions")
def regions():
    return [{"name":x,"division":d} for x,d in [("Chattogram","Chattogram"),("Cox’s Bazar","Chattogram"),("Cumilla","Chattogram"),("Feni","Chattogram"),("Dhaka","Dhaka"),("Khulna","Khulna"),("Rajshahi","Rajshahi"),("Sylhet","Sylhet"),("Barishal","Barishal"),("Rangpur","Rangpur"),("Mymensingh","Mymensingh")]]

@app.post("/api/predict", response_model=PredictionOut)
def predict(payload: ScenarioIn):
    # No validated model is bundled. Route deliberately uses the transparent demo estimator.
    return simulate(payload)

@app.post("/api/simulate", response_model=PredictionOut)
def simulate_route(payload: ScenarioIn): return simulate(payload)

@app.get("/api/risk-map")
def risk_map():
    return {"mode":"synthetic_demo","message":"Approximate city markers with synthetic indicators; not official district polygons or reports.","regions":[{"name":"Chattogram","risk_index":63,"cases":118},{"name":"Cox’s Bazar","risk_index":44,"cases":54},{"name":"Cumilla","risk_index":51,"cases":77},{"name":"Feni","risk_index":35,"cases":32},{"name":"Dhaka","risk_index":72,"cases":230}]}

@app.get("/api/alerts")
def alerts():
    return {"mode":"synthetic_demo","delivery_connected":False,"items":[{"id":"DG-104","area":"Chattogram","level":"High","date":"Next 2–4 weeks","factors":["humidity","rainfall"],"message":"Synthetic scenario signal; verify against official surveillance."}]}

@app.post("/api/data/upload", response_model=UploadSummary)
async def upload_data(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(400,"Upload a .csv file.")
    raw = await file.read()
    if len(raw) > 5_000_000: raise HTTPException(413,"CSV exceeds 5 MB limit.")
    try: text = raw.decode("utf-8-sig")
    except UnicodeDecodeError: raise HTTPException(400,"CSV must be UTF-8 encoded.")
    reader = csv.DictReader(io.StringIO(text))
    required = {"date","location","dengue_cases","rainfall_mm","temperature_c","humidity_pct"}
    if not reader.fieldnames: raise HTTPException(400,"CSV has no header row.")
    normalized = {h.strip().lower():h for h in reader.fieldnames}
    missing = required - set(normalized)
    if missing: raise HTTPException(400, f"Missing columns: {', '.join(sorted(missing))}")
    accepted=[]; rejected=0; now=datetime.utcnow().isoformat()
    for row in reader:
        try:
            date = datetime.fromisoformat(row[normalized["date"]].strip().replace("Z","+00:00")).date().isoformat()
            location=row[normalized["location"]].strip()
            cases=int(row[normalized["dengue_cases"]])
            rain=float(row[normalized["rainfall_mm"]]); temp=float(row[normalized["temperature_c"]]); humidity=float(row[normalized["humidity_pct"]])
            if not location or cases<0 or rain<0 or not -5<=temp<=55 or not 0<=humidity<=100: raise ValueError()
            accepted.append((date,location,cases,rain,temp,humidity,now))
        except (ValueError,TypeError,KeyError): rejected+=1
    # Duplicate date-location rows are rejected as a whole to avoid silent aggregation.
    keys=[(r[0],r[1]) for r in accepted]
    if len(keys)!=len(set(keys)): raise HTTPException(400,"Duplicate date-location rows detected.")
    db=sqlite3.connect(DB)
    db.executemany("INSERT INTO imported_records(date,location,dengue_cases,rainfall_mm,temperature_c,humidity_pct,imported_at) VALUES(?,?,?,?,?,?,?)",accepted)
    db.commit();db.close()
    return UploadSummary(rows_accepted=len(accepted),rows_rejected=rejected,message="Imported aggregate records to local SQLite. Not used to train a model automatically.")

@app.get("/api/model/metrics")
def model_metrics():
    return {"status":"not_trained","metrics":None,"message":"No model artifact is bundled. Train and evaluate using a real dataset with the provided chronological pipeline before reporting metrics."}
