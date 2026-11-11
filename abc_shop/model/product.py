"""Model: catalogue (Category, Product, product details) and promotion rules.

A product only shows facts that come from one controlled source (BP01): the price and status
are kept here, the available quantity comes from StockLevel (inventory.py).
Attributes shared by every product live in Product; attributes that only one product group has
live in a detail object of that group. The category names the group (detail_kind), so a product
has exactly one detail of the right kind (BR-CAT-01).
"""
from dataclasses import dataclass, fields
from datetime import date
from typing import Optional


@dataclass
class Category:
    category_id: str
    name: str
    detail_kind: str = "apparel"     # footwear | apparel | bag | watch


@dataclass
class ProductDetail:
    """Group-specific attributes of one product (abstract: use one of the subclasses)."""
    product_id: str

    KIND = ""
    LABELS = {}

    def spec_rows(self):
        """(label, value) pairs for the product page, in declaration order."""
        rows = []
        for f in fields(self):
            if f.name == "product_id":
                continue
            value = getattr(self, f.name)
            if value is None:
                continue
            if isinstance(value, bool) or f.name == "laptop_sleeve":
                value = "yes" if value else "no"
            elif isinstance(value, float) and value.is_integer():
                value = int(value)
            rows.append((self.LABELS.get(f.name, f.name.replace("_", " ")), str(value)))
        return rows

    def search_terms(self):
        """Words for keyword search: the values, and the label of a feature the product has."""
        words = []
        for label, value in self.spec_rows():
            if value == "yes":
                words.append(label.lower())
            elif value != "no":
                words.append(value)
        return " ".join(words)


@dataclass
class FootwearDetail(ProductDetail):
    sizes: str = ""
    upper_material: str = ""
    sole: str = ""
    purpose: str = ""

    KIND = "footwear"
    LABELS = {"sizes": "Sizes (EU)", "upper_material": "Upper", "sole": "Sole", "purpose": "Made for"}


@dataclass
class ApparelDetail(ProductDetail):
    sizes: str = ""
    material: str = ""
    fit: str = ""

    KIND = "apparel"
    LABELS = {"sizes": "Sizes", "material": "Material", "fit": "Fit"}


@dataclass
class BagDetail(ProductDetail):
    capacity_l: float = 0.0
    material: str = ""
    laptop_sleeve: bool = False

    KIND = "bag"
    LABELS = {"capacity_l": "Capacity (litres)", "material": "Material", "laptop_sleeve": "Laptop sleeve"}


@dataclass
class WatchDetail(ProductDetail):
    movement: str = ""
    strap: str = ""
    water_resistance_m: int = 0
    battery_days: Optional[int] = None

    KIND = "watch"
    LABELS = {"movement": "Movement", "strap": "Strap", "water_resistance_m": "Water resistance (m)",
              "battery_days": "Battery (days)"}


DETAIL_TYPES = {cls.KIND: cls for cls in (FootwearDetail, ApparelDetail, BagDetail, WatchDetail)}


@dataclass
class Product:
    product_id: str
    name: str
    category_id: str
    brand: str
    color: str
    price: float
    description: str = ""
    image: str = ""
    status: str = "active"          # active | unpublished
    detail: Optional[ProductDetail] = None

    def is_active(self):
        return self.status == "active"

    def search_text(self):
        """Text used by keyword search and by the recommender."""
        extra = self.detail.search_terms() if self.detail else ""
        return f"{self.name} {self.category_id} {self.color} {self.brand} {self.description} {extra}".strip()

    def update_price(self, new_price):
        if new_price <= 0:
            raise ValueError("price must be positive")
        self.price = round(float(new_price), 2)


@dataclass
class Promotion:
    code: str
    percent: float                  # 10 -> 10 % off the subtotal
    min_total: float
    start: str                      # ISO dates, inclusive
    end: str
    active: bool = True

    def is_valid(self, subtotal, today=None):
        today = today or date.today().isoformat()
        return (self.active and self.start <= today <= self.end
                and subtotal >= self.min_total)

    def discount_for(self, subtotal, today=None):
        """BR32: a promotion applies only when code, dates and minimum total are valid."""
        if not self.is_valid(subtotal, today):
            return 0.0
        return round(subtotal * self.percent / 100, 2)
