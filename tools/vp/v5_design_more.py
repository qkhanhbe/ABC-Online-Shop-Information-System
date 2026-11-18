"""Design diagrams the reference essay has and V5 lacked, drawn from the code paths:

  LAY03 Layers - Account (UC01, UC02)         AccountController, AuthService, CustomerDAO ...
  LAY04 Layers - Card Payment (UC09)          CheckoutService, PaymentService, PaymentGateway ...
  LAY05 Layers - Recommendation (UC33, UC34)  ShopController, OrderController, RecommenderService ...
  SD07 Log In (Design), SD08 Pay Order by Card (Design), SD09 Recommendation (Design)

    python tools/vp/v5_design_more.py layers | sequences
"""
import re
import sys

import vp

LAYERS = {
    "LAY03 Layers - Account (UC01 and UC02)": (
        [("controller", ["AccountController"]), ("service", ["AuthService"]),
         ("dao", ["CustomerDAO", "AuditDAO", "Database"]), ("model", ["User", "Customer", "Address"])],
        [("AccountController", "AuthService"), ("AuthService", "CustomerDAO"), ("AuthService", "AuditDAO"),
         ("AuthService", "Database")]),
    "LAY04 Layers - Card Payment (UC09)": (
        [("controller", ["OrderController"]),
         ("service", ["CheckoutService", "PaymentService", "InventoryService", "PaymentGateway", "SimulatedPaymentProvider"]),
         ("dao", ["PaymentDAO", "OrderDAO", "InventoryDAO", "AuditDAO", "Database"]),
         ("model", ["Payment", "Order", "StockLevel"])],
        [("OrderController", "CheckoutService"), ("CheckoutService", "PaymentService"),
         ("PaymentService", "PaymentDAO"), ("PaymentService", "OrderDAO"), ("PaymentService", "InventoryService"),
         ("PaymentService", "PaymentGateway"), ("PaymentService", "AuditDAO"), ("PaymentService", "Database"),
         ("InventoryService", "InventoryDAO")]),
    "LAY05 Layers - Recommendation (UC33 and UC34)": (
        [("controller", ["ShopController", "OrderController"]), ("ai", ["RecommenderService"]),
         ("service", ["CatalogService"]), ("dao", ["ProductDAO", "InventoryDAO", "OrderDAO"]),
         ("model", ["Product", "Order", "StockLevel"])],
        [("ShopController", "RecommenderService"), ("ShopController", "CatalogService"),
         ("OrderController", "RecommenderService"), ("RecommenderService", "ProductDAO"),
         ("RecommenderService", "InventoryDAO"), ("RecommenderService", "OrderDAO"),
         ("CatalogService", "ProductDAO"), ("CatalogService", "InventoryDAO")]),
}
REALIZE = {"LAY04 Layers - Card Payment (UC09)": [("SimulatedPaymentProvider", "PaymentGateway")]}


def frames(d):
    g = vp.call("getDiagramGeometry", quiet=True, diagramName=d)
    return {m.group(1): (int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)))
            for m in re.finditer(r"Package: (\w+) (-?\d+),(-?\d+) (\d+)x(\d+)", g)}


def draw_layers():
    for d, (layers, uses) in LAYERS.items():
        vp.call("createClassDiagram", quiet=True, diagramName=d)
        for package, names in layers:
            vp.call("addPackageShape", quiet=True, diagramName=d, packageName=package)
            for n in names:
                vp.call("addClass", quiet=True, diagramName=d, className=n, modelPackage=package)
                vp.call("moveIntoPackage", quiet=True, diagramName=d, elementName=n, packageName=package)
        for a, b in uses:
            vp.call("addUsage", quiet=True, diagramName=d, fromName=a, toName=b)
        for a, b in REALIZE.get(d, []):
            vp.call("addRealization", quiet=True, diagramName=d, fromClass=a, toClass=b)
        vp.call("autoLayoutDiagram", quiet=True, diagramName=d)
        for i, (package, _) in enumerate(layers):
            vp.call("setElementBounds", quiet=True, diagramName=d, elementName=package, x=8000, y=8000 + 3000 * i,
                    width=0, height=0)
        f, y = frames(d), 40
        for package, _ in layers:
            vp.call("setElementBounds", quiet=True, diagramName=d, elementName=package, x=40, y=y, width=0, height=0)
            y += f[package][3] + 90
        vp.call("rerouteConnectors", quiet=True, diagramName=d)
        print(vp.call("getElementCounts", quiet=True, diagramName=d).replace("\n", " "))
        vp.call("exportDiagramImage", quiet=True, diagramName=d, filePath=vp.PNG + d + ".png")


