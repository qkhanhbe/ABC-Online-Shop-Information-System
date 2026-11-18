"""The V5 domain model, written once and drawn three times (as NhiCT's Analysis, Data Model and Design files):

* Analysis (package Analysis): the business concepts; attributes without type or identifier, operations with
  typed parameters (responsibilities).
* Data Model (package Data Model): the same classes and associations with types, identifiers, role names
  and <<ORM Persistable>>; syncClassesToErd turns them into the ERD.
* Design (package model, and the other layers): the data model classes plus the operations of the code.

Names follow the Python code (PEP 8): snake_case attributes and operations, so an attribute, its column and
the field of the code have the same name.
"""

# class: (parent, [(attribute, type, is_key)], [(operation, params, return)])
# a key attribute is the identifier added in the data model; the analysis model leaves it out.
S, I, F, B = "String", "Integer", "Float", "Boolean"
CLASSES = {
    "User": (None, [("user_id", S, True), ("name", S, False), ("email", S, False), ("password_hash", S, False),
                    ("role", S, False), ("created_at", S, False)],
             [("can", "action: String", B)]),
    "Customer": ("User", [], [("update_profile", "name: String, address: Address", "void")]),
    "Address": (None, [("receiver", S, False), ("phone", S, False), ("street", S, False), ("city", S, False)],
                [("is_complete", "", B), ("one_line", "", S)]),
    "Category": (None, [("category_id", S, True), ("name", S, False), ("detail_kind", S, False)], []),
    "Product": (None, [("product_id", S, True), ("name", S, False), ("brand", S, False), ("color", S, False),
                       ("price", F, False), ("description", S, False), ("image", S, False), ("status", S, False)],
                [("is_active", "", B), ("spec_rows", "", "List<String>"), ("search_terms", "", S),
                 ("search_text", "", S), ("update_price", "new_price: Float", "void")]),
    "Footwear": ("Product", [("sizes", S, False), ("upper_material", S, False), ("sole", S, False),
                             ("purpose", S, False)],
                 [("spec_rows", "", "List<String>"), ("search_terms", "", S)]),
    "Apparel": ("Product", [("sizes", S, False), ("material", S, False), ("fit", S, False)],
                [("spec_rows", "", "List<String>"), ("search_terms", "", S)]),
    "Bag": ("Product", [("capacity_l", F, False), ("material", S, False), ("laptop_sleeve", B, False)],
            [("spec_rows", "", "List<String>"), ("search_terms", "", S)]),
    "Watch": ("Product", [("movement", S, False), ("strap", S, False), ("water_resistance_m", I, False),
                          ("battery_days", I, False)],
              [("spec_rows", "", "List<String>"), ("search_terms", "", S)]),
    "Promotion": (None, [("code", S, True), ("percent", F, False), ("min_total", F, False),
                         ("start_date", S, False), ("end_date", S, False), ("active", B, False)],
                  [("is_valid", "today: String", B), ("discount_for", "subtotal: Float", F)]),
    "Cart": (None, [("cart_id", S, True)],
             [("add_item", "product: Product, quantity: Integer", "CartItem"),
              ("update_quantity", "product_id: String, quantity: Integer", "void"),
              ("remove_item", "product_id: String", "void"), ("calc_total", "", F), ("is_empty", "", B),
              ("clear", "", "void")]),
    "CartItem": (None, [("name", S, False), ("cart_price", F, False), ("quantity", I, False)],
                 [("sub_total", "", F)]),
    "Order": (None, [("order_id", S, True), ("address", S, False), ("discount", F, False),
                     ("shipping_fee", F, False), ("total", F, False), ("status", S, False),
                     ("created_at", S, False), ("idempotency_key", S, False)],
              [("subtotal", "", F), ("calc_total", "", F),
               ("change_status", "new_status: String, actor: String, at: String, note: String", "void"),
               ("can_cancel", "", B), ("last_update", "", S)]),
    "OrderItem": (None, [("name", S, False), ("unit_price", F, False), ("quantity", I, False)],
                  [("sub_total", "", F)]),
    "StatusChange": (None, [("status", S, False), ("actor", S, False), ("at", S, False), ("note", S, False)], []),
    "Payment": (None, [("payment_id", S, True), ("attempt_ref", S, False), ("amount", F, False),
                       ("currency", S, False), ("status", S, False), ("provider_ref", S, False),
                       ("created_at", S, False)],
                [("matches", "provider_ref: String", B), ("is_final", "", B)]),
    "Shipment": (None, [("shipment_id", S, True), ("carrier_ref", S, False), ("status", S, False)],
                 [("last_seq", "", I), ("add_milestone", "code: String, at: String, location: String", "Milestone")]),
    "Milestone": (None, [("seq", I, False), ("code", S, False), ("at", S, False), ("location", S, False)], []),
    "StockLevel": (None, [("physical", I, False), ("reserved", I, False), ("threshold", I, False)],
                   [("available", "", I), ("is_low", "", B), ("apply", "event: InventoryEvent", "void")]),
    "InventoryEvent": (None, [("event_id", S, True), ("kind", S, False), ("quantity", I, False),
                              ("reference", S, False), ("reason", S, False), ("created_at", S, False)], []),
    "ReplenishmentRequest": (None, [("request_id", S, True), ("quantity", I, False), ("status", S, False),
                                    ("created_at", S, False)], []),
    "Review": (None, [("review_id", S, True), ("rating", I, False), ("text", S, False), ("status", S, False),
                      ("created_at", S, False)],
               [("validate", "", "void")]),
}

