"""Design classes read from the code of abc_shop (one entry per package), for the design class diagrams.

Class design = analysis class + methods (the lecturer's criterion): the model package keeps the classes of
the analysis and data model and adds every public method of the code; the other packages (dao, service, ai,
controller) are the classes that exist only at run time. Attribute types come from the dataclass
annotations; Python code does not annotate parameters, so their types are taken from the parameter name
(product_id -> String, quantity -> Integer, customer -> Customer ...), the way the design states them.
"""
import ast
import os
import re

APP = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "abc_shop")

PACKAGES = {
    "model": ["model/customer.py", "model/product.py", "model/cart.py", "model/order.py", "model/payment.py",
              "model/shipment.py", "model/inventory.py", "model/review.py"],
    "dao": ["dao/database.py", "dao/interfaces.py", "dao/sqlite_dao.py", "dao/image_storage.py", "dao/vector_index.py"],
    "service": ["service/auth_service.py", "service/catalog_service.py", "service/cart_service.py",
                "service/checkout_service.py", "service/payment_service.py", "service/order_service.py",
                "service/inventory_service.py", "service/shipment_service.py", "service/review_service.py",
                "service/report_service.py", "service/gateways.py"],
    "ai": ["ai/search/search_service.py", "ai/search/query_service.py", "ai/search/ranking_service.py",
           "ai/search/image_service.py", "ai/search/speech_service.py", "ai/recommender.py", "ai/review_insights.py"],
    "controller": ["controller/router.py", "controller/http.py", "controller/shop_controller.py",
                   "controller/account_controller.py", "controller/order_controller.py",
                   "controller/staff_controller.py", "controller/report_controller.py"],
}
SKIP = re.compile(r"(Error|Exception|Unavailable|Transition|Denied|NotFound)$")   # exception types are not design classes

PY = {"str": "String", "int": "Integer", "float": "Float", "bool": "Boolean", "list": "List<Object>",
      "dict": "Map", "Optional[str]": "String", "Optional[int]": "Integer"}
NAME = [  # (regex on the parameter name, type)
    (r"(^|_)id$|_id$|^code$|^email$|^password$|^name$|^text$|^status$|^kind$|^reference$|^reason$|^note$|^actor$|"
     r"^at$|^today$|^query_text$|^question$|^q$|^mode$|^role$|^permission$|^action$|^location$|^carrier_ref$|"
     r"^provider_ref$|^attempt_ref$|^card_token$|^promo_code$|^idempotency_key$|^new_status$|^entity$|^detail$|"
     r"^path$|^relative$|^filename$|^image_path$|^hypothesis$|^sql$|^prefix$|^voice$|^audio_input$|^decision$|"
     r"^address_text$|^street$|^city$|^phone$|^receiver$|^outcome$|^method$|^label$|^start$|^end$|^period$",
     "String"),
    (r"quantity|^qty$|^limit$|^k$|^rating$|^seq$|^threshold$|^width$|^n$|^value$|^days$", "Integer"),
    (r"price|amount|percent|subtotal|total|^weight$|^text_weight$|^score$", "Float"),
    (r"^request$", "Request"), (r"^customer$", "Customer"), (r"^(user|admin|manager|staff|actor_user|staff_user)$", "User"),
    (r"^product$|^p$", "Product"), (r"^cart$", "Cart"), (r"^order$|^o$", "Order"), (r"^event$|^e$", "InventoryEvent"),
    (r"^review$|^r$", "Review"), (r"^payment$", "Payment"), (r"^shipment$|^s$", "Shipment"),
    (r"^promotion$", "Promotion"), (r"^category$|^c$", "Category"), (r"^address$", "Address"),
    (r"^stock$", "StockLevel"), (r"^embedding$|^vector$|^query_embedding$", "List<Float>"),
    (r"^content$|^image$", "Bytes"), (r"^query$", "Map"), (r"^reviews$", "List<Review>"),
    (r"^products$", "List<Product>"), (r"^statuses$", "List<String>"), (r"^environ$", "Map"),
    (r"^start_response$|^encode$|^app$", "Object"), (r"^db$", "Database"), (r"^shop$", "Object"),
    (r"^storage$", "ImageStorage"), (r"^results$", "List<Map>"),
]


CONTEXT = {  # a one-letter parameter is the entity of the class it belongs to
    "Product": {"p": "Product"}, "Promotion": {"p": "Promotion"}, "Payment": {"p": "Payment"},
    "Inventory": {"s": "StockLevel", "e": "InventoryEvent"}, "Shipment": {"s": "Shipment"},
    "Review": {"r": "Review"}, "Order": {"o": "Order", "address": "String"}, "Category": {"c": "Category"},
}
PARAMS = {"key": "String", "approve": "Boolean", "aspects": "Map", "used": "Integer", "params": "List<Object>",
          "encode": "Function", "active_only": "Boolean", "currency": "String", "default": "Object", "parcels": "Integer",
          "available": "Integer", "filters": "Map", "terms": "List<String>", "clause": "String",
          "milestone": "Milestone", "result": "Map", "candidates": "List<Map>", "created_at": "String",
          "discount": "Float", "shipping_fee": "Float", "location": "String", "flash": "String",
          "parsed": "Map", "category_id": "String", "image_bytes": "Bytes", "items": "List<CartItem>"}


