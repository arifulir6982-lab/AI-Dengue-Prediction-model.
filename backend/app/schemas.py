from pydantic import BaseModel, Field, field_validator
from typing import Literal

class ScenarioIn(BaseModel):
    location: str = Field(min_length=2, max_length=80)
    period: int = Field(ge=1, le=26)
    rainfall_mm: float = Field(ge=0, le=2000)
    temperature_c: float = Field(ge=5, le=50)
    humidity_pct: float = Field(ge=0, le=100)

class Factor(BaseModel):
    name: str
    impact: int
    detail: str

class PredictionOut(BaseModel):
    mode: Literal["simulation", "model"] = "simulation"
    location: str
    period_weeks: int
    estimated_cases: int
    baseline_cases: int
    change_pct: int
    risk_index: int
    risk_level: Literal["Low", "Moderate", "High", "Critical"]
    lower_bound: int
    upper_bound: int
    factors: list[Factor]
    recommendations: list[str]
    notice: str

class UploadSummary(BaseModel):
    rows_accepted: int
    rows_rejected: int
    message: str
