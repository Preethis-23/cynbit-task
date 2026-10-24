"""
Schemas for Effort, Timeline, Cost, and Profit Estimation.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class EffortBreakdown(BaseModel):
    """Hour breakdown across engineering disciplines."""

    frontend_hours: float = 0.0
    backend_hours: float = 0.0
    database_arch_hours: float = 0.0
    ai_ml_hours: float = 0.0
    integration_hours: float = 0.0
    qa_testing_hours: float = 0.0
    devops_infra_hours: float = 0.0
    project_management_hours: float = 0.0
    contingency_hours: float = 0.0
    total_base_hours: float = 0.0


class EffortRange(BaseModel):
    """Estimated hours with uncertainty bounds."""

    min_hours: float
    likely_hours: float
    max_hours: float
    breakdown: EffortBreakdown


class TimelineRange(BaseModel):
    """Delivery timeline in calendar weeks with uncertainty bounds."""

    min_weeks: float
    likely_weeks: float
    max_weeks: float
    critical_path_notes: str


class TeamMemberRequirement(BaseModel):
    """Role needed on the delivery team."""

    role: str
    count: int = 1
    allocation_pct: int = 100
    responsibilities: str


class CommercialAssessment(BaseModel):
    """Financial calculations for internal cost, quote, profit, and margin."""

    # Parameters used
    hourly_internal_cost: float = Field(description="Internal cost rate/hr")
    hourly_billing_rate: float = Field(description="Client billing rate/hr")
    contingency_pct: float = Field(description="Applied contingency buffer %")
    target_margin_pct: float = Field(description="Target gross profit margin %")

    # Internal Cost (Hours * hourly_internal_cost)
    internal_cost_min: float
    internal_cost_likely: float
    internal_cost_max: float

    # Quotation Price (Hours * hourly_billing_rate)
    quotation_min: float
    quotation_likely: float
    quotation_max: float

    # Expected Profit (Quotation - Internal Cost)
    expected_profit_min: float
    expected_profit_likely: float
    expected_profit_max: float

    # Profit Margin % (Expected Profit / Quotation * 100)
    profit_margin_min_pct: float
    profit_margin_likely_pct: float
    profit_margin_max_pct: float

    # ML Benchmark Comparison (Optional)
    ml_predicted_hours: Optional[float] = None
    ml_model_used: Optional[str] = None
    ml_confidence_interval: Optional[str] = None

    team_composition: list[TeamMemberRequirement] = Field(default_factory=list)
    confidence_level: Literal["High", "Medium", "Low"] = "Medium"
    confidence_notes: str = ""
