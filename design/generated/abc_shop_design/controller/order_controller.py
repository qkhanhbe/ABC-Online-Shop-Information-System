"""controller.order_controller - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:                       # <<use>> and the types in the signatures
    from service.cart_service import CartService
    from view.templates import templates


class OrderController:
    def __init__(self, cart_service: CartService, checkout_service: CheckoutService, order_service: OrderService):
        self.cart_service = cart_service
        self.checkout_service = checkout_service
        self.order_service = order_service

    def cart(self, request: Request) -> Response:
        raise NotImplementedError

    def add_to_cart(self, request: Request) -> Response:
        raise NotImplementedError

    def update_cart(self, request: Request) -> Response:
        raise NotImplementedError
