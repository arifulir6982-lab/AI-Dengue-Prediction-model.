import {API_BASE} from '../config';
import type {Prediction,Scenario} from '../types';

function offlinePredict(s:Scenario):Prediction {
 const base= s.location==='Chattogram'?118:s.location==='Dhaka'?230:54;
 const rain=Math.max(-20,Math.min(35,(s.rainfall_mm-220)/12));
 const temp=Math.max(-12,Math.min(22,(s.temperature_c-28)*5));
 const humidity=Math.max(-15,Math.min(25,(s.humidity_pct-78)*1.25));
 const season=s.period>=5&&s.period<=9?12:-4;
 const score=Math.max(0,Math.min(100,35+rain+temp+humidity+season));
 const multiplier=0.72+score/100*0.85;
 const cases=Math.max(0,Math.round(base*multiplier*(s.period/4)));
 const baseline=Math.max(0,Math.round(base*(0.72+((35+season)/100)*0.85)*(s.period/4)));
 const level=score>=75?'Critical':score>=50?'High':score>=25?'Moderate':'Low';
 const spread=Math.max(8,Math.round(cases*0.28));
 return {mode:'simulation',location:s.location,period_weeks:s.period,estimated_cases:cases,baseline_cases:baseline,change_pct:baseline?Math.round((cases-baseline)/baseline*100):0,risk_index:Math.round(score),risk_level:level,lower_bound:Math.max(0,cases-spread),upper_bound:cases+spread,
 factors:[{name:'Rainfall',impact:Math.round(rain),detail:`${s.rainfall_mm} mm scenario input vs 220 mm reference`},{name:'Temperature',impact:Math.round(temp),detail:`${s.temperature_c}°C scenario input vs 28°C reference`},{name:'Relative humidity',impact:Math.round(humidity),detail:`${s.humidity_pct}% scenario input vs 78% reference`},{name:'Seasonality',impact:season,detail:'Illustrative monsoon-season adjustment'}],
 recommendations: level==='Critical'||level==='High'?['Remove standing water from rooftops, containers and construction sites.','Coordinate targeted source reduction and larval surveillance.','Healthcare facilities should review triage, fluids and diagnostic supply readiness.']:['Maintain weekly checks for standing water and covered storage.','Share symptom-awareness guidance and protect against mosquito bites.','Continue routine case reporting and local vector surveillance.'],
 notice:'Synthetic demonstration simulation only. This is not a validated forecast, clinical assessment, or official public-health alert.'};
}
export async function predictScenario(s:Scenario):Promise<Prediction>{
 if(!API_BASE) return offlinePredict(s);
 try {const r=await fetch(`${API_BASE}/api/simulate`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(s)});if(!r.ok)throw new Error('API unavailable');return await r.json();}
 catch{return offlinePredict(s);}
}
export async function getDashboard(){if(!API_BASE)return null;try{const r=await fetch(`${API_BASE}/api/dashboard`);if(!r.ok)throw new Error();return await r.json();}catch{return null;}}
