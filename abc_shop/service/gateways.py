"""Service layer: interfaces to the external providers and their simulated implementations.

Payment authorisation and physical delivery are outside the system boundary (A1 Table 5).
The shop only sends a uniquely referenced request and records the attributable result, so
the simulators below can be replaced by a real provider SDK without changing any service.
"""
import hashlib
import hmac
from abc import ABC, abstractmethod

SHARED_SECRET = b"abc-shop-demo-secret"


def sign(*parts):
    message = "|".join(str(p) for p in parts).encode()
    return hmac.new(SHARED_SECRET, message, hashlib.sha256).hexdigest()[:16]


class PaymentGateway(ABC):
    @abstractmethod
    def authorize(self, attempt_ref, amount, currency, card_token): ...


class ShippingGateway(ABC):
    @abstractmethod
    def create_delivery(self, order_id, address, parcels): ...


class SimulatedPaymentProvider(PaymentGateway):
    """tok_visa -> success, tok_declined -> declined, tok_timeout -> no answer (pending)."""

    def __init__(self):
        self.calls = []

    def authorize(self, attempt_ref, amount, currency, card_token):
        self.calls.append(attempt_ref)
        if card_token == "tok_timeout":
            return None
        status = "SUCCEEDED" if card_token == "tok_visa" else "DECLINED"
        provider_ref = "PSP-" + hashlib.sha1(attempt_ref.encode()).hexdigest()[:8].upper()
        return {"attempt_ref": attempt_ref, "status": status, "provider_ref": provider_ref,
                "amount": round(amount, 2), "currency": currency,
                "signature": sign(attempt_ref, status, provider_ref, round(amount, 2), currency)}


class SimulatedCarrier(ShippingGateway):

    def __init__(self):
        self.requests = []

    def create_delivery(self, order_id, address, parcels):
        self.requests.append((order_id, address, parcels))
        return "VNP" + hashlib.sha1(order_id.encode()).hexdigest()[:9].upper()
