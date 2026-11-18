from __future__ import annotations



class ShipmentService:

    def pick_list(self, staff: User) -> list[Order]:
        raise NotImplementedError

    def ready_list(self, staff: User) -> list[Order]:
        raise NotImplementedError

    def mark_packed(self, staff: User, order_id: str) -> Shipment:
        raise NotImplementedError

    def arrange_delivery(self, staff: User, order_id: str) -> Shipment:
        raise NotImplementedError

    def on_milestone(self, carrier_ref: str, seq: int, code: str, at: str, location: str) -> bool:
        raise NotImplementedError
