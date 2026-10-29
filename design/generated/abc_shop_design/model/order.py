"""model.order - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:                       # <<use>> and the types in the signatures
    from model.cart import Cart


@dataclass
class Order:
    order_id: str = ""
    address: str = ""
    discount: float = 0.0
    shipping_fee: float = 0.0
    status: str = ""
    created_at: str = ""
    idempotency_key: str = ""
    items: list[OrderItem] = field(default_factory=list)    # composition 1..*
    history: list[StatusChange] = field(default_factory=list)    # composition 1..*
    customer_id: str = ""    # key of Customer [1]
    promo_code: str = ""    # key of Promotion [0..1]

    def create_from_cart(self, order_id: str, cart: Cart, address: str, created_at: str, idempotency_key: str) -> Order:
        raise NotImplementedError

    def subtotal(self) -> float:
        raise NotImplementedError

    def calc_total(self) -> float:
        raise NotImplementedError

    def change_status(self, new_status: str, actor: str, at: str, note: str) -> Order:
        raise NotImplementedError

    def can_cancel(self) -> bool:
        raise NotImplementedError

    def last_update(self) -> str:
        raise NotImplementedError


@dataclass
class OrderItem:
    name: str = ""
    unit_price: float = 0.0
    quantity: int = 0
    product_id: str = ""    # key of Product [1]

    def sub_total(self) -> float:
        raise NotImplementedError


@dataclass
class StatusChange:
    status: str = ""
    actor: str = ""
    at: str = ""
    note: str = ""
