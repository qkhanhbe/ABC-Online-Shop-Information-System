from __future__ import annotations



class StatusChange:

    def __init__(self, status: str | None = None, actor: str | None = None, at: str | None = None, note: str | None = None) -> None:
        self.status: str | None = status
        self.actor: str | None = actor
        self.at: str | None = at
        self.note: str | None = note
