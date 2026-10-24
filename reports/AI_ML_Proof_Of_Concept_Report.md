# AI/ML Proof-of-Concept Report: Cynbit AI Pre-Sales Solution Architect

**Project:** Cynbit AI Pre-Sales Solution Architect  
**Deliverable:** Proof of Concept (PoC) Technical Demonstration Report  
**Date:** October 2026  
**Implementation Technology:** Python, Streamlit, Pydantic, Scikit-Learn, PyMuPDF, Python-Docx, Google Gemini / OpenAI  

---

## 1. Executive Summary

This report documents the architecture, implementation, user experience, and validation results of the **Cynbit AI Pre-Sales Solution Architect Proof-of-Concept (PoC)**. 

The application is an end-to-end, interactive decision-support system built in Python and Streamlit. It allows pre-sales engineers and solution architects to upload or paste messy, unstructured client briefs (in PDF, DOCX, or raw text format) and automatically receive a structured technical breakdown, transparent risk assessment, discipline-by-discipline effort estimation, interactive commercial financial models, past project benchmark matches, and a client-ready proposal exportable in Microsoft Word (`.docx`) and Markdown formats.

---

## 2. End-to-End System Workflow

The PoC implements a modular, seven-stage pipeline:

```text
1. Document Ingestion (PDF / DOCX / TXT / Email)
        ↓
2. Normalization & Safety Validation (Sanitization, Whitespace, Size Check)
        ↓
3. Structured Requirement Extraction (LLM / Fallback Rule-NLP Engine)
        ↓
4. Transparent Risk & Complexity Scoring (Deterministic Business Rules)
        ↓
5. Effort, Timeline & Commercial Estimation (Configurable Formula Engine)
        ↓
6. Historical Benchmark Matching & ML Inference (Cosine Similarity + Random Forest)
        ↓
7. Executive Proposal Generation & Human Review (Editable Draft + Word .docx Export)
```

---

## 3. Supported Inputs and Extraction Outputs

### 3.1 Input Formats
- **PDF Documents:** Extracted using high-performance PyMuPDF (`fitz`) with automated PyPDF fallback.
- **Microsoft Word (.docx):** Full paragraph and table parsing using `python-docx`.
- **Plain Text / Email Copies:** Direct string normalization, control character stripping, and whitespace collapse.
- **Pre-Loaded Sample Presets:** One-click demo buttons for Omnichannel E-Commerce, Healthcare Telehealth, FinTech KYC, and Ambiguous Email Briefs.

### 3.2 Structured Extraction Outputs
The system transforms raw brief text into strictly validated Pydantic models:
- **Business Objectives:** Clear statement of client strategic intent and value drivers.
- **User Roles & Personas:** Actors, access levels (Admin, Standard User, Manager), and permissions.
- **Functional Requirements:** Unique IDs (FR-01, FR-02), categories, priority (Must/Should/Could Have), and complexity.
- **Non-Functional Requirements:** Security, P95 latency targets, scalability, and compliance standards.
- **Platform Scope:** Explicit booleans for Web, iOS, Android, Admin Backoffice, and Desktop.
- **Third-Party Integrations:** External APIs categorized by complexity and system dependency.
- **Missing Information & Ambiguities:** Flagged gaps with severity ratings and exact clarification questions.
- **Technology Recommendation:** Production stack (Next.js, FastAPI, PostgreSQL, AWS, Auth0) with rationale.

---

## 4. Walkthrough & Sample Results on Test Cases

### Case Study 1: Modern Omnichannel E-Commerce Platform
- **Input:** Brief requesting customer login, catalog, Stripe/PayPal checkout, admin dashboard, iOS/Android mobile apps, and personalized AI product recommendations with 25k peak traffic.
- **Extraction Results:**
  - *Platforms:* Responsive Web (`True`), Mobile iOS/Android (`True`), Admin Dashboard (`True`).
  - *AI Feature Detected:* `True` (Personalized collaborative filtering recommendation engine).
  - *Integrations Detected:* Stripe, PayPal, SendGrid, Twilio, Cloud Vector DB.
- **Risk & Complexity Engine:**
  - *Complexity Index:* **78/100 (High)** driven by multi-platform scope, 4 external integrations, and AI layer.
  - *Risk Level:* **High (8 risk points)**.
  - *Key Triggered Rules:* Unclear peak transaction throughput (+3), Multi-platform Web+Mobile (+2), AI uncertainty (+2), Multiple third-party APIs (+2).
