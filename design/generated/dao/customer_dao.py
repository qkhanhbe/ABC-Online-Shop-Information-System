from __future__ import annotations

from abc import ABC, abstractmethod


class CustomerDAO(ABC):

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def save_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def list_customers(self) -> list[User]:
        raise NotImplementedError
