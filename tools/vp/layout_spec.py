"""Exact shape positions for the diagrams whose layout is planned by hand (grid, reading order).

Writes arrange_spec.txt (DIAGRAM-CODE|shape|x|y|w|h, w/h 0 = keep); the essay.gen plugin applies it to a copy of
the project (mode arrange), then the MCP plugin re-routes the lines in the GUI.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arrange_spec.txt")
lines = []


def put(diagram, positions):
    for name, (x, y) in positions.items():
        lines.append(f"{diagram}|{name}|{x}|{y}|0|0")


put("CL01", {"User": (40, 40), "Cart": (420, 40), "CartItem": (760, 40), "Review": (1100, 40), "Category": (1420, 40),
             "Customer": (40, 330), "Order": (420, 330), "OrderItem": (760, 330), "Product": (1100, 330),
             "ProductDetail": (1586, 430),
             "Address": (40, 640), "Promotion": (220, 660), "Payment": (430, 660), "StatusChange": (650, 660),
             "Shipment": (860, 640), "StockLevel": (1100, 640), "FootwearDetail": (1300, 640),
             "ApparelDetail": (1480, 640), "BagDetail": (1620, 640), "WatchDetail": (1810, 640),
             "Milestone": (870, 960), "InventoryEvent": (1100, 960), "ReplenishmentRequest": (1300, 960)})

put("DCL03", {"Category": (560, 40), "StockLevel": (40, 300), "Product": (480, 280), "ProductDetail": (1051, 330),
              "InventoryEvent": (130, 620), "Promotion": (420, 640), "FootwearDetail": (800, 560),
              "ApparelDetail": (970, 560), "BagDetail": (1095, 560), "WatchDetail": (1270, 560), "Order": (900, 760)})

put("ERD02", {"footwear_detail": (40, 40), "apparel_detail": (40, 190), "bag_detail": (40, 320), "watch_detail": (40, 450),
              "category": (380, 40), "product": (380, 170), "replenishment_request": (380, 430),
              "stock_level": (680, 40), "inventory_event": (680, 180), "review": (680, 400),
              "users": (960, 40), "customer_order": (960, 240), "sequence": (1300, 40), "audit_log": (1300, 140)})

put("LDM01", {"Address": (40, 40), "UserAccount": (330, 40), "Cart": (660, 40), "CartItem": (960, 40),
              "Category": (1240, 40), "Replenishment": (1520, 40), "Promotion": (1800, 40),
              "Review": (40, 330), "CustomerOrder": (330, 330), "OrderItem": (680, 330), "Product": (960, 330),
              "StockLevel": (1240, 330), "InventoryEvent": (1520, 330),
              "StatusChange": (40, 640), "Payment": (330, 640), "FootwearDetail": (760, 640),
              "ApparelDetail": (1010, 640), "BagDetail": (1240, 640), "WatchDetail": (1490, 640),
              "Shipment": (330, 900), "Milestone": (640, 900)})

# stakeholder map: internal column, the shop in the middle, external column
lines += ["STK01|Internal stakeholders|40|40|380|500", "STK01|External stakeholders|1000|40|380|500"]
put("STK01", {"Administrator": (60, 90), "Sales Staff": (60, 200), "Warehouse Staff": (60, 310), "Manager": (60, 420),
              "Customer": (1020, 90), "Supplier": (1020, 200), "Payment Provider": (1020, 310),
              "Shipping Provider": (1020, 420), "ABC Online Shop": (640, 270)})

# PKG01: layers on a grid of name-only class boxes
LAYERS = {
    "view": ["templates"],
    "controller": ["WebApp", "Request", "Response", "AccountController", "ShopController", "OrderController",
                   "StaffController", "ReportController"],
    "service": ["AuthService", "CatalogService", "CartService", "CheckoutService", "PaymentService", "OrderService",
                "InventoryService", "ShipmentService", "ReviewService", "ReportService", "PaymentGateway", "ShippingGateway"],
    "ai": ["SearchService", "QueryService", "SpeechService", "ImageService", "RankingService", "ReviewInsightService",
           "RecommenderService"],
    "dao": ["Database", "CustomerDAO", "ProductDAO", "InventoryDAO", "CartDAO", "PromotionDAO", "OrderDAO", "PaymentDAO",
            "ShipmentDAO", "ReviewDAO", "AuditDAO", "VectorIndex", "ImageStorage"],
}
MODEL = {"product": ["Category", "Product", "Promotion", "ProductDetail", "FootwearDetail", "ApparelDetail", "BagDetail",
                     "WatchDetail"],
         "customer": ["User", "Customer", "Address"], "order": ["Order", "OrderItem", "StatusChange"],
         "inventory": ["StockLevel", "InventoryEvent"], "cart": ["Cart", "CartItem"], "shipment": ["Shipment", "Milestone"],
         "payment": ["Payment"], "review": ["Review"]}
CW, CH, GX, GY, TOP, PAD, W = 150, 30, 16, 14, 40, 16, 1340
frames = []


def layer(name, names, x, y, cols, cw=CW, ch=CH):
    for i, n in enumerate(names):
        r, c = divmod(i, cols)
        lines.append(f"PKG01|{n}|{x + PAD + c * (cw + GX)}|{y + TOP + r * (ch + GY)}|{cw}|{ch}")
    rows = (len(names) + cols - 1) // cols
    w, h = cols * (cw + GX) - GX + 2 * PAD, TOP + rows * (ch + GY) - GY + PAD
    frames.append(f"PKG01|{name}|{x}|{y}|{w}|{h}")
    return w, h


layer("controller", LAYERS["controller"], 40, 40, 4)
layer("view", LAYERS["view"], 40 + W - 182, 40, 1)
layer("service", LAYERS["service"], 40, 240, 4)
layer("ai", LAYERS["ai"], 40 + W - (3 * (176 + GX) - GX + 2 * PAD), 240, 3, 176)
layer("dao", LAYERS["dao"], 40, 480, 7, CW, 42)
y0, mcw = 740, 118
x = 60
for p in ("product", "customer", "order"):
    w, h = layer(p, MODEL[p], x, y0 + 40, 4 if p == "product" else 3, mcw)
    x += w + 18
right = x
x = 60
for p in ("inventory", "cart", "shipment", "payment", "review"):
    w, h = layer(p, MODEL[p], x, y0 + 40 + 150, len(MODEL[p]), mcw)
    x += w + 18
frames.append(f"PKG01|model|40|{y0}|{max(right, x) - 40}|{40 + 150 + 86 + 20}")
lines = [f"PKG01|@namesonly|{n}" for n in MODEL["product"][3:]] + frames + lines

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")
print(len(lines), "lines ->", OUT)
