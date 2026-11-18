from __future__ import annotations

from .product import Product


class Footwear(Product):

    def __init__(self, sizes: str | None = None, upper_material: str | None = None, sole: str | None = None, purpose: str | None = None) -> None:
        super().__init__()
        self.sizes: str | None = sizes
        self.upper_material: str | None = upper_material
        self.sole: str | None = sole
        self.purpose: str | None = purpose
