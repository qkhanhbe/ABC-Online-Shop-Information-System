"""UC08 Place Order and UC09 Make Payment: main flow, alternatives and exceptions of A02 8.1-8.2."""
import pytest

from model.customer import Address
from service.errors import CheckoutError
from service.gateways import sign


def stock(shop, pid):
    return shop.inventory.stock_of(pid)


def test_successful_checkout_reserves_stock_pays_and_clears_cart(shop, users):
    shop.cart.add_item("C001", "P12", 1)
    before = stock(shop, "P12").available
    result = shop.checkout.place_order(users["C001"], "", "tok_visa")
    order = result["order"]
    assert result["payment"] == "Succeeded" and order.status == "Paid/Confirmed"
    assert stock(shop, "P12").available == before - 1 and stock(shop, "P12").reserved >= 1
    assert shop.cart.view("C001").is_empty()
    assert [h.status for h in order.history] == ["Payment Pending", "Paid/Confirmed"]


def test_promotion_and_shipping_are_part_of_the_authoritative_total(shop):
    shop.cart.add_item("C001", "P11", 1)                 # 55
    quote = shop.checkout.quote("C001", "WELCOME10")
    assert (quote["subtotal"], quote["discount"], quote["shipping"], quote["total"]) == (55, 5.5, 5.0, 54.5)
    assert shop.checkout.quote("C001", "SUMMER20")["discount"] == 0       # expired: A4
    assert "does not exist" in shop.checkout.quote("C001", "NOPE")["promo_note"]


def test_repeated_submission_returns_the_same_order(shop, users):
    shop.cart.add_item("C001", "P09", 1)
    first = shop.checkout.place_order(users["C001"], idempotency_key="k-1")
    second = shop.checkout.place_order(users["C001"], idempotency_key="k-1")
    assert second["duplicate"] and second["order"].order_id == first["order"].order_id
    assert len(shop.dao.payments.for_order(first["order"].order_id)) == 1


def test_declined_payment_releases_reservation_and_keeps_cart(shop, users):
    shop.cart.add_item("C001", "P10", 1)
    before = stock(shop, "P10").available
    result = shop.checkout.place_order(users["C001"], "", "tok_declined")
    assert result["order"].status == "Payment Failed"
    assert stock(shop, "P10").available == before
    assert [l.product_id for l in shop.cart.view("C001").items] == ["P10"]


def test_timeout_keeps_order_pending_and_reserved(shop, users):
    shop.cart.add_item("C001", "P10", 1)
    before = stock(shop, "P10").available
    result = shop.checkout.place_order(users["C001"], "", "tok_timeout")
    assert result["order"].status == "Payment Pending"
    assert stock(shop, "P10").available == before - 1


def test_insufficient_stock_stops_checkout_without_side_effects(shop, users):
    shop.cart.add_item("C001", "P15", 3)                 # P15 has 3 available
    shop.inventory.record("P15", "RESERVE", 2, "OTHER-ORDER")
    orders_before = len(shop.dao.orders.list_orders())
    with pytest.raises(CheckoutError) as err:
        shop.checkout.place_order(users["C001"])
    assert "only 1 available" in str(err.value)
    assert len(shop.dao.orders.list_orders()) == orders_before


def test_changed_price_is_reported_before_payment(shop, users):
    shop.cart.add_item("C001", "P09", 1)
    shop.catalog.change_price(users["A01"], "P09", 27)
    with pytest.raises(CheckoutError) as err:
        shop.checkout.place_order(users["C001"])
    assert "price changed 25.0 -> 27" in str(err.value)
    assert shop.cart.view("C001").items[0].cart_price == 27  # customer now confirms the real price


def test_incomplete_address_is_rejected(shop, users):
    customer = users["C001"]
    customer.address = Address("Khanh", "", "", "Ha Noi")
    shop.cart.add_item("C001", "P09", 1)
    with pytest.raises(CheckoutError):
        shop.checkout.place_order(customer)


def test_payment_callbacks_are_verified_and_idempotent(shop, users):
    shop.cart.add_item("C001", "P10", 1)
    order = shop.checkout.place_order(users["C001"], "", "tok_timeout")["order"]
    attempt = shop.dao.payments.for_order(order.order_id)[0]
    good = {"attempt_ref": attempt.attempt_ref, "status": "SUCCEEDED", "provider_ref": "PSP-X",
            "amount": attempt.amount, "currency": "USD"}
    forged = dict(good, signature="0000")
    assert shop.payment.handle_result(forged) == "Rejected"                       # E2
    wrong_amount = dict(good, amount=1.0)
    wrong_amount["signature"] = sign(attempt.attempt_ref, "SUCCEEDED", "PSP-X", 1.0, "USD")
    assert shop.payment.handle_result(wrong_amount) == "Quarantined"              # E1
    assert shop.dao.orders.get_order(order.order_id).status == "Payment Pending"
    good["signature"] = sign(attempt.attempt_ref, "SUCCEEDED", "PSP-X", attempt.amount, "USD")
    assert shop.payment.handle_result(good) == "Succeeded"
    assert shop.payment.handle_result(good) == "Succeeded"                        # A3 duplicate
    history = shop.dao.orders.get_order(order.order_id).history
    assert [h.status for h in history].count("Paid/Confirmed") == 1
