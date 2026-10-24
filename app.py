"""
Cynbit AI Pre-Sales Solution Architect
Enterprise Decision-Support Platform for Technical Discovery & Pre-Sales Engineering
Designed with professional SaaS aesthetics, crisp typography, and human-in-the-loop governance.
"""

import os
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

from config.settings import settings
from src.ingestion.parser import DocumentParser, IngestionError
from src.ai.llm_client import LLMClient
from src.engine.rules import RiskEngine
from src.engine.formulas import EstimationEngine
from src.engine.benchmark import BenchmarkSimilarityEngine
from src.engine.ml_model import ProjectMLModel
from src.export.docx_exporter import ProposalExporter
from src.schemas.project_state import ProjectAnalysisState

# Page Configuration
st.set_page_config(
    page_title="Cynbit AI Pre-Sales Solution Architect",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional Executive SaaS Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Background */
    .stApp {
        background-color: #f8fafc;
    }

    /* Top Navigation Header */
    .app-header-container {
        padding: 6px 0 16px 0;
        margin-bottom: 16px;
        border-bottom: 1px solid #e2e8f0;
    }

    .brand-eyebrow {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #2563eb;
        margin-bottom: 2px;
    }

    .brand-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.025em;
        margin: 0 0 4px 0;
        line-height: 1.2;
    }

    .brand-desc {
        font-size: 0.9rem;
        color: #64748b;
        margin: 0;
        line-height: 1.45;
    }

    /* Decision-Support Governance Banner */
    .gov-banner {
        background-color: #eff6ff;
        border: 1px solid #dbeafe;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 0.84rem;
        color: #1e40af;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Native Metric Cards Transformation */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 1px 2px rgba(0, 0, 0, 0.03);
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: #64748b !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        letter-spacing: -0.02em !important;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }

    /* Clean Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #f1f5f9;
        padding: 4px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 38px;
        border-radius: 7px;
        font-size: 0.84rem;
        font-weight: 600;
        color: #64748b;
        padding: 0 16px;
        background-color: transparent;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06) !important;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.15s ease;
    }

    div.stButton > button[kind="primary"] {
        background-color: #2563eb;
        color: #ffffff;
        border: 1px solid #1d4ed8;
        box-shadow: 0 1px 2px rgba(37, 99, 235, 0.2);
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #1d4ed8;
        border-color: #1e40af;
    }

    /* Clean Cards */
    .saas-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    .saas-card-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748b;
        margin-bottom: 4px;
    }

    .saas-card-body {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .saas-card-desc {
        font-size: 0.82rem;
        color: #64748b;
        line-height: 1.4;
    }

    /* Status Pills */
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .pill-high {
        background-color: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
    }
    .pill-medium {
        background-color: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
    }
    .pill-low {
        background-color: #f0fdf4;
        color: #15803d;
        border: 1px solid #bbf7d0;
    }
    .pill-neutral {
        background-color: #f1f5f9;
        color: #475569;
        border: 1px solid #e2e8f0;
    }

    /* Clean Expanders */
    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
        margin-bottom: 8px !important;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "analysis_state" not in st.session_state:
    st.session_state.analysis_state = None
if "active_brief_text" not in st.session_state:
    st.session_state.active_brief_text = ""
if "client_name" not in st.session_state:
    st.session_state.client_name = "RetailDirect Global"
if "human_decision" not in st.session_state:
    st.session_state.human_decision = "PENDING_REVIEW - Awaiting technical lead discovery"
if "reviewer_notes" not in st.session_state:
    st.session_state.reviewer_notes = ""
if "engine_used" not in st.session_state:
    st.session_state.engine_used = "Offline Rule Engine (Demo Safe)"


# Top Header
st.markdown("""
<div class="app-header-container">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <div class="brand-eyebrow">Cynbit Enterprise Solutions • Pre-Sales Engineering</div>
            <div class="brand-title">AI Pre-Sales Solution Architect</div>
            <div class="brand-desc">
                Automated technical discovery, risk quantification, and commercial estimation for incoming client RFPs.
            </div>
        </div>
        <div style="text-align: right;">
            <span class="pill pill-low">● System Operational</span>
            <div style="font-size: 0.76rem; color: #94a3b8; margin-top: 4px;">Human-in-the-Loop Mode</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Governance Banner
st.markdown("""
<div class="gov-banner">
    <span style="font-size: 1.15rem;">🛡️</span>
    <div>
        <b>Decision-Support Architecture:</b> All recommendations, hours, and pricing models are indicative pre-sales estimates.
        <b>Cynbit Lead Solution Architects and Executives retain sole final sign-off</b> over contractual commitments and project acceptance.
    </div>
</div>
""", unsafe_allow_html=True)


# Sidebar Configuration & Live What-If Sliders
with st.sidebar:
    st.markdown("#### ⚙️ Configuration & Engine")

    provider_choice = st.selectbox(
        "Active Reasoning Engine",
        options=["Google Gemini (Primary)", "OpenAI", "Offline Rule Engine (Demo Safe)"],
        index=0 if settings.gemini_api_key else 2,
    )
    provider_key = "gemini" if "Gemini" in provider_choice else ("openai" if "OpenAI" in provider_choice else "offline")

    if provider_key == "gemini":
        gemini_env_key = os.getenv("GEMINI_API_KEY") or settings.gemini_api_key or ""
        api_key_input = st.text_input("Gemini API Key", value=gemini_env_key, type="password", placeholder="AIzaSy...")
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
    elif provider_key == "openai":
        openai_env_key = os.getenv("OPENAI_API_KEY") or settings.openai_api_key or ""
        api_key_input = st.text_input("OpenAI API Key", value=openai_env_key, type="password", placeholder="sk-proj-...")
        if api_key_input:
            os.environ["OPENAI_API_KEY"] = api_key_input

    st.markdown("---")
    st.markdown("#### 📊 Commercial What-If Parameters")
    st.caption("Adjust sliders to test margin sensitivity in real time.")

    hourly_internal_cost = st.slider(
        "Internal Developer Cost ($/hr)",
        min_value=25.0,
        max_value=120.0,
        value=float(settings.default_hourly_cost),
        step=5.0,
        help="Blended internal salary, overhead, and tooling cost per developer hour.",
    )

    hourly_billing_rate = st.slider(
        "Client Billing Rate ($/hr)",
        min_value=50.0,
        max_value=250.0,
        value=float(settings.default_hourly_bill_rate),
        step=5.0,
        help="Standard commercial rate applied to client quotes.",
    )

    contingency_pct = st.slider(
        "Risk Contingency Buffer (%)",
        min_value=5.0,
        max_value=40.0,
        value=float(settings.default_contingency_pct),
        step=1.0,
        help="Risk contingency buffer added for technical unknowns.",
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.76rem; color: #64748b; line-height: 1.5;">
        <b>Engine:</b> Cynbit Pre-Sales Core v2.4<br>
        <b>Model:</b> Gemini 2.5 Flash / Fallback<br>
        <b>Database:</b> 160 Historical Projects
    </div>
    """, unsafe_allow_html=True)


# Helper: Load Sample Briefs
def load_sample_brief(file_name: str) -> str:
    path = os.path.join("data", "sample_briefs", file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


# Main Tabs
tab_ingest, tab_requirements, tab_risk, tab_commercials, tab_benchmark, tab_proposal, tab_evaluation = st.tabs([
    "📥 1. Document Ingestion",
    "📋 2. Requirements & Stack",
    "⚠️ 3. Complexity & Risks",
    "💰 4. Effort & Commercials",
    "🔍 5. Past Project Benchmarks",
    "📄 6. Proposal & Review",
    "📈 7. Evaluation & ML Validation",
])


# ==========================================
# TAB 1: INGESTION & PREVIEW
# ==========================================
with tab_ingest:
    st.markdown("#### Ingest Client Requirement Document")
    st.caption("Select a sample brief or upload an RFP document (PDF, DOCX, TXT) to start architectural analysis.")

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        if st.button("🛒 Omnichannel E-Commerce", use_container_width=True):
            st.session_state.active_brief_text = load_sample_brief("ecommerce_omnichannel.txt")
            st.session_state.client_name = "RetailDirect Global"
            st.rerun()
    with col_p2:
        if st.button("🏥 Healthcare Telehealth", use_container_width=True):
            st.session_state.active_brief_text = load_sample_brief("healthcare_telemed.txt")
            st.session_state.client_name = "CareConnect Health Partners"
            st.rerun()
    with col_p3:
        if st.button("💳 FinTech KYC Portal", use_container_width=True):
            st.session_state.active_brief_text = load_sample_brief("fintech_kyc_portal.txt")
            st.session_state.client_name = "Apex Compliance Labs"
            st.rerun()
    with col_p4:
        if st.button("✉️ Ambiguous Email Brief", use_container_width=True):
            st.session_state.active_brief_text = load_sample_brief("ambiguous_quick_brief.txt")
            st.session_state.client_name = "QuickVentures"
            st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col_up, col_client = st.columns([1, 1])
    with col_up:
        uploaded_file = st.file_uploader(
            "Upload Project Brief (PDF, DOCX, TXT)",
            type=settings.allowed_extensions,
            help="Files are processed strictly in memory and discarded after session.",
        )
        if uploaded_file is not None:
            parser = DocumentParser()
            try:
                ingested = parser.parse_file(uploaded_file.read(), uploaded_file.name)
                st.session_state.active_brief_text = ingested.cleaned_text
                st.success(f"Successfully parsed `{uploaded_file.name}` ({ingested.metadata.word_count:,} words)")
            except IngestionError as ie:
                st.error(f"Ingestion error: {ie}")

    with col_client:
        client_name_input = st.text_input("Client Organization Name", value=st.session_state.client_name)
        st.session_state.client_name = client_name_input

    brief_text = st.text_area(
        "Client Requirement Brief / Email Text",
        value=st.session_state.active_brief_text,
        height=220,
        placeholder="Paste client requirements, emails, or RFP scope here...",
    )
    st.session_state.active_brief_text = brief_text

    col_run, col_stats = st.columns([1, 2])
    with col_run:
        start_analysis = st.button("🚀 Analyze Brief & Generate Architecture", type="primary", use_container_width=True)

    with col_stats:
        if brief_text:
            word_count = len(brief_text.split())
            char_count = len(brief_text)
            st.markdown(f"""
            <div style="font-size: 0.82rem; color: #475569; padding-top: 8px;">
                <b>Document Stats:</b> <span class="pill pill-neutral">{word_count:,} words</span> 
                <span class="pill pill-neutral">{char_count:,} characters</span>
            </div>
            """, unsafe_allow_html=True)

    if start_analysis:
        if not brief_text.strip():
            st.error("Please enter or upload a client brief to begin analysis.")
        else:
            with st.spinner("Executing Solution Architecture Discovery Pipeline..."):
                parser = DocumentParser()
                doc = parser.parse_plain_text(brief_text, filename=st.session_state.client_name)
                client = LLMClient(provider=provider_key)

                # 1. AI Requirement Extraction
                analysis, engine_used = client.extract_requirements(doc.cleaned_text)

                # 2. Risk & Complexity Engine
                risk_result = RiskEngine.evaluate(analysis)

                # 3. Estimation & Financial Engine
                effort = EstimationEngine.calculate_effort(analysis, risk_result, contingency_pct=contingency_pct)
                timeline = EstimationEngine.calculate_timeline(
                    effort,
                    analysis.has_ai_features,
                    analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android,
                )

                # 4. ML Model Prediction
                ml_model = ProjectMLModel()
                ml_pred = ml_model.predict(analysis)

                # 5. Financial Commercials
                commercial = EstimationEngine.calculate_commercials(
                    effort=effort,
                    risk=risk_result,
                    hourly_internal_cost=hourly_internal_cost,
                    hourly_billing_rate=hourly_billing_rate,
                    contingency_pct=contingency_pct,
                    has_ai=analysis.has_ai_features,
                    has_mobile=analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android,
                    ml_predicted_hours=ml_pred.get("predicted_hours"),
                )

                # 6. Benchmark Similarity Matching
                bench_engine = BenchmarkSimilarityEngine()
                matches = bench_engine.find_similar(analysis, top_k=3)

                # 7. Package Session State
                st.session_state.analysis_state = ProjectAnalysisState(
                    session_id=f"CYN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    document=doc,
                    requirements=analysis,
                    risk=risk_result,
                    effort=effort,
                    timeline=timeline,
                    commercial=commercial,
                    benchmark_matches=matches,
                    proposal=None,
                )
                st.session_state.engine_used = engine_used
                st.success(f"Analysis Complete using {engine_used}! Explore findings across tabs 2 to 6.")


# ==========================================
# TAB 2: REQUIREMENTS & STACK
# ==========================================
with tab_requirements:
    state = st.session_state.analysis_state
    if not state:
        st.info("Please ingest and analyze a client brief in Tab 1 first.")
    else:
        req = state.requirements
        st.markdown(f"#### 📌 {req.project_name}")
        st.markdown(f"**Business Strategic Objective:** {req.business_objective}")

        # Platform & AI Chips using st.metric
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        with col_c1:
            st.metric("Web Platform", "Included" if req.platform_scope.web else "Excluded", "Responsive SPA/SSR" if req.platform_scope.web else None)
        with col_c2:
            has_mob = req.platform_scope.mobile_ios or req.platform_scope.mobile_android
            st.metric("Mobile Scope", "iOS & Android" if has_mob else "Excluded", "Cross-Platform" if has_mob else None)
        with col_c3:
            st.metric("Admin Portal", "Included" if req.platform_scope.admin_portal else "Excluded", "Role-Based RBAC" if req.platform_scope.admin_portal else None)
        with col_c4:
            st.metric("AI / ML Features", "Included" if req.has_ai_features else "Not Required", "ML Inference" if req.has_ai_features else None)

        if req.has_ai_features and req.ai_features_summary:
            st.info(f"🤖 **AI/ML Architectural Scope:** {req.ai_features_summary}")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Functional Requirements Table
        st.markdown("#### Functional Requirements Breakdown")
        fr_data = [
            {
                "ID": fr.id,
                "Category": fr.category,
                "Feature Title": fr.title,
                "Priority": fr.priority,
                "Complexity": fr.complexity,
                "Description": fr.description,
            }
            for fr in req.functional_requirements
        ]
        st.dataframe(pd.DataFrame(fr_data), use_container_width=True, hide_index=True)

        # User Roles & Non-Functional Specifications
        col_nfr, col_roles = st.columns([1, 1])
        with col_nfr:
            st.markdown("#### Non-Functional Quality Targets")
            for nfr in req.non_functional_requirements:
                st.markdown(f"""
                <div class="saas-card">
                    <div class="saas-card-title">{nfr.category}</div>
                    <div style="font-size: 0.88rem; color: #1e293b; font-weight: 500;">{nfr.description}</div>
                    <div style="font-size: 0.78rem; color: #2563eb; margin-top: 4px;">Target SLA: <b>{nfr.target_metric or 'Standard Production Metric'}</b></div>
                </div>
                """, unsafe_allow_html=True)

        with col_roles:
            st.markdown("#### User Roles & Access Hierarchy")
            for role in req.user_roles:
                st.markdown(f"""
                <div class="saas-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-weight: 700; color: #0f172a; font-size: 0.9rem;">👤 {role.role_name}</span>
                        <span class="pill pill-neutral">{role.access_level}</span>
                    </div>
                    <div class="saas-card-desc">{role.description}</div>
                </div>
                """, unsafe_allow_html=True)

        # Recommended Tech Stack
        st.markdown("#### 🛠️ Recommended Production Technology Architecture")
        rec = req.tech_recommendation

        col_st1, col_st2, col_st3 = st.columns(3)
        with col_st1:
            st.markdown(f"""
            <div class="saas-card">
                <div class="saas-card-title">Frontend & Web Client</div>
                <div class="saas-card-body">{rec.frontend}</div>
                <div class="saas-card-desc">Modern component-driven web framework with high SEO performance.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="saas-card">
                <div class="saas-card-title">Cloud Infrastructure</div>
                <div class="saas-card-body">{rec.cloud_infrastructure}</div>
                <div class="saas-card-desc">Auto-scaling containerized cloud deployment with CDN caching.</div>
            </div>
            """, unsafe_allow_html=True)
        with col_st2:
            st.markdown(f"""
            <div class="saas-card">
                <div class="saas-card-title">Backend & Microservices</div>
                <div class="saas-card-body">{rec.backend}</div>
                <div class="saas-card-desc">Asynchronous, typed API microservices with high concurrent throughput.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="saas-card">
                <div class="saas-card-title">Identity & Access Management</div>
                <div class="saas-card-body">{rec.authentication}</div>
                <div class="saas-card-desc">Enterprise OAuth 2.0 / JWT token validation and role policies.</div>
            </div>
            """, unsafe_allow_html=True)
        with col_st3:
            st.markdown(f"""
            <div class="saas-card">
                <div class="saas-card-title">Database & In-Memory Cache</div>
                <div class="saas-card-body">{rec.database}</div>
                <div class="saas-card-desc">ACID relational database storage with sub-millisecond Redis caching.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="saas-card">
                <div class="saas-card-title">AI Layer & DevOps Pipeline</div>
                <div class="saas-card-body">{rec.ai_infrastructure or 'Standard CI/CD'}</div>
                <div class="saas-card-desc">Automated GitHub Actions CI/CD pipelines with containerized deployments.</div>
            </div>
            """, unsafe_allow_html=True)

        st.info(f"💡 **Architecture Justification:** {rec.justification}")


# ==========================================
# TAB 3: COMPLEXITY & RISK ENGINE
# ==========================================
with tab_risk:
    state = st.session_state.analysis_state
    if not state:
        st.info("Please ingest and analyze a client brief in Tab 1 first.")
    else:
        risk = state.risk
        req = state.requirements

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric(
                "Risk Classification",
                f"{risk.risk_level} Risk",
                f"{risk.total_risk_score} Total Risk Points",
                delta_color="inverse" if risk.risk_level == "High" else "normal",
            )
        with col_r2:
            st.metric(
                "Architectural Complexity",
                risk.complexity_level,
                f"Score: {risk.complexity_score} / 100",
            )
        with col_r3:
            st.metric(
                "Detected Scope Gaps",
                f"{len(req.missing_information)} Items",
                "Actionable Clarifications",
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(f"**Complexity Rationale:** {risk.complexity_explanation}")

        # Missing Information & Clarification Questions
        st.markdown("#### ❓ Scope Ambiguities & Client Clarification Questions")
        if req.missing_information:
            for gap in req.missing_information:
                with st.expander(f"⚠️ [{gap.impact} Priority] {gap.category}: {gap.gap_description}", expanded=True):
                    st.markdown("**Suggested Clarification Question to Send Client:**")
                    st.code(gap.clarification_question, language="text")
        else:
            st.success("No critical information gaps identified in the brief.")

        # Transparent Rules Breakdown
        st.markdown("#### 🔍 Transparent Risk Rules Breakdown")
        rule_data = [
            {
                "Risk Rule": rf.rule_name,
                "Severity": rf.severity,
                "Points Added": f"+{rf.points}",
                "Trigger Rationale": rf.reason,
                "Recommended Mitigation": rf.mitigation,
            }
            for rf in risk.risk_factors
        ]
        st.dataframe(pd.DataFrame(rule_data), use_container_width=True, hide_index=True)


# ==========================================
# TAB 4: EFFORT & COMMERCIALS
# ==========================================
with tab_commercials:
    state = st.session_state.analysis_state
    if not state:
        st.info("Please ingest and analyze a client brief in Tab 1 first.")
    else:
        # Recompute on the fly with sidebar sliders
        effort = EstimationEngine.calculate_effort(state.requirements, state.risk, contingency_pct=contingency_pct)
        timeline = EstimationEngine.calculate_timeline(
            effort,
            state.requirements.has_ai_features,
            state.requirements.platform_scope.mobile_ios or state.requirements.platform_scope.mobile_android,
        )
        comm = EstimationEngine.calculate_commercials(
            effort=effort,
            risk=state.risk,
            hourly_internal_cost=hourly_internal_cost,
            hourly_billing_rate=hourly_billing_rate,
            contingency_pct=contingency_pct,
            has_ai=state.requirements.has_ai_features,
            has_mobile=state.requirements.platform_scope.mobile_ios or state.requirements.platform_scope.mobile_android,
            ml_predicted_hours=state.commercial.ml_predicted_hours,
        )

        st.markdown("#### Commercial Assessment & Financial Forecast")
        st.caption("Values update reactively as sidebar cost, billing rate, and contingency sliders are adjusted.")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric(
                "Estimated Effort",
                f"{effort.likely_hours:,.0f} hrs",
                f"Range: {effort.min_hours:,.0f} – {effort.max_hours:,.0f} hrs",
            )
        with col_m2:
            st.metric(
                "Delivery Timeline",
                f"{timeline.likely_weeks:.1f} wks",
                f"Bounds: {timeline.min_weeks:.1f} – {timeline.max_weeks:.1f} wks",
            )
        with col_m3:
            st.metric(
                "Quotation Price",
                f"${comm.quotation_likely:,.0f}",
                f"Range: ${comm.quotation_min:,.0f} – ${comm.quotation_max:,.0f}",
            )
        with col_m4:
            st.metric(
                "Gross Profit Margin",
                f"{comm.profit_margin_likely_pct:.1f}%",
                f"Expected Profit: ${comm.expected_profit_likely:,.0f}",
            )

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Effort Breakdown Visual Chart
        st.markdown("#### 📊 Engineering Discipline Effort Breakdown")
        bd = effort.breakdown
        breakdown_df = pd.DataFrame([
            {"Discipline": "Frontend & UI", "Hours": bd.frontend_hours},
            {"Discipline": "Backend & APIs", "Hours": bd.backend_hours},
            {"Discipline": "Database Arch", "Hours": bd.database_arch_hours},
            {"Discipline": "AI / ML Engineering", "Hours": bd.ai_ml_hours},
            {"Discipline": "Integrations", "Hours": bd.integration_hours},
            {"Discipline": "QA & Automation", "Hours": bd.qa_testing_hours},
            {"Discipline": "DevOps & Cloud", "Hours": bd.devops_infra_hours},
            {"Discipline": "PM & Arch Oversight", "Hours": bd.project_management_hours},
            {"Discipline": "Contingency Buffer", "Hours": bd.contingency_hours},
        ])

        chart = alt.Chart(breakdown_df).mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4).encode(
            x=alt.X('Hours:Q', title="Allocated Hours"),
            y=alt.Y('Discipline:N', sort='-x', title=""),
            color=alt.Color('Discipline:N', legend=None, scale=alt.Scale(scheme='tableau10')),
            tooltip=['Discipline', 'Hours'],
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

        # Recommended Staffing Composition
        st.markdown("#### 👥 Recommended Agile Delivery Pod Structure")
        team_data = [
            {
                "Role Title": t.role,
                "Headcount": t.count,
                "Allocation (%)": f"{t.allocation_pct}%",
                "Key Responsibilities": t.responsibilities,
            }
            for t in comm.team_composition
        ]
        st.dataframe(pd.DataFrame(team_data), use_container_width=True, hide_index=True)


# ==========================================
# TAB 5: PAST PROJECT BENCHMARKS
# ==========================================
with tab_benchmark:
    state = st.session_state.analysis_state
    if not state:
        st.info("Please ingest and analyze a client brief in Tab 1 first.")
    else:
        st.markdown("#### 📚 Historical Project Benchmark Matching")
        st.caption("Vector similarity matching against Cynbit's benchmark database of 160 historical project delivery records.")

        if state.benchmark_matches:
            for idx, match in enumerate(state.benchmark_matches, 1):
                col_b1, col_b2, col_b3 = st.columns([2, 1, 1])
                with col_b1:
                    st.markdown(f"**#{idx} [{match.project_id}] {match.project_name}**")
                    st.caption(f"Domain: {match.project_type} • Stack: `{match.tech_stack}`")
                    st.markdown(f"Key Drivers: *{match.key_similarities}*")
                with col_b2:
                    st.metric("Similarity Match", f"{match.similarity_score * 100:.1f}%", f"Risk: {match.risk_level}")
                with col_b3:
                    st.metric("Actual Effort Delivered", f"{match.actual_hours:,.0f} hrs", f"{match.actual_weeks:.1f} weeks")
                st.divider()
        else:
            st.info("No matching historical records found.")


# ==========================================
# TAB 6: PROPOSAL & REVIEW
# ==========================================
with tab_proposal:
    state = st.session_state.analysis_state
    if not state:
        st.info("Please ingest and analyze a client brief in Tab 1 first.")
    else:
        st.markdown("#### 📄 Executive Technical Proposal & Pre-Sales Review")

        col_act1, col_act2 = st.columns([1, 1])
        with col_act1:
            if st.button("✨ Draft Executive Proposal", type="primary", use_container_width=True):
                with st.spinner("Synthesizing client-ready proposal..."):
                    client = LLMClient(provider=provider_key)
                    proposal, p_engine = client.generate_proposal(
                        analysis=state.requirements,
                        commercial=state.commercial,
                        risk=state.risk,
                        client_name=st.session_state.client_name,
                    )
                    state.proposal = proposal
                    st.success(f"Proposal draft generated using {p_engine}!")

        with col_act2:
            st.session_state.human_decision = st.selectbox(
                "Lead Architect Pre-Sales Determination",
                options=[
                    "PENDING_REVIEW - Awaiting technical lead discovery",
                    "ACCEPT - Proceed to formal quotation and SOW",
                    "REQUEST_CLARIFICATION - Send clarification questionnaire to client",
                    "DECLINE - Out of strategic alignment or unacceptable delivery risk",
                ],
                index=0,
            )

        if state.proposal:
            prop = state.proposal

            md_content = ProposalExporter.to_markdown(prop, state.requirements, state.commercial, state.risk)
            docx_io = ProposalExporter.to_docx(prop, state.requirements, state.commercial, state.risk)

            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    label="📥 Download Proposal as Word (.docx)",
                    data=docx_io.getvalue(),
                    file_name=f"Cynbit_Proposal_{state.requirements.project_name.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            with col_dl2:
                st.download_button(
                    label="📥 Download Proposal as Markdown (.md)",
                    data=md_content,
                    file_name=f"Cynbit_Proposal_{state.requirements.project_name.replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

            st.markdown("---")
            with st.expander("📝 1. Executive Summary", expanded=True):
                prop.executive_summary = st.text_area("Executive Summary", value=prop.executive_summary, height=120)

            with st.expander("🎯 2. Scope of Work (Functional Deliverables)", expanded=True):
                scope_text = st.text_area("Scope Items (one per line)", value="\n".join(prop.scope_of_work), height=140)
                prop.scope_of_work = [s.strip() for s in scope_text.split("\n") if s.strip()]

            with st.expander("🚫 3. Out-of-Scope Exclusions", expanded=False):
                excl_text = st.text_area("Exclusions (one per line)", value="\n".join(prop.out_of_scope_exclusions), height=100)
                prop.out_of_scope_exclusions = [e.strip() for e in excl_text.split("\n") if e.strip()]

            with st.expander("🗺️ 4. Phased Delivery Roadmap", expanded=False):
                for p in prop.deliverables_by_phase:
                    st.markdown(f"**{p.phase_name}: {p.milestone}** ({p.estimated_duration_weeks:.0f} weeks)")
                    for d in p.deliverables:
                        st.markdown(f"  • {d}")

            with st.expander("❓ 5. Clarification Questions for Client", expanded=True):
                q_text = st.text_area("Questions for Client (one per line)", value="\n".join(prop.client_clarification_questions), height=120)
                prop.client_clarification_questions = [q.strip() for q in q_text.split("\n") if q.strip()]

            st.session_state.reviewer_notes = st.text_area(
                "Lead Architect Internal Audit Notes",
                value=st.session_state.reviewer_notes,
                placeholder="Enter internal solution notes, risk reservations, or special commercial agreements...",
            )


# ==========================================
# TAB 7: EVALUATION & ML DASHBOARD
# ==========================================
with tab_evaluation:
    st.markdown("#### 📈 System Evaluation & Machine Learning Validation")
    st.caption("Validation metrics across 10 benchmark test cases and Random Forest proof-of-concept performance.")

    ml_model = ProjectMLModel()
    metrics = ml_model.metrics
    if metrics:
        col_ml1, col_ml2, col_ml3 = st.columns(3)
        with col_ml1:
            st.metric("ML Effort Regressor MAE", f"{metrics.get('effort_mae_hours', 'N/A')} hrs", "Mean Absolute Error")
        with col_ml2:
            st.metric("ML Regressor R² Score", f"{metrics.get('effort_r2_score', 'N/A')}", "Variance Explained")
        with col_ml3:
            st.metric("Risk Classifier Accuracy", f"{metrics.get('risk_accuracy', 'N/A')}%", "3-Class Categorical")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("##### Random Forest Feature Importances")
        feat_df = pd.DataFrame(list(metrics.get("feature_importances", {}).items()), columns=["Feature", "Importance"])
        if not feat_df.empty:
            bar = alt.Chart(feat_df).mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4).encode(
                x=alt.X("Importance:Q", title="Relative Predictive Weight"),
                y=alt.Y("Feature:N", sort="-x", title=""),
                color=alt.value("#2563eb"),
            ).properties(height=220)
            st.altair_chart(bar, use_container_width=True)

    st.markdown("---")
    st.markdown("##### Phase 6 Benchmark Evaluation Suite Results")

    eval_json_path = os.path.join("evaluation", "evaluation_results.json")
    if os.path.exists(eval_json_path):
        import json
        with open(eval_json_path, "r") as f:
            eval_data = json.load(f)

        col_ev1, col_ev2, col_ev3, col_ev4 = st.columns(4)
        with col_ev1:
            st.metric("AI Feature Extraction", f"{eval_data.get('ai_accuracy_pct')}%")
        with col_ev2:
            st.metric("Mobile Scope Detection", f"{eval_data.get('mobile_accuracy_pct')}%")
        with col_ev3:
            st.metric("Risk Level Accuracy", f"{eval_data.get('risk_accuracy_pct')}%")
        with col_ev4:
            st.metric("Suite Execution Time", f"{eval_data.get('total_latency_seconds')}s")

        cases_df = pd.DataFrame(eval_data.get("cases", []))
        if not cases_df.empty:
            st.dataframe(
                cases_df[[
                    "id", "domain", "ai_detected", "mobile_detected", "rule_risk",
                    "expected_risk", "rule_hours", "ml_predicted_hours", "expected_range", "in_range"
                ]],
                use_container_width=True,
                hide_index=True,
            )

    st.info(
        "📝 **Academic & Commercial Integrity Note:** The Random Forest models above are trained on a labeled "
        "synthetic dataset of 160 projects for architectural proof of concept. In production, Cynbit will train "
        "these models on real historical project delivery logs, Jira velocity data, and actual margin variances."
    )
