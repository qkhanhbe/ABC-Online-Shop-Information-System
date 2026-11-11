"""model.product - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional


@dataclass
class Category:
    category_id: str = ""
    name: str = ""
    detail_kind: str = ""


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
    detail: Optional[ProductDetail] = None    # association 0..1

    def is_active(self) -> bool:
        raise NotImplementedError

    def search_text(self) -> str:
        raise NotImplementedError

    def update_price(self, new_price: float) -> None:
        raise NotImplementedError


@dataclass
class ProductDetail:
    product_id: str = ""

    def spec_rows(self) -> list:
        raise NotImplementedError

    def search_terms(self) -> str:
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


@dataclass
class ApparelDetail(ProductDetail):
    sizes: str = ""
    material: str = ""
    fit: str = ""


@dataclass
class BagDetail(ProductDetail):
    capacity_l: float = 0.0
    material: str = ""
    laptop_sleeve: bool = False


@dataclass
class FootwearDetail(ProductDetail):
    sizes: str = ""
    upper_material: str = ""
    sole: str = ""
    purpose: str = ""


@dataclass
class WatchDetail(ProductDetail):
    movement: str = ""
    strap: str = ""
    water_resistance_m: int = 0
    battery_days: int = 0
