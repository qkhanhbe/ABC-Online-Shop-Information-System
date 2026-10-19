"""Service layer: UC10 View Order History, UC11 Track Order, UC12 Cancel Order,
UC19 Process Orders (Sales Staff)."""
from model import order as states
from model.order import InvalidTransition
from service.auth_service import AuthService
from service.errors import NotFound, ValidationError


class OrderService:

    def __init__(self, db, order_dao, shipment_dao, payment_service, inventory_service, audit_dao):
        self.db = db
        self.orders = order_dao
        self.shipments = shipment_dao
        self.payments = payment_service
        self.inventory = inventory_service
        self.audit = audit_dao

    def history(self, customer_id):
        return self.orders.find_by_customer(customer_id)

    def own_order(self, customer_id, order_id):
        """A customer only sees their own orders; a foreign id looks exactly like a missing one."""
        order = self.orders.get_order(order_id)
        if order is None or order.customer_id != customer_id:
            raise NotFound("order not found")                      # UC11 E2, no disclosure
        return order

    def track(self, customer_id, order_id):
        order = self.own_order(customer_id, order_id)
        shipment = self.shipments.get_by_order(order.order_id)
        timeline = [(h.at, h.status, h.note) for h in order.history]
        if shipment:
            timeline += [(m.at, m.code.replace("_", " ").title(), m.location)
                         for m in shipment.milestones]
        timeline.sort(key=lambda t: t[0])
        return {"order": order, "status": order.status,
                "carrier_ref": shipment.carrier_ref if shipment else "",
                "timeline": timeline, "last_update": timeline[-1][0] if timeline else ""}

    def cancel(self, user, order_id, reason="customer request"):
        order = self.orders.get_order(order_id)
        if order is None or (user.role == "customer" and order.customer_id != user.user_id):
            raise NotFound("order not found")
        if user.role not in ("customer", "sales"):
            AuthService.require(user, "process_orders")
        if not order.can_cancel():
            raise ValidationError(f"an order in state '{order.status}' can no longer be cancelled")
        was_paid = self.payments.succeeded(order.order_id)
        with self.db.transaction():
            order.change_status(states.CANCELLED, user.user_id, self.db.now(), reason)
            self.inventory.release_order(order)
            self.orders.save_order(order)
            if was_paid:
                self.audit.record(user.user_id, "refund_initiated", "order", order.order_id,
                                  f"amount {order.calc_total()}")
        return order

    # --- UC19 Process Orders ---------------------------------------------------------------
    def processing_queue(self, staff):
        AuthService.require(staff, "process_orders")
        return self.orders.find_by_status(states.PAID, states.ON_HOLD)

    def start_processing(self, staff, order_id):
        AuthService.require(staff, "process_orders")
        order = self.orders.get_order(order_id)
        if order is None:
            raise NotFound("order not found")
        problems = []
        if not self.payments.succeeded(order_id):
            problems.append("payment is not confirmed")
        for item in order.items:
            if not self.inventory.is_reserved(item.product_id, order_id):
                problems.append(f"{item.product_id} is not reserved")
        if problems:                                                   # A1 manual verification
            return self.hold(staff, order_id, "; ".join(problems))
        return self._move(staff, order, states.PROCESSING, "processing confirmed")

    def hold(self, staff, order_id, reason):
        AuthService.require(staff, "process_orders")
        order = self.orders.get_order(order_id)
        return self._move(staff, order, states.ON_HOLD, reason)

    def _move(self, staff, order, new_status, note):
        try:
            order.change_status(new_status, staff.user_id, self.db.now(), note)
        except InvalidTransition as e:                                 # E1 invalid transition
            raise ValidationError(str(e))
        self.orders.save_order(order)
        self.audit.record(staff.user_id, "order_status", "order", order.order_id, new_status)
        return order
