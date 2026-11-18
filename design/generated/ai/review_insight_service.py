from __future__ import annotations



class ReviewInsightService:

    def is_noise(self, text: str) -> bool:
        raise NotImplementedError

    def split_clauses(self, text: str) -> list[str]:
        raise NotImplementedError

    def classify_clause(self, clause: str) -> Map:
        raise NotImplementedError

    def analyse_review(self, text: str, rating: int) -> Map:
        raise NotImplementedError

    def analyse(self, reviews: list[Review]) -> Map:
        raise NotImplementedError

    def label(self, aspects: Map, used: int) -> str:
        raise NotImplementedError
