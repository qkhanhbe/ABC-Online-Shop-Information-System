"""DAO layer: SQLite implementations of the interfaces in interfaces.py.

Each class maps rows to model objects and back; none of them contains a business rule.
"""
from model.cart import Cart, CartItem
from model.customer import Address, Customer, User
from model.inventory import InventoryEvent, StockLevel
from model.order import Order, OrderItem, StatusChange
from model.payment import Payment
from model.product import Category, Product, Promotion
from model.review import Review
from model.shipment import Milestone, Shipment

from dao import interfaces


class SqliteCustomerDAO(interfaces.CustomerDAO):

    def __init__(self, db):
        self.db = db

    def _to_user(self, row):
        if row is None:
            return None
        if row["role"] != "customer":
            return User(row["user_id"], row["name"], row["email"], row["password_hash"], row["role"])
        a = self.db.query_one("SELECT * FROM address WHERE customer_id = ?", (row["user_id"],))
        address = Address(a["receiver"], a["phone"], a["street"], a["city"]) if a else None
        return Customer(row["user_id"], row["name"], row["email"], row["password_hash"],
                        "customer", address, row["created_at"])

    def get_user(self, user_id):
        return self._to_user(self.db.query_one("SELECT * FROM users WHERE user_id = ?", (user_id,)))

    def find_by_email(self, email):
        return self._to_user(self.db.query_one("SELECT * FROM users WHERE email = ?",
                                               (email.strip().lower(),)))

    def save_user(self, user):
        with self.db.transaction():
            self.db.execute(
                "INSERT INTO users(user_id, name, email, password_hash, role, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET "
                "name = excluded.name, email = excluded.email, password_hash = excluded.password_hash",
                (user.user_id, user.name, user.email.lower(), user.password_hash, user.role,
                 getattr(user, "created_at", "") or self.db.now()))
            address = getattr(user, "address", None)
            if address is not None:
                self.db.execute(
                    "INSERT OR REPLACE INTO address(customer_id, receiver, phone, street, city) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (user.user_id, address.receiver, address.phone, address.street, address.city))
        return user

    def list_customers(self):
        rows = self.db.query("SELECT * FROM users WHERE role = 'customer' ORDER BY user_id")
        return [self._to_user(r) for r in rows]


class SqliteProductDAO(interfaces.ProductDAO):

    def __init__(self, db):
        self.db = db

    @staticmethod
    def _to_product(row):
        if row is None:
            return None
        return Product(row["product_id"], row["name"], row["category_id"], row["brand"],
                       row["color"], row["price"], row["description"], row["image"], row["status"])

    def get_product(self, product_id):
        return self._to_product(self.db.query_one(
            "SELECT * FROM product WHERE product_id = ?", (product_id,)))

    def list_products(self, category_id=None, active_only=True):
        sql, params = "SELECT * FROM product WHERE 1 = 1", []
        if category_id:
            sql += " AND category_id = ?"
            params.append(category_id)
        if active_only:
            sql += " AND status = 'active'"
        return [self._to_product(r) for r in self.db.query(sql + " ORDER BY product_id", params)]

    def save_product(self, p):
        self.db.execute(
            "INSERT OR REPLACE INTO product(product_id, name, category_id, brand, color, price, "
            "description, image, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p.product_id, p.name, p.category_id, p.brand, p.color, p.price, p.description,
             p.image, p.status))
        return p

    def list_categories(self):
        return [Category(r["category_id"], r["name"])
                for r in self.db.query("SELECT * FROM category ORDER BY name")]

    def save_category(self, c):
        self.db.execute("INSERT OR REPLACE INTO category(category_id, name) VALUES (?, ?)",
                        (c.category_id, c.name))
        return c


