from __future__ import annotations



class RecommenderService:

    def fit(self) -> None:
        raise NotImplementedError

    def similar(self, product_id: str, k: int) -> list[Map]:
        raise NotImplementedError

    def for_customer(self, customer_id: str, k: int) -> list[Map]:
        raise NotImplementedError
