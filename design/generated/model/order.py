from __future__ import annotations



class Order:

    def __init__(self, order_id: str | None = None, customer_id: str | None = None, address: str | None = None, discount: float | None = None, shipping_fee: float | None = None, status: str | None = None, created_at: str | None = None, promo_code: str | None = None, idempotency_key: str | None = None) -> None:
        self.order_id: str | None = order_id
        self.customer_id: str | None = customer_id
        self.address: str | None = address
        self.discount: float | None = discount
        self.shipping_fee: float | None = shipping_fee
        self.status: str | None = status
        self.created_at: str | None = created_at
        self.promo_code: str | None = promo_code
        self.idempotency_key: str | None = idempotency_key
        self._items: list[OrderItem] = []
        self._history: list[StatusChange] = []

    def subtotal(self) -> float:
        raise NotImplementedError

    def calc_total(self) -> float:
        raise NotImplementedError

    def can_cancel(self) -> bool:
        raise NotImplementedError

    def last_update(self) -> str:
        raise NotImplementedError

    def change_status(self, new_status: str, actor: str, at: str, note: str) -> Order:
        raise NotImplementedError

    def create_from_cart(self, order_id: str, cart: Cart, address: str, created_at: str, idempotency_key: str, discount: float, shipping_fee: float, promo_code: str) -> Order:
        raise NotImplementedError
