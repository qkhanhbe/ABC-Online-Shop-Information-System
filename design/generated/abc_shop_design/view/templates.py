"""view.templates - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:                       # <<use>> and the types in the signatures
    from model.cart import Cart


def cart(request: Request, cart: Cart) -> str:
    raise NotImplementedError


def product(request: Request, card: dict, reviews: list, insight: dict, similar: list) -> str:
    raise NotImplementedError
