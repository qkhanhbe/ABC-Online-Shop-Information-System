"""model.cart - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:                       # <<use>> and the types in the signatures
    from model.product import Product


@dataclass
class Cart:
    cart_id: str = ""
    items: list[CartItem] = field(default_factory=list)    # composition 0..*
    customer_id: str = ""    # key of Customer [1]

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


@dataclass
class CartItem:
    name: str = ""
    cart_price: float = 0.0
    quantity: int = 0
    product_id: str = ""    # key of Product [1]

    def sub_total(self) -> float:
        raise NotImplementedError
