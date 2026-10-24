"""
Schemas for structured requirement analysis, tech stack, and missing information.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class FunctionalRequirement(BaseModel):
    """Specific functional feature extracted from brief."""

    id: str = Field(description="Unique requirement ID (e.g., FR-01)")
    category: str = Field(description="Category (e.g., Auth, Catalog, Checkout, AI Engine)")
    title: str = Field(description="Short descriptive title")
    description: str = Field(description="Detailed explanation of what the feature must do")
    priority: Literal["Must Have", "Should Have", "Could Have"] = Field(default="Must Have")
    complexity: Literal["Low", "Medium", "High"] = Field(default="Medium")


class NonFunctionalRequirement(BaseModel):
    """Quality attributes, security, performance, or compliance needs."""

    category: Literal[
        "Security & Privacy",
        "Performance & Latency",
        "Scalability",
        "Compliance & Regulatory",
        "Availability & Reliability",
        "Maintainability",
    ] = Field(default="Performance & Latency")
    description: str
    target_metric: Optional[str] = Field(
        default=None, description="e.g., < 200ms API response, 99.9% uptime, GDPR compliance"
    )


class UserRole(BaseModel):
    """Identified personas and actors in the system."""

    role_name: str
    description: str
    access_level: Literal["Admin", "Standard User", "Manager", "External Guest", "API/System"] = Field(
        default="Standard User"
    )


class PlatformScope(BaseModel):
    """Target devices and deployment platforms."""

    web: bool = Field(default=True, description="Responsive Web application")
    mobile_ios: bool = Field(default=False, description="Apple iOS native/cross-platform")
    mobile_android: bool = Field(default=False, description="Android native/cross-platform")
    admin_portal: bool = Field(default=True, description="Backoffice/Admin Dashboard")
    desktop_app: bool = Field(default=False, description="Desktop Windows/Mac application")
    notes: Optional[str] = None


class ThirdPartyIntegration(BaseModel):
    """External API or service integration."""

    name: str = Field(description="e.g., Stripe, SendGrid, Salesforce, OpenAI, Auth0")
    category: Literal[
        "Payment Gateway",
        "Authentication / SSO",
        "CRM & ERP",
        "Communications (Email/SMS)",
        "AI / LLM Infrastructure",
        "Analytics & Telemetry",
        "Cloud Storage",
        "Other Third-Party API",
    ] = Field(default="Other Third-Party API")
    complexity: Literal["Low", "Medium", "High"] = Field(default="Medium")
    notes: Optional[str] = None


class MissingInformation(BaseModel):
    """Information gap or ambiguous item requiring clarification."""

    id: str = Field(description="e.g., GAP-01")
    category: str = Field(description="e.g., Scope, Non-Functional, Integration, Business")
    gap_description: str = Field(description="What critical detail is missing or vague")
    impact: Literal["High", "Medium", "Low"] = Field(
        default="Medium", description="Impact on estimation accuracy"
    )
    clarification_question: str = Field(
        description="Professional question to ask client to resolve ambiguity"
    )


class TechnologyRecommendation(BaseModel):
    """Recommended production-grade stack with justifications."""

    frontend: str = Field(default="Next.js (React) with TailwindCSS & TypeScript")
    backend: str = Field(default="FastAPI (Python) or Node.js / NestJS")
    database: str = Field(default="PostgreSQL with Redis caching")
    cloud_infrastructure: str = Field(default="AWS (ECS Fargate / RDS / S3 / CloudFront)")
    authentication: str = Field(default="OAuth 2.0 / JWT with Auth0 or Supabase Auth")
    ai_infrastructure: Optional[str] = Field(
        default=None, description="e.g., LangChain / Gemini API / pgvector"
    )
    ci_cd_devops: str = Field(default="GitHub Actions with Docker & Terraform")
    justification: str = Field(
        description="Clear rationale linking stack choices to project needs"
    )


class RequirementAnalysis(BaseModel):
    """Complete structured output from AI requirement extraction."""

    project_name: str = Field(default="Client Project Solution")
    business_objective: str = Field(
        description="Core business goals and problem statement client wants to solve"
    )
    user_roles: list[UserRole] = Field(default_factory=list)
    functional_requirements: list[FunctionalRequirement] = Field(default_factory=list)
    non_functional_requirements: list[NonFunctionalRequirement] = Field(default_factory=list)
    platform_scope: PlatformScope = Field(default_factory=PlatformScope)
    integrations: list[ThirdPartyIntegration] = Field(default_factory=list)
    has_ai_features: bool = Field(
        default=False, description="Flag indicating if project involves AI/ML features"
    )
    ai_features_summary: Optional[str] = None
    missing_information: list[MissingInformation] = Field(default_factory=list)
    tech_recommendation: TechnologyRecommendation = Field(
        default_factory=TechnologyRecommendation
    )
    stated_deadline_weeks: Optional[int] = Field(
        default=None, description="Client stated target deadline in weeks if mentioned"
    )
    budget_range_mentioned: Optional[str] = Field(
        default=None, description="Client mentioned budget if any"
    )
    extracted_assumptions: list[str] = Field(default_factory=list)
    extracted_exclusions: list[str] = Field(default_factory=list)
