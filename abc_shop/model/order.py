"""Model: Order, OrderItem and the order state machine (A02 Section 8, BR19).

States can only change through TRANSITIONS; the history is append-only, so the status a
customer sees is always explained by recorded events (BP04 "unclear order status").
"""
from dataclasses import dataclass, field

PAYMENT_PENDING = "Payment Pending"
PAYMENT_FAILED = "Payment Failed"
PAID = "Paid/Confirmed"
ON_HOLD = "On Hold"
PROCESSING = "Processing"
READY = "Ready for Shipment"
SHIPPED = "Shipped"
DELIVERED = "Delivered"
DELIVERY_FAILED = "Delivery Failed"
CANCELLED = "Cancelled"

TRANSITIONS = {
    PAYMENT_PENDING: {PAID, PAYMENT_FAILED, CANCELLED},
    PAYMENT_FAILED: set(),
    PAID: {PROCESSING, ON_HOLD, CANCELLED},
    ON_HOLD: {PAID, PROCESSING, CANCELLED},
    PROCESSING: {READY, ON_HOLD, CANCELLED},
    READY: {SHIPPED},
    SHIPPED: {DELIVERED, DELIVERY_FAILED},
    DELIVERY_FAILED: {SHIPPED, DELIVERED},
    DELIVERED: set(),
    CANCELLED: set(),
}
CANCELLABLE = {PAYMENT_PENDING, PAID, ON_HOLD, PROCESSING}


class InvalidTransition(ValueError):
    pass


@dataclass
class OrderItem:
    product_id: str
    name: str
    unit_price: float
    quantity: int

    def sub_total(self):
        return round(self.unit_price * self.quantity, 2)


@dataclass
class StatusChange:
    status: str
    actor: str
    at: str
    note: str = ""


@dataclass
class Order:
    order_id: str
    customer_id: str
    address: str
    items: list = field(default_factory=list)
    discount: float = 0.0
    shipping_fee: float = 0.0
    status: str = PAYMENT_PENDING
    created_at: str = ""
    promo_code: str = ""
    idempotency_key: str = ""
    history: list = field(default_factory=list)

    @classmethod
    def create_from_cart(cls, order_id, cart, address, created_at, idempotency_key="",
                         discount=0.0, shipping_fee=0.0, promo_code=""):
        """UC08 step 6: the cart lines become order lines with the authoritative price."""
        items = [OrderItem(l.product_id, l.name, l.cart_price, l.quantity) for l in cart.items]
        order = cls(order_id, cart.customer_id, address, items, discount, shipping_fee,
                    PAYMENT_PENDING, created_at, promo_code, idempotency_key)
        order.history.append(StatusChange(PAYMENT_PENDING, cart.customer_id, created_at,
                                          "order created from cart"))
        return order

    def subtotal(self):
        return round(sum(i.sub_total() for i in self.items), 2)

    def calc_total(self):
        return round(self.subtotal() - self.discount + self.shipping_fee, 2)

    def change_status(self, new_status, actor, at, note=""):
        if new_status not in TRANSITIONS.get(self.status, set()):
            allowed = ", ".join(sorted(TRANSITIONS.get(self.status, set()))) or "none"
            raise InvalidTransition(
                f"{self.order_id}: {self.status} -> {new_status} is not allowed (next: {allowed})")
        self.status = new_status
        self.history.append(StatusChange(new_status, actor, at, note))
        return self

    def can_cancel(self):
        return self.status in CANCELLABLE

    def last_update(self):
        return self.history[-1].at if self.history else self.created_at
