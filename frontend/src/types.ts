export type RiskLevel='Low'|'Moderate'|'High'|'Critical';
export type Scenario={location:string;period:number;rainfall_mm:number;temperature_c:number;humidity_pct:number};
export type Prediction={mode:'simulation'|'model';location:string;period_weeks:number;estimated_cases:number;baseline_cases:number;change_pct:number;risk_index:number;risk_level:RiskLevel;lower_bound:number;upper_bound:number;factors:{name:string;impact:number;detail:string}[];recommendations:string[];notice:string};
export type HistoricalRow={month:string;cases:number;rainfall_mm:number;temperature_c:number;humidity_pct:number;predicted?:number};
