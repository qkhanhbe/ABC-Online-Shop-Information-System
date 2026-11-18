from __future__ import annotations

from .order_dao import OrderDAO


class SqliteOrderDAO(OrderDAO):

    def get_order(self, order_id: str) -> Order:
        raise NotImplementedError

    def find_by_idempotency_key(self, key: str) -> Order:
        raise NotImplementedError

    def find_by_customer(self, customer_id: str) -> list[Order]:
        raise NotImplementedError

    def save_order(self, o: Order) -> Order:
        raise NotImplementedError

    def list_orders(self) -> list[Order]:
        raise NotImplementedError

    def find_by_status(self, statuses: list[str]) -> list[Order]:
        raise NotImplementedError