class SqliteInventoryDAO(interfaces.InventoryDAO):

    def __init__(self, db):
        self.db = db

    def get_stock(self, product_id):
        r = self.db.query_one("SELECT * FROM stock_level WHERE product_id = ?", (product_id,))
        if r is None:
            return StockLevel(product_id, 0, 0)
        return StockLevel(r["product_id"], r["physical"], r["reserved"], r["threshold"])

    def save_stock(self, s):
        self.db.execute(
            "INSERT OR REPLACE INTO stock_level(product_id, physical, reserved, threshold) "
            "VALUES (?, ?, ?, ?)", (s.product_id, s.physical, s.reserved, s.threshold))
        return s

    @staticmethod
    def _to_event(r):
        return InventoryEvent(r["event_id"], r["product_id"], r["kind"], r["quantity"],
                              r["reference"], r["reason"], r["created_at"])

    def find_event(self, product_id, kind, reference):
        r = self.db.query_one("SELECT * FROM inventory_event WHERE product_id = ? AND kind = ? "
                              "AND reference = ?", (product_id, kind, reference))
        return self._to_event(r) if r else None

    def add_event(self, e):
        self.db.execute(
            "INSERT INTO inventory_event(event_id, product_id, kind, quantity, reference, reason, "
            "created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (e.event_id, e.product_id, e.kind, e.quantity, e.reference, e.reason, e.created_at))
        return e

    def events_for(self, product_id, limit=10):
        rows = self.db.query("SELECT * FROM inventory_event WHERE product_id = ? "
                             "ORDER BY created_at DESC, event_id DESC LIMIT ?", (product_id, limit))
        return [self._to_event(r) for r in rows]

    def add_replenishment(self, request_id, product_id, quantity, at):
        self.db.execute("INSERT INTO replenishment_request(request_id, product_id, quantity, "
                        "status, created_at) VALUES (?, ?, ?, 'Requested', ?)",
                        (request_id, product_id, quantity, at))
        return request_id

    def open_replenishments(self):
        return [dict(r) for r in self.db.query(
            "SELECT * FROM replenishment_request WHERE status = 'Requested' ORDER BY request_id")]


class SqliteCartDAO(interfaces.CartDAO):

    def __init__(self, db):
        self.db = db

    def get_cart(self, customer_id):
        """The cart is created on first use: every customer has exactly one cart."""
        r = self.db.query_one("SELECT * FROM cart WHERE customer_id = ?", (customer_id,))
        if r is None:
            cart_id = "CART-" + customer_id
            self.db.execute("INSERT INTO cart(cart_id, customer_id) VALUES (?, ?)",
                            (cart_id, customer_id))
            return Cart(cart_id, customer_id)
        rows = self.db.query("SELECT * FROM cart_item WHERE cart_id = ? ORDER BY rowid",
                             (r["cart_id"],))
        items = [CartItem(i["product_id"], i["name"], i["cart_price"], i["quantity"]) for i in rows]
        return Cart(r["cart_id"], customer_id, items)

    def update_cart(self, cart):
        with self.db.transaction():
            self.db.execute("DELETE FROM cart_item WHERE cart_id = ?", (cart.cart_id,))
            for line in cart.items:
                self.db.execute("INSERT INTO cart_item(cart_id, product_id, name, cart_price, "
                                "quantity) VALUES (?, ?, ?, ?, ?)",
                                (cart.cart_id, line.product_id, line.name, line.cart_price,
                                 line.quantity))
        return cart


class SqlitePromotionDAO(interfaces.PromotionDAO):

    def __init__(self, db):
        self.db = db

    @staticmethod
    def _to_promotion(r):
        return Promotion(r["code"], r["percent"], r["min_total"], r["start_date"], r["end_date"],
                         bool(r["active"]))

    def get_promotion(self, code):
        r = self.db.query_one("SELECT * FROM promotion WHERE code = ?", (code.strip().upper(),))
        return self._to_promotion(r) if r else None

    def save_promotion(self, p):
        self.db.execute("INSERT OR REPLACE INTO promotion(code, percent, min_total, start_date, "
                        "end_date, active) VALUES (?, ?, ?, ?, ?, ?)",
                        (p.code.upper(), p.percent, p.min_total, p.start, p.end, int(p.active)))
        return p

    def list_promotions(self):
        return [self._to_promotion(r) for r in self.db.query("SELECT * FROM promotion")]


class SqliteOrderDAO(interfaces.OrderDAO):

    def __init__(self, db):
        self.db = db

    def _to_order(self, r):
        if r is None:
            return None
        items = [OrderItem(i["product_id"], i["name"], i["unit_price"], i["quantity"])
                 for i in self.db.query("SELECT * FROM order_item WHERE order_id = ? ORDER BY rowid",
                                        (r["order_id"],))]
        history = [StatusChange(h["status"], h["actor"], h["at"], h["note"])
                   for h in self.db.query("SELECT * FROM order_status_history WHERE order_id = ? "
                                          "ORDER BY id", (r["order_id"],))]
        return Order(r["order_id"], r["customer_id"], r["address"], items, r["discount"],
                     r["shipping_fee"], r["status"], r["created_at"], r["promo_code"],
                     r["idempotency_key"] or "", history)

    def get_order(self, order_id):
        return self._to_order(self.db.query_one(
            "SELECT * FROM customer_order WHERE order_id = ?", (order_id.upper(),)))

    def find_by_idempotency_key(self, key):
        return self._to_order(self.db.query_one(
            "SELECT * FROM customer_order WHERE idempotency_key = ?", (key,)))

    def find_by_customer(self, customer_id):
        rows = self.db.query("SELECT * FROM customer_order WHERE customer_id = ? "
                             "ORDER BY created_at DESC, order_id DESC", (customer_id,))
        return [self._to_order(r) for r in rows]

    def find_by_status(self, *statuses):
        marks = ",".join("?" * len(statuses))
        rows = self.db.query(f"SELECT * FROM customer_order WHERE status IN ({marks}) "
                             "ORDER BY created_at, order_id", statuses)
        return [self._to_order(r) for r in rows]

    def save_order(self, o):
        """Insert or update; status history rows are appended, never rewritten."""
        with self.db.transaction():
            self.db.execute(
                "INSERT INTO customer_order(order_id, customer_id, address, discount, shipping_fee, "
                "total, status, created_at, promo_code, idempotency_key) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(order_id) DO UPDATE SET "
                "status = excluded.status",
                (o.order_id, o.customer_id, o.address, o.discount, o.shipping_fee, o.calc_total(),
                 o.status, o.created_at, o.promo_code, o.idempotency_key or None))
            if not self.db.query_one("SELECT 1 FROM order_item WHERE order_id = ?", (o.order_id,)):
                for i in o.items:
                    self.db.execute("INSERT INTO order_item(order_id, product_id, name, unit_price, "
                                    "quantity) VALUES (?, ?, ?, ?, ?)",
                                    (o.order_id, i.product_id, i.name, i.unit_price, i.quantity))
            stored = self.db.query_one("SELECT COUNT(*) AS n FROM order_status_history "
                                       "WHERE order_id = ?", (o.order_id,))["n"]
            for h in o.history[stored:]:
                self.db.execute("INSERT INTO order_status_history(order_id, status, actor, at, note) "
                                "VALUES (?, ?, ?, ?, ?)", (o.order_id, h.status, h.actor, h.at, h.note))
        return o

    def list_orders(self):
        return [self._to_order(r) for r in self.db.query(
            "SELECT * FROM customer_order ORDER BY created_at, order_id")]


class SqlitePaymentDAO(interfaces.PaymentDAO):

    def __init__(self, db):
        self.db = db

    @staticmethod
    def _to_payment(r):
        return Payment(r["payment_id"], r["order_id"], r["attempt_ref"], r["amount"], r["currency"],
                       r["status"], r["provider_ref"], r["created_at"])

    def get_by_attempt(self, attempt_ref):
        r = self.db.query_one("SELECT * FROM payment WHERE attempt_ref = ?", (attempt_ref,))
        return self._to_payment(r) if r else None

    def for_order(self, order_id):
        return [self._to_payment(r) for r in self.db.query(
            "SELECT * FROM payment WHERE order_id = ? ORDER BY payment_id", (order_id,))]

    def save_payment(self, p):
        self.db.execute("INSERT OR REPLACE INTO payment(payment_id, order_id, attempt_ref, amount, "
                        "currency, status, provider_ref, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (p.payment_id, p.order_id, p.attempt_ref, p.amount, p.currency, p.status,
                         p.provider_ref, p.created_at))
        return p