def type_of_param(name, cls=""):
    if name == "request" and "Controller" not in cls and cls not in ("WebApp", "Response"):
        return "ReplenishmentRequest"
    for k, v in CONTEXT.items():
        if k in cls and name in v:
            return v[name]
    if name in PARAMS:
        return PARAMS[name]
    for pat, t in NAME:
        if re.search(pat, name):
            return t
    return "Object"


RETURN = [  # (regex on the method name, type)
    (r"^(is_|can|has_|exists|matches|is_final|is_order_question)", "Boolean"),
    (r"^(calc_|subtotal|sub_total|discount_for|available|score|cosine)", "Float"),
    (r"^(last_seq|available)$", "Integer"),
    (r"^(one_line|search_text|search_terms|last_update|now|next_id|transcribe|path|save_upload|hash)", "String"),
    (r"^spec_rows$", "List<String>"),
]


RETURNS_BY_CLASS = {("Database", "execute"): "Cursor", ("SearchService", "retrieve"): "List<Map>",
                    ("SearchService", "search_orders"): "List<Order>", ("AuditDAO", "record"): "void", ("SqliteAuditDAO", "record"): "void",
                    ("ReviewInsightService", "label"): "String", ("Order", "change_status"): "Order",
                    ("CartService", "update_quantity"): "Cart", ("CartService", "check_availability"): "Integer",
                    ("CatalogService", "change_price"): "Product", ("CatalogService", "set_status"): "Product",
                    ("InventoryService", "stock_of"): "StockLevel", ("OrderService", "processing_queue"): "List<Order>",
                    ("OrderService", "start_processing"): "Order", ("OrderService", "hold"): "Order",
                    ("ReportService", "exception_report"): "Map", ("ReviewService", "submit"): "Review",
                    ("ReviewService", "moderate"): "Review", ("ShipmentService", "pick_list"): "List<Order>",
                    ("ShipmentService", "ready_list"): "List<Order>", ("ShipmentService", "mark_packed"): "Shipment",
                    ("ShipmentService", "arrange_delivery"): "Shipment", ("ShipmentService", "on_milestone"): "Boolean",
                    ("SpeechService", "load"): "WhisperModel",
("PaymentDAO", "for_order"): "List<Payment>", ("SqlitePaymentDAO", "for_order"): "List<Payment>",
                    ("ReviewDAO", "for_product"): "List<Review>", ("SqliteReviewDAO", "for_product"): "List<Review>"}
RETURNS = {  # methods whose result the name does not tell
    "update_profile": "Customer", "validate": "void", "apply": "void", "create_from_cart": "Order",
    "find_by_email": "User", "find_by_idempotency_key": "Order", "get_by_attempt": "Payment",
    "get_by_carrier_ref": "Shipment", "get_by_order": "Shipment", "available": "Integer", "find": "CartItem",
    "register": "Customer", "login": "User", "create_staff": "User", "require": "void", "view": "Cart",
    "quote": "Map", "place_order": "Map", "apply_promotion": "Float", "calc_shipping": "Float",
    "handle_result": "Payment", "succeeded": "Boolean", "track": "Map", "own_order": "Order",
    "record": "InventoryEvent", "manual_event": "InventoryEvent", "product_detail": "Map", "browse": "List<Map>",
    "categories": "List<Category>", "category": "Category", "text_query": "Map", "voice_query": "Map",
    "image_query": "Map", "multimodal_query": "Map", "order_query": "Map", "weights": "List<Float>",
    "business_score": "Float", "encode": "List<Float>", "load": "Object", "analyse": "Map", "analyse_review": "Map",
    "classify_clause": "Map", "split_clauses": "List<String>", "fit": "void", "dashboard": "Map",
    "sales_report": "Map", "inventory_report": "Map", "order_report": "Map", "authorize": "Map",
    "create_delivery": "String", "get": "String", "session": "Map", "redirect": "Response", "dispatch": "Response",
    "static": "Response", "recent": "List<Map>", "build": "VectorIndex", "init_schema": "void",
    "transaction": "Database", "query": "List<Map>", "query_one": "Map", "execute": "Object", "close": "void",
    "add_milestone": "void", "last_update": "String",
    "list_products": "List<Product>", "list_categories": "List<Category>", "list_promotions": "List<Promotion>",
    "list_orders": "List<Order>", "find_by_customer": "List<Order>", "find_by_status": "List<Order>",
    "history": "List<Order>", "list_customers": "List<User>", "list_reviews": "List<Review>",
    "events_for": "List<InventoryEvent>", "open_replenishments": "List<ReplenishmentRequest>",
    "add_replenishment": "ReplenishmentRequest", "request_replenishment": "ReplenishmentRequest",
    "similar": "List<Map>", "for_customer": "List<Map>", "search": "List<Map>", "rank": "List<Map>",
    "low_stock": "List<Map>", "published": "List<Review>", "moderation_queue": "List<Review>", "search_text": "List<Map>", "search_image": "List<Map>",
}


