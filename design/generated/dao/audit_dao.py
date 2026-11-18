from __future__ import annotations

from abc import ABC, abstractmethod


class AuditDAO(ABC):

    @abstractmethod
    def recent(self, limit: int) -> list[Map]:
        raise NotImplementedError

    @abstractmethod
    def record(self, actor: str, action: str, entity: str, entity_id: str, detail: str) -> None:
        raise NotImplementedError
