from __future__ import annotations



class Category:

    def __init__(self, category_id: str | None = None, name: str | None = None, detail_kind: str | None = None) -> None:
        self.category_id: str | None = category_id
        self.name: str | None = name
        self.detail_kind: str | None = detail_kind
