from __future__ import annotations



class CheckoutService:

    def quote(self, customer_id: str, promo_code: str) -> Map:
        raise NotImplementedError

    def apply_promotion(self, code: str, subtotal: float) -> float:
        raise NotImplementedError

    def calc_shipping(self, amount: float) -> float:
        raise NotImplementedError

    def place_order(self, customer: Customer, promo_code: str, card_token: str, idempotency_key: str) -> Map:
        raise NotImplementedError
