from pydantic import BaseModel, Field
from typing import List, Optional


# ---------- INPUT SCHEMA ----------
class BrandInput(BaseModel):
    brand_name: str = Field(..., example="FitSphere")
    product: Optional[str] = Field(None, example="Online fitness coaching")
    target_audience: Optional[str] = Field(None, example="Working professionals")
    tone: Optional[str] = Field("professional", example="premium")


# ---------- NESTED OUTPUT SCHEMA ----------
class TargetAudience(BaseModel):
    age_range: str
    pain_points: List[str]
    desires: List[str]


# ---------- OUTPUT SCHEMA ----------
class BrandOutput(BaseModel):
    brand_voice: str
    core_emotions: List[str]
    target_audience: TargetAudience
    communication_style: str
    cta_style: str
