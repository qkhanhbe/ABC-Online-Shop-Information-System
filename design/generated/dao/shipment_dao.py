from __future__ import annotations

from abc import ABC, abstractmethod


class ShipmentDAO(ABC):

    @abstractmethod
    def get_by_order(self, order_id: str) -> Shipment:
        raise NotImplementedError

    @abstractmethod
    def get_by_carrier_ref(self, carrier_ref: str) -> Shipment:
        raise NotImplementedError

    @abstractmethod
    def save_shipment(self, shipment: Shipment) -> Shipment:
        raise NotImplementedError
