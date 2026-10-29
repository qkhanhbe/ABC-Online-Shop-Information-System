"""model.shipment - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


@dataclass
class Milestone:
    seq: int = 0
    code: str = ""
    at: str = ""
    location: str = ""


@dataclass
class Shipment:
    shipment_id: str = ""
    carrier_ref: str = ""
    status: str = ""
    order_id: str = ""    # key of Order [1]
    milestones: list[Milestone] = field(default_factory=list)    # composition 0..*

    def last_seq(self) -> int:
        raise NotImplementedError

    def add_milestone(self, milestone: Milestone) -> bool:
        raise NotImplementedError
