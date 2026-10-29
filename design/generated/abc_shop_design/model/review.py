"""model.review - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


@dataclass
class Review:
    review_id: str = ""
    rating: int = 0
    text: str = ""
    status: str = ""
    created_at: str = ""
    product_id: str = ""    # key of Product [1]
    customer_id: str = ""    # key of Customer [1]
    order_id: str = ""    # key of Order [1]

    def validate(self) -> Review:
        raise NotImplementedError
