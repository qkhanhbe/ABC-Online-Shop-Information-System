from __future__ import annotations



class Address:

    def __init__(self, receiver: str | None = None, phone: str | None = None, street: str | None = None, city: str | None = None) -> None:
        self.receiver: str | None = receiver
        self.phone: str | None = phone
        self.street: str | None = street
        self.city: str | None = city

    def is_complete(self) -> bool:
        raise NotImplementedError

    def one_line(self) -> str:
        raise NotImplementedError
