from __future__ import annotations

from .product import Product


class Apparel(Product):

    def __init__(self, sizes: str | None = None, material: str | None = None, fit: str | None = None) -> None:
        super().__init__()
        self.sizes: str | None = sizes
        self.material: str | None = material
        self.fit: str | None = fit
