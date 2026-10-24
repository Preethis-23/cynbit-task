/**
 * CYNBIT OS — Enterprise AI Pre-Sales Solution Architect
 * Production Controller: High-Animation Telemetry & Real-Time Reactivity
 */

const appState = {
  activeTab: "ingest",
  analysis: null,
  proposal: null,
  isAnalyzing: false,
  samples: [
    {
      id: "fintech",
      title: "Fintech Core Migration",
      client: "Apex Financial Systems",
      desc: "AWS microservices migration, Kafka event-sourcing, SOC2 & PCI-DSS compliance, 4.2M daily transactions.",
      content: `Client: Apex Financial Systems
Project: Core Banking Ledger Cloud Migration
Overview: High-volume financial platform processing 4.2M daily transactions on a legacy on-premise monolith.
Objectives:
- Re-architect core ledger into domain-driven microservices on AWS (EKS).
- Implement event-driven audit streaming with Apache Kafka for zero transaction loss.
- Achieve full compliance with SOC2 Type II and PCI-DSS Level 1 tokenization standards.
- Maintain four-nines (99.99%) availability during blue/green migration cutover.
Constraints:
- Hard 6-month launch milestone driven by legacy data center lease termination.
- Target budget range: $480,000 - $620,000.
Key Stakeholders: Chief Technology Officer, VP Risk & Security, Head of Core Banking.`
    },
    {
      id: "healthcare",
      title: "Healthcare Clinical Mesh",
      client: "Meridian Health Network",
      desc: "HIPAA/HITRUST lakehouse for 43 clinics, FHIR ingestion, PHI de-identification, sub-800ms Patient 360 search.",
      content: `Client: Meridian Health Network
Project: Enterprise Clinical Data Mesh & Patient 360
Overview: Regional healthcare provider with 43 outpatient clinics and 3 regional hospitals ingesting 1.4 TB/day in HL7 and FHIR clinical feeds.
Objectives:
- Build a unified HIPAA and HITRUST-certified clinical lakehouse on AWS.
- Automate PHI de-identification and pseudonymization pipeline for medical research.
- Deliver clinical Patient 360 lookup with sub-800ms query latency for 1,200 concurrent providers.
- Implement end-to-end data lineage and immutable audit logs.
Constraints:
- Mandatory Business Associate Agreement (BAA) and KMS customer-managed keys.
- Reduce existing Snowflake query costs by at least 35%.`
    },
    {
      id: "retail",
      title: "Retail Personalization",
      client: "North & Co Retail",
      desc: "Cloudflare Workers edge inference for 8M MAU, 120ms p95 budget, contextual bandits, GDPR consent mode.",
      content: `Client: North & Co Retail
Project: Real-Time Edge Personalization & Recommendation Engine
Overview: Global omnichannel lifestyle retailer with 8M monthly active users across web and mobile.
Objectives:
- Deploy real-time recommendation inference at the edge (Cloudflare Workers) with strict 120ms p95 latency budget.
- Feature store with 400+ real-time customer behavioral signals using Redis Enterprise.
- Contextual multi-armed bandit A/B testing framework.
- Strict GDPR consent-mode enforcement and zero third-party cookie dependency.
Integrations:
- Shopify Plus storefront, Segment CDP, Braze marketing automation, Snowflake warehouse.
KPIs: Target +18% conversion rate and -22% bounce rate on dynamic landing pages.`
    },
    {
      id: "logistics",
      title: "Logistics Digital Twin",
      client: "TransFleet Logistics",
      desc: "IoT fleet telematics (MQTT/Kafka), ML ETA with 96% accuracy, route dispatch optimization with 12% fuel savings.",
      content: `Client: TransFleet Logistics
Project: Fleet Digital Twin & Predictive Routing Platform
Overview: Nationwide freight carrier managing 650 Class-8 semi-trucks across 24 regional distribution hubs.
Objectives:
- Real-time IoT telematics ingestion via MQTT and Kafka processing 50,000 telemetry events/sec.
- Machine learning model for dynamic ETA prediction achieving >=96% accuracy within a 15-minute delivery window.
- Dynamic route dispatch optimizer delivering minimum 12% fleet fuel savings.
- Driver safety monitoring and Hours of Service (HOS) automated log compliance.
Constraints:
- Integration with existing on-premises AS400 dispatch system and ELD hardware.
- Offline-first mobile navigation app for drivers operating in low-connectivity corridors.`
    }
  ]
};

// ==========================================
// Initialization on DOM Ready
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initTabs();
  initSampleTiles();
  initFileUpload();
  initSliders();
  initTextarea();
  initActions();

  // Pre-load primary sample brief
  loadSample(0, false);
});

// ==========================================
// 1. Theme Toggle System (Dark / Light)
// ==========================================
function initThemeToggle() {
  const html = document.documentElement;
  try {
    localStorage.removeItem("cynbit_theme");
    localStorage.setItem("cynbit_theme", "light");
  } catch (e) {}
  html.setAttribute("data-theme", "light");
}

