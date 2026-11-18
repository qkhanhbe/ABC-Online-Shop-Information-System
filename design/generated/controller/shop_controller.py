from __future__ import annotations



class ShopController:

    def home(self, request: Request) -> Response:
        raise NotImplementedError

    def search(self, request: Request) -> Response:
        raise NotImplementedError

    def credits(self, request: Request) -> Response:
        raise NotImplementedError

    def product(self, request: Request, product_id: str) -> Response:
        raise NotImplementedError
