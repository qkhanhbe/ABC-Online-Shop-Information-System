from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentGateway(ABC):

    @abstractmethod
    def authorize(self, attempt_ref: str, amount: float, currency: str, card_token: str) -> Map:
        raise NotImplementedError
