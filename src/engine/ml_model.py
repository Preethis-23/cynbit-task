"""
Proof-of-Concept Machine Learning Engine.
Trains and serves Random Forest models on synthetic project data for:
1. Effort prediction (RandomForestRegressor)
2. Risk classification (RandomForestClassifier)

NOTE: Explicitly labeled as a proof-of-concept demonstration model trained on synthetic data.
Production deployment requires verified historical estimation vs. actual delivery logs.
"""

from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, classification_report

from src.schemas.requirements import RequirementAnalysis


class ProjectMLModel:
    """Random Forest demonstration model for effort and risk estimation."""

    def __init__(self, models_dir: str = "models", data_path: str = "data/synthetic_projects.csv"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.data_path = Path(data_path)

        self.effort_model_path = self.models_dir / "rf_effort_model.joblib"
        self.risk_model_path = self.models_dir / "rf_risk_model.joblib"
        self.metrics_path = self.models_dir / "model_metrics.joblib"

        self.effort_model: Optional[RandomForestRegressor] = None
        self.risk_model: Optional[RandomForestClassifier] = None
        self.metrics: Dict[str, Any] = {}

        self._load_or_train()

    @staticmethod
    def extract_features_from_analysis(analysis: RequirementAnalysis) -> list[float]:
        """Maps RequirementAnalysis object into model feature vector."""
        features_count = float(len(analysis.functional_requirements))
        integrations_count = float(len(analysis.integrations))
        has_ai = 1.0 if analysis.has_ai_features else 0.0
        has_web = 1.0 if analysis.platform_scope.web else 0.0
        has_mobile = 1.0 if (analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android) else 0.0
        user_roles_count = float(len(analysis.user_roles)) or 2.0

        # Compliance indicator
        nfr_text = " ".join([n.description for n in analysis.non_functional_requirements]).lower()
        high_compliance = 1.0 if any(k in nfr_text for k in ["hipaa", "pci", "soc2", "gdpr"]) else 0.0

        return [
            features_count,
            integrations_count,
            has_ai,
            has_web,
            has_mobile,
            user_roles_count,
            high_compliance,
        ]

    def _prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Extracts X, y_effort, y_risk from synthetic CSV."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Synthetic dataset not found at {self.data_path}")

        df = pd.read_csv(self.data_path)

        X_rows = []
        for _, row in df.iterrows():
            features_count = float(row.get("features_count", 10))
            integrations_count = float(row.get("integrations_count", 2))
            has_ai = 1.0 if row.get("has_ai") else 0.0

            plat = str(row.get("platforms", ""))
            has_web = 1.0 if "Web" in plat else 0.0
            has_mobile = 1.0 if "Mobile" in plat else 0.0

            user_roles = float(row.get("user_roles_count", 2))
            comp = str(row.get("compliance_standard", "Standard"))
            high_compliance = 1.0 if comp in ["HIPAA", "PCI-DSS Level 1", "SOC2"] else 0.0

            X_rows.append([
                features_count,
                integrations_count,
                has_ai,
                has_web,
                has_mobile,
                user_roles,
                high_compliance,
            ])

        X = np.array(X_rows, dtype=np.float64)
        y_effort = np.array(df["actual_hours"].tolist(), dtype=np.float64)
        y_risk = np.array(df["risk_level"].tolist(), dtype=object)

        return X, y_effort, y_risk

    def train(self) -> Dict[str, Any]:
        """Trains RandomForestRegressor and RandomForestClassifier on synthetic dataset."""
        X, y_effort, y_risk = self._prepare_training_data()

        # Split 80/20 train/test
        X_train, X_test, y_eff_train, y_eff_test, y_risk_train, y_risk_test = train_test_split(
            X, y_effort, y_risk, test_size=0.2, random_state=42
        )

        # 1. Effort Regressor
        self.effort_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=6,
            random_state=42,
        )
        self.effort_model.fit(X_train, y_eff_train)
        eff_preds = self.effort_model.predict(X_test)
        mae = float(mean_absolute_error(y_eff_test, eff_preds))
        r2 = float(r2_score(y_eff_test, eff_preds))

        # 2. Risk Classifier
        self.risk_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42,
        )
        self.risk_model.fit(X_train, y_risk_train)
        risk_preds = self.risk_model.predict(X_test)
        acc = float(accuracy_score(y_risk_test, risk_preds))

        # Save artifacts
        joblib.dump(self.effort_model, self.effort_model_path)
        joblib.dump(self.risk_model, self.risk_model_path)

        feature_names = [
            "Feature Count",
            "Integrations Count",
            "Has AI/ML",
            "Has Web",
            "Has Mobile",
            "User Roles Count",
            "High Compliance",
        ]
        importances = {name: round(float(imp), 3) for name, imp in zip(feature_names, self.effort_model.feature_importances_)}

        self.metrics = {
            "effort_mae_hours": round(mae, 1),
            "effort_r2_score": round(r2, 3),
            "risk_accuracy": round(acc * 100, 1),
            "feature_importances": importances,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
        }
        joblib.dump(self.metrics, self.metrics_path)

        return self.metrics

    def _load_or_train(self):
        """Loads saved models from disk, or trains if missing."""
        if self.effort_model_path.exists() and self.risk_model_path.exists() and self.metrics_path.exists():
            try:
                self.effort_model = joblib.load(self.effort_model_path)
                self.risk_model = joblib.load(self.risk_model_path)
                self.metrics = joblib.load(self.metrics_path)
                return
            except Exception:
                pass

        # Train if files not found
        if self.data_path.exists():
            self.train()

    def predict(self, analysis: RequirementAnalysis) -> Dict[str, Any]:
        """Predicts effort hours and risk classification from a requirement analysis."""
        if self.effort_model is None or self.risk_model is None:
            self._load_or_train()
            if self.effort_model is None or self.risk_model is None:
                return {"predicted_hours": None, "predicted_risk": None}

        features = np.array([self.extract_features_from_analysis(analysis)])
        predicted_hours = float(self.effort_model.predict(features)[0])
        predicted_risk = str(self.risk_model.predict(features)[0])

        return {
            "predicted_hours": round(predicted_hours, 1),
            "predicted_risk": predicted_risk,
            "metrics": self.metrics,
            "disclaimer": "Trained on synthetic proof-of-concept dataset. For advisory reference only.",
        }
