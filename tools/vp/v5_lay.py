"""LAY01, LAY02: the classes of one use case per layer (as NhiCT Figures 5.4/5.5): package frames from top to
bottom controller, service/ai, dao, model; <<use>> between the classes that call each other (taken from the
constructors in abc_shop). The model classes are only shown by name (members hidden by essay.gen mode
"v5show"), because the layers above use them as types.

    python tools/vp/v5_lay.py
"""
import re

import vp

LAYERS = {
    "LAY01 Layers - Search Products (UC05)": (
        [("controller", ["ShopController"]),
         ("ai", ["SearchService", "QueryService", "RankingService", "ImageService", "SpeechService"]),
         ("dao", ["ProductDAO", "InventoryDAO", "OrderDAO", "VectorIndex", "ImageStorage"]),
         ("model", ["Product", "StockLevel", "Order"])],
        [("ShopController", "QueryService"), ("ShopController", "SearchService"), ("ShopController", "ImageService"),
         ("ShopController", "SpeechService"), ("ShopController", "ImageStorage"), ("SearchService", "RankingService"),
         ("SearchService", "ProductDAO"), ("SearchService", "InventoryDAO"), ("SearchService", "OrderDAO"),
         ("SearchService", "VectorIndex"), ("VectorIndex", "ImageStorage")]),
    "LAY02 Layers - Cart and Checkout (UC07 and UC08)": (
        [("controller", ["OrderController"]),
         ("service", ["CheckoutService", "CartService", "PaymentService", "InventoryService", "PaymentGateway"]),
         ("dao", ["CartDAO", "PromotionDAO", "OrderDAO", "PaymentDAO", "ProductDAO", "InventoryDAO", "Database"]),
         ("model", ["Cart", "CartItem", "Promotion", "Order", "OrderItem", "Payment", "Product", "StockLevel"])],
        [("OrderController", "CartService"), ("OrderController", "CheckoutService"),
         ("CheckoutService", "CartService"), ("CheckoutService", "InventoryService"),
         ("CheckoutService", "PaymentService"), ("CheckoutService", "CartDAO"), ("CheckoutService", "OrderDAO"),
         ("CheckoutService", "PromotionDAO"), ("CheckoutService", "Database"), ("CartService", "CartDAO"),
         ("CartService", "ProductDAO"), ("CartService", "InventoryDAO"), ("InventoryService", "InventoryDAO"),
         ("InventoryService", "ProductDAO"), ("PaymentService", "PaymentDAO"), ("PaymentService", "OrderDAO"),
         ("PaymentService", "InventoryService"), ("PaymentService", "PaymentGateway")]),
}


def frames(d):
    g = vp.call("getDiagramGeometry", quiet=True, diagramName=d)
    return {m.group(1): (int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)))
            for m in re.finditer(r"Package: (\w+) (-?\d+),(-?\d+) (\d+)x(\d+)", g)}


for d, (layers, uses) in LAYERS.items():
    vp.call("createClassDiagram", quiet=True, diagramName=d)
    for package, names in layers:
        vp.call("addPackageShape", quiet=True, diagramName=d, packageName=package)
        for n in names:
            vp.call("addClass", quiet=True, diagramName=d, className=n, modelPackage=package)
            vp.call("moveIntoPackage", quiet=True, diagramName=d, elementName=n, packageName=package)
    for a, b in uses:
        vp.call("addUsage", quiet=True, diagramName=d, fromName=a, toName=b)
    vp.call("autoLayoutDiagram", quiet=True, diagramName=d)
    # stack the layer frames top-down in the order of the layers (the layout orders them by the lines only)
    f = frames(d)
    for i, (package, _) in enumerate(layers):
        vp.call("setElementBounds", quiet=True, diagramName=d, elementName=package, x=8000, y=8000 + 3000 * i,
                width=0, height=0)
    y = 40
    f = frames(d)
    for package, _ in layers:
        vp.call("setElementBounds", quiet=True, diagramName=d, elementName=package, x=40, y=y, width=0, height=0)
        y += f[package][3] + 90
    vp.call("rerouteConnectors", quiet=True, diagramName=d)
    print(vp.call("getElementCounts", quiet=True, diagramName=d).replace("\n", " "))
    vp.call("exportDiagramImage", quiet=True, diagramName=d, filePath=vp.PNG + d + ".png")
vp.call("saveProject", quiet=True)
