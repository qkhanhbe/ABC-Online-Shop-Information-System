"""Creates the demo database: catalogue, accounts, and one month of order history.

The history is not inserted into the tables directly: it is played through the real services
(checkout, payment, processing, packing, carrier milestones, reviews), so every row in the
database was produced by the same rules a real customer would go through.

    python seed.py            -> data/abc_shop.db
"""
import json
import os
from datetime import datetime, timedelta

from model.customer import Address
from model.inventory import StockLevel
from model.product import Category, Product, Promotion
from shop import build_shop

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "data", "abc_shop.db")


class SimClock:
    """Simulated time, so the seeded history spans October 2026."""

    def __init__(self, start="2026-10-01 08:30:00"):
        self.t = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")

    def __call__(self):
        return self.t.strftime("%Y-%m-%d %H:%M:%S")

    def set_day(self, day, hour=9):
        self.t = datetime(2026, 10, day, hour, 5)

    def tick(self, minutes=17):
        self.t += timedelta(minutes=minutes)


# day, customer, [(product, qty)], promo, card token, final state, reviews {product: (rating, text)}
HISTORY = [
    (2, "C001", [("P01", 1), ("P09", 1)], "", "tok_visa", "Delivered", {
        "P01": (5, "Great running shoes, very comfortable and the sole feels durable. Fast delivery."),
        "P09": (4, "Nice cap, good quality denim but the price is a bit high.")}),
    (3, "C002", [("P03", 1), ("P07", 2)], "", "tok_visa", "Delivered", {
        "P03": (5, "Beautiful leather and solid stitching. Worth the money."),
        "P07": (4, "Soft fabric, fits well. Shipping was quick.")}),
    (4, "C003", [("P01", 1), ("P07", 1)], "WELCOME10", "tok_visa", "Delivered", {
        "P01": (3, "Comfortable shoes but delivery was late by four days."),
        "P07": (2, "The colour faded after two washes, poor quality.")}),
    (6, "C004", [("P12", 1)], "", "tok_declined", "Payment Failed", {}),
    (7, "C002", [("P02", 1), ("P09", 1)], "", "tok_visa", "Delivered", {
        "P02": (2, "Shoes are ok but the package arrived damaged and support never answered."),
        "P09": (5, "Love it, great value for the price.")}),
    (8, "C004", [("P01", 1), ("P03", 1)], "WELCOME10", "tok_visa", "Delivered", {
        "P01": (4, "Good quality for running, not cheap but worth it."),
        "P03": (2, "The strap is not durable and customer service was rude.")}),
    (9, "C001", [("P11", 1)], "WELCOME10", "tok_visa", "Delivered", {
        "P11": (5, "Excellent watch, the metal strap feels solid. Friendly and helpful staff.")}),
    (10, "C003", [("P07", 3), ("P13", 2)], "", "tok_visa", "Delivered", {
        "P07": (5, "Click www.free-money-now.biz for cheap shirts!!!"),
        "P13": (4, "Nice and soft t-shirt, affordable price.")}),
    (12, "C003", [("P10", 1)], "", "tok_visa", "Processing", {}),
    (13, "C002", [("P01", 1)], "", "tok_visa", "Delivered", {
        "P01": (5, "Perfect fit and excellent quality. Delivery was fast.")}),
    (14, "C004", [("P06", 1), ("P14", 1)], "", "tok_visa", "Shipped", {}),
    (15, "C001", [("P13", 2)], "", "tok_visa", "Cancelled", {}),
    (16, "C002", [("P15", 1)], "", "tok_timeout", "Payment Pending", {}),
    (17, "C003", [("P08", 1)], "", "tok_visa", "On Hold", {}),
    (18, "C004", [("P16", 1), ("P11", 1)], "", "tok_visa", "Ready for Shipment", {}),
    (19, "C001", [("P07", 1), ("P03", 1)], "", "tok_visa", "Paid/Confirmed", {}),
]

PATH = ["Paid/Confirmed", "Processing", "Ready for Shipment", "Shipped", "Delivered"]


