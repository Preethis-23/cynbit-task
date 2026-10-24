import docx
from docx.shared import Inches, Pt, RGBColor
from pathlib import Path

def create_sample_rfp_docx():
    doc = docx.Document()
    
    # Title
    title = doc.add_heading('REQUEST FOR PROPOSAL (RFP)', level=0)
    title.runs[0].font.size = Pt(22)
    title.runs[0].font.color.rgb = RGBColor(18, 18, 16)
    
    p_sub = doc.add_paragraph('Project: Global Fleet Telematics & AI Dispatch Optimization Platform')
    p_sub.runs[0].font.bold = True
    p_sub.runs[0].font.size = Pt(13)
    p_sub.runs[0].font.color.rgb = RGBColor(79, 70, 229)
    
    p_meta = doc.add_paragraph('Issuing Client: TransFleet Logistics International\nTarget Release: Enterprise Cloud Migration Q3\nCompliance Target: SOC2 Type II, FMCSA ELD, GDPR')
    p_meta.runs[0].font.size = Pt(10)
    p_meta.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    doc.add_heading('1. Executive Overview', level=1)
    doc.add_paragraph(
        "TransFleet Logistics operates an interstate fleet of 750 Class-8 heavy transport vehicles across 32 regional distribution centers. "
        "Our existing dispatch planning relies on legacy monolithic on-premises software that struggles with real-time routing adjustments, "
        "resulting in elevated fuel consumption, driver scheduling bottlenecks, and unpredictable delivery ETAs."
    )
    doc.add_paragraph(
        "We are soliciting proposals to engineer a cloud-native, high-throughput Fleet Telematics and Predictive Dispatch Optimization Platform. "
        "The objective is to ingest high-frequency IoT sensor telemetry, predict delivery arrivals with sub-15-minute accuracy, "
        "and automate dispatch route recalculations to lower total fleet fuel burn by at least 14%."
    )

    doc.add_heading('2. Scope of Work & Functional Modules', level=1)
    modules = [
        ("FR-01: High-Throughput Telemetry Ingestion", "Stream GPS coordinates, engine diagnostics (OBD-II/CAN bus), fuel flow, and tire pressure from 750 vehicles at 10-second intervals via MQTT/Kafka broker cluster."),
        ("FR-02: Predictive AI/ML ETA Engine", "Machine learning microservice utilizing historical highway congestion, weather radar feeds, and telematics to output dynamic destination ETAs with target 96% accuracy."),
        ("FR-03: Real-Time Dynamic Route Dispatcher", "Graph-based route recalculation engine that automatically suggests alternate corridors when delays exceed 20 minutes, prioritizing toll versus fuel tradeoffs."),
        ("FR-04: Driver Mobile Companion App", "Offline-first cross-platform mobile application (iOS & Android) with turn-by-turn commercial navigation, dispatch acknowledgement, and Hours-of-Service (HOS) driver logs."),
        ("FR-05: Central Dispatcher Operations Console", "Responsive web portal for fleet managers featuring interactive geospatial map visualization, geofencing breach alerts, and real-time fleet health metrics."),
        ("FR-06: Maintenance Prediction & Diagnostics", "Rule-based and anomaly detection module flagging early transmission, brake, and coolant anomalies to prevent roadside breakdowns.")
    ]
    for m_id, desc in modules:
        p = doc.add_paragraph()
        run_title = p.add_run(f"• {m_id}: ")
        run_title.bold = True
        p.add_run(desc)

    doc.add_heading('3. Non-Functional SLAs & Technical Constraints', level=1)
    nfrs = [
        ("Throughput & Concurrency", "System must continuously ingest and persist 15,000 telemetry events/sec with p99 ingest latency under 120ms."),
        ("Availability & Resiliency", "High availability architecture with target 99.99% uptime and active-passive multi-region failover on AWS."),
        ("Security & Compliance", "Mandatory compliance with SOC2 Type II, FMCSA ELD electronic logging mandate, and end-to-end mTLS sensor authentication."),
        ("Hardware & Third-Party Integration", "Bi-directional integration with Geotab ELD hardware, Google Maps Platform enterprise fleet API, and SAP ERP dispatch ledger.")
    ]
    for nfr_title, desc in nfrs:
        p = doc.add_paragraph()
        r = p.add_run(f"• {nfr_title}: ")
        r.bold = True
        p.add_run(desc)

    doc.add_heading('4. Commercial Terms & Timeline Guidance', level=1)
    doc.add_paragraph(
        "Client Budget Estimate: $520,000 – $680,000 total professional services for Phase 1 MVP.\n"
        "Delivery Milestone Target: 24 Calendar Weeks from contract execution.\n"
        "Proposals must include discipline effort breakdown, technical architecture blueprints, identified delivery risks, and commercial milestone schedules."
    )

    out_path = Path("data/sample_briefs/global_logistics_digital_twin_rfp.docx")
    doc.save(out_path)
    print(f"Created DOCX: {out_path} ({out_path.stat().st_size} bytes)")

    # Also save as plain text for easy viewing/copying
    txt_path = Path("data/sample_briefs/global_logistics_digital_twin_rfp.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(
            "Client: TransFleet Logistics International\n"
            "Project: Global Fleet Telematics & AI Dispatch Optimization Platform\n\n"
            "Overview:\n"
            "TransFleet Logistics operates 750 Class-8 semi-trucks across 32 distribution hubs. "
            "Need cloud-native IoT telematics and AI route dispatch platform to reduce fuel burn by 14% and predict delivery ETAs with 96% accuracy.\n\n"
            "Functional Modules:\n"
            "- FR-01: Real-time MQTT/Kafka telemetry ingestion for 750 trucks (15,000 events/sec).\n"
            "- FR-02: Machine learning dynamic ETA model (<15min accuracy window).\n"
            "- FR-03: Dynamic route recalculation engine with toll/fuel optimization.\n"
            "- FR-04: Offline-first mobile app (iOS/Android) for commercial drivers with HOS logs.\n"
            "- FR-05: Web operations dispatch console with live geospatial map and geofence alerts.\n"
            "- FR-06: Predictive maintenance diagnostics for engine and brake health.\n\n"
            "Integrations:\n"
            "- Geotab ELD telematics hardware, SAP ERP billing, Google Maps Fleet API, AWS IoT Core.\n\n"
            "Non-Functional & Compliance:\n"
            "- SOC2 Type II, FMCSA ELD compliance, 99.99% availability, <120ms p99 ingest latency.\n\n"
            "Commercial Constraints:\n"
            "- Target budget: $520,000 - $680,000. Target timeline: 24 weeks."
        )
    print(f"Created TXT: {txt_path} ({txt_path.stat().st_size} bytes)")

if __name__ == "__main__":
    create_sample_rfp_docx()
