"""Model: product Review (UC13 Submit Review, UC18 Manage Reviews).

A review is linked to the delivered order it comes from, which is what makes it credible.
"""
from dataclasses import dataclass

PENDING = "pending"
PUBLISHED = "published"
REJECTED = "rejected"


@dataclass
class Review:
    review_id: str
    product_id: str
    customer_id: str
    order_id: str
    rating: int
    text: str
    status: str = PUBLISHED
    created_at: str = ""

    def validate(self):
        if not 1 <= int(self.rating) <= 5:
            raise ValueError("rating must be between 1 and 5")
        if len(self.text.strip()) < 3:
            raise ValueError("review text is too short")
        return self
