from __future__ import annotations



class Response:

    def redirect(self, location: str, flash: str, request: Request) -> Response:
        raise NotImplementedError
