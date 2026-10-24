"""
Estimation, Timeline, and Commercial Financial Calculation Engine.
Calculates transparent hours, calendar timeline, team composition, internal costs,
quotations, profit ranges, and contingency reserves.
"""

from typing import Optional
from config.settings import settings
from src.schemas.requirements import RequirementAnalysis
from src.schemas.risk import RiskAnalysisResult
from src.schemas.estimation import (
    EffortBreakdown,
    EffortRange,
    TimelineRange,
    TeamMemberRequirement,
    CommercialAssessment,
)


class EstimationEngine:
    """Calculates effort, duration, team sizing, and financial margins."""

    @staticmethod
    def calculate_effort(
        analysis: RequirementAnalysis,
        risk: RiskAnalysisResult,
        contingency_pct: float = settings.default_contingency_pct,
    ) -> EffortRange:
        """Calculates discipline-specific effort and uncertainty bounds."""
        # 1. Base functional hours
        frontend_hours = 0.0
        backend_hours = 0.0

        for fr in analysis.functional_requirements:
            if fr.complexity == "High":
                f_h, b_h = 60.0, 80.0
            elif fr.complexity == "Low":
                f_h, b_h = 20.0, 25.0
            else:  # Medium
                f_h, b_h = 35.0, 45.0
            frontend_hours += f_h
            backend_hours += b_h

        # Check if this is a lightweight/simple scope
        is_lightweight = (
            len(analysis.functional_requirements) <= 3
            and not (analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android)
            and not analysis.has_ai_features
            and not any(ig.category in ["Payment Gateway", "CRM & ERP"] for ig in analysis.integrations)
        )

        # Minimum base hours scaled by project size
        if is_lightweight:
            frontend_hours = max(frontend_hours, 40.0)
            backend_hours = max(backend_hours, 30.0)
        else:
            frontend_hours = max(frontend_hours, 80.0)
            backend_hours = max(backend_hours, 100.0)

        # 2. Platform Multiplier
        has_mobile = analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android
        if has_mobile and analysis.platform_scope.web:
            frontend_hours *= 1.45  # Multi-platform responsive/cross-platform overhead
        elif has_mobile and not analysis.platform_scope.web:
            frontend_hours *= 1.2

        if analysis.platform_scope.admin_portal:
            admin_f = 20.0 if is_lightweight else 50.0
            admin_b = 15.0 if is_lightweight else 40.0
            frontend_hours += admin_f
            backend_hours += admin_b

        # 3. Database & System Architecture
        database_hours = 15.0 if is_lightweight else (40.0 + (len(analysis.functional_requirements) * 3.0))

        # 4. Integrations
        integration_hours = 0.0
        for ig in analysis.integrations:
            if ig.complexity == "High":
                integration_hours += 70.0
            elif ig.complexity == "Low":
                integration_hours += 25.0
            else:
                integration_hours += 45.0

        if not analysis.integrations:
            integration_hours = 30.0  # Basic cloud auth / SMTP

        # 5. AI / ML Engineering
        ai_ml_hours = 0.0
        if analysis.has_ai_features:
            ai_ml_hours = 160.0

        # Subtotal Engineering
        dev_subtotal = frontend_hours + backend_hours + database_hours + integration_hours + ai_ml_hours

        # 6. QA & Test Automation (approx 18% of dev effort)
        qa_hours = round(dev_subtotal * 0.18, 1)

        # 7. DevOps & Cloud Infrastructure (approx 12% of dev effort)
        devops_hours = round(dev_subtotal * 0.12, 1)

        # 8. Project Management & Solution Architecture (approx 15% of dev effort)
        pm_hours = round(dev_subtotal * 0.15, 1)

        base_total = dev_subtotal + qa_hours + devops_hours + pm_hours

        # 9. Contingency reserve based on risk level and setting
        risk_buffer_multiplier = 1.0
        if risk.risk_level == "High":
            risk_buffer_multiplier = 1.35
        elif risk.risk_level == "Medium":
            risk_buffer_multiplier = 1.15

        effective_contingency_pct = contingency_pct * risk_buffer_multiplier
        contingency_hours = round(base_total * (effective_contingency_pct / 100.0), 1)

        likely_hours = round(base_total + contingency_hours, 1)
        min_hours = round(likely_hours * 0.85, 1)
        max_hours = round(likely_hours * 1.25, 1)

        breakdown = EffortBreakdown(
            frontend_hours=round(frontend_hours, 1),
            backend_hours=round(backend_hours, 1),
            database_arch_hours=round(database_hours, 1),
            ai_ml_hours=round(ai_ml_hours, 1),
            integration_hours=round(integration_hours, 1),
            qa_testing_hours=round(qa_hours, 1),
            devops_infra_hours=round(devops_hours, 1),
            project_management_hours=round(pm_hours, 1),
            contingency_hours=contingency_hours,
            total_base_hours=round(base_total, 1),
        )

        return EffortRange(
            min_hours=min_hours,
            likely_hours=likely_hours,
            max_hours=max_hours,
            breakdown=breakdown,
        )

    @staticmethod
    def calculate_timeline(effort: EffortRange, has_ai: bool, has_mobile: bool) -> TimelineRange:
        """
        Calculates realistic calendar duration assuming an agile pod of 3-4 developers.
        Typical agile pod capacity: ~100-130 effective engineering hours per week.
        """
        weekly_team_throughput = 110.0  # effective delivery hours / week
        likely_weeks = max(6.0, round(effort.likely_hours / weekly_team_throughput, 1))
        min_weeks = max(5.0, round(effort.min_hours / (weekly_team_throughput * 1.15), 1))
        max_weeks = max(7.0, round(effort.max_hours / (weekly_team_throughput * 0.9), 1))

        critical_path_notes = (
            f"Critical path dependencies: Architecture & DB schema design (Sprints 1-2) -> "
            f"Core backend APIs & auth (Sprints 2-4) -> {'Mobile/Web UI integration' if has_mobile else 'Web UI integration'} (Sprints 3-6) -> "
            f"{'AI recommendation pipelines & fine-tuning -> ' if has_ai else ''}"
            f"End-to-end integration & UAT hardening (Final 3 weeks)."
        )

        return TimelineRange(
            min_weeks=min_weeks,
            likely_weeks=likely_weeks,
            max_weeks=max_weeks,
            critical_path_notes=critical_path_notes,
        )

    @staticmethod
    def get_team_composition(
        effort: EffortRange,
        has_ai: bool,
        has_mobile: bool,
    ) -> list[TeamMemberRequirement]:
        """Recommends dedicated staffing roles for the project."""
        team = [
            TeamMemberRequirement(
                role="Lead Solution Architect / Tech Lead",
                count=1,
                allocation_pct=50,
                responsibilities="System design, API contracts, security review, and technical oversight.",
            ),
            TeamMemberRequirement(
                role="Senior Full-Stack / Backend Engineer",
                count=1,
                allocation_pct=100,
                responsibilities="FastAPI/Node microservices, database schemas, and integration gateways.",
            ),
            TeamMemberRequirement(
                role="Senior Frontend / Mobile Engineer",
                count=1 if not (has_mobile and effort.likely_hours > 900) else 2,
                allocation_pct=100,
                responsibilities="Next.js responsive web portal and cross-platform mobile client.",
            ),
            TeamMemberRequirement(
                role="QA Automation Engineer",
                count=1,
                allocation_pct=75,
                responsibilities="Automated API tests, Playwright UI regression, and security sanity testing.",
            ),
            TeamMemberRequirement(
                role="Technical Project Manager / Scrum Master",
                count=1,
                allocation_pct=50,
                responsibilities="Sprint backlog, client communications, timeline tracking, and risk management.",
            ),
        ]

        if has_ai:
            team.append(
                TeamMemberRequirement(
                    role="AI / ML Engineer",
                    count=1,
                    allocation_pct=50,
                    responsibilities="Vector embeddings, prompt evaluation, model integration, and evaluation metrics.",
                )
            )

        return team

    @classmethod
    def calculate_commercials(
        cls,
        effort: EffortRange,
        risk: RiskAnalysisResult,
        hourly_internal_cost: float = settings.default_hourly_cost,
        hourly_billing_rate: float = settings.default_hourly_bill_rate,
        contingency_pct: float = settings.default_contingency_pct,
        target_margin_pct: float = settings.default_target_margin_pct,
        has_ai: bool = False,
        has_mobile: bool = False,
        ml_predicted_hours: Optional[float] = None,
    ) -> CommercialAssessment:
        """
        Executes financial calculations:
        internal_cost = estimated_hours * hourly_internal_cost
        expected_profit = quotation_price - internal_cost
        profit_margin = expected_profit / quotation_price * 100
        """
        # Internal Cost
        cost_min = round(effort.min_hours * hourly_internal_cost, 2)
        cost_likely = round(effort.likely_hours * hourly_internal_cost, 2)
        cost_max = round(effort.max_hours * hourly_internal_cost, 2)

        # Quotation Price (Hours * Billing Rate)
        quote_min = round(effort.min_hours * hourly_billing_rate, 2)
        quote_likely = round(effort.likely_hours * hourly_billing_rate, 2)
        quote_max = round(effort.max_hours * hourly_billing_rate, 2)

        # Expected Profit
        profit_min = round(quote_min - cost_min, 2)
        profit_likely = round(quote_likely - cost_likely, 2)
        profit_max = round(quote_max - cost_max, 2)

        # Profit Margin %
        margin_min = round((profit_min / quote_min * 100), 1) if quote_min > 0 else 0.0
        margin_likely = round((profit_likely / quote_likely * 100), 1) if quote_likely > 0 else 0.0
        margin_max = round((profit_max / quote_max * 100), 1) if quote_max > 0 else 0.0

        team = cls.get_team_composition(effort, has_ai=has_ai, has_mobile=has_mobile)

        confidence_level = "High" if risk.risk_level == "Low" else ("Medium" if risk.risk_level == "Medium" else "Low")
        confidence_notes = (
            f"Commercial estimates prepared with a {contingency_pct:.0f}% baseline contingency. "
            f"At a standard ${hourly_billing_rate:.0f}/hr billing rate and ${hourly_internal_cost:.0f}/hr blended internal cost, "
            f"the projected gross profit margin is {margin_likely:.1f}%."
        )

        return CommercialAssessment(
            hourly_internal_cost=hourly_internal_cost,
            hourly_billing_rate=hourly_billing_rate,
            contingency_pct=contingency_pct,
            target_margin_pct=target_margin_pct,
            internal_cost_min=cost_min,
            internal_cost_likely=cost_likely,
            internal_cost_max=cost_max,
            quotation_min=quote_min,
            quotation_likely=quote_likely,
            quotation_max=quote_max,
            expected_profit_min=profit_min,
            expected_profit_likely=profit_likely,
            expected_profit_max=profit_max,
            profit_margin_min_pct=margin_min,
            profit_margin_likely_pct=margin_likely,
            profit_margin_max_pct=margin_max,
            ml_predicted_hours=ml_predicted_hours,
            ml_model_used="RandomForestRegressor (Proof of Concept)" if ml_predicted_hours else None,
            team_composition=team,
            confidence_level=confidence_level,
            confidence_notes=confidence_notes,
        )
