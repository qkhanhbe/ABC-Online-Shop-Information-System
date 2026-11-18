from __future__ import annotations



class VectorIndex:

    def add(self, product_id: str, embedding: list[float]) -> None:
        raise NotImplementedError

    def search(self, query_embedding: list[float], k: int) -> list[Map]:
        raise NotImplementedError

    def build(self, storage: ImageStorage, products: list[Product], encode: Function) -> VectorIndex:
        raise NotImplementedError
