from .schemas import ScenarioIn, PredictionOut, Factor

BASE_CASES = {"Chattogram": 118, "Dhaka": 230, "Cox’s Bazar": 54, "Cumilla": 77, "Feni": 32}

def simulate(s: ScenarioIn) -> PredictionOut:
    # Explicitly illustrative rule-based demo only. Not epidemiologically calibrated.
    base = BASE_CASES.get(s.location, 54)
    rain = max(-20, min(35, (s.rainfall_mm - 220) / 12))
    temp = max(-12, min(22, (s.temperature_c - 28) * 5))
    humidity = max(-15, min(25, (s.humidity_pct - 78) * 1.25))
    season = 12 if s.period in range(5, 10) else -4
    score = round(max(0, min(100, 35 + rain + temp + humidity + season)))
    multiplier = .72 + score / 100 * .85
    cases = max(0, round(base * multiplier * (s.period / 4)))
    baseline = max(0, round(base * (.72 + (35 + season) / 100 * .85) * (s.period / 4)))
    level = "Critical" if score >= 75 else "High" if score >= 50 else "Moderate" if score >= 25 else "Low"
    spread = max(8, round(cases * .28))
    recs = (["Remove standing water from rooftops, containers and construction sites.",
             "Coordinate targeted source reduction and larval surveillance.",
             "Healthcare facilities should review triage, fluids and diagnostic supply readiness."]
            if level in ("High", "Critical") else
            ["Maintain weekly checks for standing water and covered storage.",
             "Share symptom-awareness guidance and protect against mosquito bites.",
             "Continue routine case reporting and local vector surveillance."])
    return PredictionOut(
        location=s.location, period_weeks=s.period, estimated_cases=cases,
        baseline_cases=baseline, change_pct=round((cases-baseline)/baseline*100) if baseline else 0,
        risk_index=score, risk_level=level, lower_bound=max(0,cases-spread), upper_bound=cases+spread,
        factors=[
            Factor(name="Rainfall", impact=round(rain), detail=f"{s.rainfall_mm:g} mm vs 220 mm illustrative reference"),
            Factor(name="Temperature", impact=round(temp), detail=f"{s.temperature_c:g}°C vs 28°C illustrative reference"),
            Factor(name="Relative humidity", impact=round(humidity), detail=f"{s.humidity_pct:g}% vs 78% illustrative reference"),
            Factor(name="Seasonality", impact=season, detail="Illustrative monsoon-season adjustment"),
        ],
        recommendations=recs,
        notice="Synthetic demonstration simulation only. Not a validated forecast, clinical assessment, or official public-health alert."
    )
