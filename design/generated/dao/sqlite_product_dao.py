from __future__ import annotations

from .product_dao import ProductDAO


class SqliteProductDAO(ProductDAO):

    def get_product(self, product_id: str) -> Product:
        raise NotImplementedError

    def list_products(self, category_id: str, active_only: bool) -> list[Product]:
        raise NotImplementedError

    def save_product(self, p: Product) -> Product:
        raise NotImplementedError

    def get_category(self, category_id: str) -> Category:
        raise NotImplementedError

    def list_categories(self) -> list[Category]:
        raise NotImplementedError

    def save_category(self, c: Category) -> Category:
        raise NotImplementedError
