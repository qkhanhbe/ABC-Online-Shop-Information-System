from __future__ import annotations



class RankingService:

    def business_score(self, available: int) -> float:
        raise NotImplementedError

    def weights(self, query: Map) -> list[float]:
        raise NotImplementedError

    def rank(self, candidates: list[Map], query: Map, k: int) -> list[Map]:
        raise NotImplementedError
