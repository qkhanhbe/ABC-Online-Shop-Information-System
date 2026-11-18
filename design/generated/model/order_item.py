from __future__ import annotations



class OrderItem:

    def __init__(self, product_id: str | None = None, name: str | None = None, unit_price: float | None = None, quantity: int | None = None) -> None:
        self.product_id: str | None = product_id
        self.name: str | None = name
        self.unit_price: float | None = unit_price
        self.quantity: int | None = quantity

    def sub_total(self) -> float:
        raise NotImplementedError
