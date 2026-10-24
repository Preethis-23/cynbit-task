"""
Prompt definitions for Requirement Extraction and Proposal Generation.
"""

EXTRACTION_SYSTEM_PROMPT = """You are an elite Pre-Sales Solution Architect at Cynbit, a premier digital product engineering and AI consulting firm.
Your role is to critically analyze client requirement documents, RFPs, and emails to produce a rigorous, structured technical and commercial assessment for internal review.

CRITICAL RULES:
1. DO NOT invent or fabricate requirements. If the client does not specify something, mark it as missing information.
2. Separate explicit facts stated by the client from technical assumptions.
3. Identify all ambiguities, missing non-functional requirements, unspecified volumes, and security/compliance gaps.
4. Provide professional, direct clarification questions that Cynbit should ask the client.
5. Recommend a modern, production-grade technology stack tailored to the client's problem, with concise justification.
6. You MUST return ONLY valid JSON matching the exact schema specified.
"""

EXTRACTION_USER_PROMPT_TEMPLATE = """Please analyze the following client project brief and produce a structured requirement analysis.

=== CLIENT REQUIREMENT BRIEF ===
{brief_text}
=== END BRIEF ===

Return a JSON object with this EXACT structure:
{{
  "project_name": "Short descriptive project name",
  "business_objective": "Comprehensive summary of client's business goals and problem to solve",
  "user_roles": [
    {{
      "role_name": "Shopper / Admin / Doctor etc.",
      "description": "What this user persona does",
      "access_level": "Admin" | "Standard User" | "Manager" | "External Guest" | "API/System"
    }}
  ],
  "functional_requirements": [
    {{
      "id": "FR-01",
      "category": "Authentication / Product Catalog / Telehealth etc.",
      "title": "Short title",
      "description": "Specific functional description",
      "priority": "Must Have" | "Should Have" | "Could Have",
      "complexity": "Low" | "Medium" | "High"
    }}
  ],
  "non_functional_requirements": [
    {{
      "category": "Security & Privacy" | "Performance & Latency" | "Scalability" | "Compliance & Regulatory" | "Availability & Reliability" | "Maintainability",
      "description": "Specific requirement",
      "target_metric": "e.g., <250ms latency, 99.9% uptime, or 'Not specified by client'"
    }}
  ],
  "platform_scope": {{
    "web": true | false,
    "mobile_ios": true | false,
    "mobile_android": true | false,
    "admin_portal": true | false,
    "desktop_app": true | false,
    "notes": "Scope notes"
  }},
  "integrations": [
    {{
      "name": "Stripe / Twilio / EHR FHIR etc.",
      "category": "Payment Gateway" | "Authentication / SSO" | "CRM & ERP" | "Communications (Email/SMS)" | "AI / LLM Infrastructure" | "Analytics & Telemetry" | "Cloud Storage" | "Other Third-Party API",
      "complexity": "Low" | "Medium" | "High",
      "notes": "Purpose of integration"
    }}
  ],
  "has_ai_features": true | false,
  "ai_features_summary": "Summary of AI/ML components or null",
  "missing_information": [
    {{
      "id": "GAP-01",
      "category": "Scope" | "Technical" | "Compliance" | "Volume",
      "gap_description": "Clear explanation of what is missing or ambiguous",
      "impact": "High" | "Medium" | "Low",
      "clarification_question": "Direct, professional question to ask client"
    }}
  ],
  "tech_recommendation": {{
    "frontend": "e.g., Next.js (React) with TailwindCSS & TypeScript",
    "backend": "e.g., FastAPI (Python) or Node.js / NestJS",
    "database": "e.g., PostgreSQL with Redis caching",
    "cloud_infrastructure": "e.g., AWS (ECS / RDS / S3 / CloudFront)",
    "authentication": "e.g., OAuth 2.0 / JWT with Auth0 or Supabase",
    "ai_infrastructure": "e.g., LangChain / Gemini API / pgvector (or null if no AI)",
    "ci_cd_devops": "e.g., GitHub Actions with Docker",
    "justification": "Why this stack is ideal for this client's requirements"
  }},
  "stated_deadline_weeks": 16,
  "budget_range_mentioned": "$80,000 - $120,000 or null",
  "extracted_assumptions": [
    "Assumption 1",
    "Assumption 2"
  ],
  "extracted_exclusions": [
    "Exclusion 1",
    "Exclusion 2"
  ]
}}
"""

