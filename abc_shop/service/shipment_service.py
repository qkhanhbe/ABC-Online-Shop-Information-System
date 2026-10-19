"""Service layer: UC21 Prepare Shipment, UC22 Arrange Delivery, UC23 Update Shipment Status."""
from model import order as states
from model.order import InvalidTransition
from model.shipment import MILESTONE_TO_ORDER_STATUS, Milestone, Shipment
from service.auth_service import AuthService
from service.errors import NotFound, ValidationError


class ShipmentService:

    def __init__(self, db, shipment_dao, order_dao, inventory_service, carrier, audit_dao):
        self.db = db
        self.shipments = shipment_dao
        self.orders = order_dao
        self.inventory = inventory_service
        self.carrier = carrier
        self.audit = audit_dao

    def pick_list(self, staff):
        AuthService.require(staff, "shipment")
        return self.orders.find_by_status(states.PROCESSING)

    def ready_list(self, staff):
        AuthService.require(staff, "shipment")
        return self.orders.find_by_status(states.READY)

    def mark_packed(self, staff, order_id):
        """UC21: issue the reserved stock and make the order Ready for Shipment."""
        AuthService.require(staff, "shipment")
        order = self._order(order_id)
        if order.status != states.PROCESSING:
            raise ValidationError(f"order {order_id} is {order.status}, not Processing")
        with self.db.transaction():
            self.inventory.issue_order(order)
            shipment = Shipment(self.db.next_id("shipment", "SH"), order_id)
            self.shipments.save_shipment(shipment)
            order.change_status(states.READY, staff.user_id, self.db.now(), "packed " + shipment.shipment_id)
            self.orders.save_order(order)
        return shipment

    def arrange_delivery(self, staff, order_id):
        """UC22: send a uniquely referenced delivery request to the Shipping Provider."""
        AuthService.require(staff, "shipment")
        order = self._order(order_id)
        shipment = self.shipments.get_by_order(order_id)
        if order.status != states.READY or shipment is None:
            raise ValidationError(f"order {order_id} is not ready for shipment")
        if not shipment.carrier_ref:
            parcels = sum(i.quantity for i in order.items)
            shipment.carrier_ref = self.carrier.create_delivery(order_id, order.address, parcels)
            shipment.status = "Handed over"
            self.shipments.save_shipment(shipment)
        return shipment

    def on_milestone(self, carrier_ref, seq, code, at, location=""):
        """UC23: provider message. Duplicates / older messages never regress the status."""
        shipment = self.shipments.get_by_carrier_ref(carrier_ref)
        if shipment is None:
            self.audit.record("carrier", "unmatched_milestone", "shipment", carrier_ref, code)
            return False
        if not shipment.add_milestone(Milestone(int(seq), code, at, location)):
            return False
        order = self._order(shipment.order_id)
        target = MILESTONE_TO_ORDER_STATUS[code]
        with self.db.transaction():
            if target != order.status:
                try:
                    order.change_status(target, "shipping-provider", at, f"{code} {location}".strip())
                except InvalidTransition:
                    self.audit.record("carrier", "unmatched_milestone", "order", order.order_id, code)
                    return False
                self.orders.save_order(order)
            self.shipments.save_shipment(shipment)
        return True

    def _order(self, order_id):
        order = self.orders.get_order(order_id)
        if order is None:
            raise NotFound("order not found")
        return order
