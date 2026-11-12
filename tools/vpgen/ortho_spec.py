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
            ("UC13 Submit Review", 590), ("UC14 Manage Products", 690), ("UC16 Manage Promotions", 770),
            ("UC19 Process Orders", 870), ("UC20 Manage Inventory", 970), ("UC21 Prepare Shipment", 1050),
            ("UC25 View Management Dashboard", 1150)]
    for n, y in rows:
        d.uc(n, A, y, h=44)
    d.uc("UC09 Make Payment", B, 430, h=44)
    d.uc("UC23 Update Shipment Status", B, 950, h=44)
    d.uc("UC24 Manage Replenishment", B, 1090, h=44)
    for n, y in [("Visitor", 170), ("Customer", 470), ("Administrator", 730), ("Sales Staff", 870),
                 ("Warehouse Staff", 1010), ("Manager", 1150)]:
        d.actor(n, "L", y)
    for n, y in [("Payment Provider", 430), ("Shipping Provider", 950), ("Supplier", 1090)]:
        d.actor(n, "R", y)
    d.link("UC08 Place Order / Checkout", "UC09 Make Payment", "R", "L")
    lines = d.emit()
    gx = d.lx - 30
    d.lines = []
    d.path("Visitor", "Customer", "L", "L", [(gx, 170), (gx, 470)])
    return lines + d.lines


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


HEAD = """# Tidy redraw (Redraw.jsrc), written by ortho_spec.py.
# CODE|@at|name|cx|cy|w|h  CODE|@box|name|x|y|w|h  CODE|@bus|actor|trunkX  CODE|@link|A|B|sideA|sideB|labelSide
# CODE|@path|A|B|sideA|sideB|x,y;...  CTX01|@ctx|...  SDxx|@seq|step|minGap
CTX01|@ctx|Customer / Visitor;Administrator;Sales Staff;Warehouse Staff|Payment Provider;Shipping Provider;Supplier;Manager|570|20|240|600|40|1150|40|160|190|80
SD01|@seq|42|150
SD02|@seq|42|150
SD03|@seq|42|150
SD04|@seq|42|150
SD05|@seq|42|150
"""

if __name__ == "__main__":
    body = []
    for f in (ucd1, ucd2, ucd3, ucd4, uc00, ucai):
        body += f() + [""]
    with open(os.path.join(HERE, "redraw_spec.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEAD + "\n" + "\n".join(body))
    print("redraw_spec.txt:", sum(1 for l in body if l), "lines")
