from __future__ import annotations



class ReplenishmentRequest:

    def __init__(self, request_id: str | None = None, product_id: str | None = None, quantity: int | None = None, status: str | None = None, created_at: str | None = None) -> None:
        self.request_id: str | None = request_id
        self.product_id: str | None = product_id
        self.quantity: int | None = quantity
        self.status: str | None = status
        self.created_at: str | None = created_at
