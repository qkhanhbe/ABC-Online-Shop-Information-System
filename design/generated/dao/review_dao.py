from __future__ import annotations

from abc import ABC, abstractmethod


class ReviewDAO(ABC):

    @abstractmethod
    def for_product(self, product_id: str, status: str) -> list[Review]:
        raise NotImplementedError

    @abstractmethod
    def exists(self, customer_id: str, product_id: str, order_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save_review(self, review: Review) -> Review:
        raise NotImplementedError

    @abstractmethod
    def list_reviews(self, status: str) -> list[Review]:
        raise NotImplementedError
