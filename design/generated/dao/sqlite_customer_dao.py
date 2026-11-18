from __future__ import annotations

from .customer_dao import CustomerDAO


class SqliteCustomerDAO(CustomerDAO):

    def get_user(self, user_id: str) -> User:
        raise NotImplementedError

    def find_by_email(self, email: str) -> User:
        raise NotImplementedError

    def save_user(self, user: User) -> User:
        raise NotImplementedError

    def list_customers(self) -> list[User]:
        raise NotImplementedError
