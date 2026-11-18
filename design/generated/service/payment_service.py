from __future__ import annotations



class PaymentService:

    def request_payment(self, order: Order, card_token: str) -> Payment:
        raise NotImplementedError

    def handle_result(self, result: Map) -> Payment:
        raise NotImplementedError

    def succeeded(self, order_id: str) -> bool:
        raise NotImplementedError
