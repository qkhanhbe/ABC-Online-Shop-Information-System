from __future__ import annotations

from .user import User


class Customer(User):

    def __init__(self, address: Address | None = None) -> None:
        super().__init__()
        self._address: Address | None = address

    def update_profile(self, name: str, address: Address) -> Customer:
        raise NotImplementedError
