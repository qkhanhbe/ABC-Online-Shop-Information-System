from __future__ import annotations



class Milestone:

    def __init__(self, seq: int | None = None, code: str | None = None, at: str | None = None, location: str | None = None) -> None:
        self.seq: int | None = seq
        self.code: str | None = code
        self.at: str | None = at
        self.location: str | None = location
