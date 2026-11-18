from __future__ import annotations

from .shipping_gateway import ShippingGateway


class SimulatedCarrier(ShippingGateway):

    def create_delivery(self, order_id: str, address: Address, parcels: int) -> str:
        raise NotImplementedError
