"""Model: event-based inventory (UC20, BR20-01..04).

    available = physical - reserved,   all quantities >= 0

Every change is a typed InventoryEvent; a stock level is never overwritten directly.
"""
from dataclasses import dataclass

EVENT_KINDS = ("RECEIPT", "RESERVE", "RELEASE", "ISSUE", "ADJUST")


class StockError(ValueError):
    pass


@dataclass
class InventoryEvent:
    event_id: str
    product_id: str
    kind: str
    quantity: int
    reference: str
    reason: str = ""
    created_at: str = ""


@dataclass
class StockLevel:
    product_id: str
    physical: int = 0
    reserved: int = 0
    threshold: int = 3

    @property
    def available(self):
        return self.physical - self.reserved

    def is_low(self):
        return self.available <= self.threshold

    def apply(self, event):
        """Apply one event; raise StockError and leave the level unchanged if it is invalid."""
        q = event.quantity
        physical, reserved = self.physical, self.reserved
        if event.kind == "RECEIPT":
            physical += q
        elif event.kind == "RESERVE":
            if q > self.available:
                raise StockError(f"only {self.available} available for {self.product_id}")
            reserved += q
        elif event.kind == "RELEASE":
            if q > reserved:
                raise StockError("release exceeds reservation")
            reserved -= q
        elif event.kind == "ISSUE":
            if q > reserved:
                raise StockError("issue exceeds reservation")
            physical -= q
            reserved -= q
        elif event.kind == "ADJUST":          # signed correction with a reason code
            if not event.reason:
                raise StockError("an adjustment needs a reason")
            physical += q
        else:
            raise StockError(f"unknown event kind {event.kind}")
        if event.kind != "ADJUST" and q <= 0:
            raise StockError("quantity must be positive")
        if physical < 0 or reserved < 0 or physical - reserved < 0:
            raise StockError("resulting balance would be negative")
        self.physical, self.reserved = physical, reserved
        return self
