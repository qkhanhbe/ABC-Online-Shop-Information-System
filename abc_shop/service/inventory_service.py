"""Service layer: UC20 Manage Inventory and UC24 Manage Replenishment.

Every stock change is one typed, uniquely referenced InventoryEvent (BR20). Recording the same
reference twice returns the earlier event and changes nothing (E2 "duplicate reference").
"""
from model.inventory import InventoryEvent, StockError
from service.auth_service import AuthService
from service.errors import NotFound, ValidationError


class InventoryService:

    def __init__(self, db, inventory_dao, product_dao, audit_dao):
        self.db = db
        self.inventory = inventory_dao
        self.products = product_dao
        self.audit = audit_dao

    def record(self, product_id, kind, quantity, reference, reason="", actor="system"):
        if self.products.get_product(product_id) is None:
            raise NotFound(f"product {product_id} not found")
        previous = self.inventory.find_event(product_id, kind, reference)
        if previous:
            return previous
        with self.db.transaction():
            stock = self.inventory.get_stock(product_id)
            event = InventoryEvent(self.db.next_id("event", "EV", 4), product_id, kind,
                                   int(quantity), reference, reason, self.db.now())
            try:
                stock.apply(event)
            except StockError as e:
                raise ValidationError(str(e))
            self.inventory.add_event(event)
            self.inventory.save_stock(stock)
            if kind in ("RECEIPT", "ADJUST"):
                self.audit.record(actor, kind.lower(), "stock", product_id,
                                  f"{quantity:+d} ref={reference} {reason}".strip())
        return event

    def manual_event(self, staff, product_id, kind, quantity, reference, reason=""):
        """UC20 main flow, performed by Warehouse Staff."""
        AuthService.require(staff, "inventory")
        event = self.record(product_id, kind, quantity, reference, reason, staff.user_id)
        stock = self.inventory.get_stock(product_id)
        return {"event": event, "stock": stock, "low": stock.is_low()}

    # order-driven events (A1 Reservation, A2 Issue, A3 Release of UC20)
    def reserve_order(self, order):
        for item in order.items:
            self.record(item.product_id, "RESERVE", item.quantity, order.order_id)

    def release_order(self, order):
        for item in order.items:
            if self.inventory.find_event(item.product_id, "RESERVE", order.order_id):
                self.record(item.product_id, "RELEASE", item.quantity, order.order_id)

    def issue_order(self, order):
        for item in order.items:
            self.record(item.product_id, "ISSUE", item.quantity, order.order_id)

    def is_reserved(self, product_id, order_id):
        return self.inventory.find_event(product_id, "RESERVE", order_id) is not None

    def stock_of(self, product_id):
        return self.inventory.get_stock(product_id)

    def low_stock(self):
        result = []
        for product in self.products.list_products(active_only=False):
            stock = self.inventory.get_stock(product.product_id)
            if stock.is_low():
                result.append((product, stock))
        return result

    def request_replenishment(self, staff, product_id, quantity):
        """UC24: extends UC20 when available stock reaches the threshold."""
        AuthService.require(staff, "inventory")
        if quantity <= 0:
            raise ValidationError("quantity must be positive")
        request_id = self.db.next_id("replenishment", "RQ")
        self.inventory.add_replenishment(request_id, product_id, quantity, self.db.now())
        self.audit.record(staff.user_id, "replenish", "product", product_id, f"qty={quantity}")
        return request_id
