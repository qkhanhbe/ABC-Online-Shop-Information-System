from __future__ import annotations



class CartService:

    def view(self, customer_id: str) -> Cart:
        raise NotImplementedError

    def add_item(self, customer_id: str, product_id: str, quantity: int) -> CartItem:
        raise NotImplementedError

    def remove_item(self, customer_id: str, product_id: str) -> CartItem:
        raise NotImplementedError

    def validate_cart(self, cart: Cart) -> Cart:
        raise NotImplementedError

    def update_quantity(self, customer_id: str, product_id: str, quantity: int) -> Cart:
        raise NotImplementedError

    def check_availability(self, product_id: str, quantity: int) -> int:
        raise NotImplementedError