class SqliteShipmentDAO(interfaces.ShipmentDAO):

    def __init__(self, db):
        self.db = db

    def _to_shipment(self, r):
        if r is None:
            return None
        milestones = [Milestone(m["seq"], m["code"], m["at"], m["location"])
                      for m in self.db.query("SELECT * FROM shipment_milestone WHERE shipment_id = ? "
                                             "ORDER BY seq", (r["shipment_id"],))]
        return Shipment(r["shipment_id"], r["order_id"], r["carrier_ref"], r["status"], milestones)

    def get_by_order(self, order_id):
        return self._to_shipment(self.db.query_one(
            "SELECT * FROM shipment WHERE order_id = ?", (order_id,)))

    def get_by_carrier_ref(self, carrier_ref):
        return self._to_shipment(self.db.query_one(
            "SELECT * FROM shipment WHERE carrier_ref = ?", (carrier_ref,)))

    def save_shipment(self, s):
        with self.db.transaction():
            self.db.execute("INSERT OR REPLACE INTO shipment(shipment_id, order_id, carrier_ref, "
                            "status) VALUES (?, ?, ?, ?)",
                            (s.shipment_id, s.order_id, s.carrier_ref, s.status))
            for m in s.milestones:
                self.db.execute("INSERT OR IGNORE INTO shipment_milestone(shipment_id, seq, code, at, "
                                "location) VALUES (?, ?, ?, ?, ?)",
                                (s.shipment_id, m.seq, m.code, m.at, m.location))
        return s


