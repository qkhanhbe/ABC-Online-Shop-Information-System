from __future__ import annotations



class Promotion:

    def __init__(self, code: str | None = None, percent: float | None = None, min_total: float | None = None, start_date: str | None = None, end_date: str | None = None, active: bool | None = None) -> None:
        self.code: str | None = code
        self.percent: float | None = percent
        self.min_total: float | None = min_total
        self.start_date: str | None = start_date
        self.end_date: str | None = end_date
        self.active: bool | None = active

    def is_valid(self, subtotal: float, today: str) -> bool:
        raise NotImplementedError

    def discount_for(self, subtotal: float, today: str) -> float:
        raise NotImplementedError
