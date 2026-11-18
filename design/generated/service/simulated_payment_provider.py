from __future__ import annotations

from .payment_gateway import PaymentGateway


class SimulatedPaymentProvider(PaymentGateway):

    def authorize(self, attempt_ref: str, amount: float, currency: str, card_token: str) -> Map:
        raise NotImplementedError
