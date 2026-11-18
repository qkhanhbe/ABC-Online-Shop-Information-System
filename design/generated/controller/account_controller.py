from __future__ import annotations



class AccountController:

    def login_form(self, request: Request) -> Response:
        raise NotImplementedError

    def login(self, request: Request) -> Response:
        raise NotImplementedError

    def logout(self, request: Request) -> Response:
        raise NotImplementedError

    def register_form(self, request: Request) -> Response:
        raise NotImplementedError

    def register(self, request: Request) -> Response:
        raise NotImplementedError
