from __future__ import annotations



class Request:

    def get(self, name: str, default: Object) -> str:
        raise NotImplementedError

    def session(self) -> Map:
        raise NotImplementedError
