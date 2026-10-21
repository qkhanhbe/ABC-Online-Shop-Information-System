"""UC11 Track, UC12 Cancel, UC19 Process Orders, UC20 Inventory, UC21-23 Shipment, UC13/18 Reviews,
UC25-28 Reports - including role checks (NFR05)."""
import pytest

from service.errors import NotFound, PermissionDenied, ValidationError


def test_customer_only_tracks_own_orders(shop):
    assert shop.orders.track("C001", "O001")["status"] == "Delivered"
    with pytest.raises(NotFound):
        shop.orders.track("C001", "O002")                 # belongs to C002: looks like "not found"


def test_cancel_releases_the_reservation_and_notes_a_refund(shop, users):
    before = shop.inventory.stock_of("P07").available
    order = shop.orders.cancel(users["C001"], "O016")     # Paid/Confirmed: P07 x1, P03 x1
    assert order.status == "Cancelled"
    assert shop.inventory.stock_of("P07").available == before + 1
    assert any(a["action"] == "refund_initiated" for a in shop.dao.audit.recent())
    with pytest.raises(ValidationError):
        shop.orders.cancel(users["C001"], "O001")         # already delivered


def test_processing_needs_staff_role_and_a_paid_order(shop, users):
    with pytest.raises(PermissionDenied):
        shop.orders.start_processing(users["C001"], "O016")
    assert shop.orders.start_processing(users["S01"], "O016").status == "Processing"
    with pytest.raises(ValidationError):
        shop.orders.start_processing(users["S01"], "O001")   # Delivered -> Processing is invalid


def test_full_fulfilment_path_and_milestones(shop, users):
    shop.orders.start_processing(users["S01"], "O016")
    shop.shipping.mark_packed(users["W01"], "O016")
    ref = shop.shipping.arrange_delivery(users["W01"], "O016").carrier_ref
    assert shop.shipping.on_milestone(ref, 1, "PICKED_UP", "2026-10-20 10:00:00")
    assert not shop.shipping.on_milestone(ref, 1, "PICKED_UP", "2026-10-20 10:00:00")
    assert shop.shipping.on_milestone(ref, 2, "DELIVERED", "2026-10-21 09:00:00")
    assert shop.orders.track("C001", "O016")["status"] == "Delivered"
    assert not shop.shipping.on_milestone("UNKNOWN", 1, "PICKED_UP", "t")


def test_inventory_events_are_idempotent_and_never_negative(shop, users):
    w = users["W01"]
    first = shop.inventory.manual_event(w, "P05", "RECEIPT", 10, "GRN-77")
    again = shop.inventory.manual_event(w, "P05", "RECEIPT", 10, "GRN-77")
    assert again["event"].event_id == first["event"].event_id
    assert shop.inventory.stock_of("P05").physical == 10
    with pytest.raises(ValidationError):
        shop.inventory.manual_event(w, "P05", "ADJUST", -20, "CNT-1", "stock count")
    with pytest.raises(PermissionDenied):
        shop.inventory.manual_event(users["S01"], "P05", "RECEIPT", 1, "GRN-78")


def test_low_stock_and_replenishment(shop, users):
    low = [p.product_id for p, _ in shop.inventory.low_stock()]
    assert "P05" in low and "P15" in low
    rq = shop.inventory.request_replenishment(users["W01"], "P05", 20)
    assert rq.startswith("RQ") and shop.dao.inventory.open_replenishments()[0]["product_id"] == "P05"


def test_reviews_only_for_delivered_purchases_and_spam_waits_for_moderation(shop, users):
    with pytest.raises(ValidationError):
        shop.reviews.submit(users["C001"], "O016", "P07", 5, "great")          # not delivered
    with pytest.raises(ValidationError):
        shop.reviews.submit(users["C001"], "O001", "P01", 5, "again!")         # already reviewed
    pending = shop.reviews.moderation_queue(users["A01"])
    assert [r.review_id for r in pending] == ["R012"]
    assert shop.reviews.moderate(users["A01"], "R012", approve=False).status == "rejected"


def test_reports_are_for_managers_and_match_the_orders(shop, users):
    with pytest.raises(PermissionDenied):
        shop.reports.dashboard(users["C001"])
    d = shop.reports.dashboard(users["M01"])
    assert d["orders"] == 16 and d["exceptions"] == 2
    sales = shop.reports.sales_report(users["M01"])
    assert round(sum(sales["by_day"].values()), 2) == d["revenue"]
