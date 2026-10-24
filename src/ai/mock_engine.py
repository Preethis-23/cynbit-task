"""
Deterministic Offline AI Extractor for Cynbit Pre-Sales Solution Architect.
Extracts structured requirements, gaps, platforms, and stack recommendations
from brief text without external API calls. Ensures 100% demo and evaluation reliability.
"""

import re
from src.schemas.requirements import (
    RequirementAnalysis,
    FunctionalRequirement,
    NonFunctionalRequirement,
    UserRole,
    PlatformScope,
    ThirdPartyIntegration,
    MissingInformation,
    TechnologyRecommendation,
)


class MockExtractorEngine:
    """Pattern-based heuristic extractor used when offline or without API keys."""

    @staticmethod
    def extract(text: str, filename: str = "Client Brief") -> RequirementAnalysis:
        text_lower = text.lower()

        # Is this an inherently simple/internal informational project?
        is_simple_site = (
            ("static" in text_lower or "marketing" in text_lower or "landing" in text_lower or "directory" in text_lower)
            and not ("cart" in text_lower or "payment" in text_lower or "ai" in text_lower or "webrtc" in text_lower or "gps" in text_lower)
        )

        # 1. Project Type & Name Heuristic
        if "e-commerce" in text_lower or "retail" in text_lower or "cart" in text_lower or "store" in text_lower:
            project_type = "E-Commerce & Retail"
            project_name = "Omnichannel E-Commerce Solution"
            business_objective = (
                "Deploy a high-converting, omnichannel commerce platform enabling direct-to-consumer "
                "sales, real-time inventory management, secure payments, and personalized shopping experiences."
            )
        elif "telemed" in text_lower or "health" in text_lower or "doctor" in text_lower or "patient" in text_lower:
            project_type = "Healthcare & Telemedicine"
            project_name = "CareConnect Telehealth & Patient Portal"
            business_objective = (
                "Deliver a secure, HIPAA-compliant digital health platform connecting patients with medical "
                "specialists via WebRTC video consultations, secure messaging, and EHR integration."
            )
        elif "bank" in text_lower or "fintech" in text_lower or "kyc" in text_lower or "plaid" in text_lower:
            project_type = "Fintech & Payments"
            project_name = "Fintech KYC & Compliance Platform"
            business_objective = (
                "Build an enterprise-grade financial technology platform with strict regulatory compliance, "
                "frictionless identity verification (KYC/AML), and real-time transaction processing."
            )
        elif "delivery" in text_lower or "uber" in text_lower or "marketplace" in text_lower or "dispatch" in text_lower:
            project_type = "On-Demand Marketplace"
            project_name = "On-Demand Services Marketplace"
            business_objective = (
                "Launch a two-sided on-demand marketplace connecting local consumers with verified service "
                "providers through real-time booking, automated dispatch, and escrowed mobile payments."
            )
        elif "edtech" in text_lower or "course" in text_lower or "learning" in text_lower:
            project_type = "EdTech & Learning Management"
            project_name = "Interactive Learning & Course Management System"
            business_objective = (
                "Develop an accessible online education platform facilitating video course delivery, "
                "student assessment quizzes, certificate generation, and instructor monetization."
            )
        elif "iot" in text_lower or "sensor" in text_lower or "telemetry" in text_lower:
            project_type = "IoT & Real-time Telemetry"
            project_name = "Industrial IoT Telemetry Dashboard"
            business_objective = (
                "Deploy a high-throughput industrial telemetry platform ingesting MQTT sensor streams, "
                "visualizing real-time equipment metrics, and triggering preventive maintenance alerts."
            )
        elif "directory" in text_lower or "staff" in text_lower or "employee" in text_lower:
            project_type = "Internal Enterprise Portal"
            project_name = "Corporate Staff & Team Directory"
            business_objective = (
                "Build an internal employee directory portal with corporate SSO authentication, "
                "hierarchical organizational charts, and team contact indexing."
            )
        elif is_simple_site:
            project_type = "Corporate Web Presence"
            project_name = "Corporate Marketing & Lead Capture Site"
            business_objective = (
                "Launch a fast, accessible corporate web presence showcasing brand services, "
                "capturing customer inquiries via form workflows, and providing an administrative lead inbox."
            )
        else:
            project_type = "Custom Digital Platform"
            project_name = "Enterprise Digital Solution"
            first_line = text.strip().split("\n")[0][:80]
            business_objective = (
                f"Implement a scalable enterprise software solution: {first_line}. "
                "Aims to automate core operational workflows and enhance customer engagement."
            )

        # 2. Platform Scope
        # If mobile explicitly requested or keywords appear
        has_ios = "ios" in text_lower or "apple" in text_lower or "iphone" in text_lower or ("mobile app" in text_lower and "web only" not in text_lower)
        has_android = "android" in text_lower or "google play" in text_lower or ("mobile app" in text_lower and "web only" not in text_lower)
        has_web = "mobile only" not in text_lower
        has_admin = "admin" in text_lower or "dashboard" in text_lower or "backoffice" in text_lower or "portal" in text_lower

        platform_scope = PlatformScope(
            web=has_web,
            mobile_ios=has_ios,
            mobile_android=has_android,
            admin_portal=has_admin,
            desktop_app=False,
            notes=f"Detected scope: Web={'Yes' if has_web else 'No'}, Mobile iOS={'Yes' if has_ios else 'No'}, "
                  f"Android={'Yes' if has_android else 'No'}, Admin Dashboard={'Yes' if has_admin else 'No'}.",
        )

        # 3. AI Features Detection
        # Be careful not to falsely trigger AI on 'email' or 'retail'
        has_ai = False
        ai_keywords = ["ai ", " ai", "ai-", "recommend", "machine learning", "smart dispatch", "nlp", "llm", "biometric", "predictive"]
        if any(kw in text_lower for kw in ai_keywords):
            has_ai = True

        ai_summary = None
        if has_ai:
            ai_summary = (
                "Integrate intelligent recommendation/dispatch algorithms and machine learning "
                "models into application pipelines to enhance user engagement and conversion."
            )

        # 4. Functional Requirements Extraction
        fr_list: list[FunctionalRequirement] = []
        fr_counter = 1

        if is_simple_site:
            fr_list.append(
                FunctionalRequirement(
                    id=f"FR-{fr_counter:02d}",
                    category="Content Presentation",
                    title="Responsive Marketing & Content Pages",
                    description="High-performance presentation pages with optimized typography, responsive layouts, and SEO tags.",
                    priority="Must Have",
                    complexity="Low",
                )
            )
            fr_counter += 1
            fr_list.append(
                FunctionalRequirement(
                    id=f"FR-{fr_counter:02d}",
                    category="Lead Ingestion",
                    title="Contact & Inquiry Intake Form",
                    description="Validated client contact forms with automated email notifications and spam protection (reCAPTCHA).",
                    priority="Must Have",
                    complexity="Low",
                )
            )
            fr_counter += 1
            if has_admin:
                fr_list.append(
                    FunctionalRequirement(
                        id=f"FR-{fr_counter:02d}",
                        category="Administration",
                        title="Inquiry & Lead Management Dashboard",
                        description="Protected admin panel allowing authorized staff to view, search, and export submitted inquiries.",
                        priority="Should Have",
                        complexity="Low",
                    )
                )
                fr_counter += 1
        elif "directory" in text_lower:
            fr_list.append(
                FunctionalRequirement(
                    id=f"FR-{fr_counter:02d}",
                    category="Identity & Access",
                    title="Enterprise SSO Authentication",
                    description="Single Sign-On integration with corporate identity provider (Azure AD / Google Workspace).",
                    priority="Must Have",
                    complexity="Medium",
                )
            )
            fr_counter += 1
            fr_list.append(
                FunctionalRequirement(
                    id=f"FR-{fr_counter:02d}",
                    category="Directory Search",
                    title="Staff Directory & Org Hierarchy Index",
                    description="Searchable staff catalog by name, team, department, and direct reporting lines.",
                    priority="Must Have",
                    complexity="Low",
                )
            )
            fr_counter += 1
        else:
            # Complex / standard applications
            if any(kw in text_lower for kw in ["login", "auth", "register", "account", "profile", "user"]):
                fr_list.append(
                    FunctionalRequirement(
                        id=f"FR-{fr_counter:02d}",
                        category="Identity & Access Management",
                        title="User Authentication & Account Management",
                        description="Self-service user registration, multi-factor authentication, password reset, and role-based permissions.",
                        priority="Must Have",
                        complexity="Medium",
                    )
                )
                fr_counter += 1

            if any(kw in text_lower for kw in ["product", "catalog", "item", "inventory", "listing", "course", "sensor"]):
                fr_list.append(
                    FunctionalRequirement(
                        id=f"FR-{fr_counter:02d}",
                        category="Catalog & Data Management",
                        title="Catalog & Resource Management",
                        description="Structured management of catalog items, real-time availability, media galleries, and search indexing.",
                        priority="Must Have",
                        complexity="Medium",
                    )
                )
                fr_counter += 1

            if any(kw in text_lower for kw in ["pay", "checkout", "stripe", "paypal", "billing", "invoice"]):
                fr_list.append(
                    FunctionalRequirement(
                        id=f"FR-{fr_counter:02d}",
                        category="Financial Transactions",
                        title="Secure Checkout & Payment Gateway",
                        description="PCI-compliant payment checkout flow supporting credit cards, digital wallets, and automated receipts.",
                        priority="Must Have",
                        complexity="High",
                    )
                )
                fr_counter += 1

            if any(kw in text_lower for kw in ["book", "schedul", "calendar", "appointment", "dispatch"]):
                fr_list.append(
                    FunctionalRequirement(
                        id=f"FR-{fr_counter:02d}",
                        category="Scheduling & Operations",
                        title="Real-Time Booking & Scheduling Engine",
                        description="Dynamic appointment slot selection, automated calendar synchronization, reminders, and status tracking.",
                        priority="Must Have",
                        complexity="High",
                    )
                )
                fr_counter += 1

            if any(kw in text_lower for kw in ["message", "chat", "video", "webrtc", "consult"]):
                fr_list.append(
                    FunctionalRequirement(
                        id=f"FR-{fr_counter:02d}",
                        category="Communication",
                        title="Omnichannel Messaging & Interactive Consultations",
                        description="Secure asynchronous chat, notification triggers, or real-time audio/video session streaming.",
                        priority="Must Have",
                        complexity="High" if "video" in text_lower or "webrtc" in text_lower else "Medium",
                    )
                )
                fr_counter += 1

            if has_ai:
                fr_list.append(
                    FunctionalRequirement(
                        id=f"FR-{fr_counter:02d}",
                        category="AI & Machine Learning",
                        title="AI-Driven Intelligence & Personalization",
                        description="Predictive recommendation engine or matching algorithms leveraging embeddings and historical interactions.",
                        priority="Should Have",
                        complexity="High",
                    )
                )
                fr_counter += 1

            if has_admin:
                fr_list.append(
                    FunctionalRequirement(
                        id=f"FR-{fr_counter:02d}",
                        category="Administration",
                        title="Backoffice Administration & Operational Analytics",
                        description="Comprehensive management portal displaying key performance indicators, audit logs, and operational controls.",
                        priority="Must Have",
                        complexity="Medium",
                    )
                )
                fr_counter += 1

        if not fr_list:
            fr_list.append(
                FunctionalRequirement(
                    id="FR-01",
                    category="Core Functionality",
                    title="Primary System Capability",
                    description="Core platform business logic and user presentation layers.",
                    priority="Must Have",
                    complexity="Medium",
                )
            )

        # 5. User Roles
        user_roles = [
            UserRole(role_name="Platform Administrator", description="Full administrative access to settings, financials, and users.", access_level="Admin"),
            UserRole(role_name="Primary End-User", description="Regular customer or client accessing primary platform capabilities.", access_level="Standard User"),
        ]

        # 6. Non-Functional Requirements
        nfr_list = [
            NonFunctionalRequirement(
                category="Security & Privacy",
                description="End-to-end data encryption in transit (TLS 1.3) and at rest (AES-256) with strict role-based access control.",
                target_metric="Zero critical vulnerabilities; SOC2 / OWASP compliance",
            ),
            NonFunctionalRequirement(
                category="Performance & Latency",
                description="Sub-second API response times and optimized asset loading across web and mobile viewports.",
                target_metric="P95 API response < 300ms; Core Web Vitals score > 90",
            ),
        ]

        # 7. Integrations
        integrations: list[ThirdPartyIntegration] = []
        if "stripe" in text_lower or "paypal" in text_lower or "payment" in text_lower:
            integrations.append(
                ThirdPartyIntegration(
                    name="Stripe / PayPal",
                    category="Payment Gateway",
                    complexity="Medium",
                    notes="PCI-DSS compliant payment processing and recurring subscriptions.",
                )
            )
        if "twilio" in text_lower or "sendgrid" in text_lower or "sms" in text_lower:
            integrations.append(
                ThirdPartyIntegration(
                    name="Twilio / SendGrid",
                    category="Communications (Email/SMS)",
                    complexity="Low",
                    notes="Transactional SMS alerts and templated email notifications.",
                )
            )
        if "ehr" in text_lower or "fhir" in text_lower or "epic" in text_lower or "hl7" in text_lower:
            integrations.append(
                ThirdPartyIntegration(
                    name="Epic / Cerner EHR (FHIR/HL7)",
                    category="CRM & ERP",
                    complexity="High",
                    notes="Clinical healthcare data exchange complying with HIPAA.",
                )
            )
        if "plaid" in text_lower:
            integrations.append(
                ThirdPartyIntegration(
                    name="Plaid Banking API",
                    category="CRM & ERP",
                    complexity="High",
                    notes="Secure financial data aggregation and bank account verification.",
                )
            )
        if has_ai:
            integrations.append(
                ThirdPartyIntegration(
                    name="Google Gemini / OpenAI API",
                    category="AI / LLM Infrastructure",
                    complexity="Medium",
                    notes="LLM inference and embeddings for semantic search and recommendations.",
                )
            )
        if not integrations:
            integrations.append(
                ThirdPartyIntegration(
                    name="Core Cloud Infrastructure (AWS)",
                    category="Cloud Storage",
                    complexity="Low",
                    notes="Cloud storage and basic email notifications.",
                )
            )

        # 8. Missing Information & Ambiguity Detection
        missing: list[MissingInformation] = []
        gap_id = 1

        if not is_simple_site:
            if not any(kw in text_lower for kw in ["concurrent", "daily active", "requests per second", "peak users", "traffic volume"]):
                missing.append(
                    MissingInformation(
                        id=f"GAP-{gap_id:02d}",
                        category="Capacity & Volume",
                        gap_description="Expected concurrent user volumes and initial transaction throughput are not specified.",
                        impact="High" if not is_simple_site else "Low",
                        clarification_question="What is the anticipated peak concurrent active user volume and monthly transaction throughput for Year 1?",
                    )
                )
                gap_id += 1

            if ("mobile" in text_lower or "app" in text_lower) and not any(kw in text_lower for kw in ["native ios", "swift", "react native", "flutter", "kotlin"]):
                missing.append(
                    MissingInformation(
                        id=f"GAP-{gap_id:02d}",
                        category="Scope & Technology",
                        gap_description="Mobile app architecture is unspecified (Cross-platform React Native/Flutter vs. Native Swift/Kotlin).",
                        impact="Medium",
                        clarification_question="Do you prefer a unified cross-platform mobile codebase (React Native / Flutter) or native iOS and Android applications?",
                    )
                )
                gap_id += 1

            if not any(kw in text_lower for kw in ["hipaa", "gdpr", "pci", "soc2", "compliance", "regulatory"]):
                missing.append(
                    MissingInformation(
                        id=f"GAP-{gap_id:02d}",
                        category="Compliance & Legal",
                        gap_description="Specific data protection, geographical residency, or regulatory frameworks are not outlined.",
                        impact="Medium",
                        clarification_question="Are there specific regional compliance or data sovereignty requirements (e.g., GDPR in EU, HIPAA in US) governing user data?",
                    )
                )
                gap_id += 1
        else:
            missing.append(
                MissingInformation(
                    id=f"GAP-{gap_id:02d}",
                    category="Design & Content",
                    gap_description="Client branding assets, copywriting, and Figma designs are pending delivery.",
                    impact="Low",
                    clarification_question="Will your team provide finalized brand guidelines and copy, or should Cynbit include copywriting and UX design in the scope?",
                )
            )

        # 9. Technology Recommendation
        tech_rec = TechnologyRecommendation(
            frontend="Next.js (React) with TailwindCSS & TypeScript",
            backend="FastAPI (Python) or Node.js / NestJS" if not is_simple_site else "Next.js Static / API Routes",
            database="PostgreSQL with Redis caching" if not is_simple_site else "Lightweight SQLite / Supabase",
            cloud_infrastructure="AWS (ECS Fargate / RDS)" if not is_simple_site else "Vercel / AWS CloudFront",
            authentication="OAuth 2.0 / JWT" if not is_simple_site else "Session Cookies / HTTP Basic Auth",
            ai_infrastructure="Google Gemini API / pgvector" if has_ai else "Not Applicable",
            ci_cd_devops="GitHub Actions CI/CD with Docker",
            justification=(
                f"The proposed stack offers industry-leading developer velocity and maintainability. "
                f"Next.js ensures instant page responsiveness and high Core Web Vitals score."
            ),
        )

        deadline_match = re.search(r"(\d+)\s*(?:weeks?|wks)", text_lower)
        stated_deadline = int(deadline_match.group(1)) if deadline_match else None

        budget_match = re.search(r"\$\s*(\d{1,3}(?:,\d{3})*(?:\s*-\s*\$?\d{1,3}(?:,\d{3})*)?)", text)
        budget_str = f"${budget_match.group(1)}" if budget_match else None

        return RequirementAnalysis(
            project_name=project_name,
            business_objective=business_objective,
            user_roles=user_roles,
            functional_requirements=fr_list,
            non_functional_requirements=nfr_list,
            platform_scope=platform_scope,
            integrations=integrations,
            has_ai_features=has_ai,
            ai_features_summary=ai_summary,
            missing_information=missing,
            tech_recommendation=tech_rec,
            stated_deadline_weeks=stated_deadline,
            budget_range_mentioned=budget_str,
            extracted_assumptions=[
                "Client will provide timely access to brand guidelines, API credentials, and sandbox environments.",
                "Third-party API licensing, hosting fees, and gateway charges are paid directly by the client.",
                "Client subject matter experts will be available for weekly sprint reviews and acceptance tests.",
            ],
            extracted_exclusions=[
                "Manual data entry of legacy catalog or historical records beyond initial migration scripts.",
                "Custom hardware integration or physical point-of-sale terminal firmware.",
                "Ongoing 24/7 post-launch managed support (can be contracted via separate SLA).",
            ],
        )
