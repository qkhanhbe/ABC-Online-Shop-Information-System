from __future__ import annotations



class Review:

    def __init__(self, review_id: str | None = None, product_id: str | None = None, customer_id: str | None = None, order_id: str | None = None, rating: int | None = None, text: str | None = None, status: str | None = None, created_at: str | None = None) -> None:
        self.review_id: str | None = review_id
        self.product_id: str | None = product_id
        self.customer_id: str | None = customer_id
        self.order_id: str | None = order_id
        self.rating: int | None = rating
        self.text: str | None = text
        self.status: str | None = status
        self.created_at: str | None = created_at

    def validate(self) -> None:
        raise NotImplementedError