PROPOSAL_GENERATION_PROMPT_TEMPLATE = """You are Cynbit's Lead Solution Architect.
Generate a comprehensive, executive-ready Technical Proposal Draft based on the verified requirements and commercial estimates below.

Client Name: {client_name}
Project Name: {project_name}

=== VERIFIED REQUIREMENTS ===
Business Objective: {business_objective}
Target Platforms: {platforms}
Key Features: {features_summary}
Third-Party Integrations: {integrations_summary}
Missing Information / Clarifications: {clarifications_summary}

=== ESTIMATES & COMMERCIALS ===
Effort Range: {min_hours:.0f} - {max_hours:.0f} Hours (Likely: {likely_hours:.0f} Hours)
Timeline Range: {min_weeks:.1f} - {max_weeks:.1f} Weeks (Likely: {likely_weeks:.1f} Weeks)
Quotation Range: ${quotation_min:,.0f} - ${quotation_max:,.0f} (Target: ${quotation_likely:,.0f})
Complexity: {complexity_level}
Risk Level: {risk_level} (Key drivers: {top_risks})
Recommended Stack: {tech_stack}

Generate a structured JSON draft proposal conforming to the ProposalContent schema:
{{
  "title": "Proposal Title",
  "client_name": "{client_name}",
  "prepared_by": "Cynbit AI Pre-Sales Solutions Architecture Team",
  "date_created": "{date_str}",
  "executive_summary": "High-level summary of proposed solution, strategic alignment, and expected impact.",
  "business_context_and_goals": "Detailed problem analysis and solution objectives.",
  "scope_of_work": ["Scope bullet 1", "Scope bullet 2", ...],
  "out_of_scope_exclusions": ["Exclusion 1", "Exclusion 2", ...],
  "deliverables_by_phase": [
    {{
      "phase_name": "Phase 1: Discovery & Architecture",
      "milestone": "System Architecture & UI/UX Wireframes",
      "deliverables": ["Architecture Blueprint", "Figma Interactive Prototypes", "API Contract Spec"],
      "estimated_duration_weeks": 3.0
    }},
    {{
      "phase_name": "Phase 2: Core Engineering & Integrations",
      "milestone": "MVP Platform & Core Services",
      "deliverables": ["Backend APIs", "Responsive Web Frontend", "Third-Party Integrations"],
      "estimated_duration_weeks": 8.0
    }},
    {{
      "phase_name": "Phase 3: QA, Security & Deployment",
      "milestone": "Production Release & Handover",
      "deliverables": ["End-to-End Test Suite", "Security Audit Report", "Production CI/CD Deployment"],
      "estimated_duration_weeks": 4.0
    }}
  ],
  "recommended_tech_stack_summary": "Concise summary of chosen technologies.",
  "key_architectural_decisions": ["Decision 1", "Decision 2", ...],
  "timeline_summary": "Delivery schedule summary with milestone checkpoints.",
  "recommended_team_structure": "Staffing breakdown (e.g., 1 Tech Lead, 1 Backend, 1 Frontend, 1 QA, 0.5 PM).",
  "pricing_options_summary": "Clear summary of pricing range and payment milestone structure.",
  "assumptions_and_prerequisites": ["Assumption 1", "Assumption 2", ...],
  "client_clarification_questions": ["Question 1", "Question 2", ...],
  "next_steps": ["Step 1: Clarification workshop", "Step 2: Architecture sign-off", "Step 3: Contract finalization"]
}}
"""
