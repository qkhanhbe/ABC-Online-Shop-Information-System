from __future__ import annotations



class WebApp:

    def dispatch(self, request: Request) -> Response:
        raise NotImplementedError

    def static(self, path: str) -> Response:
        raise NotImplementedError