def type_of_return(cls, name, node):
    if cls.endswith("Controller") and name not in ("static",):
        return "Response"
    if (cls, name) in RETURNS_BY_CLASS:
        return RETURNS_BY_CLASS[(cls, name)]
    if name in RETURNS and not (name == "search_text" and cls == "Product"):
        return RETURNS[name]
    for pat, t in RETURN:
        if re.search(pat, name):
            return t
    # "return None" only, or no return statement: void
    returns = [n for n in ast.walk(node) if isinstance(n, ast.Return) and n.value is not None]
    if not returns:
        return "void"
    if name.startswith(("list_", "find_by_", "for_", "events_for", "open_", "browse", "history", "queue",
                        "moderation_queue", "published", "similar", "for_customer", "search", "rank",
                        "retrieve", "low_stock", "categories")):
        return "List<Object>"
    m = re.match(r"(get|save|find|create|add|place|update|record|register|login|change|cancel|track|own|"
                 r"request|reserve|apply|submit|pack|arrange|handle|moderate|set|remove|validate|dashboard|"
                 r"product|quote|checkout|analyse|build|encode|text_query|voice_query|image_query|"
                 r"multimodal_query|order_query)_?(\w*)", name)
    if m and m.group(2):
        word = "".join(w.capitalize() for w in m.group(2).split("_"))
        known = {"Order": "Order", "Product": "Product", "Cart": "Cart", "Stock": "StockLevel", "User": "User",
                 "Customer": "Customer", "Promotion": "Promotion", "Category": "Category", "Payment": "Payment",
                 "Shipment": "Shipment", "Review": "Review", "Event": "InventoryEvent", "Item": "CartItem",
                 "Milestone": "Milestone"}
        for k, v in known.items():
            if word.startswith(k) or word.endswith(k):
                return v
    return "Object"


def annotation(a):
    if a is None:
        return ""
    s = ast.unparse(a)
    m = re.match(r"Optional\[(\w+)\]$", s)
    if m:
        s = m.group(1)
    return PY.get(s, s)


def read_class(node):
    attrs, ops = [], []
    for st in node.body:
        if isinstance(st, ast.AnnAssign) and isinstance(st.target, ast.Name) and not st.target.id.isupper():
            attrs.append((st.target.id, annotation(st.annotation)))
        elif isinstance(st, ast.FunctionDef) and not st.name.startswith("_"):
            args = [a for a in st.args.args if a.arg not in ("self", "cls")] + ([st.args.vararg] if st.args.vararg else [])
            params = ", ".join(f"{a.arg}: {annotation(a.annotation) or type_of_param(a.arg, node.name)}" for a in args)
            ops.append((st.name, params, type_of_return(node.name, st.name, st),
                        any(isinstance(d, ast.Name) and d.id == "staticmethod" for d in st.decorator_list),
                        any(isinstance(d, ast.Name) and d.id == "abstractmethod" for d in st.decorator_list)))
    bases = [ast.unparse(b).split(".")[-1] for b in node.bases]
    return bases, attrs, ops


def classes(package):
    out = {}
    for rel in PACKAGES[package]:
        tree = ast.parse(open(os.path.join(APP, rel), encoding="utf-8").read())
        for n in tree.body:
            if isinstance(n, ast.ClassDef) and not SKIP.search(n.name):
                bases, attrs, ops = read_class(n)
                out[n.name] = {"module": rel, "bases": [b for b in bases if b not in ("ABC", "object")],
                               "attrs": attrs, "ops": ops}
    for name, c in out.items():                      # an interface returns what its implementation returns
        impl = out.get("Sqlite" + name)
        if impl:
            ret = {o[0]: o[2] for o in impl["ops"]}
            c["ops"] = [(o[0], o[1], ret.get(o[0], o[2]), o[3], True) for o in c["ops"]]
            c["interface"] = True
    return out


if __name__ == "__main__":
    for p in PACKAGES:
        c = classes(p)
        print(p, len(c), sum(len(v["ops"]) for v in c.values()), "ops")
        for k, v in c.items():
            print("   ", k, v["bases"], [a for a, _ in v["attrs"]], [f"{o[0]}({o[1]}):{o[2]}" for o in v["ops"]][:3])
