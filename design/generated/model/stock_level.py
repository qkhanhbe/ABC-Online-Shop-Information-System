from __future__ import annotations



class StockLevel:

    def __init__(self, product_id: str | None = None, physical: int | None = None, reserved: int | None = None, threshold: int | None = None) -> None:
        self.product_id: str | None = product_id
        self.physical: int | None = physical
        self.reserved: int | None = reserved
        self.threshold: int | None = threshold

    def available(self) -> int:
        raise NotImplementedError

    def is_low(self) -> bool:
        raise NotImplementedError

    def apply(self, event: InventoryEvent) -> None:
        raise NotImplementedError
