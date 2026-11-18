from __future__ import annotations

from .product import Product


class Bag(Product):

    def __init__(self, capacity_l: float | None = None, material: str | None = None, laptop_sleeve: bool | None = None) -> None:
        super().__init__()
        self.capacity_l: float | None = capacity_l
        self.material: str | None = material
        self.laptop_sleeve: bool | None = laptop_sleeve
