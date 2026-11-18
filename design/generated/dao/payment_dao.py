from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentDAO(ABC):

    @abstractmethod
    def get_by_attempt(self, attempt_ref: str) -> Payment:
        raise NotImplementedError

    @abstractmethod
    def for_order(self, order_id: str) -> list[Payment]:
        raise NotImplementedError

    @abstractmethod
    def save_payment(self, payment: Payment) -> Payment:
        raise NotImplementedError
