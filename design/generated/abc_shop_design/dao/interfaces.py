"""dao.interfaces - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:                       # <<use>> and the types in the signatures
    from model.cart import Cart
    from model.inventory import InventoryEvent
    from model.product import Product
    from model.inventory import StockLevel


class CartDAO(ABC):
    @abstractmethod
    def get_cart(self, customer_id: str) -> Cart:
        ...

    @abstractmethod
    def update_cart(self, cart: Cart) -> Cart:
        ...


class InventoryDAO(ABC):
    @abstractmethod
    def get_stock(self, product_id: str) -> StockLevel:
        ...

    @abstractmethod
    def save_stock(self, stock: StockLevel) -> None:
        ...

    @abstractmethod
    def add_event(self, event: InventoryEvent) -> None:
        ...


class ProductDAO(ABC):
    @abstractmethod
    def get_product(self, product_id: str) -> Product:
        ...

    @abstractmethod
    def list_products(self, category_id: str, active_only: bool) -> list:
        ...

    @abstractmethod
    def save_product(self, product: Product) -> None:
        ...
