"""Writes redraw_spec.txt: the hand layout of the redrawn diagrams (plugin mode "redraw", Redraw.jsrc).

Use case diagrams are drawn with horizontal and vertical lines only:
  * use cases in one or two columns, at even rows;
  * an actor with several use cases has a vertical trunk just outside the system boundary and a horizontal
    branch into the side middle of each use case; an actor with one use case stands on its row (straight line);
  * include/extend lines leave and enter side middles, straight or with one bend, the keyword above a
    horizontal segment (beside a purely vertical line);
  * generalisations run around the actor column or share one bus into the parent's side.
usage: python tools/vpgen/ortho_spec.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
H = 52                       # ellipse height (even halves: VP moves shapes with odd half sizes by a pixel)
AW, AH = 40, 72              # actor box


def width(name):
    return max(200, (8 * len(name) + 40 + 19) // 20 * 20)


class UC:
    def __init__(self, code, system=None, top=30):
        self.code, self.system, self.top = code, system, top
        self.ucs, self.actors, self.lines, self.size = {}, {}, [], {}

    def uc(self, name, cx, cy, h=H, w=None):
        w = w or width(name)
        self.ucs[name] = (cx, cy, w, h)

    def bounds(self):
        xs = [cx - w / 2 for cx, cy, w, h in self.ucs.values()]
        xe = [cx + w / 2 for cx, cy, w, h in self.ucs.values()]
        ye = [cy + h / 2 for cx, cy, w, h in self.ucs.values()]
        left, right = int(min(xs)) - 50, int(max(xe)) + 50
        return left, self.top, right - left, int(max(ye)) + 50 - self.top

    def actor(self, name, side, cy, trunk=True):
        self.actors[name] = (side, cy, trunk)

    def link(self, a, b, sa, sb, label="R"):
        self.lines.append(f"{self.code}|@link|{a}|{b}|{sa}|{sb}|{label}")

    def path(self, a, b, sa, sb, pts):
        self.lines.append(f"{self.code}|@path|{a}|{b}|{sa}|{sb}|" + ";".join(f"{x},{y}" for x, y in pts))

    def emit(self, extra=()):
        left, top, w, h = self.bounds()
        right = left + w
        out = []
        if self.system:
            out.append(f"{self.code}|@box|{self.system}|{left}|{top}|{w}|{h}")
        for n, (cx, cy, uw, uh) in self.ucs.items():
            out.append(f"{self.code}|@at|{n}|{cx}|{cy}|{uw}|{uh}")
        self.ltrunk, self.rtrunk = left - 50, right + 50
        self.lx, self.rx = left - 200, right + 140          # actor box x (left / right column)
        for n, (side, cy, trunk) in self.actors.items():
            x = self.lx if side == "L" else self.rx
            out.append(f"{self.code}|@box|{n}|{x}|{cy - AH // 2}|{AW}|{AH}")
            if trunk:
                out.append(f"{self.code}|@bus|{n}|{self.ltrunk if side == 'L' else self.rtrunk}")
        return out + list(extra) + self.lines


def ucd1():
    d = UC("UCD1", "ABC Online Shop - Account and Catalogue")
    cx = 560
    for n, y in [("UC06 View Product Details", 110), ("UC04 Browse Products", 210), ("UC05 Search Products", 310),
                 ("UC01 Register Account", 410), ("UC03 Manage Profile", 540), ("UC02 Login", 640)]:
        d.uc(n, cx, y)
    d.actor("Visitor", "L", 260)
    d.actor("Customer", "L", 590)
    d.actor("Staff", "R", 640)
    lines = d.emit()
    gx = d.lx - 30
    d.lines = []
    d.path("Visitor", "Customer", "L", "L", [(gx, 260), (gx, 590)])
    return lines + d.lines


def ucd2():
    d = UC("UCD2", "ABC Online Shop - Cart, Order and Payment")
    A, B, C = 440, 820, 1210
    d.uc("UC07 Manage Shopping Cart", A, 110)
    d.uc("UC11 Track Order", A, 530)
    d.uc("UC10 View Order History", A, 710)
    d.uc("UC30 Check Product Availability", B, 110)
    d.uc("UC08 Place Order / Checkout", B, 340, h=60)
    d.uc("UC09 Make Payment", B, 580)
    d.uc("UC12 Cancel Order", B, 710)
    d.uc("UC13 Submit Review", B, 830)
    d.uc("UC29 Validate Cart", C, 220)
    d.uc("UC31 Calculate Order Total", C, 340)
    d.uc("UC32 Apply Promotion", C, 460)
    d.actor("Customer", "L", 410)
    d.actor("Payment Provider", "R", 580)
    d.actor("Sales Staff", "R", 710)
    o = "UC08 Place Order / Checkout"
    d.link("UC07 Manage Shopping Cart", "UC30 Check Product Availability", "R", "L")
    d.link(o, "UC30 Check Product Availability", "T", "B", "L")
    d.link(o, "UC29 Validate Cart", "T+70", "L")
    d.link(o, "UC31 Calculate Order Total", "R", "L")
    d.link(o, "UC32 Apply Promotion", "B+70", "L")
    d.link(o, "UC09 Make Payment", "B", "T", "L")
    d.link("UC10 View Order History", "UC12 Cancel Order", "R", "L")
    d.link("UC10 View Order History", "UC13 Submit Review", "B", "L")
    return d.emit()


def ucd3():
    d = UC("UCD3", "ABC Online Shop - Administration")
    cx = 560
    for n, y in [("UC17 Manage Customers", 110), ("UC16 Manage Promotions", 210), ("UC15 Manage Categories", 310),
                 ("UC18 Manage Reviews", 410), ("UC14 Manage Products", 510)]:
        d.uc(n, cx, y)
    d.actor("Administrator", "L", 310)
    d.actor("Sales Staff", "R", 110)
    return d.emit()


def ucd4():
    d = UC("UCD4", "ABC Online Shop - Operations and Reporting")
    cx = 540
    rows = [("UC19 Process Orders", 100), ("UC24 Manage Replenishment", 210), ("UC20 Manage Inventory", 330),
            ("UC21 Prepare Shipment", 420), ("UC22 Arrange Delivery", 510), ("UC23 Update Shipment Status", 600),
            ("UC25 View Management Dashboard", 720), ("UC26 Generate Sales Report", 810),
            ("UC27 Generate Inventory Report", 900), ("UC28 Generate Order and Exception Report", 990)]
    for n, y in rows:
        d.uc(n, cx, y)
    d.actor("Sales Staff", "L", 100)
    d.actor("Warehouse Staff", "L", 360)
    d.actor("Manager", "L", 855)
    d.actor("Supplier", "R", 210)
    d.actor("Shipping Provider", "R", 555)
    d.link("UC20 Manage Inventory", "UC24 Manage Replenishment", "T", "B", "L")
    return d.emit()


def uc00():
    d = UC("UC00", "ABC Online Shop")
    A, B = 480, 880
    rows = [("UC04 Browse Products", 90), ("UC05 Search Products", 170), ("UC01 Register Account", 250),
            ("UC07 Manage Shopping Cart", 350), ("UC08 Place Order / Checkout", 430), ("UC11 Track Order", 510),
            ("UC13 Submit Review", 590), ("UC02 Login", 690),
            ("UC14 Manage Products", 890), ("UC16 Manage Promotions", 970),
            ("UC19 Process Orders", 1070), ("UC20 Manage Inventory", 1170), ("UC21 Prepare Shipment", 1250),
            ("UC25 View Management Dashboard", 1350)]
    for n, y in rows:
        d.uc(n, A, y, h=44)
    d.uc("UC09 Make Payment", B, 430, h=44)
    d.uc("UC23 Update Shipment Status", B, 1170, h=44)
    d.uc("UC24 Manage Replenishment", B, 1310, h=44)
    for n, y in [("Visitor", 170), ("Customer", 520), ("Administrator", 930), ("Sales Staff", 1070),
                 ("Warehouse Staff", 1210), ("Manager", 1350)]:
        d.actor(n, "L", y)
    d.actor("Staff", "L", 790, trunk=False)          # abstract: the four staff actors log in through it
    for n, y in [("Payment Provider", 430), ("Shipping Provider", 1170), ("Supplier", 1310)]:
        d.actor(n, "R", y)
    d.link("UC08 Place Order / Checkout", "UC09 Make Payment", "R", "L")
    d.link("Staff", "UC02 Login", "R", "B")
    show = ["UC00|@show|UC02 Login|UseCase", "UC00|@show|Staff|Actor",
            "UC00|@ensure|Customer|UC02 Login|Association", "UC00|@ensure|Staff|UC02 Login|Association"]
    show += [f"UC00|@ensure|Staff|{n}|Generalization" for n in ("Administrator", "Sales Staff", "Warehouse Staff", "Manager")]
    lines = d.emit()
    gx = d.lx - 30
    d.lines = []
    d.path("Visitor", "Customer", "L", "L", [(gx, 170), (gx, 520)])
    for n, y in [("Administrator", 930), ("Sales Staff", 1070), ("Warehouse Staff", 1210), ("Manager", 1350)]:
        d.path("Staff", n, "L", "L", [(gx, 790), (gx, y)])
    return show + lines + d.lines


def ucai():
    d = UC("UC_AI", None, top=40)
    A, B = 560, 1000
    d.uc("Ask About My Orders", A, 90)
    d.uc("UC18 Manage Reviews", A, 210)
    d.uc("UC06 View Product Details", A, 330)
    d.uc("UC05 Search Products", A, 610, h=60)
    d.uc("UC25 View Management Dashboard", A, 970)
    d.uc("Flag Noisy Review", B, 210)
    d.uc("UC33 View Review Insights", B, 330)
    d.uc("UC34 View Recommendations", B, 430)
    d.uc("Search by Keyword", B, 610)
    d.uc("Search by Text and Image", B, 690)
    d.uc("Search by Image", B, 770)
    d.uc("Search by Voice", B, 850)
    d.actor("Customer", "L", 90)
    d.actor("Administrator", "L", 210)
    d.actor("Visitor", "L", 470)
    d.actor("Manager", "L", 970)
    d.actor("Speech / Vision Engine", "R", 810)
    d.link("UC18 Manage Reviews", "Flag Noisy Review", "R", "L")
    d.link("UC06 View Product Details", "UC33 View Review Insights", "R", "L")
    d.link("UC06 View Product Details", "UC34 View Recommendations", "B", "L")
    parent = "UC05 Search Products"
    bus = (A + width(parent) // 2 + B - width("Search by Text and Image") // 2) // 2
    for child, y in [("Search by Text and Image", 690), ("Search by Image", 770), ("Search by Voice", 850)]:
        d.path(parent, child, "R", "L", [(bus, 610), (bus, y)])
    d.link(parent, "Search by Keyword", "R", "L")
    lines = d.emit([f"UC_AI|@box|@note|{B - 130}|{940}|260|70"])
    gx = d.lx - 50
    d.lines = []
    d.path("Visitor", "Customer", "L", "L", [(gx, 470), (gx, 90)])
    return lines + d.lines


# ---------------------------------------------------------------- DM01 data model (ORM persistable classes)
# The persistent classes behind the 21 domain tables of abc_shop/dao/schema.sql (users holds User and Customer,
# ProductDetail is abstract with one table per kind; the technical tables sequence and audit_log are left out).
DM_CLASSES = {
    "User": "userId:String;name:String;email:String;passwordHash:String;role:String",
    "Customer": "createdAt:Date",
    "Address": "receiver:String;phone:String;street:String;city:String",
    "Category": "categoryId:String;name:String;detailKind:String",
    "Product": "productId:String;name:String;brand:String;color:String;price:Decimal;description:String;image:String;status:String",
    "ProductDetail": "",
    "FootwearDetail": "sizes:String;upperMaterial:String;sole:String;purpose:String",
    "ApparelDetail": "sizes:String;material:String;fit:String",
    "BagDetail": "capacityL:Decimal;material:String;laptopSleeve:Boolean",
    "WatchDetail": "movement:String;strap:String;waterResistanceM:Integer;batteryDays:Integer",
    "StockLevel": "physical:Integer;reserved:Integer;threshold:Integer",
    "InventoryEvent": "eventId:String;kind:String;quantity:Integer;reference:String;reason:String;createdAt:Date",
    "ReplenishmentRequest": "requestId:String;quantity:Integer;status:String;createdAt:Date",
    "Cart": "cartId:String",
    "CartItem": "name:String;cartPrice:Decimal;quantity:Integer",
    "Promotion": "code:String;percent:Decimal;minTotal:Decimal;startDate:Date;endDate:Date;active:Boolean",
    "Order": "orderId:String;address:String;discount:Decimal;shippingFee:Decimal;total:Decimal;status:String;createdAt:Date;idempotencyKey:String",
    "OrderItem": "name:String;unitPrice:Decimal;quantity:Integer",
    "StatusChange": "id:Integer;status:String;actor:String;at:Date;note:String",
    "Payment": "paymentId:String;attemptRef:String;amount:Decimal;currency:String;status:String;providerRef:String;createdAt:Date",
    "Shipment": "shipmentId:String;carrierRef:String;status:String",
    "Milestone": "seq:Integer;code:String;at:Date;location:String",
    "Review": "reviewId:String;rating:Integer;text:String;status:String;createdAt:Date",
}
# (whole or from, to, name, multiplicity at from, multiplicity at to, composition at the from end)
DM_ASSOCS = [
    ("Product", "ProductDetail", "described by", "1", "0..1", 1),
    ("Product", "Category", "belongs to", "0..*", "1", 0),
    ("CartItem", "Product", "refers to", "0..*", "1", 0),
    ("Cart", "CartItem", "contains", "1", "0..*", 1),
    ("Customer", "Cart", "owns", "1", "0..1", 0),
    ("Customer", "Address", "delivers to", "1", "0..1", 0),
    ("Customer", "Order", "places", "1", "0..*", 0),
    ("Order", "OrderItem", "contains", "1", "1..*", 1),
    ("OrderItem", "Product", "refers to", "0..*", "1", 0),
    ("Order", "StatusChange", "records", "1", "1..*", 1),
    ("Order", "Payment", "paid by", "1", "0..*", 0),
    ("Order", "Promotion", "uses", "0..*", "0..1", 0),
    ("Order", "Shipment", "shipped as", "1", "0..1", 0),
    ("Shipment", "Milestone", "tracked by", "1", "0..*", 1),
    ("Product", "StockLevel", "has", "1", "0..1", 0),
    ("Product", "InventoryEvent", "explained by", "1", "0..*", 0),
    ("Product", "ReplenishmentRequest", "replenished by", "1", "0..*", 0),
    ("Review", "Product", "about", "0..*", "1", 0),
    ("Customer", "Review", "writes", "1", "0..*", 0),
    ("Review", "Order", "verified by", "0..*", "1", 0),
]
DM_GENS = [("User", "Customer"), ("ProductDetail", "FootwearDetail"), ("ProductDetail", "ApparelDetail"),
           ("ProductDetail", "BagDetail"), ("ProductDetail", "WatchDetail")]


def dm01():
    code = "DM01"
    W, PITCH, X0 = 230, 360, 40
    col = lambda k: X0 + k * PITCH

    def height(n):
        return 46 + 19 * n + 12          # CE draws an attribute row about 19 px high

    grid = {   # class: (column, row)
        "FootwearDetail": (0, 1), "ApparelDetail": (1, 1), "BagDetail": (2, 1), "WatchDetail": (3, 1),
        "ReplenishmentRequest": (0, 2), "ProductDetail": (1, 2), "Address": (4, 2),
        "Category": (0, 3), "Product": (1, 3), "CartItem": (2, 3), "Cart": (3, 3), "Customer": (4, 3), "User": (5, 3),
        "InventoryEvent": (0, 4), "StockLevel": (1, 4), "Review": (3, 4),
        "OrderItem": (2, 5), "Order": (3, 5), "Shipment": (4, 5), "Milestone": (5, 5),
        "StatusChange": (2, 6), "Payment": (3, 7), "Promotion": (4, 6),
    }
    n_attr = {c: (len(a.split(";")) if a else 0) for c, a in DM_CLASSES.items()}
    rows = sorted({r for _, r in grid.values()})
    tops, y = {}, 40
    for r in rows:
        tops[r] = y
        hmax = max(height(n_attr[c]) for c, (_, rr) in grid.items() if rr == r)
        y += hmax + (110 if r in (1, 2, 4) else 90)
    box = {}
    for c, (k, r) in grid.items():
        w = 160 if c == "ProductDetail" else W
        x = col(k) + (W - w) // 2
        box[c] = (x, tops[r], w, height(n_attr[c]))
    cx = lambda c: box[c][0] + box[c][2] // 2
    cy = lambda c: box[c][1] + box[c][3] // 2

    out = [f"{code}|@diagram|DM01 Data Model (ORM Persistable Classes)"]
    for c in DM_CLASSES:
        x, yy, w, h = box[c]
        out.append(f"{code}|@class|{c}|{x}|{yy}|{w}|{h}|{1 if c == 'ProductDetail' else 0}|{DM_CLASSES[c]}")
    for a, b, nm, ma, mb, comp in DM_ASSOCS:
        out.append(f"{code}|@assoc|{a}|{b}|{nm}|{ma}|{mb}|{comp}")
    for g, sp in DM_GENS:
        out.append(f"{code}|@gen|{g}|{sp}")

    def off(c, y):                       # side offset that puts a horizontal line at height y
        o = y - cy(c)
        return f"{'+' if o >= 0 else ''}{o}"

    def chain(a, b, y, label="R"):        # straight horizontal link, a left of b
        out.append(f"{code}|@link|{a}|{b}|R{off(a, y)}|L{off(b, y)}|{label}")

    r3 = tops[3] + 40
    chain("Category", "Product", r3)
    chain("Product", "CartItem", r3)
    chain("CartItem", "Cart", r3)
    chain("Cart", "Customer", r3)
    chain("Customer", "User", r3)
    r5 = tops[5] + 40
    chain("OrderItem", "Order", r5)
    chain("Order", "Shipment", r5)
    chain("Shipment", "Milestone", r5)
    link = lambda a, b, sa, sb, lab="R": out.append(f"{code}|@link|{a}|{b}|{sa}|{sb}|{lab}")
    link("Product", "ProductDetail", "T", "B")
    link("Product", "StockLevel", "B", "T")
    link("Customer", "Address", "T", "B")
    link("Order", "Payment", "B", "T")
    link("Review", "Order", "B", "T")
    pb = box["Product"][1] + box["Product"][3]
    link("Product", "Review", f"R{off('Product', pb - 30)}", "T")
    link("Product", "OrderItem", f"R{off('Product', pb - 10)}", "T", "L")
    link("Product", "InventoryEvent", f"L{off('Product', pb - 20)}", "T", "L")
    link("Product", "ReplenishmentRequest", "T-95", "R", "L")
    link("Customer", "Review", "B-70", "R", "L")
    link("Order", "StatusChange", "B-70", "R", "L")
    link("Order", "Promotion", "B+70", "L")
    ygap = tops[5] - 45
    ox, ux = cx("Order") + 70, cx("Customer") + 60
    out.append(f"{code}|@path|Customer|Order|B+60|T+70|{ux},{ygap};{ox},{ygap}|R")
    bus = tops[2] - 55
    pdx = cx("ProductDetail")
    for kind in ("FootwearDetail", "BagDetail", "WatchDetail"):
        out.append(f"{code}|@path|ProductDetail|{kind}|T|B|{pdx},{bus};{cx(kind)},{bus}")
    link("ProductDetail", "ApparelDetail", "T", "B")
    return out


# ---------------------------------------------------------------- DCL05 data access layer
DCL05_DAOS = [
    ("CustomerDAO", 4, "find_by_email(email)"), ("ProductDAO", 6, "list_products(category_id=None, active_only=True)"),
    ("InventoryDAO", 7, "add_replenishment(request_id, product_id, quantity, at)"), ("PromotionDAO", 3, "save_promotion(promotion)"),
    ("ReviewDAO", 4, "exists(customer_id, product_id, order_id)"), ("CartDAO", 2, "get_cart(customer_id)"),
    ("OrderDAO", 6, "find_by_idempotency_key(key)"), ("PaymentDAO", 3, "get_by_attempt(attempt_ref)"),
    ("ShipmentDAO", 3, "get_by_carrier_ref(carrier_ref)"), ("AuditDAO", 2, "record(actor, action, entity, entity_id, detail=)")]


def dcl05():
    code, gap = "DCL05", 50
    hi = lambda ops: 46 + 8 + 19 * ops + 14
    width = lambda longest: max(220, 7 * len(longest) + 30)
    cols, x = [], 40
    for k in range(5):
        w = max(width(DCL05_DAOS[k][2]), width(DCL05_DAOS[k + 5][2]), width("SqliteInventoryDAO"))
        cols.append((x, w))
        x += w + gap
    out = []
    ha = max(hi(n) for _, n, _ in DCL05_DAOS[:5])
    hd = max(hi(n) for _, n, _ in DCL05_DAOS[5:])
    himpl = 46 + 19 + 14 + 8
    yA = 40
    yB = yA + ha + 70
    bus1 = yB + himpl + 40
    yM = bus1 + 40
    hdb = 46 + 19 * 2 + 19 * 8 + 20
    bus2 = yM + hdb + 40
    yC = bus2 + 40
    yD = yC + himpl + 70
    for k in range(5):
        cx, cw = cols[k]
        for (name, n, _), (yi, yimpl, grp) in ((DCL05_DAOS[k], (yA, yB, 1)), (DCL05_DAOS[k + 5], (yD, yC, 2))):
            out.append(f"{code}|@box|{name}|{cx}|{yi}|{cw}|{hi(n)}")
            out.append(f"{code}|@box|Sqlite{name}|{cx}|{yimpl}|{cw}|{himpl}")
            out.append(f"{code}|@link|{name}|Sqlite{name}|{'B' if grp == 1 else 'T'}|{'T' if grp == 1 else 'B'}|R")
    dbx, dbw = cols[2]
    dbc = dbx + dbw // 2
    out.append(f"{code}|@box|Database|{dbx}|{yM}|{dbw}|{hdb}")
    out.append(f"{code}|@box|VectorIndex|{cols[3][0]}|{yM}|{cols[3][1]}|{46 + 19 + 19 * 3 + 20}")
    out.append(f"{code}|@box|ImageStorage|{cols[4][0]}|{yM}|{cols[4][1]}|{46 + 19 + 19 * 3 + 20}")
    out.append(f"{code}|@link|VectorIndex|ImageStorage|R|L|R")
    for k in range(5):
        cx, cw = cols[k]
        c = cx + cw // 2
        for name, side, bus, dside in ((DCL05_DAOS[k][0], "B", bus1, "T"), (DCL05_DAOS[k + 5][0], "T", bus2, "B")):
            if c == dbc:
                out.append(f"{code}|@link|Sqlite{name}|Database|{side}|{dside}|R")
            else:
                out.append(f"{code}|@path|Sqlite{name}|Database|{side}|{dside}|{c},{bus};{dbc},{bus}|R")
    return out


HEAD = """# Tidy redraw (Redraw.jsrc), written by ortho_spec.py.
# CODE|@at|name|cx|cy|w|h  CODE|@box|name|x|y|w|h  CODE|@bus|actor|trunkX  CODE|@link|A|B|sideA|sideB|labelSide
# CODE|@path|A|B|sideA|sideB|x,y;...  CTX01|@ctx|...  SDxx|@seq|step|minGap
CTX01|@ctx|Customer / Visitor;Administrator;Sales Staff;Warehouse Staff|Payment Provider;Shipping Provider;Supplier;Manager|570|20|240|600|40|1150|40|160|190|80
SD01|@seq|42|150
SD02|@seq|42|150
SD03|@seq|42|150
SD04|@seq|42|150
SD05|@seq|42|150
SD06|@seq|42|150
"""

if __name__ == "__main__":
    body = []
    for f in (ucd1, ucd2, ucd3, ucd4, uc00, ucai, dm01, dcl05):
        body += f() + [""]
    with open(os.path.join(HERE, "redraw_spec.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEAD + "\n" + "\n".join(body))
    print("redraw_spec.txt:", sum(1 for l in body if l), "lines")
