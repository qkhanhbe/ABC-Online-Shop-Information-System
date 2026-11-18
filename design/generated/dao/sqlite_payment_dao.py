from __future__ import annotations

from .payment_dao import PaymentDAO


class SqlitePaymentDAO(PaymentDAO):

    def get_by_attempt(self, attempt_ref: str) -> Payment:
        raise NotImplementedError

    def for_order(self, order_id: str) -> list[Payment]:
        raise NotImplementedError

    def save_payment(self, p: Payment) -> Payment:
        raise NotImplementedError
