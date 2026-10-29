"""model.product - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


@dataclass
class Category:
    category_id: str = ""
    name: str = ""


@dataclass
class Product:
    product_id: str = ""
    name: str = ""
    brand: str = ""
    color: str = ""
    price: float = 0.0
    description: str = ""
    image: str = ""
    status: str = ""
    category_id: str = ""    # key of Category [1]

    def is_active(self) -> bool:
        raise NotImplementedError

    def search_text(self) -> str:
        raise NotImplementedError

    def update_price(self, new_price: float) -> None:
        raise NotImplementedError


@dataclass
class Promotion:
    code: str = ""
    percent: float = 0.0
    min_total: float = 0.0
    start: str = ""
    end: str = ""
    active: bool = False

    def is_valid(self, subtotal: float, today: str) -> bool:
        raise NotImplementedError

    def discount_for(self, subtotal: float, today: str) -> float:
        raise NotImplementedError
