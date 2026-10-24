"""
Schemas for Complexity and Risk Engine.
"""

from typing import Literal
from pydantic import BaseModel, Field


class RiskFactor(BaseModel):
    """Individual evaluated risk rule item."""

    rule_name: str
    points: int = Field(description="Point contribution (+1 to +5)")
    triggered: bool
    reason: str
    severity: Literal["High", "Medium", "Low", "Info"] = "Medium"
    mitigation: str


class ComplexityFactor(BaseModel):
    """Driver of development complexity."""

    category: str
    description: str
    impact: Literal["High", "Medium", "Low"]


class RiskAnalysisResult(BaseModel):
    """Aggregate risk and complexity assessment."""

    complexity_level: Literal["Low", "Medium", "High"]
    complexity_score: int = Field(ge=0, le=100)
    complexity_explanation: str
    complexity_factors: list[ComplexityFactor] = Field(default_factory=list)

    risk_level: Literal["Low", "Medium", "High"]
    total_risk_score: int = Field(ge=0)
    risk_factors: list[RiskFactor] = Field(default_factory=list)
    top_risk_summary: list[str] = Field(default_factory=list)
    recommended_mitigations: list[str] = Field(default_factory=list)
    disclaimer: str = Field(
        default="Preliminary rule-based risk score for pre-sales decision support. "
        "Must be reviewed by Cynbit Technical Leads before quotation commitment."
    )
