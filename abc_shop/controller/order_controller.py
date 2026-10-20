"""Presentation layer: UC07 Manage Shopping Cart, UC08 Place Order, UC10 View Order History,
UC11 Track Order, UC12 Cancel Order, UC13 Submit Review."""
import uuid

from controller.http import Response
from service.auth_service import AuthService
from service.errors import CheckoutError, ValidationError
from view import templates


class OrderController:

    def __init__(self, shop):
        self.cart_service = shop.cart
        self.checkout_service = shop.checkout
        self.order_service = shop.orders
        self.review_service = shop.reviews
        self.recommender = shop.recommender

    @staticmethod
    def _customer(request):
        return AuthService.require(request.user, "cart")

    def cart(self, request):
        customer = self._customer(request)
        return Response(templates.cart(request, self.cart_service.view(customer.user_id)))

    def add_to_cart(self, request):
        customer = self._customer(request)
        product_id = request.get("product_id")
        try:
            self.cart_service.add_item(customer.user_id, product_id, int(request.get("qty", "1")))
        except ValidationError as e:
            return Response.redirect(f"/product/{product_id}", str(e), request)
        return Response.redirect("/cart", "Added to cart.", request)

    def update_cart(self, request):
        customer = self._customer(request)
        try:
            self.cart_service.update_quantity(customer.user_id, request.get("product_id"),
                                              int(request.get("qty", "0")))
        except ValidationError as e:
            return Response.redirect("/cart", str(e), request)
        return Response.redirect("/cart", "Cart updated.", request)

    def checkout_form(self, request):
        customer = self._customer(request)
        quote = self.checkout_service.quote(customer.user_id, request.get("promo"))
        request.session["checkout_key"] = request.session.get("checkout_key") or uuid.uuid4().hex
        return Response(templates.checkout(request, customer, quote, request.get("promo"),
                                           request.session["checkout_key"]))

    def checkout(self, request):
        customer = self._customer(request)
        try:
            result = self.checkout_service.place_order(customer, request.get("promo"),
                                                       request.get("card", "tok_visa"),
                                                       request.get("key") or None)
        except CheckoutError as e:
            return Response.redirect("/cart", "Checkout stopped: " + str(e), request)
        request.session.pop("checkout_key", None)
        order = result["order"]
        self.recommender.fit()
        return Response.redirect(f"/orders/{order.order_id}",
                                 f"Order {order.order_id}: {order.status}.", request)

    def history(self, request):
        customer = AuthService.require(request.user, "own_orders")
        orders = self.order_service.history(customer.user_id)
        picks = self.recommender.for_customer(customer.user_id, 4)
        return Response(templates.order_history(request, orders, picks))

    def track(self, request, order_id):
        customer = AuthService.require(request.user, "own_orders")
        tracking = self.order_service.track(customer.user_id, order_id)
        return Response(templates.track(request, tracking))

    def cancel(self, request, order_id):
        customer = AuthService.require(request.user, "own_orders")
        self.order_service.cancel(customer, order_id)
        return Response.redirect(f"/orders/{order_id}", "Order cancelled.", request)

    def review(self, request, order_id):
        customer = AuthService.require(request.user, "review")
        review = self.review_service.submit(customer, order_id, request.get("product_id"),
                                            int(request.get("rating", "5")), request.get("text"))
        note = ("Thank you - your review is published." if review.status == "published"
                else "Thank you - your review is waiting for moderation.")
        return Response.redirect(f"/orders/{order_id}", note, request)
