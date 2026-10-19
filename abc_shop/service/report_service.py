"""Service layer: UC25 View Management Dashboard, UC26 Sales Report, UC27 Inventory Report,
UC28 Order and Exception Report.

Reports are computed from the same operational records that run the shop (BP05), so a figure
can always be traced back to orders, payments and inventory events.
"""
from collections import Counter, defaultdict

from model import order as states
from service.auth_service import AuthService

REVENUE_STATES = {states.PAID, states.PROCESSING, states.READY, states.SHIPPED, states.DELIVERED}
EXCEPTION_STATES = {states.ON_HOLD, states.PAYMENT_PENDING, states.DELIVERY_FAILED}


class ReportService:

    def __init__(self, db, order_dao, product_dao, inventory_dao, audit_dao):
        self.db = db
        self.orders = order_dao
        self.products = product_dao
        self.inventory = inventory_dao
        self.audit = audit_dao

    def dashboard(self, manager):
        AuthService.require(manager, "reports")
        orders = self.orders.list_orders()
        sold = [o for o in orders if o.status in REVENUE_STATES]
        low = [p.product_id for p in self.products.list_products(active_only=False)
               if self.inventory.get_stock(p.product_id).is_low()]
        return {"orders": len(orders), "revenue": round(sum(o.calc_total() for o in sold), 2),
                "average_order": round(sum(o.calc_total() for o in sold) / len(sold), 2) if sold else 0,
                "by_status": dict(Counter(o.status for o in orders)),
                "exceptions": sum(1 for o in orders if o.status in EXCEPTION_STATES),
                "low_stock": low, "refreshed_at": self.db.now()}

    def sales_report(self, manager, start="0000-00-00", end="9999-99-99"):
        AuthService.require(manager, "reports")
        by_day, by_category = defaultdict(float), defaultdict(float)
        units = Counter()
        for o in self.orders.list_orders():
            if o.status not in REVENUE_STATES or not start <= o.created_at[:10] <= end:
                continue
            by_day[o.created_at[:10]] += o.calc_total()
            for i in o.items:
                product = self.products.get_product(i.product_id)
                by_category[product.category_id] += i.sub_total()
                units[i.name] += i.quantity
        return {"period": (start, end), "by_day": dict(sorted(by_day.items())),
                "by_category": {k: round(v, 2) for k, v in sorted(by_category.items())},
                "top_products": units.most_common(5)}

    def inventory_report(self, manager):
        AuthService.require(manager, "reports")
        rows = []
        for p in self.products.list_products(active_only=False):
            s = self.inventory.get_stock(p.product_id)
            rows.append({"product_id": p.product_id, "name": p.name, "physical": s.physical,
                         "reserved": s.reserved, "available": s.available, "low": s.is_low()})
        return rows

    def exception_report(self, manager):
        AuthService.require(manager, "reports")
        orders = [o for o in self.orders.list_orders() if o.status in EXCEPTION_STATES]
        alerts = [a for a in self.audit.recent(50)
                  if a["action"] in ("quarantined", "rejected_callback", "unmatched_milestone",
                                     "timeout", "refund_needed", "refund_initiated")]
        return {"orders": [(o.order_id, o.status, o.history[-1].note if o.history else "")
                           for o in orders], "alerts": alerts}
