from __future__ import annotations

from .shipment_dao import ShipmentDAO


class SqliteShipmentDAO(ShipmentDAO):

    def get_by_order(self, order_id: str) -> Shipment:
        raise NotImplementedError

    def get_by_carrier_ref(self, carrier_ref: str) -> Shipment:
        raise NotImplementedError

    def save_shipment(self, s: Shipment) -> Shipment:
        raise NotImplementedError
