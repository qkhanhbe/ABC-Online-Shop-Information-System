"""Model: Payment attempt (UC09).

Only status and references are stored - never card data (NFR10 privacy). One attempt has a
unique attempt_ref; a provider result is accepted only when reference and amount match.
"""
from dataclasses import dataclass

PENDING = "Pending"
SUCCEEDED = "Succeeded"
FAILED = "Failed"


@dataclass
class Payment:
    payment_id: str
    order_id: str
    attempt_ref: str
    amount: float
    currency: str = "USD"
    status: str = PENDING
    provider_ref: str = ""
    created_at: str = ""

    def matches(self, attempt_ref, amount, currency):
        return (attempt_ref == self.attempt_ref and currency == self.currency
                and abs(float(amount) - self.amount) < 0.005)

    def is_final(self):
        return self.status in (SUCCEEDED, FAILED)
