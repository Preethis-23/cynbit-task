"""
FastAPI Server for Cynbit AI Pre-Sales Solution Architect.
Exposes REST endpoints for requirement analysis, financial simulation, proposal generation, and Word/Markdown exports.
Serves custom frontend SPA from static/ directory.
"""

import io
import os
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config.settings import settings
from src.ingestion.parser import DocumentParser, IngestionError
from src.ai.llm_client import LLMClient
from src.engine.rules import RiskEngine
from src.engine.formulas import EstimationEngine
from src.engine.benchmark import BenchmarkSimilarityEngine
from src.engine.ml_model import ProjectMLModel
from src.export.docx_exporter import ProposalExporter
from src.schemas.requirements import RequirementAnalysis
from src.schemas.risk import RiskAnalysisResult
from src.schemas.estimation import CommercialAssessment, EffortRange
from src.schemas.proposal import ProposalContent

app = FastAPI(
    title="Cynbit AI Pre-Sales Solution Architect API",
    description="REST backend for technical discovery, risk quantification, and commercial estimation",
    version="2.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Models
class AnalyzeRequest(BaseModel):
    text: str
    client_name: str = "Prospective Client"
    provider: str = "gemini"
    hourly_cost: float = settings.default_hourly_cost
    billing_rate: float = settings.default_hourly_bill_rate
    contingency_pct: float = settings.default_contingency_pct
    gemini_key: Optional[str] = None
    openai_key: Optional[str] = None


class RecalculateRequest(BaseModel):
    requirements: dict
    risk: dict
    hourly_cost: float
    billing_rate: float
    contingency_pct: float
    ml_predicted_hours: Optional[float] = None


class ProposalRequest(BaseModel):
    requirements: dict
    commercial: dict
    risk: dict
    client_name: str
    provider: str = "gemini"


class ExportDocxRequest(BaseModel):
    proposal: dict
    requirements: dict
    commercial: dict
    risk: dict


# Endpoints
@app.get("/api/samples")
def get_sample_briefs():
    """Returns available pre-loaded sample client briefs."""
    samples_dir = Path("data/sample_briefs")
    result = []
    sample_files = [
        ("ecommerce_omnichannel.txt", "🛒 Omnichannel E-Commerce", "RetailDirect Global"),
        ("healthcare_telemed.txt", "🏥 Healthcare Telehealth", "CareConnect Health Partners"),
        ("fintech_kyc_portal.txt", "💳 FinTech KYC Portal", "Apex Compliance Labs"),
        ("ambiguous_quick_brief.txt", "✉️ Ambiguous Email Brief", "QuickVentures"),
    ]
    for filename, title, client in sample_files:
        p = samples_dir / filename
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                result.append({"id": filename, "title": title, "client": client, "text": f.read()})
    return result


@app.post("/api/analyze")
def analyze_brief(req: AnalyzeRequest):
    """Executes end-to-end analysis on client brief text."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Requirement text cannot be empty.")

    # Configure temporary API keys if provided
    if req.gemini_key:
        os.environ["GEMINI_API_KEY"] = req.gemini_key
    if req.openai_key:
        os.environ["OPENAI_API_KEY"] = req.openai_key

    parser = DocumentParser()
    try:
        doc = parser.parse_plain_text(req.text, filename=req.client_name)
    except IngestionError as err:
        raise HTTPException(status_code=400, detail=str(err))

    client = LLMClient(provider=req.provider)
    analysis, engine_used = client.extract_requirements(doc.cleaned_text)
    risk = RiskEngine.evaluate(analysis)

    effort = EstimationEngine.calculate_effort(analysis, risk, contingency_pct=req.contingency_pct)
    timeline = EstimationEngine.calculate_timeline(
        effort,
        analysis.has_ai_features,
        analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android,
    )

    ml_model = ProjectMLModel()
    ml_pred = ml_model.predict(analysis)

    commercial = EstimationEngine.calculate_commercials(
        effort=effort,
        risk=risk,
        hourly_internal_cost=req.hourly_cost,
        hourly_billing_rate=req.billing_rate,
        contingency_pct=req.contingency_pct,
        has_ai=analysis.has_ai_features,
        has_mobile=analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android,
        ml_predicted_hours=ml_pred.get("predicted_hours"),
    )

    bench_engine = BenchmarkSimilarityEngine()
    matches = bench_engine.find_similar(analysis, top_k=3)

    return {
        "engine_used": engine_used,
        "document": doc.model_dump(),
        "requirements": analysis.model_dump(),
        "risk": risk.model_dump(),
        "effort": effort.model_dump(),
        "timeline": timeline.model_dump(),
        "commercial": commercial.model_dump(),
        "benchmark_matches": [m.model_dump() for m in matches],
        "ml_predictions": ml_pred,
    }


@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    client_name: str = Form("Prospective Client"),
):
    """Parses an uploaded PDF, DOCX, or TXT file into text."""
    parser = DocumentParser()
    content = await file.read()
    try:
        doc = parser.parse_file(content, file.filename)
        return {
            "filename": file.filename,
            "cleaned_text": doc.cleaned_text,
            "word_count": doc.metadata.word_count,
            "char_count": doc.metadata.char_count,
            "warnings": doc.metadata.warnings,
        }
    except IngestionError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/recalculate")
def recalculate_commercials(req: RecalculateRequest):
    """Recomputes commercial margins and effort breakdown dynamically."""
    analysis = RequirementAnalysis.model_validate(req.requirements)
    risk = RiskAnalysisResult.model_validate(req.risk)

    effort = EstimationEngine.calculate_effort(analysis, risk, contingency_pct=req.contingency_pct)
    timeline = EstimationEngine.calculate_timeline(
        effort,
        analysis.has_ai_features,
        analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android,
    )
    commercial = EstimationEngine.calculate_commercials(
        effort=effort,
        risk=risk,
        hourly_internal_cost=req.hourly_cost,
        hourly_billing_rate=req.billing_rate,
        contingency_pct=req.contingency_pct,
        has_ai=analysis.has_ai_features,
        has_mobile=analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android,
        ml_predicted_hours=req.ml_predicted_hours,
    )

    return {
        "effort": effort.model_dump(),
        "timeline": timeline.model_dump(),
        "commercial": commercial.model_dump(),
    }


@app.post("/api/generate-proposal")
def generate_proposal(req: ProposalRequest):
    """Generates an executive proposal draft."""
    analysis = RequirementAnalysis.model_validate(req.requirements)
    commercial = CommercialAssessment.model_validate(req.commercial)
    risk = RiskAnalysisResult.model_validate(req.risk)

    client = LLMClient(provider=req.provider)
    proposal, engine_used = client.generate_proposal(analysis, commercial, risk, req.client_name)

    md_content = ProposalExporter.to_markdown(proposal, analysis, commercial, risk)

    return {
        "engine_used": engine_used,
        "proposal": proposal.model_dump(),
        "markdown": md_content,
    }


@app.post("/api/export-docx")
def export_docx(req: ExportDocxRequest):
    """Exports proposal to a Microsoft Word (.docx) file."""
    proposal = ProposalContent.model_validate(req.proposal)
    analysis = RequirementAnalysis.model_validate(req.requirements)
    commercial = CommercialAssessment.model_validate(req.commercial)
    risk = RiskAnalysisResult.model_validate(req.risk)

    docx_io = ProposalExporter.to_docx(proposal, analysis, commercial, risk)

    safe_title = analysis.project_name.replace(" ", "_")[:30]
    filename = f"Cynbit_Proposal_{safe_title}.docx"

    return StreamingResponse(
        docx_io,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/api/evaluation")
def get_evaluation():
    """Returns evaluation benchmark metrics and Random Forest model metrics."""
    eval_path = Path("evaluation/evaluation_results.json")
    eval_data = {}
    if eval_path.exists():
        with open(eval_path, "r") as f:
            eval_data = json.load(f)

    ml_model = ProjectMLModel()

    return {
        "benchmark_evaluation": eval_data,
        "ml_model_metrics": ml_model.metrics,
    }


# Static Frontend Mount
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
