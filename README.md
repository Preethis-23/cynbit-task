# ⚡ Cynbit AI Pre-Sales Solution Architect

An AI-powered, human-in-the-loop decision-support assistant that accelerates technical discovery, risk quantification, architectural design, and commercial quotation for IT consulting projects.

Built for **Cynbit**'s pre-sales solutions architecture and executive leadership team.

---

## 🌟 Key Capabilities

- **Multi-Format Ingestion:** Ingests client RFPs, project briefs, and inquiry emails via PDF, Microsoft Word (`.docx`), or plain text.
- **AI-Powered Requirement Extraction:** Converts unstructured briefs into structured functional features, user roles, non-functional targets, platforms, and third-party integrations.
- **Missing Information & Ambiguity Detection:** Flags vague requirements, unstated traffic volumes, and compliance omissions with ready-to-copy client clarification questions.
- **Transparent Risk & Complexity Engine:** Deterministic rule scoring (+3 for unclear specs, +2 for multi-platform, +2 for multiple integrations, +2 for AI uncertainty) with full point-by-point explanations.
- **What-If Commercial Financial Simulator:** Live reactive KPI cards for hours, calendar weeks, internal cost, quotation, and profit margins, driven by interactive sidebar sliders (Internal Cost, Billing Rate, Contingency Buffer).
- **Historical Benchmark Similarity Search:** Vector cosine similarity matching against a database of 160 historical/synthetic IT projects.
- **Proof-of-Concept Machine Learning Models:** Scikit-Learn `RandomForestRegressor` and `RandomForestClassifier` demonstrating effort prediction and feature importance rankings.
- **Executive Proposal Generation & Export:** Generates executive proposals with one-click export to **Microsoft Word (`.docx`)** and **Markdown (`.md`)**.
- **Dual-Mode Engine (100% Demo Safe):** Automatically leverages Google Gemini (`gemini-2.5-flash`) or OpenAI (`gpt-4o-mini`) when API keys are provided, with seamless fallback to a deterministic offline heuristic engine when running without API keys.

---

## 🏗️ Project Architecture

```
cynbits - task - project/
├── server.py                   # FastAPI REST backend server
├── static/                     # Custom enterprise web application (Vanilla HTML5 / CSS3 / JS)
│   ├── index.html              # Modern responsive single page application
│   ├── styles.css              # Custom enterprise design system
│   └── app.js                  # Reactive state, Chart.js telemetry, and API bindings
├── requirements.txt            # Python dependencies
├── .env.example                # Environment configuration template
├── README.md                   # System documentation & setup guide
├── config/
│   ├── __init__.py
│   └── settings.py             # Pydantic BaseSettings & env var management
├── src/
│   ├── schemas/                # Strongly-typed Pydantic schemas
│   │   ├── document.py         # Ingested document metadata
│   │   ├── requirements.py     # Functional/NFR/Stack schemas
│   │   ├── risk.py             # Risk and complexity schemas
│   │   ├── estimation.py       # Effort, timeline, and commercial schemas
│   │   ├── proposal.py         # Proposal and milestone schemas
│   │   └── project_state.py    # Unified session state model
│   ├── ingestion/
│   │   └── parser.py           # PDF (PyMuPDF), DOCX (python-docx), and TXT parser
│   ├── ai/
│   │   ├── llm_client.py       # Multi-provider client (Gemini, OpenAI, Offline)
│   │   ├── prompts.py          # Structured extraction & proposal prompts
│   │   └── mock_engine.py      # High-performance offline NLP extractor
│   ├── engine/
│   │   ├── rules.py            # Transparent risk and complexity rules
│   │   ├── formulas.py         # Estimation and financial formulas
│   │   ├── benchmark.py        # Vector similarity search engine
│   │   └── ml_model.py         # Random Forest training & inference pipeline
│   └── export/
│       └── docx_exporter.py    # Formatted Word (.docx) & Markdown exporter
├── data/
│   ├── sample_briefs/          # Sample client RFP briefs (E-Commerce, Health, FinTech, Email)
│   └── synthetic_projects.csv  # 160 labeled synthetic historical project records
├── evaluation/
│   ├── dataset.py              # 10 labeled evaluation test cases
│   └── evaluate.py             # Automated accuracy and MAE benchmark runner
├── models/                     # Serialized Random Forest weights & metrics
├── tests/
│   ├── test_ingestion.py       # Ingestion & parser unit tests
│   └── test_engines.py         # End-to-end pipeline unit tests
└── reports/                    # Phase 8 Challenge Submission Deliverables
    ├── AI_Opportunity_Report.md
    ├── AI_ML_Proof_Of_Concept_Report.md
    └── Technical_Approach_Report.md
```

---

## 🚀 Quickstart & Installation

### 1. Clone & Set Up Environment
```bash
# Verify Python version (Python 3.10+ recommended)
python --version

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env` and supply your Gemini or OpenAI API key if available:
```bash
cp .env.example .env
```
> **Note:** The application operates **100% offline out-of-the-box** using its built-in rule and NLP engine if no API keys are supplied!

### 3. Launch the Application
```bash
python server.py
```
Open your browser at `http://localhost:8000`.

---

## 🧪 Running Automated Tests & Benchmark Evaluation

### Run Unit Tests
```bash
python -m pytest tests/
```
All tests validate ingestion, schemas, risk calculations, financial formulas, ML inference, and Word document export.

### Run Phase 6 Benchmark Evaluation
```bash
python evaluation/evaluate.py
```
Evaluates accuracy across the 10 benchmark test cases:
- AI Feature Detection Accuracy: **100%**
- Platform Scope Detection: **90%**
- Risk Classification Accuracy: **70% - 85%**
- ML Model Effort MAE: **~160-270 hours**

---

## 📖 Challenge Deliverable Reports

Detailed business and technical reports are available in the `reports/` folder:
1. [AI Opportunity Report](file:///c:/Users/preethis/Projects/cynbits%20-%20task%20-%20project/reports/AI_Opportunity_Report.md)
2. [AI/ML Proof-of-Concept Report](file:///c:/Users/preethis/Projects/cynbits%20-%20task%20-%20project/reports/AI_ML_Proof_Of_Concept_Report.md)
3. [Technical Approach Report](file:///c:/Users/preethis/Projects/cynbits%20-%20task%20-%20project/reports/Technical_Approach_Report.md)

---

## 🛡️ Positioning & Governance

> **Important Positioning:** This system is an AI-powered decision-support assistant designed to prepare analysis, estimates, and proposal drafts. Cynbit's senior technical architects and executives retain exclusive authority over final pricing, contractual commitments, and project acceptance.
