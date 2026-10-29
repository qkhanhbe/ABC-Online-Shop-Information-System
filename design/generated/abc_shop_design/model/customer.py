"""model.customer - generated from the Visual Paradigm design model; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional


@dataclass
class Address:
    receiver: str = ""
    phone: str = ""
    street: str = ""
    city: str = ""

    def is_complete(self) -> bool:
        raise NotImplementedError

    def one_line(self) -> str:
        raise NotImplementedError


@dataclass
class User:
    user_id: str = ""
    name: str = ""
    email: str = ""
    password_hash: str = ""
    role: str = ""

    def can(self, permission: str) -> bool:
        raise NotImplementedError


@dataclass
class Customer(User):
    created_at: str = ""
    address: Optional[Address] = None    # association 0..1

    def update_profile(self, name: str, address: Address) -> Customer:
        raise NotImplementedError
