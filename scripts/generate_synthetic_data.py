"""
Generator for synthetic historical IT project dataset.
Creates realistic project records for benchmark similarity matching and Random Forest ML training.
Clearly labeled as synthetic data for proof-of-concept purposes.
"""

import random
import pandas as pd
from pathlib import Path

# Seed for reproducibility
random.seed(42)

PROJECT_TYPES = [
    "E-Commerce & Retail",
    "Healthcare & Telemedicine",
    "Fintech & Payments",
    "SaaS B2B Platform",
    "Logistics & Supply Chain",
    "EdTech & Learning Management",
    "On-Demand Marketplace",
    "IoT & Real-time Telemetry",
]

PLATFORMS_OPTIONS = [
    "Web Only",
    "Mobile Only",
    "Web + Mobile",
    "Web + Mobile + Admin",
]

COMPLIANCE_OPTIONS = ["Standard", "GDPR/CCPA", "HIPAA", "PCI-DSS Level 1", "SOC2"]

TECH_STACKS = [
    "Next.js / FastAPI / PostgreSQL / AWS",
    "React Native / Node.js / MongoDB / GCP",
    "React / Django / PostgreSQL / AWS",
    "Flutter / Go / PostgreSQL / Azure",
    "Next.js / Spring Boot / MySQL / AWS",
    "Vue.js / FastAPI / PostgreSQL / Docker",
]

def generate_record(i: int) -> dict:
    ptype = random.choice(PROJECT_TYPES)
    platforms = random.choice(PLATFORMS_OPTIONS)
    compliance = random.choice(COMPLIANCE_OPTIONS)
    tech = random.choice(TECH_STACKS)
    
    # Feature count depends partly on project type
    base_features = {
        "E-Commerce & Retail": random.randint(10, 22),
        "Healthcare & Telemedicine": random.randint(12, 24),
        "Fintech & Payments": random.randint(12, 26),
        "SaaS B2B Platform": random.randint(8, 20),
        "Logistics & Supply Chain": random.randint(10, 22),
        "EdTech & Learning Management": random.randint(7, 16),
        "On-Demand Marketplace": random.randint(12, 25),
        "IoT & Real-time Telemetry": random.randint(9, 18),
    }[ptype]
    
    integrations = random.randint(1, 6)
    has_ai = random.choice([True, False, False, True, False])
    user_roles = random.randint(2, 5)
    
    # Calculate base effort based on realistic industry rules
    feature_effort = base_features * random.uniform(42, 58)
    platform_multiplier = 1.0
    if platforms == "Web + Mobile":
        platform_multiplier = 1.45
    elif platforms == "Web + Mobile + Admin":
        platform_multiplier = 1.65
    elif platforms == "Mobile Only":
        platform_multiplier = 1.2
        
    integration_effort = integrations * random.uniform(35, 60)
    ai_effort = (random.uniform(120, 260)) if has_ai else 0.0
    compliance_multiplier = 1.25 if compliance in ["HIPAA", "PCI-DSS Level 1", "SOC2"] else 1.0
    
    base_hours = (feature_effort * platform_multiplier + integration_effort + ai_effort) * compliance_multiplier
    # Add natural variance
    actual_hours = round(base_hours * random.uniform(0.92, 1.12), 1)
    
    # Timeline in weeks: assuming team of 3-5 engineers (approx 120-160 effective hours/wk)
    team_capacity_per_week = random.uniform(100, 150)
    actual_weeks = max(6.0, round(actual_hours / team_capacity_per_week, 1))
    
    # Determine risk score and level
    risk_points = 0
    if integrations > 2:
        risk_points += 2
    if "Mobile" in platforms and "Web" in platforms:
        risk_points += 2
    if has_ai:
        risk_points += 2
    if compliance in ["HIPAA", "PCI-DSS Level 1"]:
        risk_points += 2
    if base_features > 16:
        risk_points += 2
        
    if risk_points >= 6:
        risk_level = "High"
    elif risk_points >= 3:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    # Complexity
    if actual_hours > 1200 or risk_points >= 6:
        complexity = "High"
    elif actual_hours > 650 or risk_points >= 3:
        complexity = "Medium"
    else:
        complexity = "Low"
        
    brief_summary = f"{ptype} system with {base_features} core features across {platforms}. " \
                    f"Includes {integrations} third-party integrations, {compliance} compliance standards. " \
                    f"{'Includes AI/ML capabilities. ' if has_ai else ''}" \
                    f"Built with {tech}."

    return {
        "project_id": f"CYN-SYNTH-{i:03d}",
        "project_name": f"{ptype} Solution {i}",
        "project_type": ptype,
        "features_count": base_features,
        "platforms": platforms,
        "integrations_count": integrations,
        "has_ai": has_ai,
        "user_roles_count": user_roles,
        "compliance_standard": compliance,
        "tech_stack": tech,
        "actual_hours": actual_hours,
        "actual_weeks": actual_weeks,
        "risk_level": risk_level,
        "complexity_level": complexity,
        "brief_summary": brief_summary,
    }

def main():
    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    records = [generate_record(i) for i in range(1, 161)]
    df = pd.DataFrame(records)
    
    csv_path = out_dir / "synthetic_projects.csv"
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} synthetic project records to {csv_path}")

if __name__ == "__main__":
    main()
