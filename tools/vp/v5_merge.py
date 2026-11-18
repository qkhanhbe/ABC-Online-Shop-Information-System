"""One class diagram per phase, laid out wide (three rows) for a landscape page:

  CL01  analysis classes: attribute names only (no type, no identifier, no method)
  ORM01 (was DM01) persistent classes: + identifier, types, <<ORM Persistable>>, association names and multiplicities
  DCL01 design classes (package model): + the methods of the code
The classes of part 2 (CL02, DM02, DCL02) are added to part 1; the eight associations drawn only on part 2 are
removed from the model and drawn again on part 1, so no association exists twice. Part 2 diagrams are deleted
afterwards by essay.gen mode tidy (the MCP plugin has no tool to delete a diagram).

    python tools/vp/v5_merge.py
"""
import re

import vp
from v5_spec import ASSOCIATIONS, CLASSES, FIGURES

# names before the merge (part 1 was renamed afterwards by essay.gen mode v5org, see tools/vpgen/v5_tidy2.txt)
PHASES = {
    "analysis": ("CL01 Analysis Classes - Customers Catalogue and Orders",
                 "CL02 Analysis Classes - Order History Delivery Stock and Reviews", "Analysis"),
    "datamodel": ("DM01 Data Model Classes - Customers Catalogue and Orders",
                  "DM02 Data Model Classes - Order History Delivery Stock and Reviews", "Data Model"),
    "design": ("DCL01 Design Classes (model) - Customers Catalogue and Orders",
               "DCL02 Design Classes (model) - Order History Delivery Stock and Reviews", "model"),
}
CURRENT = {"analysis": "CL01 Analysis Class Diagram", "datamodel": "ORM01 Class Diagram with Multiplicity and Labels (ORM)",
           "design": "DCL01 Design Class Diagram (model)"}
NAV = {("Cart", "CartItem"): "items", ("Order", "OrderItem"): "items", ("Order", "StatusChange"): "history",
       ("Shipment", "Milestone"): "milestones", ("Customer", "Address"): "address"}

# three rows on a grid of columns; a class sits next to the classes it is linked to, the kinds of product under
# Product so their generalizations share one bus
CELLS = {
    "Address": (0, 0), "Customer": (0, 1), "Payment": (0, 2),
    "User": (1, 0), "StatusChange": (1, 2),
    "Cart": (2, 0), "Order": (2, 1), "Shipment": (2, 2),
    "CartItem": (3, 0), "OrderItem": (3, 1), "Milestone": (3, 2),
    "Review": (4, 0), "Promotion": (4, 2),
    "Category": (5, 0), "Product": (5, 1), "Footwear": (5, 2),
    "ReplenishmentRequest": (6, 0), "StockLevel": (6, 1), "Apparel": (6, 2),
    "InventoryEvent": (7, 1), "Bag": (7, 2),
    "Watch": (8, 2),
}

# the design classes carry their methods and Order is about 1200 px wide, so DCL01 uses five rows instead of three
# (landscape page about 1.6:1); the kinds of product stand in one column right of Product, on one generalization bus
DESIGN_CELLS = {
    "User": (0, 0), "Customer": (0, 1), "Address": (0, 2), "Payment": (0, 3),
    "Cart": (1, 0), "Order": (1, 1), "Shipment": (1, 2), "Milestone": (1, 3),
    "CartItem": (2, 0), "OrderItem": (2, 1), "StatusChange": (2, 2), "Promotion": (2, 3),
    "Review": (3, 0), "Product": (3, 1), "StockLevel": (3, 2), "InventoryEvent": (3, 3), "ReplenishmentRequest": (3, 4),
    "Category": (4, 0), "Footwear": (4, 1), "Apparel": (4, 2), "Bag": (4, 3), "Watch": (4, 4),
}


def sizes(d, rename=None):
    g = vp.call("getDiagramGeometry", quiet=True, diagramName=d)
    rename = rename or {}
    return {rename.get(m.group(1), m.group(1)): (int(m.group(4)), int(m.group(5)))
            for m in re.finditer(r"(?:Class|Table): (\w+) (-?\d+),(-?\d+) (\d+)x(\d+)", g)}


