"""Unit tests of the model classes: the business rules that live in the classes themselves."""
import pytest

from model.cart import Cart
from model.inventory import InventoryEvent, StockError, StockLevel
from model.order import InvalidTransition, Order
from model.product import Product, Promotion
from model.shipment import Milestone, Shipment

SHOES = Product("P01", "Nike Running Shoes", "shoes", "Nike", "black", 120)
CAP = Product("P09", "Blue Denim Cap", "cap", "Levis", "blue", 25)


def test_cart_adds_to_an_existing_line_and_totals_the_lines():
    cart = Cart("CART-C001", "C001")
    cart.add_item(SHOES, 1)
    cart.add_item(CAP, 2)
    cart.add_item(SHOES, 1)
    assert [(l.product_id, l.quantity) for l in cart.items] == [("P01", 2), ("P09", 2)]
    assert cart.calc_total() == 290
    cart.update_quantity("P09", 0)
    assert cart.calc_total() == 240


def test_order_follows_only_the_allowed_transitions():
    cart = Cart("CART-C001", "C001")
    cart.add_item(SHOES, 1)
    order = Order.create_from_cart("O100", cart, "addr", "2026-10-20 10:00:00", shipping_fee=0)
    assert order.status == "Payment Pending" and order.calc_total() == 120
    order.change_status("Paid/Confirmed", "psp", "t1")
    with pytest.raises(InvalidTransition):
        order.change_status("Shipped", "S01", "t2")          # Processing / Ready cannot be skipped
    order.change_status("Processing", "S01", "t3")
    assert [h.status for h in order.history] == ["Payment Pending", "Paid/Confirmed", "Processing"]


def test_stock_level_keeps_available_equal_physical_minus_reserved():
    s = StockLevel("P01", 5, 0)
    s.apply(InventoryEvent("E1", "P01", "RESERVE", 3, "O1"))
    assert (s.physical, s.reserved, s.available) == (5, 3, 2)
    s.apply(InventoryEvent("E2", "P01", "ISSUE", 3, "O1"))
    assert (s.physical, s.reserved, s.available) == (2, 0, 2)
    with pytest.raises(StockError):
        s.apply(InventoryEvent("E3", "P01", "RESERVE", 3, "O2"))
    with pytest.raises(StockError):
        s.apply(InventoryEvent("E4", "P01", "ADJUST", -1, "C1"))   # adjustment without reason
    assert s.available == 2                                         # unchanged after failures


def test_promotion_checks_dates_and_minimum_total():
    promo = Promotion("WELCOME10", 10, 50, "2026-10-01", "2026-12-31")
    assert promo.discount_for(100, "2026-10-20") == 10
    assert promo.discount_for(40, "2026-10-20") == 0
    assert promo.discount_for(100, "2027-01-01") == 0


def test_shipment_ignores_duplicate_and_older_milestones():
    sh = Shipment("SH1", "O1", "VNP1")
    assert sh.add_milestone(Milestone(1, "PICKED_UP", "t1"))
    assert sh.add_milestone(Milestone(2, "IN_TRANSIT", "t2"))
    assert not sh.add_milestone(Milestone(2, "IN_TRANSIT", "t2"))
    assert not sh.add_milestone(Milestone(1, "PICKED_UP", "t1"))
    assert sh.status == "IN_TRANSIT"
