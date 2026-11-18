from __future__ import annotations



class Shipment:

    def __init__(self, shipment_id: str | None = None, order_id: str | None = None, carrier_ref: str | None = None, status: str | None = None) -> None:
        self.shipment_id: str | None = shipment_id
        self.order_id: str | None = order_id
        self.carrier_ref: str | None = carrier_ref
        self.status: str | None = status
        self._milestones: list[Milestone] = []

    def last_seq(self) -> int:
        raise NotImplementedError

    def add_milestone(self, milestone: Milestone) -> None:
        raise NotImplementedError
