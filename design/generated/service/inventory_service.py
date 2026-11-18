from __future__ import annotations



class InventoryService:

    def record(self, product_id: str, kind: str, quantity: int, reference: str, reason: str, actor: str) -> InventoryEvent:
        raise NotImplementedError

    def manual_event(self, staff: User, product_id: str, kind: str, quantity: int, reference: str, reason: str) -> InventoryEvent:
        raise NotImplementedError

    def reserve_order(self, order: Order) -> None:
        raise NotImplementedError

    def release_order(self, order: Order) -> None:
        raise NotImplementedError

    def issue_order(self, order: Order) -> None:
        raise NotImplementedError

    def is_reserved(self, product_id: str, order_id: str) -> bool:
        raise NotImplementedError

    def low_stock(self) -> list[Map]:
        raise NotImplementedError

    def request_replenishment(self, staff: User, product_id: str, quantity: int) -> ReplenishmentRequest:
        raise NotImplementedError

    def stock_of(self, product_id: str) -> StockLevel:
        raise NotImplementedError
