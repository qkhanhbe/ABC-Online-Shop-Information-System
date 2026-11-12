import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = os.path.join(ROOT, "diagrams")
SRC = os.path.join(ROOT, "abc_shop")
DES = os.path.join(ROOT, "design")
GEN = os.path.join(DES, "generated", "abc_shop_design")


def sql_tables(*names):
    """CREATE TABLE statements of the script generated from the ER model."""
    text = open(os.path.join(DES, "create_tables.sql"), encoding="utf-8").read()
    out = []
    for n in names:
        a = text.index("CREATE TABLE " + n + " (")
        out.append(text[a:text.index(");", a) + 2])
    return "\n".join(out)


def gen_class(rel, name, keep=None):
    """One class of a generated module, optionally only the first `keep` methods."""
    text = open(os.path.join(GEN, rel), encoding="utf-8").read()
    m = re.search(r"((?:@dataclass\n)?class " + name + r"\b.*?)(?=\n\n\n|\Z)", text, re.S)
    body = m.group(1)
    if keep is not None:
        parts = re.split(r"\n(?=    (?:@abstractmethod\n    )?def )", body)
        body = "\n".join(parts[:keep + 1]) + ("\n    # ... " + str(len(parts) - keep - 1) + " more methods in the same form"
                                              if len(parts) > keep + 1 else "")
    return body


def gen_head(rel):
    """Module docstring and imports of a generated module."""
    text = open(os.path.join(GEN, rel), encoding="utf-8").read()
    return text[:text.index("\n\n\n")]


