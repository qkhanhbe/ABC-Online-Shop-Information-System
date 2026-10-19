"""Service layer: UC09 Make Payment.

  * one payment attempt = one unique attempt_ref (BR09-02)
  * a provider result changes the order only if its signature, reference, amount and
    currency match (E1/E2), and only once (A3 "duplicate callback")
  * no answer = Payment Pending, never "please pay again" (A2 "timeout")
"""
from model import order as states
from model.payment import FAILED, PENDING, SUCCEEDED, Payment
from service.gateways import sign


class PaymentService:

    def __init__(self, db, payment_dao, order_dao, inventory_service, gateway, audit_dao):
        self.db = db
        self.payments = payment_dao
        self.orders = order_dao
        self.inventory = inventory_service
        self.gateway = gateway
        self.audit = audit_dao

    def request_payment(self, order, card_token):
        payment = Payment(self.db.next_id("payment", "PAY"), order.order_id,
                          f"{order.order_id}-A{len(self.payments.for_order(order.order_id)) + 1}",
                          order.calc_total(), "USD", PENDING, "", self.db.now())
        self.payments.save_payment(payment)
        result = self.gateway.authorize(payment.attempt_ref, payment.amount, payment.currency,
                                        card_token)
        if result is None:                                   # A2 timeout
            self.audit.record("payment", "timeout", "payment", payment.attempt_ref)
            return PENDING
        return self.handle_result(result)

    def handle_result(self, result):
        """Provider callback. Returns the payment status after the result is applied."""
        payment = self.payments.get_by_attempt(result.get("attempt_ref", ""))
        expected = sign(result.get("attempt_ref"), result.get("status"), result.get("provider_ref"),
                        result.get("amount"), result.get("currency"))
        if payment is None or result.get("signature") != expected:
            self.audit.record("payment", "rejected_callback", "payment",
                              str(result.get("attempt_ref")), "unknown or unsigned result")
            return "Rejected"                                # E2: no state change
        if not payment.matches(result["attempt_ref"], result["amount"], result["currency"]):
            self.audit.record("payment", "quarantined", "payment", payment.attempt_ref,
                              "amount or currency mismatch")
            return "Quarantined"                             # E1: no state change
        if payment.is_final():
            return payment.status                            # A3: duplicate, no second effect

        order = self.orders.get_order(payment.order_id)
        with self.db.transaction():
            payment.provider_ref = result["provider_ref"]
            if result["status"] == "SUCCEEDED":
                payment.status = SUCCEEDED
                if order.status == states.PAYMENT_PENDING:
                    order.change_status(states.PAID, "payment-provider", self.db.now(),
                                        f"paid {payment.amount} {payment.currency} ref {payment.provider_ref}")
                else:                                        # A4 late success on a closed order
                    self.audit.record("payment", "refund_needed", "order", order.order_id,
                                      "late payment success")
            else:
                payment.status = FAILED
                if order.status == states.PAYMENT_PENDING:
                    order.change_status(states.PAYMENT_FAILED, "payment-provider", self.db.now(),
                                        "payment declined")
                    self.inventory.release_order(order)
            self.payments.save_payment(payment)
            self.orders.save_order(order)
        return payment.status

    def succeeded(self, order_id):
        return any(p.status == SUCCEEDED for p in self.payments.for_order(order_id))
