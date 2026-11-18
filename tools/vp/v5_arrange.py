"""Places the classes of a wide design diagram on a grid of rows (centred), then lets the plugin re-route the
lines orthogonally. The auto layout puts unconnected classes on one row, which gives a 5000 px strip.

    python tools/vp/v5_arrange.py
"""
import re

import vp

GRIDS = {
    "DCL03 Design Classes (dao) - Data Access Objects": [
        ["CustomerDAO", "ProductDAO", "InventoryDAO", "CartDAO", "PromotionDAO"],
        ["SqliteCustomerDAO", "SqliteProductDAO", "SqliteInventoryDAO", "SqliteCartDAO", "SqlitePromotionDAO"],
        ["ImageStorage", "Database", "VectorIndex"],
        ["SqliteOrderDAO", "SqlitePaymentDAO", "SqliteShipmentDAO", "SqliteReviewDAO", "SqliteAuditDAO"],
        ["OrderDAO", "PaymentDAO", "ShipmentDAO", "ReviewDAO", "AuditDAO"]],
    "DCL04 Design Classes (service) - Business Services": [
        ["CheckoutService", "OrderService", "ShipmentService"],
        ["CartService", "PaymentService", "InventoryService", "ShippingGateway"],
        ["PaymentGateway", "SimulatedCarrier"],
        ["SimulatedPaymentProvider"],
        ["AuthService", "CatalogService", "ReviewService", "ReportService"]],
    "DCL05 Design Classes (ai) - Search Review Insights and Recommendations": [
        ["SearchService", "QueryService"],
        ["RankingService", "ImageService", "SpeechService"],
        ["RecommenderService", "ReviewInsightService"]],
    "DCL06 Design Classes (controller) - Web Controllers": [
        ["Request", "WebApp", "Response"],
        ["ShopController", "AccountController", "OrderController", "StaffController", "ReportController"]],
}


def sizes(d):
    g = vp.call("getDiagramGeometry", quiet=True, diagramName=d)
    return {m.group(1): (int(m.group(4)), int(m.group(5)))
            for m in re.finditer(r"(?:Class|Interface): (\w+) (-?\d+),(-?\d+) (\d+)x(\d+)", g)}


def arrange(d, rows, gap_x=60, gap_y=110, left=40, top=40):
    size = sizes(d)
    for i, n in enumerate(size):          # park every class out of the way first, so no placement collides
        vp.call("setElementBounds", quiet=True, diagramName=d, elementName=n, x=9000 + 700 * (i % 6),
                y=9000 + 700 * (i // 6), width=0, height=0)
    widths = [sum(size[n][0] for n in r) + gap_x * (len(r) - 1) for r in rows]
    full = max(widths)
    y = top
    for r, w in zip(rows, widths):
        x = left + (full - w) // 2
        for n in r:
            vp.call("setElementBounds", quiet=True, diagramName=d, elementName=n, x=x, y=y, width=0, height=0)
            x += size[n][0] + gap_x
        y += max(size[n][1] for n in r) + gap_y
    vp.call("rerouteConnectors", quiet=True, diagramName=d)
    vp.call("layoutConnectorLabels", quiet=True, diagramName=d)
    vp.call("exportDiagramImage", quiet=True, diagramName=d, filePath=vp.PNG + d + ".png")


if __name__ == "__main__":
    for d, rows in GRIDS.items():
        arrange(d, rows)
        print("arranged", d)
    vp.call("saveProject", quiet=True)
