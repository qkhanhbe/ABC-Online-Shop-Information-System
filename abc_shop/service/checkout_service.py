"""Service layer: UC08 Place Order / Checkout with its included use cases
UC29 Validate Cart, UC30 Check Product Availability, UC31 Calculate Order Total,
UC32 Apply Promotion (extension) and UC09 Make Payment.

Main success scenario of A02 Section 8.1, step numbers in the comments.
"""
import uuid

from model.order import Order
from model.payment import SUCCEEDED
from service.errors import CheckoutError

FREE_SHIPPING_FROM = 100.0
SHIPPING_FEE = 5.0


class CheckoutService:

    def __init__(self, db, cart_dao, order_dao, promotion_dao, cart_service, inventory_service,
                 payment_service):
        self.db = db
        self.carts = cart_dao
        self.orders = order_dao
        self.promotions = promotion_dao
        self.cart_service = cart_service
        self.inventory = inventory_service
        self.payments = payment_service

    def quote(self, customer_id, promo_code=""):
        """Steps 1-5: validated cart and the authoritative total, nothing is stored."""
        cart = self.carts.get_cart(customer_id)
        problems = self.cart_service.validate_cart(cart)               # UC29 + UC30
        subtotal = cart.calc_total()
        discount, promo_note = self.apply_promotion(promo_code, subtotal)   # UC32
        shipping = self.calc_shipping(subtotal - discount)                 # UC31
        return {"cart": cart, "problems": problems, "subtotal": subtotal, "discount": discount,
                "shipping": shipping, "total": round(subtotal - discount + shipping, 2),
                "promo_note": promo_note}

    def apply_promotion(self, code, subtotal):
        if not code:
            return 0.0, ""
        promotion = self.promotions.get_promotion(code)
        if promotion is None:
            return 0.0, f"promotion {code} does not exist"             # A4
        discount = promotion.discount_for(subtotal, self.db.now()[:10])
        if discount == 0:
            return 0.0, f"promotion {code} is not valid for this order"
        return discount, f"{promotion.code}: -{promotion.percent:g}%"

    @staticmethod
    def calc_shipping(amount):
        return 0.0 if amount >= FREE_SHIPPING_FROM else SHIPPING_FEE

    def place_order(self, customer, promo_code="", card_token="tok_visa", idempotency_key=None):
        idempotency_key = idempotency_key or uuid.uuid4().hex
        existing = self.orders.find_by_idempotency_key(idempotency_key)
        if existing:                                                     # A7 repeated submission
            return {"order": existing, "payment": existing.status, "duplicate": True}

        if customer.address is None or not customer.address.is_complete():
            raise CheckoutError(["delivery address is incomplete"])      # A3
        quote = self.quote(customer.user_id, promo_code)
        if quote["problems"]:
            raise CheckoutError(quote["problems"])                       # A1, A2
        cart = quote["cart"]

        # step 6: reserve stock and create one Payment Pending order - atomically (E1)
        with self.db.transaction():
            order = Order.create_from_cart(
                self.db.next_id("order", "O"), cart, customer.address.one_line(), self.db.now(),
                idempotency_key, quote["discount"], quote["shipping"],
                promo_code.upper() if quote["discount"] else "")
            self.orders.save_order(order)
            self.inventory.reserve_order(order)

        # steps 7-8: UC09 Make Payment
        status = self.payments.request_payment(order, card_token)
        if status == SUCCEEDED:
            cart.clear()
            self.carts.update_cart(cart)                                 # cart cleared only when paid
        return {"order": self.orders.get_order(order.order_id), "payment": status,
                "duplicate": False}
