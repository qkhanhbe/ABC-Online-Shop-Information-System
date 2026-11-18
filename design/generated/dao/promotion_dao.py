from __future__ import annotations

from abc import ABC, abstractmethod


class PromotionDAO(ABC):

    @abstractmethod
    def get_promotion(self, code: str) -> Promotion:
        raise NotImplementedError

    @abstractmethod
    def save_promotion(self, promotion: Promotion) -> Promotion:
        raise NotImplementedError

    @abstractmethod
    def list_promotions(self) -> list[Promotion]:
        raise NotImplementedError
