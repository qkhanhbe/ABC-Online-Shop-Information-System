from __future__ import annotations

from abc import ABC, abstractmethod


class ShippingGateway(ABC):

    @abstractmethod
    def create_delivery(self, order_id: str, address: Address, parcels: int) -> str:
        raise NotImplementedError