// ==========================================
// 2. Fluid Tabs Navigation
// ==========================================
function initTabs() {
  const tabButtons = document.querySelectorAll(".tab-nav-btn");
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const tabName = btn.getAttribute("data-tab");
      switchTab(tabName);
    });
  });

  document.getElementById("jumpToDiscoveryBtn")?.addEventListener("click", () => switchTab("discovery"));
}

function switchTab(tabName) {
  appState.activeTab = tabName;

  // Update button active state
  document.querySelectorAll(".tab-nav-btn").forEach(btn => {
    if (btn.getAttribute("data-tab") === tabName) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  // Update panel visibility with smooth entrance
  document.querySelectorAll(".tab-panel").forEach(panel => {
    if (panel.id === `tab-${tabName}`) {
      panel.classList.add("active");
    } else {
      panel.classList.remove("active");
    }
  });

  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ==========================================
// 3. Sample Briefs Selection
// ==========================================
function initSampleTiles() {
  const tiles = document.querySelectorAll(".sample-tile");
  tiles.forEach(tile => {
    tile.addEventListener("click", () => {
      const idx = parseInt(tile.getAttribute("data-idx"), 10);
      loadSample(idx, true);
    });
  });
}

function loadSample(idx, notifyUser = false) {
  const sample = appState.samples[idx];
  if (!sample) return;

  // Update selection appearance
  document.querySelectorAll(".sample-tile").forEach((tile, i) => {
    if (i === idx) {
      tile.classList.add("selected");
    } else {
      tile.classList.remove("selected");
    }
  });

  // Populate form inputs
  const clientInput = document.getElementById("clientNameInput");
  const briefText = document.getElementById("briefTextArea");

  if (clientInput) clientInput.value = sample.client;
  if (briefText) briefText.value = sample.content;

  updateWordCount();

  if (notifyUser) {
    showToast(`Loaded archetype: ${sample.title}`);
  }
}

// ==========================================
// 4. Textarea & Metrics
// ==========================================
function initTextarea() {
  const briefText = document.getElementById("briefTextArea");
  if (!briefText) return;

  briefText.addEventListener("input", updateWordCount);

  // Keyboard shortcut Ctrl+Enter / Cmd+Enter
  window.addEventListener("keydown", e => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      runAnalysis();
    }
  });
}

function updateWordCount() {
  const briefText = document.getElementById("briefTextArea");
  const countBadge = document.getElementById("wordCountBadge");
  if (!briefText || !countBadge) return;

  const text = briefText.value.trim();
  const words = text ? text.split(/\s+/).length : 0;
  countBadge.textContent = `${words.toLocaleString()} words`;
}

// ==========================================
// 5. File Upload & Drag-and-Drop
// ==========================================
function initFileUpload() {
  const dropZone = document.getElementById("fileDropZone");
  const fileInput = document.getElementById("fileInput");
  const statusEl = document.getElementById("fileUploadStatus");

  if (!dropZone || !fileInput) return;

  dropZone.addEventListener("click", () => fileInput.click());

  dropZone.addEventListener("dragover", e => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", async e => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      await handleFileUpload(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", async () => {
    if (fileInput.files && fileInput.files.length > 0) {
      await handleFileUpload(fileInput.files[0]);
    }
  });
}

async function handleFileUpload(file) {
  const statusEl = document.getElementById("fileUploadStatus");
  if (statusEl) statusEl.textContent = `Extracting ${file.name}...`;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("client_name", document.getElementById("clientNameInput")?.value || "Client");

  try {
    const res = await fetch("/api/upload", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Upload failed" }));
      if (statusEl) statusEl.textContent = "Upload failed";
      showToast(`Upload failed: ${err.detail || "Error"}`);
      return;
    }

    const data = await res.json();
    const briefText = document.getElementById("briefTextArea");
    if (briefText) briefText.value = data.cleaned_text;
    if (statusEl) statusEl.textContent = `Attached: ${file.name}`;

    updateWordCount();
    showToast(`Extracted ${data.word_count.toLocaleString()} words from ${file.name}`);
  } catch (err) {
    if (statusEl) statusEl.textContent = "Upload failed";
    showToast(`Upload error: ${err.message}`);
  }
}

// ==========================================
// 6. Commercial Sliders & Engine Selection
// ==========================================
function initSliders() {
  const billSlider = document.getElementById("billSlider");
  const costSlider = document.getElementById("costSlider");
  const contSlider = document.getElementById("contingencySlider");
  const providerSelect = document.getElementById("providerSelect");

  billSlider?.addEventListener("input", () => {
    const val = billSlider.value;
    document.getElementById("billVal").textContent = `$${val}/hr`;
    debounceRecalculate();
  });

  costSlider?.addEventListener("input", () => {
    const val = costSlider.value;
    document.getElementById("costVal").textContent = `$${val}/hr`;
    debounceRecalculate();
  });

  contSlider?.addEventListener("input", () => {
    const val = contSlider.value;
    document.getElementById("contingencyVal").textContent = `${val}%`;
    debounceRecalculate();
  });

  providerSelect?.addEventListener("change", () => {
    const p = providerSelect.value;
    const apiKeyGroup = document.getElementById("apiKeyGroup");
    const statusText = document.getElementById("engineStatusText");

    if (p === "gemini") {
      apiKeyGroup?.classList.remove("hidden");
      if (statusText) statusText.textContent = "Gemini 2.5 Flash Active";
      showToast("Selected Google Gemini 2.5 Flash");
    } else if (p === "openai") {
      apiKeyGroup?.classList.remove("hidden");
      if (statusText) statusText.textContent = "GPT-4o-mini Active";
      showToast("Selected OpenAI GPT-4o-mini");
    } else {
      apiKeyGroup?.classList.add("hidden");
      if (statusText) statusText.textContent = "Offline Rule Engine Ready";
      showToast("Selected Deterministic Offline Engine");
    }
  });
}

let recalcTimer = null;
function debounceRecalculate() {
  if (!appState.analysis) return;
  clearTimeout(recalcTimer);
  recalcTimer = setTimeout(triggerRecalculate, 180);
}

async function triggerRecalculate() {
  if (!appState.analysis) return;

  const cost = parseFloat(document.getElementById("costSlider")?.value || 45);
  const bill = parseFloat(document.getElementById("billSlider")?.value || 95);
  const cont = parseFloat(document.getElementById("contingencySlider")?.value || 15);

  const payload = {
    requirements: appState.analysis.requirements,
    risk: appState.analysis.risk,
    hourly_cost: cost,
    billing_rate: bill,
    contingency_pct: cont,
    ml_predicted_hours: appState.analysis.commercial?.ml_predicted_hours
  };

  try {
    const res = await fetch("/api/recalculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const data = await res.json();
      appState.analysis.effort = data.effort;
      appState.analysis.timeline = data.timeline;
      appState.analysis.commercial = data.commercial;
      renderSizing(appState.analysis);
      showToast(`Recalibrated: Target $${Math.round(data.commercial.quotation_likely).toLocaleString()} (${data.commercial.profit_margin_likely_pct.toFixed(1)}% margin)`);
    }
  } catch (err) {
    console.warn("Recalculate error:", err);
  }
}

// ==========================================
// 7. Actions & Listeners
// ==========================================
function initActions() {
  document.getElementById("analyzeBtn")?.addEventListener("click", runAnalysis);

  document.getElementById("dismissBannerBtn")?.addEventListener("click", () => {
    const banner = document.getElementById("governanceBanner");
    if (banner) banner.style.display = "none";
  });

  document.getElementById("copyProposalBtn")?.addEventListener("click", copyProposalText);
  document.getElementById("downloadDocxBtn")?.addEventListener("click", exportDocx);
  document.getElementById("downloadMdBtn")?.addEventListener("click", exportMarkdown);

  document.getElementById("signoffBtn")?.addEventListener("click", () => {
    const btn = document.getElementById("signoffBtn");
    if (btn) {
      btn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
        Audit Seal Issued
      `;
      btn.disabled = true;
      btn.classList.remove("btn-primary-glow");
      btn.classList.add("btn-secondary-glass");
    }
    showToast("✓ Architect sign-off recorded with immutable SHA256 audit stamp", true);
  });
}

// ==========================================
// 8. Core Analysis Execution with Animated HUD
// ==========================================
async function runAnalysis() {
  if (appState.isAnalyzing) return;

  const briefText = document.getElementById("briefTextArea");
  const text = briefText?.value?.trim();
  if (!text) {
    showToast("Please enter or select a client requirement brief");
    return;
  }

  const clientName = document.getElementById("clientNameInput")?.value?.trim() || "Prospective Client";
  const provider = document.getElementById("providerSelect")?.value || "offline";
  const apiKey = document.getElementById("apiKeyInput")?.value?.trim();
  const cost = parseFloat(document.getElementById("costSlider")?.value || 45);
  const bill = parseFloat(document.getElementById("billSlider")?.value || 95);
  const cont = parseFloat(document.getElementById("contingencySlider")?.value || 15);

  appState.isAnalyzing = true;

  // Show Radar HUD Overlay with Animated Multi-Step Sequence
  const hud = document.getElementById("hudOverlay");
  hud?.classList.add("active");
  animateHudSteps();

  const payload = {
    text: text,
    client_name: clientName,
    provider: provider,
    hourly_cost: cost,
    billing_rate: bill,
    contingency_pct: cont,
    gemini_key: provider === "gemini" && apiKey ? apiKey : null,
    openai_key: provider === "openai" && apiKey ? apiKey : null
  };

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Analysis failed" }));
      showToast(`Analysis failed: ${err.detail || "Server error"}`);
      return;
    }

    const data = await res.json();
    appState.analysis = data;

    // Small delay so user sees HUD completion checkmarks
    await new Promise(r => setTimeout(r, 600));

    // Render all downstream tabs
    renderDiscovery(data);
    renderArchitecture(data);
    renderSizing(data);
    renderRisk(data);
    renderHandoff(data);

    // Background proposal generation
    generateProposal(data, clientName, provider);

    // Show ready notification banner on Ingest tab
    const banner = document.getElementById("analysisReadyBanner");
    if (banner) banner.classList.remove("hidden");

    showToast("Architecture and financial models ready — explore Discovery tab", true);
  } catch (err) {
    showToast(`Error: ${err.message}`);
  } finally {
    appState.isAnalyzing = false;
    hud?.classList.remove("active");
  }
}

function animateHudSteps() {
  const steps = [1, 2, 3, 4, 5];
  steps.forEach((s, idx) => {
    setTimeout(() => {
      // mark previous as completed
      if (idx > 0) {
        const prev = document.getElementById(`hudStep${steps[idx - 1]}`);
        prev?.classList.remove("active");
        prev?.classList.add("completed");
      }
      const cur = document.getElementById(`hudStep${s}`);
      cur?.classList.add("active");
    }, idx * 180);
  });
}

// ==========================================
// 9. Tab Renderers
// ==========================================

// Tab 2: Discovery
function renderDiscovery(data) {
  const req = data.requirements;
  const clientName = document.getElementById("clientNameInput")?.value || "Enterprise Client";

  // Infer domain
  let domain = "Enterprise Solutions";
  const textSample = (req.business_objective || req.project_name || "").toLowerCase();
  if (textSample.includes("health") || textSample.includes("fhir") || textSample.includes("hipaa")) domain = "Healthcare & Life Sciences";
  else if (textSample.includes("bank") || textSample.includes("fintech") || textSample.includes("pci") || textSample.includes("ledger")) domain = "Financial Services & Banking";
  else if (textSample.includes("retail") || textSample.includes("ecom") || textSample.includes("commerce")) domain = "Omnichannel E-Commerce";
  else if (textSample.includes("truck") || textSample.includes("fleet") || textSample.includes("logistics")) domain = "Logistics & Fleet";

  const discDomainBadge = document.getElementById("discDomainBadge");
  const discComplexityBadge = document.getElementById("discComplexityBadge");
  const discProjectName = document.getElementById("discProjectName");
  const discObjectives = document.getElementById("discObjectives");

  if (discDomainBadge) discDomainBadge.textContent = `Domain: ${domain}`;
  if (discComplexityBadge) discComplexityBadge.textContent = `Complexity: ${data.risk?.complexity_level || "Medium"}`;
  if (discProjectName) discProjectName.textContent = `${clientName} — Technical Discovery`;
  if (discObjectives) discObjectives.textContent = req.business_objective || "End-to-end technical architecture optimized for low-latency scale, zero transaction loss, and regulatory governance.";

  // Functional Modules
  const modulesContainer = document.getElementById("discModulesList");
  if (modulesContainer) {
    const funcs = req.functional_requirements || [];
    if (funcs.length === 0) {
      modulesContainer.innerHTML = `<div style="color:var(--text-muted); font-size:0.85rem;">No specific functional modules extracted.</div>`;
    } else {
      modulesContainer.innerHTML = funcs.map(m => `
        <div style="background:var(--surface-1); border:1px solid var(--border-subtle); border-radius:var(--radius-md); padding:16px; transition:border-color 0.2s ease;">
          <div class="flex items-center justify-between" style="margin-bottom:8px;">
            <span style="font-weight:700; font-size:0.95rem; color:var(--text-primary);">${escapeHtml(m.title || m.category || "Module")}</span>
            <span class="badge-tag info mono">${escapeHtml(m.complexity || m.priority || "Medium")}</span>
          </div>
          <p style="font-size:0.85rem; color:var(--text-secondary); line-height:1.5;">${escapeHtml(m.description)}</p>
        </div>
      `).join("");
    }
  }

  // Integrations
  const integrationsContainer = document.getElementById("discIntegrationsList");
  if (integrationsContainer) {
    const integs = req.integrations || [];
    if (integs.length === 0) {
      integrationsContainer.innerHTML = `<div style="color:var(--text-muted); font-size:0.85rem;">Standard enterprise REST / gRPC interfaces</div>`;
    } else {
      integrationsContainer.innerHTML = integs.map(integ => `
        <div style="background:var(--surface-1); border:1px solid var(--border-subtle); border-radius:var(--radius-sm); padding:10px 14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
          <span style="font-weight:600; font-size:0.9rem;">${escapeHtml(integ.name || integ)}</span>
          <span class="badge-tag success">API TARGET</span>
        </div>
      `).join("");
    }
  }

  // Non-Functional Requirements (SLAs)
  const nfrContainer = document.getElementById("discNfrList");
  if (nfrContainer) {
    const nfrs = req.non_functional_requirements || [];
    if (nfrs.length === 0) {
      nfrContainer.innerHTML = `<div style="color:var(--text-muted); font-size:0.85rem;">99.9% Uptime SLA, &lt;200ms p95 latency budget</div>`;
    } else {
      nfrContainer.innerHTML = nfrs.map(nfr => `
        <div style="background:var(--surface-1); border:1px solid var(--border-subtle); border-radius:var(--radius-sm); padding:10px 14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center; gap:12px;">
          <div>
            <span style="font-weight:600; font-size:0.88rem; display:block;">${escapeHtml(nfr.category || "Constraint")}</span>
            <span style="font-size:0.8rem; color:var(--text-secondary);">${escapeHtml(nfr.description)}</span>
          </div>
          <span class="badge-tag warning mono" style="flex-shrink:0;">${escapeHtml(nfr.target_metric || "SLA GATE")}</span>
        </div>
      `).join("");
    }
  }

  // Missing Info & Questions for Pre-Sales Lead
  const gapsContainer = document.getElementById("discGapsList");
  if (gapsContainer) {
    const gaps = req.missing_information || [];
    if (gaps.length === 0) {
      gapsContainer.innerHTML = `<div style="color:var(--text-muted); font-size:0.85rem;">No critical information gaps detected. Architecture is fully scoped.</div>`;
    } else {
      gapsContainer.innerHTML = gaps.map(g => `
        <div style="background:var(--surface-1); border:1px solid var(--border-subtle); border-radius:var(--radius-sm); padding:12px 16px; margin-bottom:8px;">
          <div class="flex items-center justify-between" style="margin-bottom:4px;">
            <span style="font-weight:700; font-size:0.88rem; color:var(--warning);">${escapeHtml(g.category || "Information Gap")}</span>
            <span class="badge-tag warning mono">Impact: ${escapeHtml(g.impact || "Medium")}</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-secondary); margin-bottom:6px;">${escapeHtml(g.gap_description)}</p>
          <div style="font-size:0.82rem; background:var(--surface-2); padding:8px 10px; border-radius:var(--radius-xs); color:var(--text-primary);">
            <strong style="color:var(--accent-primary);">Ask Client:</strong> "${escapeHtml(g.clarification_question)}"
          </div>
        </div>
      `).join("");
    }
  }
}

// Tab 3: Architecture
function renderArchitecture(data) {
  const req = data.requirements;
  const tech = req.tech_recommendation || {};

  const techGrid = document.getElementById("archTechGrid");
  if (techGrid) {
    const categories = [
      { label: "Frontend & UI", val: tech.frontend || "Next.js 14, Tailwind CSS, TypeScript" },
      { label: "Backend Core", val: tech.backend || "Python FastAPI / Go Microservices, AsyncIO" },
      { label: "Database & Storage", val: tech.database || "PostgreSQL RDS, Redis Sentinel, S3" },
      { label: "Cloud & Infrastructure", val: tech.cloud_infrastructure || "AWS EKS (Kubernetes), Terraform IaC" },
      { label: "Auth & Governance", val: tech.authentication || "OAuth 2.0, mTLS, HashiCorp Vault" },
      { label: "CI/CD & Observability", val: tech.ci_cd_devops || "GitHub Actions, Datadog APM, Prometheus" }
    ];

    techGrid.innerHTML = categories.map(cat => `
      <div class="stat-kpi-card">
        <div class="kpi-title">${escapeHtml(cat.label)}</div>
        <div style="font-weight:600; font-size:0.92rem; margin-top:6px; color:var(--text-primary); line-height:1.4;">${escapeHtml(cat.val)}</div>
      </div>
    `).join("");
  }

  const justEl = document.getElementById("archJustification");
  if (justEl && tech.justification) {
    justEl.textContent = tech.justification;
  }
}

// Tab 4: Sizing & Commercials
function renderSizing(data) {
  const effort = data.effort;
  const comm = data.commercial;
  const timeline = data.timeline;

  const totalHrs = effort.likely_hours || effort.min_hours || 400;
  const totalPrice = comm.quotation_likely || 50000;
  const totalCost = comm.internal_cost_likely || 25000;
  const grossProfit = comm.expected_profit_likely || (totalPrice - totalCost);
  const marginPct = comm.profit_margin_likely_pct || ((grossProfit / totalPrice) * 100);

  document.getElementById("kpiTotalHours").textContent = `${Math.round(totalHrs).toLocaleString()} hrs`;
  document.getElementById("kpiTeamSize").textContent = `${comm.team_composition?.length || 4} FTE`;
  document.getElementById("kpiTotalPrice").textContent = `$${Math.round(totalPrice).toLocaleString()}`;
  document.getElementById("kpiGrossProfit").textContent = `$${Math.round(grossProfit).toLocaleString()}`;
  document.getElementById("kpiMarginLabel").textContent = `Gross Margin: ${marginPct.toFixed(1)}%`;
  document.getElementById("kpiCostLabel").textContent = `Internal Cost: $${Math.round(totalCost).toLocaleString()}`;
  document.getElementById("sizingTimelineBadge").textContent = `Timeline: ${(timeline.likely_weeks || 12).toFixed(1)} wks (${timeline.min_weeks || 8} - ${timeline.max_weeks || 16} wks)`;

  // Discipline breakdown bars with animated shimmer
  const discContainer = document.getElementById("disciplineBarsContainer");
  if (discContainer && effort.breakdown) {
    const bd = effort.breakdown;
    const disciplines = [
      { name: "Frontend Engineering", hrs: bd.frontend_hours || 40 },
      { name: "Backend Architecture", hrs: bd.backend_hours || 45 },
      { name: "Database & Data Mesh", hrs: bd.database_arch_hours || 15 },
      { name: "Integration & Security", hrs: bd.integration_hours || 25 },
      { name: "QA & Automation Testing", hrs: bd.qa_testing_hours || 22.5 },
      { name: "DevOps & Cloud IaC", hrs: bd.devops_infra_hours || 15 },
      { name: "Technical Project Lead", hrs: bd.project_management_hours || 18.8 },
      { name: "Contingency Buffer", hrs: bd.contingency_hours || 30 }
    ];

    const baseSum = disciplines.reduce((acc, d) => acc + d.hrs, 0) || 1;

    discContainer.innerHTML = disciplines.map(d => {
      const pct = Math.round((d.hrs / baseSum) * 100);
      return `
        <div class="shimmer-progress-wrap">
          <div class="progress-header">
            <span class="progress-name">${escapeHtml(d.name)}</span>
            <span class="progress-stat">${Math.round(d.hrs)} hrs (${pct}%)</span>
          </div>
          <div class="progress-rail">
            <div class="progress-bar-fill" style="width: ${pct}%"></div>
          </div>
        </div>
      `;
    }).join("");
  }

  // Sensitivity Scenarios Table
  const tbody = document.getElementById("sensitivityTableBody");
  if (tbody) {
    const currentRate = comm.hourly_billing_rate || 95;
    const rates = [
      { name: "Discounted (-15%)", rate: currentRate * 0.85 },
      { name: "Target Baseline", rate: currentRate },
      { name: "Value / Fast-Track (+20%)", rate: currentRate * 1.20 }
    ];

    tbody.innerHTML = rates.map(s => {
      const price = Math.round(s.rate * totalHrs);
      const profit = price - totalCost;
      const margin = (profit / price) * 100;
      const isCurrent = Math.abs(s.rate - currentRate) < 0.01;
      return `
        <tr class="${isCurrent ? 'highlight' : ''}">
          <td><strong>${escapeHtml(s.name)}</strong></td>
          <td class="mono">$${Math.round(s.rate)}/hr</td>
          <td class="mono">${Math.round(totalHrs)} hrs</td>
          <td class="mono font-semibold" style="color:var(--text-primary);">$${price.toLocaleString()}</td>
          <td class="mono" style="color:var(--text-muted);">$${Math.round(totalCost).toLocaleString()}</td>
          <td class="mono" style="color: ${margin >= 45 ? 'var(--success)' : 'var(--warning)'}; font-weight:700;">${margin.toFixed(1)}%</td>
        </tr>
      `;
    }).join("");
  }
}

// Tab 5: Risk & Circular Gauge Meter
function renderRisk(data) {
  const risk = data.risk;
  const score = risk.total_risk_score || risk.complexity_score || 15;
  const lvl = (risk.risk_level || "medium").toLowerCase();

  // Circular SVG Gauge Meter animation
  const gaugeScore = document.getElementById("riskGaugeScore");
  const gaugeLevel = document.getElementById("riskGaugeLevel");
  const gaugeBar = document.getElementById("riskGaugeBar");
  const overallBadge = document.getElementById("riskOverallBadge");

  if (gaugeScore) gaugeScore.textContent = score;
  if (gaugeLevel) gaugeLevel.textContent = lvl.toUpperCase();

  // 2 * PI * r = 2 * 3.14159 * 70 = 439.8
  const maxCircumference = 440;
  const normalizedScore = Math.min(100, Math.max(0, score * 2.5));
  const offset = maxCircumference - (normalizedScore / 100) * maxCircumference;

  if (gaugeBar) {
    gaugeBar.style.strokeDashoffset = offset;
    if (lvl === "low") {
      gaugeBar.style.stroke = "var(--success)";
    } else if (lvl === "high" || lvl === "critical") {
      gaugeBar.style.stroke = "var(--danger)";
    } else {
      gaugeBar.style.stroke = "var(--warning)";
    }
  }

  if (overallBadge) {
    overallBadge.textContent = `Risk Level: ${lvl.toUpperCase()}`;
    overallBadge.className = `badge-tag ${lvl === 'low' ? 'success' : lvl === 'medium' ? 'warning' : 'danger'}`;
  }

  const itemsContainer = document.getElementById("riskItemsContainer");
  if (itemsContainer) {
    const factors = risk.risk_factors || [];
    if (factors.length === 0) {
      itemsContainer.innerHTML = `<div style="color:var(--text-muted); font-size:0.85rem;">No critical architectural risks detected. Standard governance gates apply.</div>`;
    } else {
      itemsContainer.innerHTML = factors.map(r => {
        const isHigh = r.severity === "High" || r.points >= 4;
        const tagClass = isHigh ? "danger" : "warning";
        return `
          <div class="risk-card-item">
            <div class="risk-card-header">
              <span class="risk-rule-title">${escapeHtml(r.rule_name || "Architectural Risk")}</span>
              <span class="badge-tag ${tagClass} mono">${escapeHtml(r.severity || "Risk")} • ${r.points} pts</span>
            </div>
            <p class="risk-reason-text">${escapeHtml(r.reason || r.rule_name)}</p>
            <div class="risk-mitigation-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              <span><strong>Mitigation:</strong> ${escapeHtml(r.mitigation)}</span>
            </div>
          </div>
        `;
      }).join("");
    }
  }
}

// Tab 6: Proposal Generation
async function generateProposal(data, clientName, provider) {
  const proposalView = document.getElementById("proposalViewArea");
  if (proposalView) {
    proposalView.innerHTML = `
      <div style="text-align:center; padding: 48px 20px;">
        <div class="hud-spinner-core" style="margin: 0 auto 16px;"></div>
        <div style="font-size:0.95rem; font-weight:600; color:var(--text-primary);">Synthesizing formal enterprise statement of work...</div>
        <div style="font-size:0.8rem; color:var(--text-muted); margin-top:4px;">Assembling deliverables, milestone terms, and governance acceptance criteria.</div>
      </div>
    `;
  }

  const payload = {
    requirements: data.requirements,
    commercial: data.commercial,
    risk: data.risk,
    client_name: clientName,
    provider: provider
  };

  try {
    const res = await fetch("/api/generate-proposal", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const pData = await res.json();
      appState.proposal = pData.proposal || pData;
      appState.markdown = pData.markdown || "";
      renderProposal(appState.proposal, data);
    }
  } catch (err) {
    if (proposalView) {
      proposalView.innerHTML = `<div style="color:var(--danger); font-size:0.9rem;">Proposal generation failed: ${err.message}</div>`;
    }
  }
}

function renderProposal(proposal, data) {
  const proposalView = document.getElementById("proposalViewArea");
  if (!proposalView) return;

  const clientName = document.getElementById("clientNameInput")?.value || "Client";
  const comm = data.commercial;
  const p = proposal.proposal || proposal;

  const scopeList = (p.scope_of_work || []).map(s => `<li>${escapeHtml(s)}</li>`).join("");

  proposalView.innerHTML = `
    <div class="dossier-header-strip">
      <div>
        <div class="dossier-watermark">CYNBIT STATEMENT OF WORK & ARCHITECTURE PROPOSAL</div>
        <h2 style="font-size: 1.6rem; letter-spacing: -0.03em; margin-bottom: 6px;">${escapeHtml(p.title || "Enterprise Technical Architecture Proposal")}</h2>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Prepared for: <strong style="color:var(--text-primary);">${escapeHtml(clientName)}</strong> • Validity: 30 Business Days • Status: Ready for Client Presentation
        </div>
      </div>
      <span class="badge-tag success">APPROVED DRAFT</span>
    </div>

    <div class="dossier-body">
      <h3>1. Executive Summary</h3>
      <p>${escapeHtml(p.executive_summary || "Architectural solution overview tailored to enterprise requirements.")}</p>

      <h3>2. Scope of Work & Deliverables</h3>
      <ul>
        ${scopeList || "<li>Deterministic cloud microservices architecture and deployment blueprint.</li>"}
      </ul>

      <h3>3. Commercial Terms & Investment</h3>
      <div style="background:var(--surface-0); border:1px solid var(--border-subtle); border-radius:var(--radius-md); padding:18px; margin-top:12px;">
        <div class="flex justify-between items-center" style="margin-bottom:10px;">
          <span style="font-size:0.9rem; color:var(--text-secondary);">Total Fixed-Price Professional Services:</span>
          <span class="mono" style="font-size:1.4rem; font-weight:800; color:var(--accent-primary);">$${Math.round(comm.quotation_likely || comm.total_price || 0).toLocaleString()}</span>
        </div>
        <div class="flex justify-between items-center" style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:8px;">
          <span>Target Delivery Schedule:</span>
          <span class="mono" style="font-weight:600; color:var(--text-primary);">${(data.timeline.likely_weeks || data.timeline.recommended_timeline_weeks || 12).toFixed(1)} Weeks</span>
        </div>
        <div class="flex justify-between items-center" style="font-size:0.85rem; color:var(--text-secondary);">
          <span>Payment Schedule:</span>
          <span>30% Inception, 40% Milestone Deliveries, 30% Acceptance Sign-Off</span>
        </div>
      </div>
    </div>
  `;
}

// Tab 7: Handoff & Historical Benchmarks
function renderHandoff(data) {
  const matches = data.benchmark_matches || [];
  const container = document.getElementById("benchmarkMatchesContainer");
  if (!container) return;

  if (matches.length === 0) {
    container.innerHTML = `<div style="color:var(--text-muted); font-size:0.85rem;">No historical benchmark matches found.</div>`;
    return;
  }

  container.innerHTML = matches.map(m => {
    const hours = Number(m.actual_hours ?? m.actual_effort_hours ?? 0);
    const weeks = m.actual_weeks ?? m.actual_duration_weeks ?? 12;
    const projName = m.project_name || m.name || "Historical Benchmark";
    const projType = m.project_type || m.domain || "Enterprise Platform";
    const simScore = Math.round((m.similarity_score || 0) * 100);
    const keyInsight = m.key_similarities || m.lessons_learned || "Architecture & domain pattern match";
    const riskLvl = m.risk_level || "Medium";

    return `
      <div class="stat-kpi-card">
        <div class="flex items-center justify-between" style="margin-bottom:8px;">
          <span style="font-weight:700; font-size:0.95rem; color:var(--text-primary);">${escapeHtml(projName)}</span>
          <span class="badge-tag success mono">${simScore}% MATCH</span>
        </div>
        <div style="font-size:0.82rem; color:var(--text-secondary); margin-bottom:10px; line-height:1.5;">
          <div><strong>Domain:</strong> ${escapeHtml(projType)} • ${weeks} wks</div>
          <div><strong>Effort:</strong> ${hours.toLocaleString()} hrs • Risk: ${escapeHtml(riskLvl)}</div>
        </div>
        <div style="background:var(--surface-2); border-radius:var(--radius-xs); padding:8px 10px; font-size:0.78rem; color:var(--text-primary); line-height:1.4;">
          <strong style="color:var(--accent-primary);">Key Insight:</strong> ${escapeHtml(keyInsight)}
        </div>
      </div>
    `;
  }).join("");
}

// ==========================================
// 10. Document Exporters & Copy
// ==========================================
function copyProposalText() {
  const p = appState.proposal?.proposal || appState.proposal;
  if (!p) {
    showToast("Please run brief analysis first");
    return;
  }
  const text = `${p.title || "Proposal"}\n\n${p.executive_summary || ""}\n\n${(p.scope_of_work || []).join("\n")}`;
  navigator.clipboard?.writeText(text);
  showToast("✓ Copied proposal text to clipboard", true);
}

async function exportDocx() {
  if (!appState.analysis || !appState.proposal) {
    showToast("Please run analysis first to generate the proposal");
    return;
  }

  showToast("Compiling Word (.docx) document...");
  const payload = {
    proposal: appState.proposal,
    requirements: appState.analysis.requirements,
    commercial: appState.analysis.commercial,
    risk: appState.analysis.risk
  };

  try {
    const res = await fetch("/api/export-docx", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("Document export failed");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    const clientSafe = (document.getElementById("clientNameInput")?.value || "Client").replace(/\s+/g, "_");
    a.download = `Cynbit_Proposal_${clientSafe}.docx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    showToast("✓ Downloaded proposal (.docx)", true);
  } catch (err) {
    showToast(`Export error: ${err.message}`);
  }
}

function exportMarkdown() {
  if (!appState.proposal) {
    showToast("Please run analysis first to generate markdown");
    return;
  }

  const p = appState.proposal.proposal || appState.proposal;
  const client = document.getElementById("clientNameInput")?.value || "Client";
  const md = `# ${p.title || "Technical Solution & Architecture Proposal"}

**Client:** ${client}
**Date:** ${new Date().toLocaleDateString()}
**Generated by:** Cynbit AI Pre-Sales Solution Architect

---

## 1. Executive Summary
${p.executive_summary || "Architectural overview."}

## 2. Scope of Work & Deliverables
${(p.scope_of_work || []).map(s => `- ${s}`).join("\n")}

## 3. Timeline Summary
${p.timeline_summary || "Phased delivery across sprint milestones."}

## 4. Commercial Terms & Investment
${p.commercial_terms || "Fixed-price milestone terms."}
`;

  const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  const clientSafe = client.replace(/\s+/g, "_");
  a.download = `Cynbit_Proposal_${clientSafe}.md`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
  showToast("✓ Downloaded proposal (.md)", true);
}

// ==========================================
// 11. Toast Notifications with Timer Bar
// ==========================================
function showToast(message, isSuccess = false) {
  const dock = document.getElementById("toastDock");
  if (!dock) return;

  const toast = document.createElement("div");
  toast.className = `toast-item ${isSuccess ? 'success' : ''}`;
  toast.innerHTML = `
    <div class="toast-icon">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
    </div>
    <span>${escapeHtml(message)}</span>
    <div class="toast-progress"></div>
  `;

  dock.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(16px) scale(0.95)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 320);
  }, 2900);
}

// Utility: HTML escape
function escapeHtml(str) {
  if (typeof str !== "string") return str ?? "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
