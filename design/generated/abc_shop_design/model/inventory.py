"""model.inventory - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


@dataclass
class InventoryEvent:
    event_id: str = ""
    kind: str = ""
    quantity: int = 0
    reference: str = ""
    reason: str = ""
    created_at: str = ""
    product_id: str = ""    # key of Product [1]


@dataclass
class StockLevel:
    physical: int = 0
    reserved: int = 0
    threshold: int = 0
    product_id: str = ""    # key of Product [1]

    def available(self) -> int:
        raise NotImplementedError

    def is_low(self) -> bool:
        raise NotImplementedError

    def apply(self, event: InventoryEvent) -> StockLevel:
        raise NotImplementedError
