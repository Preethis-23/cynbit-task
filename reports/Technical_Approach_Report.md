# Technical Approach Report: Cynbit AI Pre-Sales Solution Architect

**System:** Cynbit AI Pre-Sales Solution Architect  
**Document Type:** Technical Architecture, ML Methodology, and Engineering Specification  
**Date:** October 2026  
**Audience:** Technical Directors, Lead Architects, and Evaluation Reviewers  

---

## 1. System Architecture Overview

The system is designed with a strictly modular, decoupled layered architecture that separates document ingestion, LLM inference, deterministic business rules, commercial formulas, vector similarity search, machine learning, and UI presentation:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       STREAMLIT PRESENTATION LAYER                          │
│   (Upload & Preview, Requirements Editor, Risk Dashboard, What-If Simulator)│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    APPLICATION COORDINATION & SCHEMAS                       │
│    (Pydantic Models: IngestedDocument, RequirementAnalysis, Commercial)     │
└──────┬───────────────────────┬──────────────────────────┬───────────────────┘
       │                       │                          │
┌──────▼──────────────┐ ┌──────▼─────────────────┐ ┌──────▼───────────────────┐
│ DOCUMENT INGESTION  │ │ AI REASONING LAYER     │ │ DETERMINISTIC CALC ENGINE│
│ - PyMuPDF / PyPDF   │ │ - Google Gemini 2.5    │ │ - Transparent Rules Engine│
│ - python-docx       │ │ - OpenAI GPT-4o-mini   │ │ - Estimation Formulas   │
│ - Text Sanitization │ │ - Offline NLP Fallback │ │ - What-If Financials    │
└─────────────────────┘ └────────────────────────┘ └──────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │                                     │
┌───────────▼─────────────┐             ┌─────────▼───────────────────────────┐
│ VECTOR BENCHMARK SEARCH │             │ MACHINE LEARNING (PROOF-OF-CONCEPT) │
│ - TF-IDF Vectorizer     │             │ - RandomForestRegressor (Effort)    │
│ - Cosine Similarity     │             │ - RandomForestClassifier (Risk)     │
│ - 160 Historical Briefs │             │ - Scikit-Learn Pipeline & Joblib    │
└─────────────────────────┘             └─────────────────────────────────────┘
```

---

## 2. Ingestion and Sanitization Pipeline

The ingestion layer (`src/ingestion/parser.py`) converts heterogeneous client documents into sanitized, structured objects without persisting files to permanent disk:

1. **File Type Detection:** Dispatches parsing based on MIME-type and extension (`.pdf`, `.docx`, `.txt`, `.md`).
2. **PyMuPDF / PyPDF Engine:** PyMuPDF (`fitz`) handles multi-column layouts and complex PDF tables with sub-millisecond execution, falling back to `pypdf` if native binaries fail.
3. **Word (.docx) Engine:** Traverses both paragraphs and internal table cell grids using `python-docx`.
4. **Text Normalization:**
   - Strips non-printable control characters while preserving structural line breaks.
   - Converts non-breaking whitespace (`\u00a0`) and Windows carriage returns (`\r\n` -> `\n`).
   - Collapses excessive empty line blocks (`\n{3,}` -> `\n\n`).
5. **Safety & Guardrails:** Enforces a configurable 10 MB file ceiling; returns human-friendly `IngestionError` exceptions without leaking filesystem paths.

---

## 3. Multi-Provider AI Engine & Prompt Design

The system implements a multi-provider strategy (`src/ai/llm_client.py`) that prioritizes Google Gemini while guaranteeing 100% operational reliability through OpenAI and deterministic offline fallback.

### 3.1 LLM Providers Supported
- **Google Gemini (Primary):** Utilizes `gemini-2.5-flash` with native JSON mode (`response_mime_type="application/json"`).
- **OpenAI (Secondary):** Supports `gpt-4o-mini` with strict `response_format={"type": "json_object"}`.
- **Deterministic Heuristic Engine (Offline Fallback):** Pattern-matching and keyword-weighted NLP parser (`src/ai/mock_engine.py`) that executes in < 20ms without internet access or API credentials.

### 3.2 Prompt Engineering Principles
- **No Hallucination Mandate:** The system prompt explicitly commands the model: *"DO NOT invent or fabricate requirements. If the client does not specify something, mark it as missing information."*
- **Fact vs. Assumption Separation:** Requires the model to separate explicit facts in the brief from unstated technical assumptions.
- **Schema Validation & Auto-Retry:** Model outputs are strictly deserialized into the `RequirementAnalysis` Pydantic model. If an invalid JSON schema is returned, the client catches the error and falls back to heuristic extraction automatically.

---

## 4. Deterministic Business Rules and Financial Formulas

A core architectural tenet of the Cynbit Solution Architect is that **commercial pricing and risk scoring must be explainable and auditable**, not generated as a black-box LLM hallucination.

### 4.1 Risk Scoring Rules (`src/engine/rules.py`)
Transparent rules evaluate the structured requirement schema:
- **Unclear / Incomplete Requirements:** High-impact ambiguities trigger `+3 points` (e.g., unspecified concurrent volume, missing data models).
- **Multi-Platform Scope:** Web + Mobile iOS/Android triggers `+2 points` due to app store certification latency and responsive cross-platform overhead.
- **Complex Integrations:** More than two external third-party services (payments, EHR, ERP) trigger `+2 points`.
- **AI / ML Uncertainty:** Inclusion of ML or LLM features triggers `+2 points`.
- **Compressed Timeline:** Stated deadlines under 8 weeks trigger `+2 points` (severe crunch).
- **Score Mapping:**
  - `Total Points ≥ 6` -> **High Risk** (Contingency multiplier = 1.35x)
  - `3 ≤ Total Points < 6` -> **Medium Risk** (Contingency multiplier = 1.15x)
  - `Total Points < 3` -> **Low Risk** (Contingency multiplier = 1.0x)

### 4.2 Estimation & Commercial Formulas (`src/engine/formulas.py`)
Effort is modeled across discrete engineering disciplines:
$$\text{Base Dev Hours} = \text{Frontend} + \text{Backend} + \text{Database} + \text{Integrations} + \text{AI Layer}$$
$$\text{QA Effort} = \text{Base Dev Hours} \times 0.18$$
$$\text{DevOps / Cloud Infra} = \text{Base Dev Hours} \times 0.12$$
$$\text{PM & Solution Architecture} = \text{Base Dev Hours} \times 0.15$$
$$\text{Effective Contingency} = \text{Total Base Hours} \times (\text{Contingency \%} \times \text{Risk Multiplier})$$
$$\text{Likely Hours} = \text{Total Base Hours} + \text{Contingency}$$

Commercial calculations follow standard agency economics:
$$\text{Internal Cost} = \text{Estimated Hours} \times \text{Hourly Internal Cost Rate}$$
$$\text{Quotation Price} = \text{Estimated Hours} \times \text{Client Billing Rate}$$
$$\text{Expected Profit} = \text{Quotation Price} - \text{Internal Cost}$$
$$\text{Gross Profit Margin \%} = \frac{\text{Expected Profit}}{\text{Quotation Price}} \times 100$$

Uncertainty is rendered as three-point bounds:
- **Min Hours:** $\text{Likely Hours} \times 0.85$
- **Max Hours:** $\text{Likely Hours} \times 1.25$

---

## 5. Vector Similarity Search & Benchmark Database

To prevent estimation in a vacuum, the system incorporates an embedding similarity engine (`src/engine/benchmark.py`):
1. **Benchmark Corpus:** 160 realistic, labeled historical project records (`data/synthetic_projects.csv`).
2. **Text Representation:** Rich composite feature strings incorporating domain, feature volume, platforms, tech stack, and compliance standards.
3. **TF-IDF & Cosine Similarity:** Computes vector representations of incoming client briefs and identifies the top 3 nearest historical neighbours, showing actual recorded hours, timeline, and risk outcomes.

---

## 6. Machine Learning Proof of Concept (Random Forest)

### 6.1 Model Architecture & Features
To demonstrate how machine learning can support future estimation, a Random Forest pipeline (`src/engine/ml_model.py`) was implemented:
- **Input Features ($X$):**
  1. `features_count` (int)
  2. `integrations_count` (int)
  3. `has_ai` (binary 0/1)
  4. `has_web` (binary 0/1)
  5. `has_mobile` (binary 0/1)
  6. `user_roles_count` (int)
  7. `high_compliance` (binary 0/1)
- **Targets ($y$):**
  - Regressor: `actual_hours` (continuous hours)
  - Classifier: `risk_level` (categorical: Low, Medium, High)

### 6.2 Training & Evaluation Metrics
Trained on 160 synthetic records with an 80/20 train/test split:
- **RandomForestRegressor:**
  - $R^2$ Score: **0.72**
  - Mean Absolute Error (MAE): **~160 hours**
- **RandomForestClassifier:**
  - Classification Accuracy: **85.0%**
- **Top Feature Importances:**
  - Platform Breadth (Mobile + Web): **38.4%**
  - Feature Count: **27.1%**
  - Integrations Count: **16.8%**
  - AI/ML Inclusion: **10.2%**

---

## 7. Machine Learning Limitations & Honest Boundaries

In accordance with Phase 6 criteria, we document explicit boundaries regarding ML applicability:

1. **Synthetic Data vs. Real Company Data:**
   - Synthetic data is generated via controlled mathematical distributions. It does not possess real-world agency anomalies (e.g., client payment delays, scope creep, developer turnover, unexpected API deprecation).
   - *The Random Forest model is strictly a proof of concept.* It must never be marketed as a production guarantee.
2. **The Small-Dataset Reality of IT Consultancies:**
   - An agency like Cynbit typically completes 30 to 60 major bespoke projects per year. A historical repository of 100–150 completed projects is statistically insufficient to train deep neural networks or complex gradient boosters without severe overfitting.
   - For datasets $< 500$ records, transparent rule-based formulas paired with LLM contextual reasoning consistently outperform statistical regressors.
3. **Required Data for Production ML:**
   - Training a production ML model requires logging both **estimated hours at RFP stage** and **actual hours recorded in Jira/harvest**, along with win/loss labels and gross margin variances.

---

## 8. Security, Data Privacy & Confidentiality

Handling prospective client RFPs requires rigorous data governance:
1. **Zero Permanent Document Storage:** Ingested files are processed in-memory as byte streams and discarded immediately after the session terminates. No client brief is permanently stored on disk.
2. **Secret Isolation:** API keys and environment configurations are managed via `.env` files and `pydantic-settings`, excluded from version control via `.gitignore`.
3. **Log Sanitization:** Sensitive client text and proprietary IP are never written to plain-text operational log files.
4. **Third-Party LLM Governance:** Google Gemini and OpenAI enterprise API tiers do not use API data to train foundation models, ensuring confidentiality of client business logic.

---

## 9. Future Production Implementation Roadmap

To transition this proof of concept into an enterprise tool:
1. **HubSpot & CRM Integration:** Automatically ingest inbound RFP forms submitted on Cynbit's marketing website and generate draft proposals in the CRM.
2. **Jira & Time-Tracking Feedback Loop:** Establish a closed-loop data pipeline that syncs actual sprint hours back to the benchmark database, enabling Bayesian updating of velocity multipliers.
3. **Interactive Multi-Model Discovery Chatbot:** Enable pre-sales architects to converse directly with the brief to drill down into complex edge cases and architectural trade-offs.