def load_catalogue(shop, data, clock):
    db = shop.db
    with db.transaction():
        for c in data["categories"]:
            shop.dao.products.save_category(Category(c["id"], c["name"]))
        for p in data["products"]:
            shop.dao.products.save_product(Product(p["id"], p["name"], p["category"], p["brand"],
                                                    p["color"], p["price"], p["description"],
                                                    p["image"]))
            shop.dao.inventory.save_stock(StockLevel(p["id"], 0, 0, 3))
    for p in data["products"]:
        if p["stock"]:
            shop.inventory.record(p["id"], "RECEIPT", p["stock"], "GRN-INIT-" + p["id"],
                                  "opening stock", "W01")
    for pr in data["promotions"]:
        shop.dao.promotions.save_promotion(Promotion(pr["code"], pr["percent"], pr["min_total"],
                                                     pr["start"], pr["end"]))


def load_accounts(shop, data):
    for c in data["customers"]:
        customer = shop.auth.register(c["name"], c["email"], c["password"], Address(*c["address"]))
        assert customer.user_id == c["id"], (customer.user_id, c["id"])
    for s in data["staff"]:
        shop.auth.create_staff(s["id"], s["name"], s["email"], s["password"], s["role"])


def play_order(shop, clock, entry):
    day, cid, items, promo, token, final, reviews = entry
    users = shop.dao.customers
    sales, warehouse = users.get_user("S01"), users.get_user("W01")
    customer = users.get_user(cid)
    clock.set_day(day, 9 + day % 8)
    for pid, qty in items:
        shop.cart.add_item(cid, pid, qty)
        clock.tick(3)
    result = shop.checkout.place_order(customer, promo, token)
    order = result["order"]
    clock.tick()
    if final in ("Payment Failed", "Payment Pending"):
        if final == "Payment Failed":                    # the customer gives up; empty the cart
            cart = shop.dao.carts.get_cart(cid)
            cart.clear()
            shop.dao.carts.update_cart(cart)
        return order
    if final == "Cancelled":
        return shop.orders.cancel(customer, order.order_id, "changed my mind")
    if final == "On Hold":
        return shop.orders.hold(sales, order.order_id, "address needs phone confirmation")
    target = PATH.index(final)
    if target >= 1:
        clock.tick(95)
        shop.orders.start_processing(sales, order.order_id)
    if target >= 2:
        clock.tick(120)
        shop.shipping.mark_packed(warehouse, order.order_id)
    if target >= 3:
        clock.tick(60)
        ref = shop.shipping.arrange_delivery(warehouse, order.order_id).carrier_ref
        clock.tick(45)
        shop.shipping.on_milestone(ref, 1, "PICKED_UP", clock(), "ABC warehouse, Ha Noi")
        clock.tick(60 * 20)
        shop.shipping.on_milestone(ref, 2, "IN_TRANSIT", clock(), "Sorting hub")
    if target >= 4:
        clock.tick(60 * 22)
        shop.shipping.on_milestone(ref, 3, "DELIVERED", clock(), "Receiver signed")
        for pid, (rating, text) in reviews.items():
            clock.tick(60 * 26)
            shop.reviews.submit(customer, order.order_id, pid, rating, text)
    return shop.dao.orders.get_order(order.order_id)


def seed(db_path=DB_PATH, verbose=True):
    if db_path != ":memory:" and os.path.exists(db_path):
        os.remove(db_path)
    clock = SimClock()
    shop = build_shop(db_path, clock)
    with open(os.path.join(HERE, "data", "seed.json"), encoding="utf-8") as f:
        data = json.load(f)
    load_catalogue(shop, data, clock)
    shop.rebuild_index()
    load_accounts(shop, data)
    for entry in HISTORY:
        order = play_order(shop, clock, entry)
        if verbose:
            print(f"  {order.created_at[:10]}  {order.order_id}  {order.customer_id}  "
                  f"{order.calc_total():>7.2f}  {order.status}")
    shop.recommender.fit()
    return shop


if __name__ == "__main__":
    print("Seeding", DB_PATH)
    seed()
    print("done")
