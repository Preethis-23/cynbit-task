"""
Unit tests for all core calculation and estimation engines.
"""

from src.ai.mock_engine import MockExtractorEngine
from src.engine.rules import RiskEngine
from src.engine.formulas import EstimationEngine
from src.engine.benchmark import BenchmarkSimilarityEngine
from src.engine.ml_model import ProjectMLModel
from src.export.docx_exporter import ProposalExporter
from src.ai.llm_client import LLMClient


def test_ecommerce_pipeline():
    sample_brief = (
        "We need an omnichannel e-commerce platform with customer login, product catalog, "
        "checkout with Stripe, admin dashboard, iOS/Android mobile apps, and AI product recommendations."
    )
    analysis = MockExtractorEngine.extract(sample_brief)
    assert analysis.has_ai_features is True
    assert analysis.platform_scope.web is True
    assert analysis.platform_scope.mobile_ios is True
    assert len(analysis.functional_requirements) >= 4

    risk = RiskEngine.evaluate(analysis)
    assert risk.risk_level in ["Medium", "High"]
    assert risk.complexity_score > 50

    effort = EstimationEngine.calculate_effort(analysis, risk)
    assert effort.min_hours < effort.likely_hours < effort.max_hours
    assert effort.likely_hours > 700

    timeline = EstimationEngine.calculate_timeline(effort, analysis.has_ai_features, True)
    assert timeline.likely_weeks >= 8.0

    commercial = EstimationEngine.calculate_commercials(
        effort,
        risk,
        hourly_internal_cost=45.0,
        hourly_billing_rate=95.0,
        has_ai=analysis.has_ai_features,
        has_mobile=True,
    )
    assert commercial.quotation_likely > commercial.internal_cost_likely
    assert commercial.profit_margin_likely_pct > 30.0

    # Benchmark search
    benchmark_engine = BenchmarkSimilarityEngine()
    matches = benchmark_engine.find_similar(analysis, top_k=3)
    assert len(matches) > 0

    # ML prediction
    ml_model = ProjectMLModel()
    preds = ml_model.predict(analysis)
    assert preds["predicted_hours"] is not None

    # Proposal Generation & DOCX export
    client = LLMClient()
    proposal, engine_name = client.generate_proposal(analysis, commercial, risk, "RetailDirect Global")
    assert proposal.client_name == "RetailDirect Global"
    assert len(proposal.scope_of_work) > 0

    md_text = ProposalExporter.to_markdown(proposal, analysis, commercial, risk)
    assert "# Technical Solution Proposal" in md_text or "# " in md_text
    assert "Executive Summary" in md_text

    docx_bytes = ProposalExporter.to_docx(proposal, analysis, commercial, risk)
    assert docx_bytes.getvalue().startswith(b"PK")  # Valid docx zip signature
