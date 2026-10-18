"""Model: catalogue (Category, Product) and promotion rules.

A product only shows facts that come from one controlled source (BP01): the price and status
are kept here, the available quantity comes from StockLevel (inventory.py).
"""
from dataclasses import dataclass
from datetime import date


@dataclass
class Category:
    category_id: str
    name: str


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

    def is_active(self):
        return self.status == "active"

    def search_text(self):
        """Text used by keyword search and by the recommender."""
        return f"{self.name} {self.category_id} {self.color} {self.brand} {self.description}"

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
