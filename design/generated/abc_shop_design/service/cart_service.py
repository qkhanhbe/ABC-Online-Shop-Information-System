"""service.cart_service - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:                       # <<use>> and the types in the signatures
    from model.cart import Cart
    from dao.interfaces import CartDAO
    from dao.interfaces import InventoryDAO
    from dao.interfaces import ProductDAO


class CartService:
    def __init__(self, carts: CartDAO, products: ProductDAO, inventory: InventoryDAO):
        self.carts = carts
        self.products = products
        self.inventory = inventory

    def view(self, customer_id: str) -> Cart:
        raise NotImplementedError

    def add_item(self, customer_id: str, product_id: str, quantity: int) -> Cart:
        raise NotImplementedError

    def update_quantity(self, customer_id: str, product_id: str, quantity: int) -> Cart:
        raise NotImplementedError

    def remove_item(self, customer_id: str, product_id: str) -> Cart:
        raise NotImplementedError

    def check_availability(self, product_id: str, quantity: int) -> int:
        raise NotImplementedError

    def validate_cart(self, cart: Cart) -> list:
        raise NotImplementedError