class SqliteReviewDAO(interfaces.ReviewDAO):

    def __init__(self, db):
        self.db = db

    @staticmethod
    def _to_review(r):
        return Review(r["review_id"], r["product_id"], r["customer_id"], r["order_id"], r["rating"],
                      r["text"], r["status"], r["created_at"])

    def for_product(self, product_id, status="published"):
        return [self._to_review(r) for r in self.db.query(
            "SELECT * FROM review WHERE product_id = ? AND status = ? ORDER BY created_at DESC",
            (product_id, status))]

    def exists(self, customer_id, product_id, order_id):
        return self.db.query_one("SELECT 1 FROM review WHERE customer_id = ? AND product_id = ? "
                                 "AND order_id = ?", (customer_id, product_id, order_id)) is not None

    def save_review(self, r):
        self.db.execute("INSERT OR REPLACE INTO review(review_id, product_id, customer_id, order_id, "
                        "rating, text, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (r.review_id, r.product_id, r.customer_id, r.order_id, r.rating, r.text,
                         r.status, r.created_at))
        return r

    def list_reviews(self, status=None):
        if status:
            rows = self.db.query("SELECT * FROM review WHERE status = ? ORDER BY review_id", (status,))
        else:
            rows = self.db.query("SELECT * FROM review ORDER BY review_id")
        return [self._to_review(r) for r in rows]


class SqliteAuditDAO(interfaces.AuditDAO):

    def __init__(self, db):
        self.db = db

    def record(self, actor, action, entity, entity_id, detail=""):
        self.db.execute("INSERT INTO audit_log(actor, action, entity, entity_id, detail, at) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (actor, action, entity, entity_id, detail, self.db.now()))

    def recent(self, limit=20):
        return [dict(r) for r in self.db.query(
            "SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,))]
