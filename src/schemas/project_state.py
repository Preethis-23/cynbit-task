"""
Unified session state schema combining ingestion, requirements, estimation, risks, and proposal.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from src.schemas.document import IngestedDocument
from src.schemas.requirements import RequirementAnalysis
from src.schemas.risk import RiskAnalysisResult
from src.schemas.estimation import EffortRange, TimelineRange, CommercialAssessment
from src.schemas.proposal import ProposalContent


class BenchmarkMatch(BaseModel):
    """Similar historical or synthetic project match."""

    project_id: str
    project_name: str
    project_type: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    actual_hours: float
    actual_weeks: float
    risk_level: str
    tech_stack: str
    key_similarities: str


class ProjectAnalysisState(BaseModel):
    """Complete project state saved and editable in session."""

    session_id: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    document: IngestedDocument
    requirements: RequirementAnalysis
    risk: RiskAnalysisResult
    effort: EffortRange
    timeline: TimelineRange
    commercial: CommercialAssessment
    benchmark_matches: list[BenchmarkMatch] = Field(default_factory=list)
    proposal: Optional[ProposalContent] = None
    is_human_reviewed: bool = False
    reviewer_notes: Optional[str] = None
    final_decision: Optional[str] = None  # "ACCEPT", "REJECT", "REQUEST_CLARIFICATION"
