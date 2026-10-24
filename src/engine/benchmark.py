"""
Benchmark Project Similarity Engine.
Compares a new client project brief against synthetic historical project records
using TF-IDF and cosine similarity embeddings.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.schemas.requirements import RequirementAnalysis
from src.schemas.project_state import BenchmarkMatch


class BenchmarkSimilarityEngine:
    """Finds most similar past projects from the historical synthetic database."""

    def __init__(self, data_path: Optional[str] = None):
        self.csv_path = Path(data_path or "data/synthetic_projects.csv")
        self.df: Optional[pd.DataFrame] = None
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self._load_and_index()

    def _load_and_index(self):
        """Loads CSV and indexes corpus text."""
        if not self.csv_path.exists():
            return

        self.df = pd.read_csv(self.csv_path)
        # Create rich text representation for embedding similarity
        corpus = []
        for _, row in self.df.iterrows():
            text = (
                f"{row.get('project_type', '')} {row.get('brief_summary', '')} "
                f"{row.get('tech_stack', '')} {row.get('platforms', '')} "
                f"Features: {row.get('features_count', '')} AI: {row.get('has_ai', '')}"
            )
            corpus.append(text)

        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def find_similar(
        self,
        analysis: RequirementAnalysis,
        top_k: int = 3,
    ) -> list[BenchmarkMatch]:
        """Finds top-k closest historical projects."""
        if self.df is None or self.vectorizer is None or self.tfidf_matrix is None:
            self._load_and_index()
            if self.df is None:
                return []

        # Construct query representation from requirement analysis
        platforms = []
        if analysis.platform_scope.web:
            platforms.append("Web")
        if analysis.platform_scope.mobile_ios or analysis.platform_scope.mobile_android:
            platforms.append("Mobile")
        if analysis.platform_scope.admin_portal:
            platforms.append("Admin")
        platform_str = " + ".join(platforms)

        query_text = (
            f"{analysis.project_name} {analysis.business_objective} "
            f"{platform_str} AI: {analysis.has_ai_features} "
            f"Integrations: {len(analysis.integrations)} "
            f"{' '.join([f.title for f in analysis.functional_requirements[:6]])} "
            f"{analysis.tech_recommendation.backend} {analysis.tech_recommendation.frontend}"
        )

        query_vec = self.vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        top_indices = similarities.argsort()[::-1][:top_k]

        matches: list[BenchmarkMatch] = []
        for idx in top_indices:
            score = float(similarities[idx])
            row = self.df.iloc[idx]

            # Key similarities description
            common_elements = []
            if row.get("has_ai") == analysis.has_ai_features:
                common_elements.append("AI/ML scope match")
            if str(row.get("platforms")).lower() in platform_str.lower() or platform_str.lower() in str(row.get("platforms")).lower():
                common_elements.append("Platform architecture match")
            if abs(row.get("features_count", 0) - len(analysis.functional_requirements)) <= 3:
                common_elements.append("Similar feature volume")

            key_sim = ", ".join(common_elements) if common_elements else "Architectural and domain pattern match"

            matches.append(
                BenchmarkMatch(
                    project_id=str(row.get("project_id", "CYN-000")),
                    project_name=str(row.get("project_name", "Historical Project")),
                    project_type=str(row.get("project_type", "Digital Platform")),
                    similarity_score=round(score, 3),
                    actual_hours=float(row.get("actual_hours", 0.0)),
                    actual_weeks=float(row.get("actual_weeks", 0.0)),
                    risk_level=str(row.get("risk_level", "Medium")),
                    tech_stack=str(row.get("tech_stack", "Standard Stack")),
                    key_similarities=key_sim,
                )
            )

        return matches
