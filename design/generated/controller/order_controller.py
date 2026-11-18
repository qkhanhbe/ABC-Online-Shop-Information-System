from __future__ import annotations



class OrderController:

    def cart(self, request: Request) -> Response:
        raise NotImplementedError

    def add_to_cart(self, request: Request) -> Response:
        raise NotImplementedError

    def update_cart(self, request: Request) -> Response:
        raise NotImplementedError

    def checkout_form(self, request: Request) -> Response:
        raise NotImplementedError

    def checkout(self, request: Request) -> Response:
        raise NotImplementedError

    def history(self, request: Request) -> Response:
        raise NotImplementedError

    def track(self, request: Request, order_id: str) -> Response:
        raise NotImplementedError

    def cancel(self, request: Request, order_id: str) -> Response:
        raise NotImplementedError

    def review(self, request: Request, order_id: str) -> Response:
        raise NotImplementedError
