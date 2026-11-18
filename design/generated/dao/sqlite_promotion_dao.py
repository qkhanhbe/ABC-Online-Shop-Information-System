from __future__ import annotations

from .promotion_dao import PromotionDAO


class SqlitePromotionDAO(PromotionDAO):

    def get_promotion(self, code: str) -> Promotion:
        raise NotImplementedError

    def save_promotion(self, p: Promotion) -> Promotion:
        raise NotImplementedError

    def list_promotions(self) -> list[Promotion]:
        raise NotImplementedError
