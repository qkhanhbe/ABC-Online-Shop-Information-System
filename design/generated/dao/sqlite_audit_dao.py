from __future__ import annotations

from .audit_dao import AuditDAO


class SqliteAuditDAO(AuditDAO):

    def recent(self, limit: int) -> list[Map]:
        raise NotImplementedError

    def record(self, actor: str, action: str, entity: str, entity_id: str, detail: str) -> None:
        raise NotImplementedError
