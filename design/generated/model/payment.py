from __future__ import annotations



class Payment:

    def __init__(self, payment_id: str | None = None, order_id: str | None = None, attempt_ref: str | None = None, amount: float | None = None, currency: str | None = None, status: str | None = None, provider_ref: str | None = None, created_at: str | None = None) -> None:
        self.payment_id: str | None = payment_id
        self.order_id: str | None = order_id
        self.attempt_ref: str | None = attempt_ref
        self.amount: float | None = amount
        self.currency: str | None = currency
        self.status: str | None = status
        self.provider_ref: str | None = provider_ref
        self.created_at: str | None = created_at

    def matches(self, attempt_ref: str, amount: float, currency: str) -> bool:
        raise NotImplementedError

    def is_final(self) -> bool:
        raise NotImplementedError
