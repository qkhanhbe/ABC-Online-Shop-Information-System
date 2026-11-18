from __future__ import annotations

from .review_dao import ReviewDAO


class SqliteReviewDAO(ReviewDAO):

    def for_product(self, product_id: str, status: str) -> list[Review]:
        raise NotImplementedError

    def exists(self, customer_id: str, product_id: str, order_id: str) -> bool:
        raise NotImplementedError

    def save_review(self, r: Review) -> Review:
        raise NotImplementedError

    def list_reviews(self, status: str) -> list[Review]:
        raise NotImplementedError
