from __future__ import annotations



class Product:

    def __init__(self, product_id: str | None = None, name: str | None = None, category_id: str | None = None, brand: str | None = None, color: str | None = None, price: float | None = None, description: str | None = None, image: str | None = None, status: str | None = None) -> None:
        self.product_id: str | None = product_id
        self.name: str | None = name
        self.category_id: str | None = category_id
        self.brand: str | None = brand
        self.color: str | None = color
        self.price: float | None = price
        self.description: str | None = description
        self.image: str | None = image
        self.status: str | None = status

    def is_active(self) -> bool:
        raise NotImplementedError

    def spec_rows(self) -> list[str]:
        raise NotImplementedError

    def search_terms(self) -> str:
        raise NotImplementedError

    def search_text(self) -> str:
        raise NotImplementedError

    def update_price(self, new_price: float) -> None:
        raise NotImplementedError
