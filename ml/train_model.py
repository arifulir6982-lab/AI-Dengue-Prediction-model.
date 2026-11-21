"""Train an optional baseline and RandomForest on a real monthly dataset.
Never use synthetic_demo_monthly.csv to claim model performance.
"""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

REQUIRED={"date","location","dengue_cases","rainfall_mm","temperature_c","humidity_pct"}

def wape(y, p):
    denom=np.abs(y).sum()
    return float(np.abs(y-p).sum()/denom*100) if denom else None

def make_features(frame):
    x=frame.copy().sort_values(["location","date"])
    for lag in [1,2,3]:
        x[f"cases_lag_{lag}"]=x.groupby("location")["dengue_cases"].shift(lag)
        for col in ["rainfall_mm","temperature_c","humidity_pct"]:
            x[f"{col}_lag_{lag}"]=x.groupby("location")[col].shift(lag)
    month=x["date"].dt.month
    x["month_sin"]=np.sin(2*np.pi*month/12);x["month_cos"]=np.cos(2*np.pi*month/12)
    x["location_code"]=x["location"].astype("category").cat.codes
    return x.dropna(subset=["dengue_cases"])

def main():
    ap=argparse.ArgumentParser();ap.add_argument("csv");ap.add_argument("--output",default="artifacts/dengue_rf.joblib");args=ap.parse_args()
    path=Path(args.csv);df=pd.read_csv(path);df.columns=[c.strip().lower() for c in df.columns]
    if not REQUIRED.issubset(df.columns): raise SystemExit(f"Missing columns: {sorted(REQUIRED-set(df.columns))}")
    if "synthetic_demo" in path.name.lower(): raise SystemExit("Refusing to train on bundled synthetic demo data.")
    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    df["dengue_cases"]=pd.to_numeric(df["dengue_cases"],errors="coerce")
    for c in ["rainfall_mm","temperature_c","humidity_pct"]: df[c]=pd.to_numeric(df[c],errors="coerce")
    df=df.dropna(subset=["date","location","dengue_cases"]).sort_values(["date","location"])
    if (df["dengue_cases"]<0).any(): raise SystemExit("Negative case counts found.")
    # Monthly aggregation. Weather values are period means; cases are period totals.
    monthly=df.set_index("date").groupby("location").resample("MS").agg({"dengue_cases":"sum","rainfall_mm":"mean","temperature_c":"mean","humidity_pct":"mean"}).reset_index()
    feat=make_features(monthly)
    cols=[c for c in feat.columns if c.startswith(("cases_lag_","rainfall_mm_lag_","temperature_c_lag_","humidity_pct_lag_"))]+["month_sin","month_cos","location_code"]
    feat=feat.dropna(subset=["cases_lag_1","cases_lag_2","cases_lag_3"])
    feat=feat.sort_values("date");split=max(1,int(len(feat)*.8))
    unique_dates=np.sort(feat["date"].unique())
    cutoff=unique_dates[max(1,int(len(unique_dates)*.8))-1]
    train,test=feat[feat["date"]<=cutoff],feat[feat["date"]>cutoff]
    if len(train)<24 or len(test)<6: raise SystemExit("Need at least 30 usable monthly rows after lagging; more history is strongly recommended.")
    Xtr=train[cols];Xte=test[cols];ytr=train["dengue_cases"].to_numpy();yte=test["dengue_cases"].to_numpy()
    model=Pipeline([("imputer",SimpleImputer(strategy="median")),("rf",RandomForestRegressor(n_estimators=400,min_samples_leaf=2,random_state=42,n_jobs=-1))])
    model.fit(Xtr,ytr);pred=np.maximum(0,model.predict(Xte))
    baseline=np.maximum(0,test["cases_lag_1"].to_numpy())
    metrics={"test_rows":len(test),"mae":float(mean_absolute_error(yte,pred)),"rmse":float(mean_squared_error(yte,pred)**.5),"wape_pct":wape(yte,pred),"baseline_mae":float(mean_absolute_error(yte,baseline)),"baseline_rmse":float(mean_squared_error(yte,baseline)**.5),"baseline_wape_pct":wape(yte,baseline),"interval_method":"90th percentile absolute held-out residual","empirical_abs_residual_q90":float(np.quantile(np.abs(yte-pred),.9))}
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);joblib.dump({"model":model,"feature_columns":cols,"metrics":metrics},out)
    print(json.dumps({"artifact":str(out),"metrics":metrics},indent=2))
if __name__=="__main__":main()
