from __future__ import annotations



class InventoryEvent:

    def __init__(self, event_id: str | None = None, product_id: str | None = None, kind: str | None = None, quantity: int | None = None, reference: str | None = None, reason: str | None = None, created_at: str | None = None) -> None:
        self.event_id: str | None = event_id
        self.product_id: str | None = product_id
        self.kind: str | None = kind
        self.quantity: int | None = quantity
        self.reference: str | None = reference
        self.reason: str | None = reason
        self.created_at: str | None = created_at
