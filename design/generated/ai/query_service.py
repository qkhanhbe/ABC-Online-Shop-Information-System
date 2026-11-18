from __future__ import annotations



class QueryService:

    def text_query(self, text: str) -> Map:
        raise NotImplementedError

    def voice_query(self, text: str) -> Map:
        raise NotImplementedError

    def image_query(self, embedding: list[float]) -> Map:
        raise NotImplementedError

    def multimodal_query(self, text: str, embedding: list[float], text_weight: float) -> Map:
        raise NotImplementedError

    def order_query(self, text: str, customer_id: str, mode: str) -> Map:
        raise NotImplementedError

    def is_order_question(self, text: str) -> bool:
        raise NotImplementedError
