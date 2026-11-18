from __future__ import annotations

from .cart_dao import CartDAO


class SqliteCartDAO(CartDAO):

    def get_cart(self, customer_id: str) -> Cart:
        raise NotImplementedError

    def update_cart(self, cart: Cart) -> Cart:
        raise NotImplementedError
