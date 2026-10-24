"""
Pydantic Schemas for Cynbit Pre-Sales Solution Architect.
"""

from src.schemas.document import DocumentMetadata, IngestedDocument
from src.schemas.requirements import (
    FunctionalRequirement,
    NonFunctionalRequirement,
    UserRole,
    PlatformScope,
    ThirdPartyIntegration,
    MissingInformation,
    TechnologyRecommendation,
    RequirementAnalysis,
)
from src.schemas.risk import RiskFactor, ComplexityFactor, RiskAnalysisResult
from src.schemas.estimation import (
    EffortBreakdown,
    EffortRange,
    TimelineRange,
    TeamMemberRequirement,
    CommercialAssessment,
)
from src.schemas.proposal import DeliverableItem, ProposalContent
from src.schemas.project_state import BenchmarkMatch, ProjectAnalysisState

__all__ = [
    "DocumentMetadata",
    "IngestedDocument",
    "FunctionalRequirement",
    "NonFunctionalRequirement",
    "UserRole",
    "PlatformScope",
    "ThirdPartyIntegration",
    "MissingInformation",
    "TechnologyRecommendation",
    "RequirementAnalysis",
    "RiskFactor",
    "ComplexityFactor",
    "RiskAnalysisResult",
    "EffortBreakdown",
    "EffortRange",
    "TimelineRange",
    "TeamMemberRequirement",
    "CommercialAssessment",
    "DeliverableItem",
    "ProposalContent",
    "BenchmarkMatch",
    "ProjectAnalysisState",
]
