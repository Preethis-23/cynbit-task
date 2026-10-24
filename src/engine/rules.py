"""
Transparent Risk and Complexity Scoring Engine.
Maps objective project attributes to explainable risk factors, points, and severity levels.
"""

from src.schemas.requirements import RequirementAnalysis
from src.schemas.risk import RiskFactor, ComplexityFactor, RiskAnalysisResult


class RiskEngine:
    """Evaluates risk and complexity using deterministic, fully-explained business rules."""

    @staticmethod
    def evaluate(analysis: RequirementAnalysis) -> RiskAnalysisResult:
        factors: list[RiskFactor] = []
        total_risk_score = 0

        # Rule 1: Missing or Ambiguous Requirements
        unclear_count = len(analysis.missing_information)
        has_high_gaps = any(g.impact == "High" for g in analysis.missing_information)
        if has_high_gaps and unclear_count >= 2:
            pts = 3
            total_risk_score += pts
            factors.append(
                RiskFactor(
                    rule_name="Unclear or Incomplete Requirements",
                    points=pts,
                    triggered=True,
                    reason=f"Found {unclear_count} information gaps with high-impact ambiguities (e.g., unspecified user volumes or architecture).",
                    severity="High",
                    mitigation="Conduct a paid Technical Discovery sprint to clarify user stories and non-functional specifications before signing fixed-price SOW.",
                )
            )
        elif has_high_gaps:
            pts = 2
            total_risk_score += pts
            factors.append(
                RiskFactor(
                    rule_name="Critical Information Gap",
                    points=pts,
                    triggered=True,
                    reason=f"Detected critical ambiguity in brief ({analysis.missing_information[0].gap_description}).",
                    severity="Medium",
                    mitigation="Confirm critical specification before finalizing contractual bounds.",
                )
            )
        elif unclear_count >= 2:
            pts = 1
            total_risk_score += pts
            factors.append(
                RiskFactor(
                    rule_name="Minor Informational Gaps",
                    points=pts,
                    triggered=True,
                    reason=f"Found {unclear_count} minor clarifications (e.g. brand assets or copywriting).",
                    severity="Low",
                    mitigation="Review during kickoff onboarding.",
                )
            )

        # Rule 2: Multiple Third-Party Integrations (> 2 integrations -> +2 points)
        external_integrations = [
            ig for ig in analysis.integrations
            if ig.category in ["Payment Gateway", "CRM & ERP", "AI / LLM Infrastructure"]
        ]
        integration_count = len(external_integrations)
        if integration_count > 2:
            pts = 2
            total_risk_score += pts
            factors.append(
                RiskFactor(
                    rule_name="High Integration Dependency (>2 External Systems)",
                    points=pts,
                    triggered=True,
                    reason=f"Project relies on {integration_count} complex third-party systems. External API latency and breaking changes present delivery risks.",
                    severity="Medium",
                    mitigation="Implement circuit breakers, mock sandbox adapters for local development, and require early client sign-off on API credentials.",
                )
            )
        elif integration_count >= 1:
            factors.append(
                RiskFactor(
                    rule_name="External Service Integration",
                    points=1,
                    triggered=True,
                    reason=f"Project integrates with {integration_count} external service(s).",
                    severity="Low",
                    mitigation="Verify API documentation and sandbox access early in Sprint 1.",
                )
            )
            total_risk_score += 1

        # Rule 3: Multi-Platform Scope (Web + Mobile -> +2 points)
        is_multi_platform = analysis.platform_scope.web and (
            analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android
        )
        if is_multi_platform:
            pts = 2
            total_risk_score += pts
            factors.append(
                RiskFactor(
                    rule_name="Multi-Platform Development (Web + Mobile)",
                    points=pts,
                    triggered=True,
                    reason="Simultaneous delivery across responsive web and mobile operating systems increases QA surface area, app store approval latency, and responsive UI overhead.",
                    severity="Medium",
                    mitigation="Adopt a unified cross-platform mobile framework (e.g., React Native) with shared TypeScript types and automated CI/CD builds.",
                )
            )

        # Rule 4: AI/ML Feature Inclusion (+2 points)
        if analysis.has_ai_features:
            pts = 2
            total_risk_score += pts
            factors.append(
                RiskFactor(
                    rule_name="AI/ML Algorithm Uncertainty",
                    points=pts,
                    triggered=True,
                    reason="Inclusion of AI/ML or LLM features introduces non-deterministic outputs, latency overhead, inference cost management, and dependency on prompt/data readiness.",
                    severity="Medium",
                    mitigation="Implement structured evaluation benchmarks, caching layers, and clear fallback heuristics when model confidence is low.",
                )
            )

        # Rule 5: Unusually Aggressive Deadline (+1 or +2 points)
        if analysis.stated_deadline_weeks is not None:
            if analysis.stated_deadline_weeks < 8:
                pts = 2
                total_risk_score += pts
                factors.append(
                    RiskFactor(
                        rule_name="Unusually Compressed Timeline (<8 Weeks)",
                        points=pts,
                        triggered=True,
                        reason=f"Client requested a {analysis.stated_deadline_weeks}-week deadline, which is severely compressed for this feature scope.",
                        severity="High",
                        mitigation="Descope to a strict Phase 1 MVP or negotiate a phased delivery with MVP at week 8 and secondary features at week 12.",
                    )
                )
            elif analysis.stated_deadline_weeks <= 12 and (is_multi_platform or analysis.has_ai_features):
                pts = 1
                total_risk_score += pts
                factors.append(
                    RiskFactor(
                        rule_name="Tight Delivery Window",
                        points=pts,
                        triggered=True,
                        reason=f"Requested {analysis.stated_deadline_weeks} weeks leaves minimal buffer for integration testing and app store approvals.",
                        severity="Medium",
                        mitigation="Allocate dedicated senior engineers and enforce strict scope freezes after sprint 2.",
                    )
                )

        # Rule 6: High Feature Density (> 10 functional features -> +1 point)
        fr_count = len(analysis.functional_requirements)
        if fr_count > 10:
            pts = 1
            total_risk_score += pts
            factors.append(
                RiskFactor(
                    rule_name="Broad Functional Scope (>10 Core Features)",
                    points=pts,
                    triggered=True,
                    reason=f"Detected {fr_count} functional requirements in initial brief. High risk of scope creep without strict change control.",
                    severity="Medium",
                    mitigation="Establish a formal change-request process with explicit sprint velocity caps.",
                )
            )

        # Determine Risk Level
        if total_risk_score >= 6:
            risk_level = "High"
        elif total_risk_score >= 3:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # Complexity Analysis
        complexity_factors: list[ComplexityFactor] = []
        comp_score = 20  # Base complexity

        # Feature volume
        comp_score += min(fr_count * 4, 30)
        complexity_factors.append(
            ComplexityFactor(
                category="Feature Volume",
                description=f"{fr_count} distinct functional requirements identified.",
                impact="High" if fr_count > 8 else "Medium",
            )
        )

        # Platforms
        platform_count = sum(
            [
                analysis.platform_scope.web,
                analysis.platform_scope.mobile_ios,
                analysis.platform_scope.mobile_android,
                analysis.platform_scope.admin_portal,
                analysis.platform_scope.desktop_app,
            ]
        )
        comp_score += platform_count * 5
        complexity_factors.append(
            ComplexityFactor(
                category="Platform Breadth",
                description=f"Supporting {platform_count} platform targets (Web, Mobile, Admin, etc.).",
                impact="High" if platform_count >= 3 else "Medium",
            )
        )

        # Integrations
        comp_score += min(integration_count * 6, 25)
        if integration_count > 0:
            complexity_factors.append(
                ComplexityFactor(
                    category="External Integrations",
                    description=f"{integration_count} third-party APIs/gateways requiring custom auth and webhook handling.",
                    impact="High" if integration_count > 2 else "Medium",
                )
            )

        # AI
        if analysis.has_ai_features:
            comp_score += 15
            complexity_factors.append(
                ComplexityFactor(
                    category="AI / Machine Learning",
                    description="Requires model integration, prompt engineering, vector embeddings, and evaluation pipelines.",
                    impact="High",
                )
            )

        comp_score = min(comp_score, 100)

        if comp_score >= 65:
            complexity_level = "High"
            complexity_explanation = (
                f"High architectural complexity (Score: {comp_score}/100) driven by multi-platform scope, "
                f"{integration_count} third-party integration(s), and {'AI/ML intelligence layers' if analysis.has_ai_features else 'extensive business logic'}."
            )
        elif comp_score >= 40:
            complexity_level = "Medium"
            complexity_explanation = (
                f"Moderate architectural complexity (Score: {comp_score}/100). Standard modern web/mobile architecture "
                f"with clear integration points and manageable state flows."
            )
        else:
            complexity_level = "Low"
            complexity_explanation = (
                f"Low architectural complexity (Score: {comp_score}/100). Well-defined, standard application patterns "
                f"with minimal third-party dependencies."
            )

        top_risks = [f"{f.rule_name} (+{f.points} pts): {f.reason}" for f in factors if f.points >= 2]
        mitigations = [f.mitigation for f in factors if f.mitigation]

        return RiskAnalysisResult(
            complexity_level=complexity_level,
            complexity_score=comp_score,
            complexity_explanation=complexity_explanation,
            complexity_factors=complexity_factors,
            risk_level=risk_level,
            total_risk_score=total_risk_score,
            risk_factors=factors,
            top_risk_summary=top_risks,
            recommended_mitigations=mitigations,
        )
