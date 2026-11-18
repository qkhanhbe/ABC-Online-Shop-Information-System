from __future__ import annotations



class AuthService:

    def register(self, name: str, email: str, password: str, address: Address) -> Customer:
        raise NotImplementedError

    def login(self, email: str, password: str) -> User:
        raise NotImplementedError

    def create_staff(self, user_id: str, name: str, email: str, password: str, role: str) -> User:
        raise NotImplementedError

    def require(self, user: User, permission: str) -> None:
        raise NotImplementedError
