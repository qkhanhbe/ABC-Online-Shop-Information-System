"""model.payment - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


@dataclass
class Payment:
    payment_id: str = ""
    attempt_ref: str = ""
    amount: float = 0.0
    currency: str = ""
    status: str = ""
    provider_ref: str = ""
    created_at: str = ""
    order_id: str = ""    # key of Order [1]

    def matches(self, attempt_ref: str, amount: float, currency: str) -> bool:
        raise NotImplementedError

    def is_final(self) -> bool:
        raise NotImplementedError