def arrange(d, gap_x=110, gap_y=210, rename=None, cells=None):
    """Place the classes (or the tables of the data model; rename maps a table name to its class) on the CELLS grid."""
    CELLS = cells or globals()["CELLS"]
    real = {v: k for k, v in (rename or {}).items()}
    size = sizes(d, rename)
    for n, (w, h) in size.items():                 # never narrower than the class name (VP cuts it with "...")
        size[n] = (max(w, 9 * len(n) + 34), h)
    for i, n in enumerate(size):
        vp.call("setElementBounds", quiet=True, diagramName=d, elementName=real.get(n, n), x=12000 + 800 * (i % 6),
                y=12000 + 800 * (i // 6), width=0, height=0)
    ncol, nrow = 1 + max(c for c, _ in CELLS.values()), 1 + max(r for _, r in CELLS.values())
    width = [max([size[n][0] for n, (c, _) in CELLS.items() if c == k] or [0]) for k in range(ncol)]
    height = [max([size[n][1] for n, (_, r) in CELLS.items() if r == k] or [0]) for k in range(nrow)]
    xs, ys = [40], [40]
    for w in width[:-1]:
        xs.append(xs[-1] + w + gap_x)
    for h in height[:-1]:
        ys.append(ys[-1] + h + gap_y)
    for n, (c, r) in CELLS.items():
        w, h = size[n]
        vp.call("setElementBounds", quiet=True, diagramName=d, elementName=real.get(n, n), x=xs[c] + (width[c] - w) // 2,
                y=ys[r] + (height[r] - h) // 2, width=w, height=0)
    vp.call("rerouteConnectors", quiet=True, diagramName=d)
    vp.call("layoutConnectorLabels", quiet=True, diagramName=d)


def merge(phase):
    d1, d2, package = PHASES[phase]
    typed = phase != "analysis"
    for name in FIGURES["after"]:
        if name not in FIGURES["core"]:
            vp.call("addClass", quiet=True, diagramName=d1, className=name, modelPackage=package)
    for a, b, ma, mb, label, kind, ra, rb in ASSOCIATIONS:
        if a in FIGURES["core"] and b in FIGURES["core"]:
            continue                                         # drawn on part 1 already
        kind_name = "Composition" if kind == "comp" else "Association"
        print(vp.call("removeRelationship", quiet=True, diagramName=d2, fromClass=a, toClass=b,
                      relationshipType=kind_name)[:90])
        if kind == "comp":
            vp.call("addComposition", quiet=True, diagramName=d1, fromClass=a, toClass=b, fromMultiplicity=ma,
                    toMultiplicity=mb)
        else:
            vp.call("addAssociation", quiet=True, diagramName=d1, fromClass=a, toClass=b, fromMultiplicity=ma,
                    toMultiplicity=mb, name=label)
        if phase == "design":
            role = NAV.get((a, b))
            vp.call("setAssociationProperties", quiet=True, diagramName=d1, fromClass=a, toClass=b, name=label,
                    fromRole="-", toRole=role or "-", fromNavigable="false", toNavigable="true" if role else "false")
        else:
            vp.call("setAssociationProperties", quiet=True, diagramName=d1, fromClass=a, toClass=b, name=label,
                    fromRole=ra if typed else "", toRole=rb if typed else "")
    if phase != "design":                                   # methods belong to the design (phase 5) only
        for name, (_, _, ops) in CLASSES.items():
            for op, _, _ in ops:
                vp.call("removeOperation", quiet=True, diagramName=d1, className=name, operationName=op)
    if typed and phase == "datamodel":
        vp.call("addStereotypeToClasses", quiet=True, diagramName=d1, classNames="*", stereotype="ORM Persistable",
                robustnessIcon="false")
    arrange(d1, cells=DESIGN_CELLS if phase == "design" else None)
    print(vp.call("getElementCounts", quiet=True, diagramName=d1).replace("\n", " "))
    vp.call("exportDiagramImage", quiet=True, diagramName=d1, filePath=vp.PNG + d1 + ".png")


if __name__ == "__main__":
    import sys
    args = sys.argv[1:] or ["analysis", "datamodel", "design"]
    if args[0] == "arrange":                                 # only lay out the merged diagram(s) again
        for phase in args[1:]:
            arrange(CURRENT[phase], cells=DESIGN_CELLS if phase == "design" else None)
            vp.call("exportDiagramImage", quiet=True, diagramName=CURRENT[phase], filePath=vp.PNG + CURRENT[phase] + ".png")
    else:
        for phase in args:
            merge(phase)
    vp.call("saveProject", quiet=True)
