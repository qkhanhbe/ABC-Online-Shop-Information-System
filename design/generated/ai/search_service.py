from __future__ import annotations



class SearchService:

    def search(self, query: Map, k: int) -> list[Map]:
        raise NotImplementedError

    def search_text(self, terms: list[str], filters: Map) -> list[Map]:
        raise NotImplementedError

    def search_image(self, query_embedding: list[float], k: int) -> list[Map]:
        raise NotImplementedError

    def retrieve(self, query: Map) -> list[Map]:
        raise NotImplementedError

    def search_orders(self, query: Map) -> list[Order]:
        raise NotImplementedError
