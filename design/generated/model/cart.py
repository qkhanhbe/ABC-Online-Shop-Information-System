from __future__ import annotations



class Cart:

    def __init__(self, cart_id: str | None = None, customer_id: str | None = None) -> None:
        self.cart_id: str | None = cart_id
        self.customer_id: str | None = customer_id
        self._items: list[CartItem] = []

    def find(self, product_id: str) -> CartItem:
        raise NotImplementedError

    def add_item(self, product: Product, quantity: int) -> CartItem:
        raise NotImplementedError

    def update_quantity(self, product_id: str, quantity: int) -> None:
        raise NotImplementedError

    def remove_item(self, product_id: str) -> None:
        raise NotImplementedError

    def calc_total(self) -> float:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError
