from __future__ import annotations



class Database:

    def init_schema(self) -> None:
        raise NotImplementedError

    def now(self) -> str:
        raise NotImplementedError

    def transaction(self) -> Database:
        raise NotImplementedError

    def next_id(self, name: str, prefix: str, width: int) -> str:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def execute(self, sql: str, params: list[Object]) -> Cursor:
        raise NotImplementedError

    def query(self, sql: str, params: list[Object]) -> list[Map]:
        raise NotImplementedError

    def query_one(self, sql: str, params: list[Object]) -> Map:
        raise NotImplementedError