BLOCKS = [
    ("h1", "CHAPTER 4. DESIGN"),
    ("p", "This chapter follows the six steps our lecturer set for the design part of the essay. I start again from the "
          "class diagram of the analysis (Section 4.1), turn it into a data model and a real database (Section 4.2), "
          "update the design class diagram with typed attributes, methods and relationships (Section 4.3), place the "
          "classes in layers and show how they depend on each other (Section 4.4), generate code from that layered "
          "model (Section 4.5) and close with the decisions and their costs (Section 4.6). The work builds on the four "
          "transformation steps \"from analysis to design\" that we practised in Test 01, and on the search architecture "
          "of Assignment 06."),
    ("p", "All diagrams of the chapter belong to the same Visual Paradigm project as the rest of the essay "
          "(TieuLuan_KHANHBQ.vpp) and were drawn in Visual Paradigm Community Edition. I drew them through the "
          "Visual Paradigm MCP plugin, which adds shapes and lines through Visual Paradigm's Open API and routes every line "
          "horizontally and vertically around the boxes. The finishing touches the plugin cannot make, such as a "
          "keyword on a dependency or the size of the multiplicity labels, are done by a small plugin of my own "
          "(essay.gen). That plugin also reads the finished model back. It writes the SQL script of Section 4.2 and "
          "exports the design classes for the code generator of Section 4.5. The database and the code therefore come "
          "from the diagrams, not from a second copy typed by hand."),

    # ------------------------------------------------------------------ 4.1
    ("h2", "4.1. Class Diagram in Analysis"),
    ("p", "The analysis class diagram is the model of Section 2.5, built from the use case specifications with the "
          "noun-phrase method. For this chapter I updated it and checked it once more against the use cases. It names "
          "the things the shop has to remember and how they are connected. It has attributes but no methods, no "
          "screens and no decisions about storage. Every later step changes it, so I first list what I updated, "
          "then describe it in words and explain every relationship; each change in Sections 4.2 to 4.5 should be "
          "traceable to a line in this section."),
    ("table", "Updates of the analysis class diagram", ["Element", "Before (Section 2.5)", "Updated", "Reason"], [
        ["ReplenishmentRequest", "missing", "New class with requestId, quantity, status, createdAt", "UC24 creates a request that the supplier answers; it is information the shop keeps"],
        ["Customer - Review", "missing", "Association writes, 1 to 0..*", "A review is written by a customer; Review - Order alone does not say by whom"],
        ["Cart - Order", "missing", "Dependency &lt;&lt;create&gt;&gt; checkout", "Checkout uses the cart to create the order; no lasting link remains"],
        ["Customer - Cart", "1 to 1", "1 to 0..1", "The cart is created when the first product is added"],
        ["Association names", "eleven of eighteen named", "every association named", "Each line reads as a sentence: Order contains OrderItem"],
        ["Attributes", "some identifiers and dates missing", "paymentId, reviewId, createdAt, location, description, image, name in the lines", "Needed by the use cases (UC06 shows the image, UC11 the location)"]], [32, 30, 50, 53]),
    ("h3", "4.1.1. The classes in words"),
    ("p", "The twenty-three classes fall into four groups. The <b>people</b> group describes who uses the shop. User is "
          "anyone who logs in, with an id, a name, an email address and a role. Customer is a kind of User that "
          "also has a registration date. Staff accounts are plain Users whose role is sales, warehouse, admin or "
          "manager; they have no attributes of their own, so they need no subclass. Address holds the receiver, phone, "
          "street and city of one delivery address."),
    ("p", "The <b>shopping</b> group describes what a customer intends to buy and what was bought. Cart is the "
          "customer's open basket, and CartItem is one line of it, with a quantity and the cart price shown while the "
          "customer is still shopping. Order is created at checkout. It has a status, the discount, the shipping fee, "
          "the delivery address copied at that moment and the idempotency key of the checkout form. OrderItem is one "
          "line of the order with the unit price actually charged. StatusChange is one entry of the order's "
          "history: who changed the status, when and why. Promotion is a discount code with a percentage, a minimum "
          "total and a period of validity."),
    ("p", "The <b>fulfilment</b> group describes what happens after checkout. Payment is one payment attempt, with "
          "the attempt reference sent to the provider, the amount, the currency and the result. Shipment is one "
          "delivery with the carrier's reference, and Milestone is one carrier message (picked up, in transit, "
          "delivered) with a sequence number. Review is the customer's rating and text about a product they received."),
    ("p", "The <b>catalogue and stock</b> group describes what the shop sells. Product has a name, a brand, a colour, a "
          "price, a description, an image and a status (active or unpublished), and belongs to one Category. Its stock "
          "is a separate StockLevel with the physical and reserved quantities and a low-stock threshold. The "
          "derived attribute /available is physical minus reserved. The attributes that only one group of products has "
          "live in the abstract ProductDetail and its four kinds (FootwearDetail, ApparelDetail, BagDetail, WatchDetail); "
          "Category.detailKind names the kind its products use. Every change of the stock is an InventoryEvent of a "
          "kind (receipt, reserve, release, issue, adjust) with a reference that identifies its cause, and a "
          "ReplenishmentRequest asks the supplier for more."),
    ("p", "Two attributes look like duplicates but mean different things. CartItem.cartPrice and OrderItem.unitPrice "
          "both copy Product.price, but the cart price may still change before checkout, while the order price is a "
          "historical fact: the price the customer actually paid. Order.deliveryAddress is the same kind of copy, "
          "because a customer who moves must not change where an old parcel went."),
    ("h3", "4.1.2. Relationships"),
    ("p", "Choosing the kind of each relationship is where an analysis class diagram says the most about the business. "
          "The table gives every relationship its kind, its multiplicity and the reason behind it. Read the "
          "multiplicity from left to right: \"1 to 0..*\" between Customer and Order means that one customer places zero "
          "or more orders and every order is placed by exactly one customer. The updated diagram follows the table."),
    ("table", "Relationships of the analysis class diagram", ["Relationship", "Kind", "Multiplicity", "Reason"], [
        ["Customer - User", "Generalization", "-", "A customer is a user with a registration date"],
        ["Customer delivers to Address", "Aggregation", "1 to 0..1", "The address belongs to the customer but can be replaced"],
        ["Customer owns Cart", "Association", "1 to 0..1", "At most one open cart, created on first use"],
        ["Customer places Order", "Association", "1 to 0..*", "Any number of orders, each with one customer"],
        ["Customer writes Review", "Association", "1 to 0..*", "Each review has one author"],
        ["Cart contains CartItem", "Composition", "1 to 0..*", "Lines live only inside their cart; an empty cart is allowed"],
        ["Order contains OrderItem", "Composition", "1 to 1..*", "An order without lines cannot exist"],
        ["Order records StatusChange", "Composition", "1 to 1..*", "The history is part of the order and starts with its creation"],
        ["CartItem, OrderItem refers to Product", "Association", "0..* to 1", "Each line is about one product"],
        ["Order paid by Payment", "Association", "1 to 0..*", "Several attempts are possible (UC09 A5 retry)"],
        ["Order uses Promotion", "Association", "0..* to 0..1", "At most one code per order"],
        ["Order shipped as Shipment", "Association", "1 to 0..1", "A shipment exists only after packing"],
        ["Shipment tracked by Milestone", "Composition", "1 to 0..*", "Carrier messages about one shipment"],
        ["Review verified by Order; Review about Product", "Association", "0..* to 1", "A review needs a delivered order of that product (FR14)"],
        ["Product belongs to Category", "Association", "0..* to 1", "Every product is in one category"],
        ["Product has StockLevel", "Association", "1 to 1", "Stock is kept apart so that two roles do not edit one record (BP01, BP02)"],
        ["StockLevel explained by InventoryEvent", "Association", "1 to 0..*", "Every quantity is explained by events (FR19)"],
        ["Product replenished by ReplenishmentRequest", "Association", "1 to 0..*", "UC24 may ask several times for one product"],
        ["Cart to Order, &lt;&lt;create&gt;&gt; checkout", "Dependency", "-", "The cart is used to create the order; the order does not remember the cart"]], [52, 24, 22, 67]),
    ("figl", os.path.join(D, "CL01 Analysis Class Diagram.png"), "Analysis class diagram of ABC Online Shop, updated with association names, multiplicities and the checkout dependency - VP diagram \"CL01 Analysis Class Diagram\""),
    ("p", "The dependency from Cart to Order is the choice I would defend first. An association would claim that every "
          "order remembers the cart it came from, which is not true: the cart is emptied after checkout and used again. "
          "A dependency with the &lt;&lt;create&gt;&gt; keyword and the name checkout says exactly what happens. In the "
          "design this relationship becomes a method, Order.create_from_cart(cart), and not a stored key. The "
          "composition Order-StatusChange is the other one worth a word: the history is not a log kept beside the "
          "order, it is part of the order, and the state machine of Section 2.6 can only be trusted because every "
          "transition leaves an entry."),

    # ------------------------------------------------------------------ 4.2
    ("h2", "4.2. Data Model and Database"),
    ("p", "The data model decides what is stored and how the stored records are linked. I derived the physical model "
          "from the analysis classes with the mapping rules of Section 4.2.1. I drew it as two entity relationship "
          "diagrams (Figures ERD01 and ERD02), generated the SQL script from those diagrams and created a working "
          "database from the script (Section 4.2.3)."),
    ("h3", "4.2.1. From classes to tables"),
    ("p", "Most classes become one table each, but several relationships needed a decision. The table lists the "
          "decisions and the reason for each."),
    ("table", "Mapping rules from analysis classes to tables", ["Class or relationship", "Decision in the database", "Reason"], [
        ["User and Customer (generalization)", "One table users with a role column", "Customer adds only a date; staff add nothing. One table keeps login in one place"],
        ["Address (aggregation, 0..1)", "Table address whose key customer_id is also the foreign key", "One address per customer; deleting the customer removes it"],
        ["Cart (1 to 0..1)", "cart.customer_id NOT NULL UNIQUE", "UNIQUE is the database form of 0..1"],
        ["Compositions (lines, history, milestones)", "Child key contains the parent key: (cart_id, product_id), (order_id, product_id), (shipment_id, seq)", "A line cannot exist without its parent; one line per product"],
        ["Order", "Table customer_order", "ORDER is a reserved word in SQL"],
        ["Order uses Promotion", "Column promo_code, no foreign key", "The code is kept as it was used, even if the promotion is later deleted"],
        ["Order.deliveryAddress", "Column address (text)", "A historical copy, not a reference"],
        ["Cart to Order, &lt;&lt;create&gt;&gt;", "No table and no key", "It is an event, not stored data"],
        ["Rules of Chapter 2 (BR, NFR07)", "CHECK and UNIQUE constraints", "The database rejects what the code might miss"],
        ["Technical needs", "Tables sequence (readable ids O001) and audit_log (NFR06)", "Not in the analysis; required by design"]], [42, 65, 58]),
    ("h3", "4.2.2. Tables and relationships"),
    ("p", "The result is twenty-three tables: twenty-one from the twenty-three analysis classes (User and Customer share "
          "the table users, the abstract ProductDetail has no table of its own, and StatusChange becomes "
          "order_status_history) plus the technical tables sequence and audit_log. The table lists them with their keys; a "
          "key written as PK, FK is a primary key that is also a foreign key."),
    ("table", "The twenty-three tables of the database", ["Table", "Primary key", "Foreign keys", "Holds"], [
        ["users", "user_id", "-", "Customers and staff with role and password hash"],
        ["address", "customer_id (PK, FK)", "customer_id → users", "One delivery address per customer"],
        ["cart", "cart_id", "customer_id → users (UNIQUE)", "Open baskets"],
        ["cart_item", "cart_id, product_id", "cart_id → cart, product_id → product", "Basket lines with cart price"],
        ["customer_order", "order_id", "customer_id → users", "Orders with status, totals, idempotency key"],
        ["order_item", "order_id, product_id", "order_id → customer_order, product_id → product", "Order lines with the price paid"],
        ["order_status_history", "id", "order_id → customer_order", "Every status change"],
        ["payment", "payment_id", "order_id → customer_order", "Payment attempts (attempt_ref UNIQUE)"],
        ["shipment", "shipment_id", "order_id → customer_order (UNIQUE)", "One delivery per order"],
        ["shipment_milestone", "shipment_id, seq", "shipment_id → shipment", "Carrier messages in sequence"],
        ["category", "category_id", "-", "Product categories"],
        ["product", "product_id", "category_id → category", "Attributes every product has: name, brand, colour, price, status"],
        ["footwear_detail, apparel_detail, bag_detail, watch_detail", "product_id (PK, FK)", "product_id → product",
         "Attributes of one product group; category.detail_kind says which table"],
        ["stock_level", "product_id (PK, FK)", "product_id → product", "Physical, reserved, threshold"],
        ["inventory_event", "event_id", "product_id → product", "Typed stock events"],
        ["replenishment_request", "request_id", "product_id → product", "Requests to the supplier"],
        ["review", "review_id", "product_id → product, customer_id → users, order_id → customer_order", "Verified reviews"],
        ["promotion", "code", "-", "Discount codes"],
        ["audit_log", "id", "-", "Who changed what (NFR06)"],
        ["sequence", "name", "-", "Counters for readable ids"]], [32, 32, 58, 43]),
    ("p", "The twenty-two foreign keys are of two kinds, and it helps to read them by meaning. <b>Ownership</b> keys tie a "
          "record to the record it belongs to: a cart line to its cart, an order line, a payment, a shipment and a "
          "status change to their order, a milestone to its shipment, an address and a cart to their customer. "
          "The parent is mandatory and the key is NOT NULL. <b>Reference</b> keys point to something that lives on "
          "independently, such as the product of a line or of a review, or the category of a product. Deleting an "
          "order line must not delete the product. In ERD01 and ERD02 the notation is Visual Paradigm's crow's foot: a "
          "bar means one, a circle zero and the three-pronged foot many. A gold key marks a primary key, a key with a "
          "green arrow a column that is both primary and foreign key, N a column that may be empty and the red U a "
          "unique column. The model is split into two diagrams so that the column names stay readable; users, "
          "product and customer_order appear in both as views of the same tables."),
    ("figl", os.path.join(D, "ERD01 Physical Data Model - Customers, Carts and Orders.png"), "Physical data model, part 1: customers, carts, orders, payments and shipments - VP diagram \"ERD01\""),
    ("figl", os.path.join(D, "ERD02 Physical Data Model - Catalogue, Stock and Reviews.png"), "Physical data model, part 2: catalogue, stock, reviews and the technical tables - VP diagram \"ERD02\""),
    ("p", "Before generating the script I checked the tables against the normal forms. <b>1NF</b>: every column holds "
          "one value; an address is split into receiver, phone, street and city, and everything that repeats (lines, "
          "payments, milestones, events) has its own table. <b>2NF</b>: the composite keys are (cart_id, product_id), "
          "(order_id, product_id) and (shipment_id, seq), and every other column of those tables depends on the whole "
          "key; a line's name and price belong to that line, not to the product alone. <b>3NF</b>: no column depends on "
          "another non-key column. Three columns look like exceptions but are not. order_item.unit_price and "
          "order_item.name are the facts at checkout, and customer_order.total is the amount the customer confirmed; "
          "they must not change when the catalogue changes. The schema is therefore in third normal form, with these "
          "intended historical values."),
    ("h3", "4.2.3. Generating the database"),
    ("p", "Visual Paradigm generates SQL from a physical ERD through Tools > DB > Generate Database, which first needs a "
          "database configuration (a JDBC driver and a dialect) in the project. Its programming interface "
          "(DatabaseManager.generateCreateSQL) failed for every database type with \"Dialect class not found\" when "
          "it was called without that configuration, so the script of this section was not produced by that menu. Instead of "
          "typing the script by hand, I added a DDL export to my essay.gen plugin. It walks the ER model table by table "
          "and writes each column with its type and its NOT NULL, UNIQUE, DEFAULT and CHECK rules, then the primary key "
          "and every foreign key, taken from the relationship lines. The CHECK and DEFAULT rules are stored in the "
          "model itself, in the column specification of each table, so they are visible in Visual Paradigm and not only "
          "in the script. Tables are written parents first, so that every REFERENCES clause points to a table that "
          "already exists. The result is design/create_tables.sql with 23 CREATE TABLE statements and 22 foreign keys. "
          "Two of the generated statements look like this:"),
    ("code", sql_tables("stock_level", "cart_item")),
    ("p", "Each constraint carries a requirement. The CHECK on stock_level is the database side of \"stock never "
          "becomes negative\" (FR19, BR20). The UNIQUE key on customer_order.idempotency_key is UC08 A7: one order per "
          "submitted form. The UNIQUE key on cart.customer_id is the multiplicity 0..1 of Customer owns Cart. Keeping "
          "these rules in the database as well as in the code is intended redundancy: the code gives the user a clear "
          "message, and the database guarantees that no other path, such as a manual correction script, can break the "
          "rule."),
    ("p", "To see whether the script really works I created the database from it. The program design/build_db.py runs "
          "create_tables.sql on an empty SQLite file and compares the result with abc_shop/dao/schema.sql, the schema "
          "the application ships with. It then lets the real application seed one month of shop history into the "
          "generated database, through the same services the web pages use. Finally it runs six statements that the "
          "constraints must reject."),
    ("term", os.path.join(DES, "build_db_output.txt"), "The database created from the generated script, compared with the application schema, filled by the application and checked with statements that must fail", 165),
    ("p", "Block [2] shows the one real gap between model and schema. Two rules are composite unique keys: an "
          "inventory event is recorded once per (product, kind, reference), and a customer reviews a product once per "
          "order. Visual Paradigm's ERD marks uniqueness per column, and the Community Edition has no tool for a unique "
          "index over several columns. These two keys are therefore written only in schema.sql, and the services "
          "check them before inserting (InventoryService looks up the reference first, ReviewService.exists()). Block [3] "
          "is the strongest test: 16 orders with their lines, payments, shipments, stock events and reviews were "
          "stored in tables generated from the diagram, without a single error. Block [4] shows that the database "
          "itself refuses an order line for an unknown product, a second cart, a reservation above the physical "
          "stock, a rating of 6, a double-submitted checkout and an unknown role. The four triggers of BR-CAT-01 are "
          "the second gap: an ERD has no notation for a trigger, so they too live only in schema.sql."),
    ("p", "The menu path of Visual Paradigm Enterprise is the alternative way to produce the same database, and the steps "
          "are kept in the project's README so that it can be shown live: open ERD01 or ERD02, choose Tools > DB > "
          "Database Configuration, select SQLite with the bundled driver and the file design/abc_design_vp.db, then "
          "Tools > DB > Generate Database with \"Create database\" and \"Export to DDL\"; the DDL file it writes can be "
          "compared with create_tables.sql by build_db.py."),

    # ------------------------------------------------------------------ 4.3
    ("h2", "4.3. Class Diagram in Design"),
    ("p", "The design class diagram describes the classes that will be written as code. Every attribute has a type, "
          "every method has typed parameters and a return type, and every relationship says which class knows which. "
          "My starting point was the analysis model of Section 4.1 and the four steps of Test 01: add methods, replace "
          "call-only associations by use dependencies, introduce data access objects, and group the classes into "
          "packages. The first two steps are this section; the last two are Section 4.4."),
    ("h3", "4.3.1. What I updated"),
    ("p", "The table lists the changes from the analysis model to the design model. Most of them come from the "
          "database of Section 4.2 or from the target language, Python."),
    ("table", "Updates of the design classes", ["Element", "Analysis", "Design", "Reason"], [
        ["Names and types", "camelCase, String, DateTime", "snake_case, str, float, int, bool", "The design is written for Python (PEP 8); dates travel as ISO text, as in SQLite"],
        ["Methods", "none", "Typed operations in every model class", "Step 1 of Test 01; code generation needs the signatures"],
        ["Stored links to other aggregates", "Associations", "Directed associations named after the key field (customer_id, order_id, product_id)", "These objects are loaded by different DAOs; the design keeps the key, like the table"],
        ["Parts", "Compositions", "Compositions named items, history, milestones", "The whole holds the list of its parts"],
        ["Customer - Address", "Aggregation", "Directed association address, 0..1", "The customer object carries its address"],
        ["Cart to Order, &lt;&lt;create&gt;&gt;", "Dependency", "Order.create_from_cart(cart) + &lt;&lt;use&gt;&gt; Order → Cart", "A call, not a stored link"],
        ["Cart - Product", "via CartItem", "&lt;&lt;use&gt;&gt; Cart → Product for add_item(product, quantity)", "The method reads the product's id, name and price"],
        ["Order uses Promotion", "Association", "Directed association promo_code, 0..1", "The order keeps the code it used (Section 4.2.1)"],
        ["ReplenishmentRequest", "Class", "No class; a row written by InventoryDAO", "It has no behaviour; a class would only carry data the DAO already returns"],
        ["Customer.orders", "-", "Not in the model", "Orders are found by OrderDAO.find_by_customer; the field I once had in the code was never used and was removed"]], [32, 28, 55, 50]),
    ("p", "The change I thought about longest is the third row. In Step 2 of Test 01 I followed the lecturer's rule: "
          "when a method of class A takes an object of class B and uses its attributes, the design shows a "
          "&lt;&lt;use&gt;&gt; dependency from A to B instead of the association. I kept that rule for the calls, "
          "Order.create_from_cart(cart) and Cart.add_item(product). But for links that are stored, a dependency says too "
          "little: a cart must know whose cart it is, although no method takes a Customer. So I went back to "
          "associations, now directed, with the name of the field that holds the link. A name that ends in _id says "
          "that the field holds the other object's key, not the object. That is the deliberate decision \"reference by "
          "id between aggregates\": Payment, Shipment and Review are loaded and saved by other DAOs and other use cases "
          "than their Order, and an object reference would force every DAO to load half of the database."),
    ("h3", "4.3.2. Attributes and methods"),
    ("p", "The model classes keep the attributes of the analysis, now typed, with the exceptions above. Attributes are "
          "public (+), because a Python dataclass field is read directly by the DAOs and the views and the language has "
          "no private fields. The methods come from Step 1 of Test 01, where the lecturer distinguished two kinds of "
          "method. A method of the class itself works on the class's own data, such as calc_total() in Cart. A method "
          "linked to another class takes an object of that class as a parameter and uses its attributes, such as "
          "add_item(product, quantity), which reads the product's id, name and price."),
    ("table", "Methods of the model classes", ["Class", "Methods of the class itself", "Methods linked to another class"], [
        ["User / Customer", "can(permission)", "update_profile(name, address : Address)"],
        ["Address", "is_complete(), one_line()", "-"],
        ["Cart / CartItem", "find, update_quantity, remove_item, calc_total, is_empty, clear / sub_total", "add_item(product : Product, quantity)"],
        ["Order / OrderItem", "subtotal, calc_total, change_status, can_cancel, last_update / sub_total", "create_from_cart(order_id, cart : Cart, ...)"],
        ["Payment", "matches(attempt_ref, amount, currency), is_final()", "-"],
        ["Shipment", "last_seq()", "add_milestone(milestone : Milestone)"],
        ["Review", "validate()", "-"],
        ["Product / Promotion", "is_active, search_text, update_price / is_valid, discount_for", "-"],
        ["StockLevel", "available(), is_low()", "apply(event : InventoryEvent)"]], [30, 82, 53]),
    ("p", "Three placements are worth explaining. calc_total() is in Cart and Order while sub_total() is in CartItem and "
          "OrderItem: each line computes its own amount and the whole adds the lines, so no class reaches inside "
          "another to multiply prices; each class is the information expert for its own total. change_status() is in "
          "Order, not in a service, because the transition table of Section 2.6 is a property of the order: a service "
          "decides <i>when</i> to change a status, never <i>whether</i> a transition is legal. And apply(event) is in "
          "StockLevel, because the rule \"never negative\" belongs to the stock, not to whoever records the event."),
    ("p", "The three figures show the updated design classes, split like the ERD for legibility: customers, carts and "
          "orders, then payment, shipment and review of an order, then the catalogue and the stock. A class that "
          "belongs to another figure appears with its name only, for example Product in the first figure and Order in "
          "the second and third."),
    ("figl", os.path.join(D, "DCL01 Design Classes - Customers, Carts and Orders.png"), "Design classes, part 1: customers, carts and orders with typed attributes, methods, key fields and compositions - VP diagram \"DCL01\""),
    ("fig", os.path.join(D, "DCL02 Design Classes - Payment, Shipment and Review.png"), "Design classes, part 2: payment, shipment and review of an order - VP diagram \"DCL02\"", 150),
    ("fig", os.path.join(D, "DCL03 Design Classes - Catalogue and Inventory.png"), "Design classes, part 3: catalogue, promotion and event-based stock - VP diagram \"DCL03\"", 150),
    ("h3", "4.3.3. Relationships"),
    ("p", "The table explains every relationship of the design classes and how it appears in the code. Read together "
          "with the relationship table of Section 4.1.2, it shows what happened to each analysis relationship."),
    ("table", "Relationships of the design classes and their form in code", ["Relationship", "Kind and multiplicity", "Name", "Form in the code"], [
        ["Customer - User", "Generalization", "-", "class Customer(User)"],
        ["Customer → Address", "Association, 1 to 0..1", "address", "Field address: Optional[Address]"],
        ["Cart, Order with their lines; Order with StatusChange; Shipment with Milestone", "Composition, 1 to 0..* / 1..*", "items, history, milestones", "Field list[...] with default_factory=list"],
        ["Cart, Order, Review → Customer", "Association, 0..1 / 0..* to 1", "customer_id", "Field customer_id: str (key)"],
        ["CartItem, OrderItem, StockLevel, InventoryEvent, Review → Product", "Association, 0..* to 1", "product_id", "Field product_id: str (key)"],
        ["Payment, Shipment, Review → Order", "Association, 0..* / 0..1 to 1", "order_id", "Field order_id: str (key)"],
        ["Product → Category", "Association, 0..* to 1", "category_id", "Field category_id: str (key)"],
        ["Order → Promotion", "Association, 0..* to 0..1", "promo_code", "Field promo_code: str (code)"],
        ["Order, Cart, StockLevel &lt;&lt;use&gt;&gt;", "Dependency", "-", "Parameter types of create_from_cart, add_item, apply"]], [55, 38, 28, 44]),
    ("p", "For a key field the direction of the association follows the foreign key of Section 4.2: the class whose "
          "table holds the key holds the field, so Cart → Customer matches cart.customer_id and CartItem → Product "
          "matches cart_item.product_id. For a composition the direction is reversed: in the database the key sits in "
          "the part (order_item.order_id), but in the code the whole holds the list of parts, because the parts are "
          "created and read through their owner and never on their own."),

    # ------------------------------------------------------------------ 4.4
    ("h2", "4.4. Layers, Classes and Relationships"),
    ("p", "Web-based e-commerce systems are usually built in layers, and the lecture recommends three layers in the MVC "
          "style. I compared this with two alternatives. A single-layer design, in which each page reads and writes "
          "the database itself, is quick to start but repeats the root cause of the shop's problems: data handled in "
          "many places in many ways. Microservices (catalogue, orders, payments, search as separate services) would "
          "suit a large shop with several teams. Here they would add network calls and distributed consistency "
          "problems to a checkout that must reserve stock and create an order atomically. A <b>layered monolith</b> is "
          "the right size: one deployable application, divided inside so that each part can change alone (NFR09), and "
          "divisible into services later along the same package lines."),
    ("h3", "4.4.1. Layers and packages"),
    ("p", "The design keeps the view, controller, DAO and model packages of the lecture's MVC model and adds two "
          "packages. A <b>service</b> package between controller and DAO holds the business rules of each use case, "
          "because putting the checkout rules into a controller would mix HTTP handling with stock and payment logic "
          "and make both hard to test. An <b>ai</b> package sits beside the services at the same level, because the "
          "AI components of Chapter 3 are application logic that reads the same DAOs. The six packages are:"),
    ("bullets", [
        "<b>view</b>: the module templates, one function per page (home, product, cart, checkout, track, staff and report pages); it holds no rule;",
        "<b>controller</b>: WebApp (the router and front controller), Request and Response, and five controllers, one per group of use cases;",
        "<b>service</b>: ten services, one per area (auth, catalogue, cart, checkout, payment, order, inventory, shipment, review, report), and the two gateway interfaces to the providers;",
        "<b>ai</b>: the search components of Assignment 06 (SearchService, QueryService, SpeechService, ImageService, RankingService), ReviewInsightService and RecommenderService;",
        "<b>dao</b>: Database, ten DAO interfaces and their SQLite implementations (not drawn), VectorIndex and ImageStorage;",
        "<b>model</b>: the twenty-three design classes of Section 4.3 in eight sub-packages that follow the life cycle of the data: customer, cart, order, payment, shipment, review, product, inventory."]),
    ("p", "Dependencies run controller → view, controller → service and ai, service and ai → dao, and dao → model, plus "
          "service and ai → model, because services receive, change and return model objects. Nothing goes from view or "
          "controller to dao, nothing goes upwards, and nothing in model depends on anything. The module shop.py is the "
          "composition root, the only place that creates objects and connects the layers. It is not drawn because "
          "it depends on every package by definition. Cart and CartItem form their own sub-package, because a customer "
          "can abandon a cart without affecting any order; Order, OrderItem and StatusChange are together because they "
          "only exist after a purchase."),
    ("figl", os.path.join(D, "PKG01 Layers, Packages and Classes.png"), "Layers of the application: the six packages, their classes and the &lt;&lt;use&gt;&gt; dependencies between them - VP diagram \"PKG01\""),
    ("h3", "4.4.2. Data access objects"),
    ("p", "The dao layer separates storage from business logic. A data access object collects every read and write for "
          "one kind of model object. It has two parts: an interface that declares <i>what</i> can be done "
          "(get_order(id), save_order(order)) and an implementation that knows <i>how</i> (SQL against the tables of "
          "Section 4.2). Services depend only on the interfaces, so the storage can change without touching them. Two "
          "decisions are worth recording. A missing record returns None or an empty list instead of raising an error, "
          "because \"not found\" is an expected outcome of several use cases (UC11 E2) and the service decides what it "
          "means. And all implementations share one Database object, which owns the connection and offers "
          "transaction(): a service that must change several kinds of data atomically opens one transaction, and every "
          "DAO call inside it joins it."),
    ("table", "DAO interfaces of the dao layer", ["Interface", "Main methods", "Tables behind it"], [
        ["CustomerDAO", "get_user, find_by_email, save_user, list_customers", "users, address"],
        ["ProductDAO", "get_product, list_products(category_id, active_only), save_product, list_categories", "product, category"],
        ["InventoryDAO", "get_stock, save_stock, find_event(product, kind, ref), add_event, add_replenishment", "stock_level, inventory_event, replenishment_request"],
        ["CartDAO", "get_cart(customer_id) (created on first use), update_cart", "cart, cart_item"],
        ["PromotionDAO", "get_promotion(code), save_promotion, list_promotions", "promotion"],
        ["OrderDAO", "get_order, find_by_idempotency_key, find_by_customer, find_by_status, save_order", "customer_order, order_item, order_status_history"],
        ["PaymentDAO", "get_by_attempt(ref), for_order, save_payment", "payment"],
        ["ShipmentDAO", "get_by_order, get_by_carrier_ref, save_shipment", "shipment, shipment_milestone"],
        ["ReviewDAO, AuditDAO", "for_product, exists, save_review / record, recent", "review / audit_log"]], [28, 85, 52]),
    ("h3", "4.4.3. One slice through the layers"),
    ("p", "A package diagram shows the layers but not the classes that talk to each other. The next figure therefore "
          "cuts one slice through all five layers: everything that takes part when a customer adds a product to the "
          "cart (UC07, with the included UC30 Check Product Availability). The templates module in view shows the cart. "
          "OrderController in controller handles the form and uses CartService. CartService uses three DAO "
          "interfaces, because it needs the cart, the product and the stock, and each DAO uses the model class it returns. "
          "The SQLite implementations are left out because they add one realization arrow per interface and no new "
          "dependency. All dashed arrows between layers point downwards, except the one from the controller to the "
          "view it renders. The same links also appear inside the class boxes, as the attributes cart_service of "
          "OrderController and carts, products and inventory of CartService. The attribute is how the object holds "
          "its collaborator in the code; the &lt;&lt;use&gt;&gt; arrow is how the layer diagram shows the dependency."),
    ("figl", os.path.join(D, "DCL04 Layer Slice - Add a Product to the Cart.png"), "One slice through the layers: the classes that take part in adding a product to the cart - VP diagram \"DCL04\""),
    ("table", "One request through the layers: a customer adds two units of a product to the cart", ["Step", "Layer and class", "What happens"], [
        ["1", "view: templates.product", "The product page posts product_id and qty to /cart/add"],
        ["2", "controller: WebApp, OrderController.add_to_cart", "Routes the request; checks the role 'cart'; calls the service with the session customer id"],
        ["3", "service: CartService.add_item", "Loads the product (ProductDAO) and the cart (CartDAO); checks availability with InventoryDAO (UC30)"],
        ["4", "model: Cart.add_item", "Adds to an existing line or creates one with the current price"],
        ["5", "dao: CartDAO.update_cart", "Stores the cart and its lines in cart and cart_item in one transaction"],
        ["6", "controller → view", "Redirects to /cart, which templates.cart renders"]], [12, 62, 91]),
    ("h3", "4.4.4. Services and controllers"),
    ("p", "Every use case has a home in one service, and every service receives its collaborators through its "
          "constructor, so a test can build it on an in-memory database or replace the payment gateway."),
    ("table", "Service classes of the service layer", ["Service", "Responsibility", "Collaborators", "Use cases"], [
        ["AuthService", "Register, login, password hashing, role checks", "CustomerDAO, AuditDAO", "UC01-02"],
        ["CatalogService", "Browse, product details with availability, product and promotion maintenance", "ProductDAO, InventoryDAO, PromotionDAO", "UC04, UC06, UC14, UC16"],
        ["CartService", "Cart lines, availability, cart validation", "CartDAO, ProductDAO, InventoryDAO", "UC07, UC29-30"],
        ["CheckoutService", "Quote, promotion, atomic order creation, payment request", "CartDAO, OrderDAO, PromotionDAO, CartService, InventoryService, PaymentService", "UC08, UC31-32"],
        ["PaymentService", "Payment attempts, verified callbacks, failures", "PaymentDAO, OrderDAO, InventoryService, PaymentGateway", "UC09"],
        ["OrderService", "History, tracking, cancellation, processing queue", "OrderDAO, ShipmentDAO, PaymentService, InventoryService", "UC10-12, UC19"],
        ["InventoryService", "Idempotent stock events, low stock, replenishment", "InventoryDAO, ProductDAO", "UC20, UC24"],
        ["ShipmentService", "Packing, delivery request, milestones", "ShipmentDAO, OrderDAO, InventoryService, ShippingGateway", "UC21-23"],
        ["ReviewService, ReportService", "Eligibility and moderation / dashboard and reports", "ReviewDAO, OrderDAO / OrderDAO, ProductDAO, InventoryDAO", "UC13, UC18 / UC25-28"]], [30, 52, 60, 23]),
    ("p", "The controllers are the system's interface to the web browser. A route without a use case is either a "
          "missing requirement or not needed, so every route is listed with the use case it serves. Security (NFR05) is "
          "met by structure: the router loads the user of the session once, and every service method that changes data "
          "checks the caller's permission, so a new page cannot forget the check. A customer's own data is always read "
          "with the customer id of the session, never with an id taken from the request."),
    ("table", "Routes of the web application and the use cases they serve", ["Method and path", "Controller", "Use case", "Role"], [
        ["GET /, GET /product/{id}", "ShopController", "UC04, UC06, UC33-34", "any"],
        ["GET|POST /search", "ShopController", "UC05 (text, voice, image)", "any"],
        ["GET|POST /login, /register", "AccountController", "UC01, UC02", "any"],
        ["GET /cart, POST /cart/add, /cart/update", "OrderController", "UC07", "customer"],
        ["GET|POST /checkout", "OrderController", "UC08, UC09, UC29-32", "customer"],
        ["GET /orders, /orders/{id}, POST .../cancel, .../review", "OrderController", "UC10-13", "customer (own orders)"],
        ["GET /staff/orders, POST .../{process|hold|pack|ship}", "StaffController", "UC19, UC21, UC22", "sales, warehouse"],
        ["GET|POST /staff/inventory, /admin/reviews", "StaffController", "UC20, UC24, UC18", "warehouse, admin"],
        ["GET /reports", "ReportController", "UC25-28", "manager"]], [62, 32, 40, 31]),
    ("p", "Checkout is the request where layering matters most, so its design sequence diagram uses the real class and "
          "method names. Messages 3-4 implement UC08 A7: the idempotency key of the form is looked up first, and a "
          "second submission returns the existing order. Messages 8-10 run inside one database transaction (E1), and "
          "payment is requested only after the transaction has committed, so that a provider never receives a request "
          "for an order that does not exist."),
    ("fig", os.path.join(D, "SD05 Checkout Through the Layers (Design).png"), "Checkout through the layers - VP diagram \"SD05 Checkout Through the Layers (Design)\"", 165),
    ("p", "Order tracking is the design counterpart of the analysis sequence SD02. The analysis control object becomes "
          "two classes: OrderController.track handles the request and first asks AuthService.require for the role "
          "own_orders (messages 2-4), and OrderService.track does the work of the use case (5-11). OrderService.own_order "
          "reads the order with OrderDAO.get_order and raises NotFound both when the order does not exist and when it "
          "belongs to another customer, so a foreign order id looks exactly like a missing one (UC11 E2, NFR05). "
          "ShipmentDAO.get_by_order returns the shipment, which is absent before packing; the timeline is then built "
          "from the order history alone, otherwise the carrier milestones are merged in by time. The view "
          "templates.track renders the page (12-13). The analysis entities Order and Shipment are now read through "
          "their DAOs, which the analysis model did not need to know. The two error branches and the optional "
          "milestones are written as a guard note under the lifelines with the message numbers they belong to."),
    ("fig", os.path.join(D, "SD06 Track Order (Design).png"), "Order tracking through the layers - VP diagram \"SD06 Track Order (Design)\"", 165),

    # ------------------------------------------------------------------ 4.5
    ("h2", "4.5. Code Generated from the Layered Model"),
    ("p", "The last design step checks the model in the strictest way I know: turning it into code that an interpreter "
          "accepts and comparing it with the program. The Community Edition of Visual Paradigm has no code generator, and "
          "Python is not one of Visual Paradigm's target languages anyway. I therefore wrote design/generate_code.py. "
          "With --live it reads the design classes of DCL01 to DCL04 from the open project through the MCP plugin "
          "(classes, owners, attributes, operations, relationships with roles and multiplicities) and stores them in "
          "model_export.json; then it writes one Python module per model sub-package and per class of the other "
          "layers. Because the export is stored, the code can be regenerated without Visual Paradigm, and running the "
          "script again after every change of the diagrams keeps the code from drifting away from them."),
    ("h3", "4.5.1. From model elements to Python"),
    ("p", "The mapping rules are kept simple, so that anyone can predict the code from the diagram."),
    ("table", "Mapping rules from the design model to Python", ["Model element", "Python code"], [
        ["Layer package (view, controller, service, dao, model)", "Python package (folder) of abc_shop_design"],
        ["Sub-package of model (cart, order, ...)", "Module model/cart.py, model/order.py, ..."],
        ["Class of model", "@dataclass class; every field gets a default value"],
        ["Class of another layer", "class whose __init__ receives and stores its attributes (the collaborators)"],
        ["Class with &lt;&lt;interface&gt;&gt; (DAO)", "class CartDAO(ABC) with @abstractmethod methods, collected in dao/interfaces.py"],
        ["&lt;&lt;module&gt;&gt; (templates)", "module-level functions"],
        ["Generalization Customer → User", "class Customer(User) and an import of the base class"],
        ["Attribute +name : Type", "field name: Type"],
        ["Navigable association end with a name ending in _id / _code", "field holding the key: customer_id: str  # key of Customer [1]"],
        ["Composition or association with a many end", "field items: list[CartItem] = field(default_factory=list)"],
        ["Association with a 0..1 end", "field address: Optional[Address] = None"],
        ["Operation +name(p : T) : R", "def name(self, p: T) -> R: raise NotImplementedError"],
        ["&lt;&lt;use&gt;&gt; dependency and types in signatures", "import of the supplier under TYPE_CHECKING (no import cycle at run time)"]], [70, 95]),
    ("h3", "4.5.2. Packages and classes"),
    ("p", "The generated project has five packages with twelve modules and twenty-eight classes. The program "
          "design/check_code.py checks the result. It lists the packages and classes, compiles and imports every "
          "module, and then compares each generated class with the hand-written class of the same name in abc_shop/: "
          "every field and every method of the model must exist in the code. Finally it prints the members of one "
          "generated class."),
    ("term", os.path.join(DES, "check_code_output.txt"), "Packages and classes generated from the model, compiled, imported and compared with the hand-written application", 165),
    ("p", "Block [3] is the point of the exercise: all 28 classes of the model exist in the application with every field "
          "and method the diagram promises. Getting there was the best review of the model I have done. The first "
          "comparison found a field orders in the hand-written Customer that no diagram had and no code used; I removed "
          "it from the code rather than adding it to the model. It also showed that StockLevel.available is a "
          "property in the code and a method in the model, a Python detail that the comparison accepts. And it found "
          "that the package diagram could not be read by the generator, because the plugin's "
          "relationship export works only on class diagrams. Package ownership is therefore read from the owner of "
          "each class on the class diagrams, which is the same information."),
    ("h3", "4.5.3. Class code"),
    ("p", "The generated classes show the relationships of Section 4.3 in their plainest form. The module of the cart "
          "sub-package comes first. The composition with CartItem becomes the list items, the association with Customer "
          "the key field customer_id, and the &lt;&lt;use&gt;&gt; dependency on Product an import for type checking "
          "only, because add_item(product) needs the type but Cart stores no product:"),
    ("code", gen_head("model/cart.py") + "\n\n\n" + gen_class("model/cart.py", "Cart", 2) + "\n\n\n" + gen_class("model/cart.py", "CartItem")),
    ("p", "Generalization is the base class of the generated class; the association with Address is an optional "
          "field, because the multiplicity is 0..1:"),
    ("code", gen_class("model/customer.py", "Customer")),
    ("p", "Above the model, a DAO interface becomes an abstract base class, and the service holds the three DAO "
          "interfaces of the slice as the attributes shown in its class box in DCL04:"),
    ("code", gen_class("dao/interfaces.py", "CartDAO") + "\n\n\n" + gen_class("service/cart_service.py", "CartService", 2)),
    ("h3", "4.5.4. What the generated code does and does not contain"),
    ("p", "The generated code contains the whole structure: packages, modules, classes, fields, signatures, inheritance "
          "and the key fields of every stored link. It does not contain behaviour; every method body raises "
          "NotImplementedError. That is the natural limit of generating code from a class diagram, which describes what "
          "exists and not what happens. The behaviour comes from the use case specifications, the activity and sequence "
          "diagrams and the state machine, and Chapter 5 describes how it was written. Two smaller gaps are intended. The "
          "DAO implementations need SQL that matches the tables of Section 4.2, which is written by hand against the "
          "generated schema. And a composition and an association look the same in Python; the comment after the "
          "field is the only trace of the difference, which shows in behaviour: deleting a cart also deletes its lines "
          "(ON DELETE CASCADE in schema.sql)."),

    # ------------------------------------------------------------------ 4.6
    ("h2", "4.6. Conclusion"),
    ("p", "The design started from twenty-three analysis classes and ended with a database of twenty-three tables and "
          "twenty-two foreign keys, generated from the physical model, and with twenty-eight Python classes in five layers generated from the "
          "class diagrams, all of which exist in the running application. Each step could be checked against the one "
          "before it. The tables were checked against the classes through the mapping rules, the design classes "
          "against the tables through the direction of the key fields, and the layers against the use cases through "
          "the request of Section 4.4.3. The code was checked against the diagrams by check_code.py, and the database "
          "by build_db.py. The table shows how the design serves the non-functional requirements of Chapter 1."),
    ("table", "Non-functional requirements and the parts of the design that serve them", ["Requirement", "Part of the design"], [
        ["NFR09 Maintainability", "Layers with downward dependencies; services depend on DAO interfaces, not on SQLite; a test enforces the layer rule"],
        ["NFR05 Access control", "Permission checks in the services; customer data read with the session's customer id"],
        ["NFR06 Auditability", "audit_log table and AuditDAO for price, stock, status and moderation changes"],
        ["NFR07 Integrity", "Idempotency key, unique attempt reference, unique stock event reference, milestone sequence; CHECK and UNIQUE rules generated from the ERD"],
        ["NFR10 Privacy", "Payment stores status and references only; the provider handles card data"],
        ["NFR01-02 Performance", "Read-only queries for browsing; the vector index is kept in memory and rebuilt only when the catalogue changes"],
        ["AI-N1 Replaceable AI", "AI components in their own package behind fixed methods: transcribe, encode, search, analyse, similar"]], [42, 123]),
    ("p", "The table below records the main decisions in a compact form inspired by architecture decision records: the "
          "decision, the alternative I rejected and the price I accepted. The third column matters most to me, because "
          "it shows what each decision gives up."),
    ("table", "Design decisions, rejected alternatives and accepted costs", ["Decision", "Rejected alternative", "Accepted cost"], [
        ["Layered monolith, MVC + service + DAO", "Microservices", "Parts cannot be scaled separately"],
        ["Service layer between controller and DAO", "Rules in controllers", "One more class per area"],
        ["Reference by key between aggregates", "Object references everywhere", "Extra DAO calls to load related data"],
        ["One users table for all roles", "One table per role", "Role-specific columns would need nullable columns"],
        ["Order owns its transition table", "Status checks in each service", "Model and diagram must change together"],
        ["Stock as typed events", "Stock as one editable number", "More rows; the balance is recalculated"],
        ["SQL and Python generated from the model", "Typing them by hand", "Two plugin scripts to maintain"],
        ["Rules in database and code", "Rules only in code", "Rules written twice"]], [55, 50, 60]),
    ("p", "Testability follows from the same structure: every service depends on DAO interfaces and receives them "
          "through its constructor, so a test can build the whole shop on an in-memory database or give it a payment "
          "gateway that times out. The next step of the lecturer's plan is the evaluation of the code, and the "
          "generated classes are its starting point. Chapter 5 shows how the method bodies were filled in, and how far "
          "the running code still matches this model."),
]
