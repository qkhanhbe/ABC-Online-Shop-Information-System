from __future__ import annotations

from abc import ABC, abstractmethod


class CartDAO(ABC):

    @abstractmethod
    def get_cart(self, customer_id: str) -> Cart:
        raise NotImplementedError

    @abstractmethod
    def update_cart(self, cart: Cart) -> Cart:
        raise NotImplementedError
