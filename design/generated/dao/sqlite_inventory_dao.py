from __future__ import annotations

from .inventory_dao import InventoryDAO


class SqliteInventoryDAO(InventoryDAO):

    def get_stock(self, product_id: str) -> StockLevel:
        raise NotImplementedError

    def save_stock(self, s: StockLevel) -> StockLevel:
        raise NotImplementedError

    def find_event(self, product_id: str, kind: str, reference: str) -> InventoryEvent:
        raise NotImplementedError

    def add_event(self, e: InventoryEvent) -> InventoryEvent:
        raise NotImplementedError

    def events_for(self, product_id: str, limit: int) -> list[InventoryEvent]:
        raise NotImplementedError

    def open_replenishments(self) -> list[ReplenishmentRequest]:
        raise NotImplementedError

    def add_replenishment(self, request: ReplenishmentRequest) -> ReplenishmentRequest:
        raise NotImplementedError