# sequence: lifelines (name, type), steps (kind, from, to, text, number), fragments
SEQUENCES = {
    "SD07 Log In (Design)": (
        [("Customer", "actor"), ("WebApp", "boundary"), ("AccountController", "control"), ("AuthService", "control"),
         ("CustomerDAO", "entity")],
        [("call", "Customer", "WebApp", "POST /login (email, password)", "1"),
         ("call", "WebApp", "AccountController", "login(request)", "2"),
         ("call", "AccountController", "AuthService", "login(email, password)", "3"),
         ("call", "AuthService", "CustomerDAO", "find_by_email(email)", "4"),
         ("ret", "CustomerDAO", "AuthService", "user or None", "5"),
         ("call", "AuthService", "AuthService", "check_password(password, hash)", "6"),
         ("ret", "AuthService", "AccountController", "user", "7"),
         ("call", "AccountController", "AccountController", "session[user_id] = user_id", "8"),
         ("ret", "AccountController", "WebApp", "redirect to the page of the role", "9"),
         ("ret", "AuthService", "AccountController", "ValidationError (incorrect)", "10"),
         ("ret", "AccountController", "WebApp", "400 login page", "11"),
         ("ret", "WebApp", "Customer", "response with session cookie", "12")],
        [("alt", "user found and password matches|else", "AuthService,AccountController,WebApp", "7", "11", "10")]),
    "SD08 Pay Order by Card (Design)": (
        [("CheckoutService", "control"), ("PaymentService", "control"), ("PaymentDAO", "entity"),
         ("PaymentGateway", "boundary"), ("OrderDAO", "entity"), ("Order", "entity"), ("InventoryService", "control")],
        [("call", "CheckoutService", "PaymentService", "request_payment(order, card_token)", "1"),
         ("call", "PaymentService", "PaymentDAO", "save_payment(payment Pending)", "2"),
         ("call", "PaymentService", "PaymentGateway", "authorize(attempt_ref, amount, currency, token)", "3"),
         ("ret", "PaymentGateway", "PaymentService", "signed result", "4"),
         ("call", "PaymentService", "PaymentService", "handle_result(result)", "5"),
         ("call", "PaymentService", "PaymentDAO", "get_by_attempt(attempt_ref)", "6"),
         ("ret", "PaymentDAO", "PaymentService", "payment", "7"),
         ("call", "PaymentService", "PaymentService", "check signature, amount, currency", "8"),
         ("call", "PaymentService", "OrderDAO", "get_order(order_id)", "9"),
         ("ret", "OrderDAO", "PaymentService", "order", "10"),
         ("call", "PaymentService", "Order", "change_status(Paid)", "11"),
         ("call", "PaymentService", "Order", "change_status(Payment Failed)", "12"),
         ("call", "PaymentService", "InventoryService", "release_order(order)", "13"),
         ("call", "PaymentService", "PaymentDAO", "save_payment(payment)", "14"),
         ("call", "PaymentService", "OrderDAO", "save_order(order)", "15"),
         ("ret", "PaymentService", "CheckoutService", "payment status", "16")],
        [("alt", "SUCCEEDED|DECLINED", "PaymentService,Order,InventoryService", "11", "13", "12")]),
    "SD09 Recommendation (Design)": (
        [("Customer", "actor"), ("ShopController", "control"), ("RecommenderService", "control"),
         ("ProductDAO", "entity"), ("OrderDAO", "entity"), ("InventoryDAO", "entity")],
        [("call", "Customer", "ShopController", "GET /product/{product_id}", "1"),
         ("call", "ShopController", "RecommenderService", "similar(product_id, 4)", "2"),
         ("call", "RecommenderService", "RecommenderService", "fit()", "3"),
         ("call", "RecommenderService", "ProductDAO", "list_products()", "4"),
         ("ret", "ProductDAO", "RecommenderService", "products (TF-IDF of search_text)", "5"),
         ("call", "RecommenderService", "OrderDAO", "list_orders()", "6"),
         ("ret", "OrderDAO", "RecommenderService", "orders (co-purchase counts)", "7"),
         ("call", "RecommenderService", "InventoryDAO", "get_stock(candidate)", "8"),
         ("ret", "InventoryDAO", "RecommenderService", "available", "9"),
         ("call", "RecommenderService", "RecommenderService", "score = 0.7 content + 0.3 co-purchase", "10"),
         ("call", "RecommenderService", "ProductDAO", "get_product(best k)", "11"),
         ("ret", "RecommenderService", "ShopController", "top 4 (product, score)", "12"),
         ("ret", "ShopController", "Customer", "product page: Customers also like", "13")],
        [("opt", "model not built yet", "RecommenderService,ProductDAO,OrderDAO", "3", "7", ""),
         ("loop", "each other product", "RecommenderService,InventoryDAO", "8", "10", "")]),
}


def draw_sequences():
    for d, (lifelines, steps, fragments) in SEQUENCES.items():
        vp.call("createSequenceDiagram", quiet=True, diagramName=d)
        for name, kind in lifelines:
            vp.call("addLifeline", quiet=True, diagramName=d, lifelineName=name, className="", lifelineType=kind)
        for kind, a, b, text, n in steps:
            if kind == "call":
                vp.call("addMessage", quiet=True, diagramName=d, fromLifeline=a, toLifeline=b, messageName=text,
                        sequenceNumber=n, messageType="sync")
            else:
                vp.call("addReturnMessage", quiet=True, diagramName=d, fromLifeline=a, toLifeline=b, messageName=text,
                        sequenceNumber=n)
        for op, guard, covered, a, b, starts in fragments:
            print(vp.call("addCombinedFragment", quiet=True, diagramName=d, operator=op, guard=guard,
                          coveredLifelines=covered, fromSeq=a, toSeq=b, operandStarts=starts)[:100])
        print(vp.call("getElementCounts", quiet=True, diagramName=d).replace("\n", " "))
        vp.call("exportDiagramImage", quiet=True, diagramName=d, filePath=vp.PNG + d + ".png")


if __name__ == "__main__":
    {"layers": draw_layers, "sequences": draw_sequences}[sys.argv[1]]()
    vp.call("saveProject", quiet=True)