- **Commercial Assessment:**
  - *Estimated Effort:* **1,772 hours** (Min: 1,506h, Max: 2,215h).
  - *Timeline:* **16.1 calendar weeks** with an agile pod of 4 engineers.
  - *Internal Cost ($45/hr):* $79,740.
  - *Quotation Price ($95/hr):* **$168,340**.
  - *Projected Gross Profit:* $88,600 (**52.6% gross margin**).

### Case Study 2: Ambiguous Quick Email Brief ("Uber for Services in 6 Weeks")
- **Input:** Short 6-sentence founder email requesting an on-demand marketplace with payments, worker/client mobile apps, AI matching, and launch in 6 weeks.
- **Extraction Results:**
  - *Missing Information Detected:* 4 critical gaps (Undefined transaction volume, unspecified mobile framework, missing regulatory compliance, undefined AI training corpora).
- **Risk Assessment:**
  - *Risk Level:* **High (8 risk points)**.
  - *Critical Rule Triggered:* **Unusually Compressed Timeline (<8 weeks): +2 risk points**.
  - *Recommendation:* System alerts reviewer that 6 weeks is unfeasible for multi-app native delivery; recommends descoping to a single-platform MVP or expanding timeline to 12 weeks.

---

## 5. User Interface & Interactive Experience

The Streamlit interface provides a high-density, professional command center organized into seven purpose-built tabs:

1. **Tab 1: Document Ingestion:** File drag-and-drop, sample brief quick-loaders, raw/cleaned text preview, and document statistics.
2. **Tab 2: Requirements & Tech Stack:** Interactive table of functional requirements, user roles, non-functional targets, and architectural stack recommendations.
3. **Tab 3: Complexity & Risks:** Visual risk badge (Low/Medium/High), architectural complexity progress bar, and point-by-point rule explanations with specific client clarification questions.
4. **Tab 4: Effort & Commercials (What-If Simulator):** Live financial recalculation driven by sidebar sliders (Developer Cost, Billing Rate, Contingency Buffer). Includes Altair discipline breakdown bar charts and recommended staffing tables.
5. **Tab 5: Past Project Benchmarks:** Cosine similarity vector search matching the brief against 160 historical project records to show actual delivery hours and real-world variance.
6. **Tab 6: Proposal & Human Review:** Editable proposal sections (Executive Summary, Scope, Exclusions, Roadmap), Executive Decision dropdown (Accept, Decline, Clarify), and one-click **Word (.docx)** and **Markdown (.md)** downloads.
7. **Tab 7: Evaluation & ML Validation:** Live display of Random Forest model metrics (MAE, R², Feature Importances) and 10-case evaluation suite accuracy.

---

## 6. Machine Learning Proof of Concept Demonstration

To validate how machine learning can augment rule-based heuristics as Cynbit accumulates data:
- **Synthetic Training Dataset:** 160 realistic, multi-domain project records (`data/synthetic_projects.csv`) containing feature counts, platforms, integrations, compliance standards, and actual recorded hours.
- **RandomForestRegressor (Effort):** Trained on engineered project feature vectors to predict total delivery hours. Achieved an R² score of ~0.72 and Mean Absolute Error (MAE) of ~160 hours on unseen test records.
- **RandomForestClassifier (Risk):** Evaluates multi-class risk (Low, Medium, High) with 85%+ accuracy on labeled test records.
- **Feature Importance Insights:** Confirms that *Platform Breadth (Web + Mobile)* and *Integration Count* are the primary drivers of effort variance in software development.

---

## 7. Human-in-the-Loop Governance & Guardrails

The PoC strictly enforces non-autonomous governance:
- **No Automated Commitments:** The assistant cannot send quotations directly to clients or bind Cynbit contractually.
- **Editable Drafts:** Every section of the extracted requirements, assumptions, and proposal text is fully editable by the human reviewer inside the application.
- **Audit Disclaimer:** Every proposal output automatically embeds a formal disclaimer clarifying that all estimates are indicative ranges subject to technical discovery and executive sign-off.
- **Dual-Mode Engine:** Operates seamlessly with Google Gemini / OpenAI when API keys are available, and transitions transparently to a deterministic offline heuristic engine when disconnected, ensuring zero demo downtime.
