from __future__ import annotations



class ImageStorage:

    def path(self, relative: str) -> str:
        raise NotImplementedError

    def exists(self, relative: str) -> bool:
        raise NotImplementedError

    def save_upload(self, filename: str, content: Bytes) -> str:
        raise NotImplementedError
