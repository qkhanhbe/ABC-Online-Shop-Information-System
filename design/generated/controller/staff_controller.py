from __future__ import annotations



class StaffController:

    def orders(self, request: Request) -> Response:
        raise NotImplementedError

    def order_action(self, request: Request, order_id: str, action: str) -> Response:
        raise NotImplementedError

    def inventory(self, request: Request) -> Response:
        raise NotImplementedError

    def inventory_event(self, request: Request) -> Response:
        raise NotImplementedError

    def reviews(self, request: Request) -> Response:
        raise NotImplementedError

    def moderate(self, request: Request, review_id: str) -> Response:
        raise NotImplementedError
