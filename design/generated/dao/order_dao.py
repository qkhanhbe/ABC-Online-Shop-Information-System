from __future__ import annotations

from abc import ABC, abstractmethod


class OrderDAO(ABC):

    @abstractmethod
    def get_order(self, order_id: str) -> Order:
        raise NotImplementedError

    @abstractmethod
    def find_by_idempotency_key(self, key: str) -> Order:
        raise NotImplementedError

    @abstractmethod
    def find_by_customer(self, customer_id: str) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    def save_order(self, order: Order) -> Order:
        raise NotImplementedError

    @abstractmethod
    def list_orders(self) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    def find_by_status(self, statuses: list[str]) -> list[Order]:
        raise NotImplementedError
