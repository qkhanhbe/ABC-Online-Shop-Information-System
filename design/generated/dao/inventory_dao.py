from __future__ import annotations

from abc import ABC, abstractmethod


class InventoryDAO(ABC):

    @abstractmethod
    def get_stock(self, product_id: str) -> StockLevel:
        raise NotImplementedError

    @abstractmethod
    def save_stock(self, stock: StockLevel) -> StockLevel:
        raise NotImplementedError

    @abstractmethod
    def find_event(self, product_id: str, kind: str, reference: str) -> InventoryEvent:
        raise NotImplementedError

    @abstractmethod
    def add_event(self, event: InventoryEvent) -> InventoryEvent:
        raise NotImplementedError

    @abstractmethod
    def events_for(self, product_id: str, limit: int) -> list[InventoryEvent]:
        raise NotImplementedError

    @abstractmethod
    def open_replenishments(self) -> list[ReplenishmentRequest]:
        raise NotImplementedError

    @abstractmethod
    def add_replenishment(self, request: ReplenishmentRequest) -> ReplenishmentRequest:
        raise NotImplementedError
