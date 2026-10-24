"""
Schemas for Draft Proposal generation and presentation.
"""

from typing import Optional
from pydantic import BaseModel, Field


class DeliverableItem(BaseModel):
    """Specific deliverable committed in the proposal."""

    phase_name: str
    milestone: str
    deliverables: list[str]
    estimated_duration_weeks: float


class ProposalContent(BaseModel):
    """Structured client-facing proposal draft."""

    title: str = Field(default="Cynbit Technical Solution Proposal & Estimate")
    client_name: str = Field(default="Prospective Client")
    prepared_by: str = Field(default="Cynbit AI Pre-Sales Solutions Architecture Team")
    date_created: str

    executive_summary: str
    business_context_and_goals: str
    scope_of_work: list[str]
    out_of_scope_exclusions: list[str]
    deliverables_by_phase: list[DeliverableItem]

    recommended_tech_stack_summary: str
    key_architectural_decisions: list[str]

    timeline_summary: str
    recommended_team_structure: str

    pricing_options_summary: str
    assumptions_and_prerequisites: list[str]
    client_clarification_questions: list[str]
    next_steps: list[str]

    expert_review_disclaimer: str = Field(
        default="NOTICE: This pre-sales solution assessment and proposal draft was prepared by "
        "the Cynbit AI Pre-Sales Solution Architect assistant for initial review and decision support. "
        "All figures, timelines, and architectural commitments are indicative ranges subject to "
        "formal technical discovery and Cynbit executive sign-off."
    )
