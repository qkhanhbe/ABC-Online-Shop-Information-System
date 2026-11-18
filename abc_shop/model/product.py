"""Model: catalogue (Category, Product and its four kinds) and promotion rules.

A product only shows facts that come from one controlled source (BP01): the price and status
are kept here, the available quantity comes from StockLevel (inventory.py).
Attributes shared by every product live in Product; each kind of product (Footwear, Apparel, Bag,
Watch) is a subclass that adds the attributes of its kind and is stored in a table of its own that
shares the product's key (table per subclass). The category names the kind (detail_kind), so a
product is always of the kind of its category (BR-CAT-01).
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
class Product:
    """A listing. Attributes every product has live here; each kind of product is a subclass that adds the
    attributes of its kind (BR-CAT-01: the category names the kind)."""
    product_id: str
    name: str
    category_id: str
    brand: str
    color: str
    price: float
    description: str = ""
    image: str = ""
    status: str = "active"          # active | unpublished

    KIND = ""
    LABELS = {}

    def is_active(self):
        return self.status == "active"

    def spec_rows(self):
        """(label, value) pairs of the attributes of the kind, for the product page; a plain Product has none."""
        rows = []
        for f in fields(self):
            if f.name in _COMMON:
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
        """Words of the kind for keyword search: the values, and the label of a feature the product has."""
        words = []
        for label, value in self.spec_rows():
            if value == "yes":
                words.append(label.lower())
            elif value != "no":
                words.append(value)
        return " ".join(words)

    def search_text(self):
        """Text used by keyword search and by the recommender."""
        return (f"{self.name} {self.category_id} {self.color} {self.brand} {self.description} "
                f"{self.search_terms()}").strip()

    def update_price(self, new_price):
        if new_price <= 0:
            raise ValueError("price must be positive")
        self.price = round(float(new_price), 2)


_COMMON = {f.name for f in fields(Product)}


@dataclass
class Footwear(Product):
    sizes: str = ""
    upper_material: str = ""
    sole: str = ""
    purpose: str = ""

    KIND = "footwear"
    LABELS = {"sizes": "Sizes (EU)", "upper_material": "Upper", "sole": "Sole", "purpose": "Made for"}


@dataclass
class Apparel(Product):
    sizes: str = ""
    material: str = ""
    fit: str = ""

    KIND = "apparel"
    LABELS = {"sizes": "Sizes", "material": "Material", "fit": "Fit"}


@dataclass
class Bag(Product):
    capacity_l: float = 0.0
    material: str = ""
    laptop_sleeve: bool = False

    KIND = "bag"
    LABELS = {"capacity_l": "Capacity (litres)", "material": "Material", "laptop_sleeve": "Laptop sleeve"}


@dataclass
class Watch(Product):
    movement: str = ""
    strap: str = ""
    water_resistance_m: int = 0
    battery_days: Optional[int] = None

    KIND = "watch"
    LABELS = {"movement": "Movement", "strap": "Strap", "water_resistance_m": "Water resistance (m)",
              "battery_days": "Battery (days)"}


KINDS = {cls.KIND: cls for cls in (Footwear, Apparel, Bag, Watch)}


def kind_fields(cls):
    """The attributes a kind adds to Product: the columns of its own table besides the shared key."""
    return [f.name for f in fields(cls) if f.name not in _COMMON]


@dataclass
class Promotion:
    code: str
    percent: float                  # 10 -> 10 % off the subtotal
    min_total: float
    start_date: str                 # ISO dates, inclusive
    end_date: str
    active: bool = True

    def is_valid(self, subtotal, today=None):
        today = today or date.today().isoformat()
        return (self.active and self.start_date <= today <= self.end_date
                and subtotal >= self.min_total)

    def discount_for(self, subtotal, today=None):
        """BR32: a promotion applies only when code, dates and minimum total are valid."""
        if not self.is_valid(subtotal, today):
            return 0.0
        return round(subtotal * self.percent / 100, 2)
