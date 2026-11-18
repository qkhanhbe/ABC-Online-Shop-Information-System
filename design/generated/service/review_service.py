from __future__ import annotations



class ReviewService:

    def published(self, product_id: str) -> list[Review]:
        raise NotImplementedError

    def moderation_queue(self, admin: User) -> list[Review]:
        raise NotImplementedError

    def submit(self, customer: Customer, order_id: str, product_id: str, rating: int, text: str) -> Review:
        raise NotImplementedError

    def moderate(self, admin: User, review_id: str, approve: bool) -> Review:
        raise NotImplementedError