# (from, to, from_mult, to_mult, name, kind, from_role, to_role); composition: from = whole
ASSOCIATIONS = [
    ("Customer", "Address", "1", "0..1", "delivers to", "assoc", "customer", "address"),
    ("Customer", "Cart", "1", "0..1", "owns", "assoc", "customer", "cart"),
    ("Cart", "CartItem", "1", "0..*", "contains", "comp", "cart", "items"),
    ("CartItem", "Product", "0..*", "1", "refers to", "assoc", "cart_items", "product"),
    ("Product", "Category", "0..*", "1", "belongs to", "assoc", "products", "category"),
    ("Customer", "Order", "1", "0..*", "places", "assoc", "customer", "orders"),
    ("Order", "OrderItem", "1", "1..*", "contains", "comp", "order", "items"),
    ("OrderItem", "Product", "0..*", "1", "refers to", "assoc", "order_items", "product"),
    ("Order", "Payment", "1", "0..*", "paid by", "assoc", "order", "payments"),
    ("Order", "Promotion", "0..*", "0..1", "uses", "assoc", "orders", "promotion"),
    ("Order", "Shipment", "1", "0..1", "shipped as", "assoc", "order", "shipment"),
    ("Order", "StatusChange", "1", "1..*", "records", "comp", "order", "history"),
    ("Shipment", "Milestone", "1", "0..*", "tracked by", "comp", "shipment", "milestones"),
    ("Product", "StockLevel", "1", "1", "has", "assoc", "product", "stock"),
    ("Product", "InventoryEvent", "1", "0..*", "explained by", "assoc", "product", "events"),
    ("Product", "ReplenishmentRequest", "1", "0..*", "replenished by", "assoc", "product", "requests"),
    ("Review", "Product", "0..*", "1", "about", "assoc", "reviews", "product"),
    ("Customer", "Review", "1", "0..*", "writes", "assoc", "customer", "reviews"),
    ("Review", "Order", "0..*", "1", "verified by", "assoc", "reviews", "order"),
]

# the two figures of each model (NhiCT Figures 2.1 / 2.2 and 4.1 / 4.2); a class drawn on both is an anchor
FIGURES = {
    "core": ["User", "Customer", "Address", "Cart", "CartItem", "Category", "Product", "Footwear", "Apparel", "Bag",
             "Watch", "Promotion", "Order", "OrderItem", "Payment", "Shipment"],
    "after": ["Customer", "Order", "Product", "Shipment", "StatusChange", "Milestone", "StockLevel",
              "InventoryEvent", "ReplenishmentRequest", "Review"],
}
