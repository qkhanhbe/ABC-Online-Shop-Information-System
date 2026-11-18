from __future__ import annotations



class OrderService:

    def history(self, customer_id: str) -> list[Order]:
        raise NotImplementedError

    def own_order(self, customer_id: str, order_id: str) -> Order:
        raise NotImplementedError

    def track(self, customer_id: str, order_id: str) -> Map:
        raise NotImplementedError

    def cancel(self, user: User, order_id: str, reason: str) -> bool:
        raise NotImplementedError

    def processing_queue(self, staff: User) -> list[Order]:
        raise NotImplementedError

    def start_processing(self, staff: User, order_id: str) -> Order:
        raise NotImplementedError

    def hold(self, staff: User, order_id: str, reason: str) -> Order:
        raise NotImplementedError
