"""Service layer: UC13 Submit Review, UC18 Manage Reviews.

Human in the loop: a review that the AI flags as noise is not published automatically; it
waits for an Administrator (Chapter 3, fallback and human-control requirements).
"""
from model import order as states
from model.review import PENDING, PUBLISHED, REJECTED, Review
from service.auth_service import AuthService
from service.errors import NotFound, ValidationError


class ReviewService:

    def __init__(self, db, review_dao, order_dao, audit_dao, insight_service=None):
        self.db = db
        self.reviews = review_dao
        self.orders = order_dao
        self.audit = audit_dao
        self.insights = insight_service

    def submit(self, customer, order_id, product_id, rating, text):
        order = self.orders.get_order(order_id)
        if order is None or order.customer_id != customer.user_id:
            raise NotFound("order not found")
        if order.status != states.DELIVERED:
            raise ValidationError("only delivered purchases can be reviewed")
        if product_id not in {i.product_id for i in order.items}:
            raise ValidationError("this product is not part of the order")
        if self.reviews.exists(customer.user_id, product_id, order_id):
            raise ValidationError("this purchase has already been reviewed")
        review = Review(self.db.next_id("review", "R"), product_id, customer.user_id, order_id,
                        int(rating), text.strip(), PUBLISHED, self.db.now()).validate()
        if self.insights and self.insights.is_noise(review.text):
            review.status = PENDING
        self.reviews.save_review(review)
        return review

    def published(self, product_id):
        return self.reviews.for_product(product_id)

    def moderation_queue(self, admin):
        AuthService.require(admin, "moderate_reviews")
        return self.reviews.list_reviews(PENDING)

    def moderate(self, admin, review_id, approve):
        AuthService.require(admin, "moderate_reviews")
        review = next((r for r in self.reviews.list_reviews() if r.review_id == review_id), None)
        if review is None:
            raise NotFound("review not found")
        review.status = PUBLISHED if approve else REJECTED
        self.reviews.save_review(review)
        self.audit.record(admin.user_id, "moderate", "review", review_id, review.status)
        return review
