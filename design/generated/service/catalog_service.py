from __future__ import annotations



class CatalogService:

    def browse(self, category_id: str) -> list[Map]:
        raise NotImplementedError

    def categories(self) -> list[Category]:
        raise NotImplementedError

    def category(self, category_id: str) -> Category:
        raise NotImplementedError

    def product_detail(self, product_id: str) -> Map:
        raise NotImplementedError

    def save_product(self, admin: User, product: Product) -> Product:
        raise NotImplementedError

    def save_promotion(self, admin: User, promotion: Promotion) -> Promotion:
        raise NotImplementedError

    def change_price(self, admin: User, product_id: str, new_price: float) -> Product:
        raise NotImplementedError

    def set_status(self, admin: User, product_id: str, status: str) -> Product:
        raise NotImplementedError
