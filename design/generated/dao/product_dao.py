from __future__ import annotations

from abc import ABC, abstractmethod


class ProductDAO(ABC):

    @abstractmethod
    def get_product(self, product_id: str) -> Product:
        raise NotImplementedError

    @abstractmethod
    def list_products(self, category_id: str, active_only: bool) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    def save_product(self, product: Product) -> Product:
        raise NotImplementedError

    @abstractmethod
    def get_category(self, category_id: str) -> Category:
        raise NotImplementedError

    @abstractmethod
    def list_categories(self) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    def save_category(self, category: Category) -> Category:
        raise NotImplementedError
