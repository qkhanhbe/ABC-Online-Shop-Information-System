"""Model: Shipment and carrier milestones (UC21-UC23, UC11 Track Order).

A milestone carries the carrier's sequence number; duplicates and older messages are kept
out, so the visible status never moves backwards (BR11 "no regression").
"""
from dataclasses import dataclass, field

MILESTONE_TO_ORDER_STATUS = {
    "PICKED_UP": "Shipped",
    "IN_TRANSIT": "Shipped",
    "OUT_FOR_DELIVERY": "Shipped",
    "DELIVERED": "Delivered",
    "FAILED_ATTEMPT": "Delivery Failed",
}


@dataclass
class Milestone:
    seq: int
    code: str
    at: str
    location: str = ""


@dataclass
class Shipment:
    shipment_id: str
    order_id: str
    carrier_ref: str = ""
    status: str = "Packed"
    milestones: list = field(default_factory=list)

    def last_seq(self):
        return max((m.seq for m in self.milestones), default=0)

    def add_milestone(self, milestone):
        """Return True if accepted; False for a duplicate or out-of-sequence message."""
        if milestone.code not in MILESTONE_TO_ORDER_STATUS:
            raise ValueError(f"unknown milestone {milestone.code}")
        if milestone.seq <= self.last_seq():
            return False
        self.milestones.append(milestone)
        self.status = milestone.code
        return True
