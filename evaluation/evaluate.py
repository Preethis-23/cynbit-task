"""
Evaluation and Validation Runner for Phase 6.
Evaluates extraction accuracy, risk classification, and effort estimation error.
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, Any

# Ensure project root in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluation.dataset import EVALUATION_CASES
from src.ai.llm_client import LLMClient
from src.engine.rules import RiskEngine
from src.engine.formulas import EstimationEngine
from src.engine.ml_model import ProjectMLModel


def run_evaluation() -> Dict[str, Any]:
    print("=" * 70)
    print("CYNBIT PRE-SALES SOLUTION ARCHITECT - SYSTEM EVALUATION RUNNER")
    print("=" * 70)

    client = LLMClient()
    ml_model = ProjectMLModel()

    total_cases = len(EVALUATION_CASES)
    ai_correct = 0
    mobile_correct = 0
    risk_correct = 0
    effort_in_range_count = 0
    ml_effort_errors = []
    case_results = []

    start_total = time.time()

    for idx, case in enumerate(EVALUATION_CASES, 1):
        t0 = time.time()
        brief = case["brief"]
        analysis, engine_used = client.extract_requirements(brief)
        risk = RiskEngine.evaluate(analysis)
        effort = EstimationEngine.calculate_effort(analysis, risk)
        ml_res = ml_model.predict(analysis)
        latency = round(time.time() - t0, 3)

        # Check AI extraction
        ai_match = (analysis.has_ai_features == case["expected_has_ai"])
        if ai_match:
            ai_correct += 1

        # Check Mobile extraction
        has_mobile = analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android
        mobile_match = (has_mobile == case["expected_has_mobile"])
        if mobile_match:
            mobile_correct += 1

        # Check Risk classification
        risk_match = (risk.risk_level == case["expected_risk"])
        if risk_match:
            risk_correct += 1

        # Check Rule-based effort in expected range
        g_min, g_max = case["ground_truth_hours_range"]
        in_range = (g_min <= effort.likely_hours <= g_max)
        if in_range:
            effort_in_range_count += 1

        # ML error
        mid_ground = (g_min + g_max) / 2.0
        ml_hrs = ml_res["predicted_hours"] or effort.likely_hours
        ml_err = abs(ml_hrs - mid_ground)
        ml_effort_errors.append(ml_err)

        case_res = {
            "id": case["id"],
            "domain": case["domain"],
            "ai_detected": analysis.has_ai_features,
            "ai_correct": ai_match,
            "mobile_detected": has_mobile,
            "mobile_correct": mobile_match,
            "rule_risk": risk.risk_level,
            "expected_risk": case["expected_risk"],
            "risk_correct": risk_match,
            "rule_hours": effort.likely_hours,
            "ml_predicted_hours": ml_hrs,
            "expected_range": f"{g_min}-{g_max}h",
            "in_range": in_range,
            "missing_gaps_count": len(analysis.missing_information),
            "latency_sec": latency,
        }
        case_results.append(case_res)

        print(f"[{case['id']}] {case['domain']:<32} | Risk: {risk.risk_level} (Exp: {case['expected_risk']}) "
              f"| Rule: {effort.likely_hours:.0f}h | ML: {ml_hrs:.0f}h | Gaps: {len(analysis.missing_information)}")

    total_latency = round(time.time() - start_total, 2)
    ai_acc = round((ai_correct / total_cases) * 100, 1)
    mob_acc = round((mobile_correct / total_cases) * 100, 1)
    risk_acc = round((risk_correct / total_cases) * 100, 1)
    effort_range_acc = round((effort_in_range_count / total_cases) * 100, 1)
    ml_mae = round(sum(ml_effort_errors) / len(ml_effort_errors), 1)

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY METRICS")
    print("=" * 70)
    print(f"Total Test Cases:                    {total_cases}")
    print(f"AI Feature Detection Accuracy:       {ai_acc}%")
    print(f"Platform (Mobile) Scope Accuracy:    {mob_acc}%")
    print(f"Risk Classification Accuracy:        {risk_acc}%")
    print(f"Rule-Based Effort in Range:          {effort_range_acc}%")
    print(f"ML Model Mean Absolute Error (MAE):  {ml_mae} hours")
    print(f"Total Evaluation Latency:            {total_latency}s (Avg: {total_latency/total_cases:.2f}s/case)")
    print("=" * 70)

    summary = {
        "total_cases": total_cases,
        "ai_accuracy_pct": ai_acc,
        "mobile_accuracy_pct": mob_acc,
        "risk_accuracy_pct": risk_acc,
        "effort_in_range_pct": effort_range_acc,
        "ml_mae_hours": ml_mae,
        "total_latency_seconds": total_latency,
        "cases": case_results,
    }

    out_file = Path("evaluation/evaluation_results.json")
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved evaluation metrics to {out_file}")

    return summary


if __name__ == "__main__":
    run_evaluation()
