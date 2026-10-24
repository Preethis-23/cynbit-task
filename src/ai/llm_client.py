"""
Unified LLM Client supporting Google Gemini, OpenAI, and deterministic offline fallback.
Validates structured JSON output against Pydantic schemas with auto-retry.
"""

import json
import os
import re
from datetime import datetime
from typing import Optional, Tuple

from config.settings import settings
from src.schemas.requirements import RequirementAnalysis
from src.schemas.proposal import ProposalContent, DeliverableItem
from src.schemas.estimation import CommercialAssessment
from src.schemas.risk import RiskAnalysisResult
from src.ai.prompts import (
    EXTRACTION_SYSTEM_PROMPT,
    EXTRACTION_USER_PROMPT_TEMPLATE,
    PROPOSAL_GENERATION_PROMPT_TEMPLATE,
)
from src.ai.mock_engine import MockExtractorEngine


class LLMClient:
    """Multi-provider client for requirement analysis and proposal synthesis."""

    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or settings.llm_provider).lower()
        self.gemini_key = os.getenv("GEMINI_API_KEY") or settings.gemini_api_key
        self.openai_key = os.getenv("OPENAI_API_KEY") or settings.openai_api_key

    def _clean_json_markdown(self, raw: str) -> str:
        """Strip markdown fences ```json ... ``` from LLM response."""
        cleaned = raw.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned.strip()

    def _call_gemini(self, prompt: str, system_prompt: str) -> str:
        """Execute request via Google Gemini API."""
        if not self.gemini_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        # Attempt 1: google.genai client (version 2.x)
        try:
            from google import genai
            client = genai.Client(api_key=self.gemini_key)
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config={
                    "system_instruction": system_prompt,
                    "response_mime_type": "application/json",
                },
            )
            return response.text
        except Exception:
            # Attempt 2: google.generativeai legacy package
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=self.gemini_key)
            model = genai_legacy.GenerativeModel(
                model_name=settings.gemini_model,
                system_instruction=system_prompt,
                generation_config={"response_mime_type": "application/json"},
            )
            response = model.generate_content(prompt)
            return response.text

    def _call_openai(self, prompt: str, system_prompt: str) -> str:
        """Execute request via OpenAI API."""
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY is not configured.")

        from openai import OpenAI
        client = OpenAI(api_key=self.openai_key)
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        return response.choices[0].message.content or "{}"

    def extract_requirements(self, brief_text: str) -> Tuple[RequirementAnalysis, str]:
        """
        Extracts structured requirements.
        Returns (RequirementAnalysis, engine_name_used).
        """
        user_prompt = EXTRACTION_USER_PROMPT_TEMPLATE.format(brief_text=brief_text)

        # 1. Check if configured for Gemini
        if self.provider == "gemini" and self.gemini_key:
            try:
                raw_json = self._call_gemini(user_prompt, EXTRACTION_SYSTEM_PROMPT)
                cleaned = self._clean_json_markdown(raw_json)
                parsed = json.loads(cleaned)
                return RequirementAnalysis.model_validate(parsed), f"Google Gemini ({settings.gemini_model})"
            except Exception as err:
                print(f"[LLM Warning] Gemini extraction failed: {err}. Falling back to offline engine.")

        # 2. Check OpenAI
        elif self.provider == "openai" and self.openai_key:
            try:
                raw_json = self._call_openai(user_prompt, EXTRACTION_SYSTEM_PROMPT)
                cleaned = self._clean_json_markdown(raw_json)
                parsed = json.loads(cleaned)
                return RequirementAnalysis.model_validate(parsed), f"OpenAI ({settings.openai_model})"
            except Exception as err:
                print(f"[LLM Warning] OpenAI extraction failed: {err}. Falling back to offline engine.")

        # 3. Fallback: High-Quality Offline Mock Engine
        result = MockExtractorEngine.extract(brief_text)
        return result, "Offline Rule & NLP Engine (Zero API Dependency)"

    def generate_proposal(
        self,
        analysis: RequirementAnalysis,
        commercial: CommercialAssessment,
        risk: RiskAnalysisResult,
        client_name: str = "Prospective Client",
    ) -> Tuple[ProposalContent, str]:
        """
        Generates executive client proposal draft.
        Returns (ProposalContent, engine_name_used).
        """
        features_summary = ", ".join([f"{fr.title} ({fr.priority})" for fr in analysis.functional_requirements[:5]])
        integrations_summary = ", ".join([ig.name for ig in analysis.integrations]) or "Standard Cloud APIs"
        clarifications_summary = "; ".join([g.gap_description for g in analysis.missing_information[:3]])
        top_risks = "; ".join(risk.top_risk_summary) or "Standard software development execution risk"
        platforms = f"Web={analysis.platform_scope.web}, iOS={analysis.platform_scope.mobile_ios}, Android={analysis.platform_scope.mobile_android}"
        tech_stack = f"Frontend: {analysis.tech_recommendation.frontend} | Backend: {analysis.tech_recommendation.backend} | DB: {analysis.tech_recommendation.database} | Cloud: {analysis.tech_recommendation.cloud_infrastructure}"
        date_str = datetime.now().strftime("%B %d, %Y")

        prompt = PROPOSAL_GENERATION_PROMPT_TEMPLATE.format(
            client_name=client_name,
            project_name=analysis.project_name,
            business_objective=analysis.business_objective,
            platforms=platforms,
            features_summary=features_summary,
            integrations_summary=integrations_summary,
            clarifications_summary=clarifications_summary,
            min_hours=commercial.internal_cost_min / commercial.hourly_internal_cost if commercial.hourly_internal_cost else 800,
            max_hours=commercial.internal_cost_max / commercial.hourly_internal_cost if commercial.hourly_internal_cost else 1200,
            likely_hours=commercial.internal_cost_likely / commercial.hourly_internal_cost if commercial.hourly_internal_cost else 1000,
            min_weeks=8.0,
            max_weeks=16.0,
            likely_weeks=12.0,
            quotation_min=commercial.quotation_min,
            quotation_max=commercial.quotation_max,
            quotation_likely=commercial.quotation_likely,
            complexity_level=risk.complexity_level,
            risk_level=risk.risk_level,
            top_risks=top_risks,
            tech_stack=tech_stack,
            date_str=date_str,
        )

        system_prompt = "You are Cynbit's Lead Solution Architect preparing an executive technical proposal draft in JSON format."

        # Attempt Gemini
        if self.provider == "gemini" and self.gemini_key:
            try:
                raw_json = self._call_gemini(prompt, system_prompt)
                cleaned = self._clean_json_markdown(raw_json)
                data = json.loads(cleaned)
                return ProposalContent.model_validate(data), f"Google Gemini ({settings.gemini_model})"
            except Exception as err:
                print(f"[Proposal Warning] Gemini proposal failed: {err}. Falling back to template synthesis.")

        # Attempt OpenAI
        elif self.provider == "openai" and self.openai_key:
            try:
                raw_json = self._call_openai(prompt, system_prompt)
                cleaned = self._clean_json_markdown(raw_json)
                data = json.loads(cleaned)
                return ProposalContent.model_validate(data), f"OpenAI ({settings.openai_model})"
            except Exception as err:
                print(f"[Proposal Warning] OpenAI proposal failed: {err}. Falling back to template synthesis.")

        # Deterministic High-Quality Fallback
        scope_items = [f"{fr.title}: {fr.description}" for fr in analysis.functional_requirements]
        clarifications = [gap.clarification_question for gap in analysis.missing_information]

        fallback_proposal = ProposalContent(
            title=f"Technical Solution Proposal: {analysis.project_name}",
            client_name=client_name,
            prepared_by="Cynbit AI Pre-Sales Solutions Architecture Team",
            date_created=date_str,
            executive_summary=(
                f"Cynbit is pleased to submit this preliminary pre-sales solution architecture for {analysis.project_name}. "
                f"Based on the initial client brief, our team has formulated a modern, scalable engineering roadmap "
                f"designed to achieve {analysis.business_objective[:150]}... while maintaining enterprise-grade security and velocity."
            ),
            business_context_and_goals=analysis.business_objective,
            scope_of_work=scope_items,
            out_of_scope_exclusions=analysis.extracted_exclusions or [
                "Legacy data extraction and physical tape backups.",
                "Third-party software subscription and cloud licensing fees.",
                "Custom hardware integration beyond standard mobile devices.",
            ],
            deliverables_by_phase=[
                DeliverableItem(
                    phase_name="Phase 1: Technical Discovery & Architecture",
                    milestone="Architecture Blueprint & UX Prototypes",
                    deliverables=[
                        "Detailed System Architecture Design Document (SADD)",
                        "Interactive UX/UI Wireframes and Design System",
                        "REST / GraphQL API Schema Specifications",
                        "Threat Modeling and Security Compliance Review",
                    ],
                    estimated_duration_weeks=3.0,
                ),
                DeliverableItem(
                    phase_name="Phase 2: Core Platform Engineering",
                    milestone="Functional Alpha & MVP Platform",
                    deliverables=[
                        "Core Business Logic and Microservice / Monolith Backend APIs",
                        "Responsive Web Client & Mobile Framework Deployment",
                        "Payment Gateway & Third-Party System Integrations",
                        "Initial Staging Environment Deployment",
                    ],
                    estimated_duration_weeks=7.0,
                ),
                DeliverableItem(
                    phase_name="Phase 3: AI Intelligence, QA & Hardening",
                    milestone="Feature Complete Beta & User Acceptance Testing",
                    deliverables=[
                        "AI/ML Feature Pipelines & Recommendation Embeddings" if analysis.has_ai_features else "Advanced Reporting & Analytics Modules",
                        "Automated Unit, Integration, and Load Test Suites",
                        "Penetration Testing and Vulnerability Remediation",
                        "Client User Acceptance Testing (UAT) Sign-off",
                    ],
                    estimated_duration_weeks=4.0,
                ),
                DeliverableItem(
                    phase_name="Phase 4: Production Launch & Operational Handover",
                    milestone="Production Go-Live & Post-Launch Monitoring",
                    deliverables=[
                        "Multi-Region Cloud Infrastructure Launch with CI/CD",
                        "Monitoring, Logging, and Alerting Dashboards (Datadog/CloudWatch)",
                        "Engineering Knowledge Transfer & As-Built Documentation",
                        "30-Day Post-Launch Warranty Period",
                    ],
                    estimated_duration_weeks=2.0,
                ),
            ],
            recommended_tech_stack_summary=analysis.tech_recommendation.justification,
            key_architectural_decisions=[
                f"Frontend: {analysis.tech_recommendation.frontend} for responsive cross-device performance.",
                f"Backend: {analysis.tech_recommendation.backend} for secure asynchronous API processing.",
                f"Database: {analysis.tech_recommendation.database} for relational integrity and caching speed.",
                f"Cloud: {analysis.tech_recommendation.cloud_infrastructure} ensuring auto-scaling and high availability.",
                f"Authentication: {analysis.tech_recommendation.authentication}.",
            ],
            timeline_summary=(
                f"Total projected execution duration is approximately 12 to 16 calendar weeks, "
                f"structured in four iterative agile milestones with bi-weekly sprint demos."
            ),
            recommended_team_structure=(
                "Dedicated Agile Pod: 1 Technical Lead / Architect (50%), 1 Senior Backend Engineer (100%), "
                "1 Senior Frontend / Mobile Engineer (100%), 1 QA & Test Automation Specialist (75%), "
                "and 1 Technical Project Manager / Scrum Master (50%)."
            ),
            pricing_options_summary=(
                f"Indicative quotation range: ${commercial.quotation_min:,.0f} to ${commercial.quotation_max:,.0f} "
                f"(Baseline Estimate: ${commercial.quotation_likely:,.0f}). "
                f"Structured on milestone-based billing: 25% on Project Kickoff, 25% on Architecture Sign-off, "
                f"25% on Beta UAT, and 25% on Final Production Go-Live."
            ),
            assumptions_and_prerequisites=analysis.extracted_assumptions,
            client_clarification_questions=clarifications or [
                "What is the expected peak concurrent active user volume?",
                "Are there specific third-party systems requiring custom APIs?",
            ],
            next_steps=[
                "1. Schedule a 45-minute Technical Discovery Session with Cynbit's Lead Architect.",
                "2. Review and answer client clarification questions to refine scope bounds.",
                "3. Finalize Master Services Agreement (MSA) and Statement of Work (SOW).",
                "4. Mobilize sprint engineering team for Sprint 0 Kickoff.",
            ],
        )

        return fallback_proposal, "Cynbit Template & Heuristic Synthesis Engine"
