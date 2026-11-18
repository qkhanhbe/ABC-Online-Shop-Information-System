from __future__ import annotations



class User:

    def __init__(self, user_id: str | None = None, name: str | None = None, email: str | None = None, password_hash: str | None = None, role: str | None = None, created_at: str | None = None) -> None:
        self.user_id: str | None = user_id
        self.name: str | None = name
        self.email: str | None = email
        self.password_hash: str | None = password_hash
        self.role: str | None = role
        self.created_at: str | None = created_at

    def can(self, permission: str) -> bool:
        raise NotImplementedError
