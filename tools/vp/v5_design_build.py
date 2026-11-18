"""Draws the V5 design in the open Visual Paradigm project (MCP plugin) and generates the code from it.

    python tools/vp/v5_design_build.py classes    DCL01..DCL06: one design class diagram per package
    python tools/vp/v5_design_build.py layers     LAY01, LAY02: the packages of two slices with <<use>>
    python tools/vp/v5_design_build.py code       generateCode per package -> design/generated/<package>

The classes come from the code (v5_design_spec.py); the model package keeps the associations of the
analysis/data model (v5_spec.py). An association end is navigable only where the code holds the reference
(Cart.items, Order.items, Order.history, Shipment.milestones, Customer.address); elsewhere the code refers
to the other aggregate by its key, which the class shows as an attribute (customer_id, product_id ...).
"""
import ast
import os
import re
import sys

import vp
from v5_design_spec import APP, PACKAGES, classes
from v5_spec import ASSOCIATIONS, FIGURES

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIAGRAMS = {
    "model": ["DCL01 Design Class Diagram (model)"],
    "dao": ["DCL02 Design Class Diagram (dao)"],
    "service": ["DCL03 Design Class Diagram (service)"],
    "ai": ["DCL04 Design Class Diagram (ai)"],
    "controller": ["DCL05 Design Class Diagram (controller)"],
}
NAV = {("Cart", "CartItem"): "items", ("Order", "OrderItem"): "items", ("Order", "StatusChange"): "history",
       ("Shipment", "Milestone"): "milestones", ("Customer", "Address"): "address"}
ROLE_FIELDS = {(a, r) for (a, _), r in NAV.items()}


def add_members(name, spec, d):
    for attr, typ in spec["attrs"]:
        if (name, attr) in ROLE_FIELDS:
            continue
        vp.call("addAttribute", quiet=True, className=name, attributeName=attr, attributeType=typ,
                visibility="public", diagramName=d)
    for op, params, ret, _static, abstract in spec["ops"]:
        vp.call("addOperation", quiet=True, className=name, operationName=op, returnType=ret, params=params,
                visibility="public", isAbstract=bool(abstract and spec.get("interface")), diagramName=d)


def uses_in_package(package, specs):
    """<<use>> between classes of one package: the collaborators a class receives in __init__."""
    names = set(specs)
    snake = {re.sub(r"(?<!^)(?=[A-Z])", "_", n).lower(): n for n in names}
    out = set()
    for rel in PACKAGES[package]:
        tree = ast.parse(open(os.path.join(APP, rel), encoding="utf-8").read())
        for c in [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name in names]:
            for f in [f for f in c.body if isinstance(f, ast.FunctionDef) and f.name == "__init__"]:
                for a in f.args.args[1:]:
                    target = snake.get(a.arg) or snake.get(a.arg.replace("_service", "") + "_service")
                    if a.arg in ("payment_gateway", "gateway", "provider"):
                        target = "PaymentGateway"
                    if a.arg in ("shipping_gateway", "carrier"):
                        target = "ShippingGateway"
                    if target and target != c.name and target in names:
                        out.add((c.name, target))
    return sorted(out)


def draw_classes():
    for package, diagrams in DIAGRAMS.items():
        specs = classes(package)
        figs = ([FIGURES["core"], FIGURES["after"]] if package == "model" else [list(specs)])
        made = set()
        for d, names in zip(diagrams, figs):
            vp.call("createClassDiagram", quiet=True, diagramName=d)
            for name in names:
                spec = specs[name]
                stereo = "Interface" if spec.get("interface") or name in ("PaymentGateway", "ShippingGateway") else ""
                vp.call("addClass", quiet=True, diagramName=d, className=name, stereotype=stereo, modelPackage=package)
                if name not in made:
                    made.add(name)
                    add_members(name, spec, d)
            for name in names:
                for base in specs[name]["bases"]:
                    if base in names:
                        if specs[base].get("interface") or base in ("PaymentGateway", "ShippingGateway"):
                            vp.call("addRealization", quiet=True, diagramName=d, fromClass=name, toClass=base)
                        else:
                            vp.call("addGeneralization", quiet=True, diagramName=d, fromClass=name, toClass=base)
            if package == "model":
                for a, b, ma, mb, label, kind, _ra, _rb in ASSOCIATIONS:
                    if a in names and b in names and not (d == diagrams[1] and a in FIGURES["core"] and b in FIGURES["core"]):
                        if kind == "comp":
                            vp.call("addComposition", quiet=True, diagramName=d, fromClass=a, toClass=b,
                                    fromMultiplicity=ma, toMultiplicity=mb)
                        else:
                            vp.call("addAssociation", quiet=True, diagramName=d, fromClass=a, toClass=b,
                                    fromMultiplicity=ma, toMultiplicity=mb, name=label)
                        role = NAV.get((a, b))
                        vp.call("setAssociationProperties", quiet=True, diagramName=d, fromClass=a, toClass=b,
                                name=label, fromRole="-", toRole=role or "-", fromNavigable="false",
                                toNavigable="true" if role else "false")
            else:
                for a, b in uses_in_package(package, specs):
                    if a in names and b in names:
                        vp.call("addUsage", quiet=True, diagramName=d, fromName=a, toName=b)
                if package == "dao":
                    for name in names:
                        if name.startswith("Sqlite"):
                            vp.call("addUsage", quiet=True, diagramName=d, fromName=name, toName="Database")
            vp.call("autoLayoutDiagram", quiet=True, diagramName=d)
            vp.call("layoutConnectorLabels", quiet=True, diagramName=d)
            print(vp.call("getElementCounts", quiet=True, diagramName=d).replace("\n", " "))
            vp.call("exportDiagramImage", quiet=True, diagramName=d, filePath=vp.PNG + d + ".png")


LAYERS = {
    "LAY01 Layers - Search Products (UC05)": [
        ("controller", ["ShopController"]),
        ("ai", ["SearchService", "QueryService", "RankingService", "ImageService", "SpeechService"]),
        ("dao", ["ProductDAO", "InventoryDAO", "VectorIndex", "ImageStorage"]),
        ("model", ["Product", "StockLevel"])],
    "LAY02 Layers - Cart and Checkout (UC07 and UC08)": [
        ("controller", ["OrderController"]),
        ("service", ["CartService", "CheckoutService", "InventoryService", "PaymentService"]),
        ("dao", ["CartDAO", "OrderDAO", "ProductDAO", "InventoryDAO", "PaymentDAO", "Database"]),
        ("model", ["Cart", "Order", "Product", "StockLevel", "Payment"])],
}
LAYER_USES = {
    "LAY01 Layers - Search Products (UC05)": [
        ("ShopController", "SearchService"), ("ShopController", "QueryService"), ("ShopController", "ImageService"),
        ("ShopController", "SpeechService"), ("SearchService", "RankingService"), ("SearchService", "ProductDAO"),
        ("SearchService", "InventoryDAO"), ("SearchService", "VectorIndex"), ("ImageService", "ImageStorage")],
    "LAY02 Layers - Cart and Checkout (UC07 and UC08)": [
        ("OrderController", "CartService"), ("OrderController", "CheckoutService"),
        ("CheckoutService", "CartService"), ("CheckoutService", "InventoryService"),
        ("CheckoutService", "PaymentService"), ("CheckoutService", "OrderDAO"), ("CheckoutService", "Database"),
        ("CartService", "CartDAO"), ("CartService", "ProductDAO"), ("CartService", "InventoryDAO"),
        ("InventoryService", "InventoryDAO"), ("PaymentService", "PaymentDAO"), ("PaymentService", "OrderDAO")],
}


def draw_layers():
    for d, layers in LAYERS.items():
        vp.call("createClassDiagram", quiet=True, diagramName=d)
        for package, names in layers:
            vp.call("addPackageShape", quiet=True, diagramName=d, packageName=package)
            for n in names:
                vp.call("addClass", quiet=True, diagramName=d, className=n, modelPackage=package)
                vp.call("moveIntoPackage", quiet=True, diagramName=d, elementName=n, packageName=package)
        for a, b in LAYER_USES[d]:
            vp.call("addUsage", quiet=True, diagramName=d, fromName=a, toName=b)
        vp.call("autoLayoutDiagram", quiet=True, diagramName=d)
        print(vp.call("getElementCounts", quiet=True, diagramName=d).replace("\n", " "))
        vp.call("exportDiagramImage", quiet=True, diagramName=d, filePath=vp.PNG + d + ".png")


def generate_code():
    """One generateCode call per package; the calls and results replace section 4 of design/vp_tool_log.txt."""
    import glob
    import py_compile
    log, total = ["==== 4. Design class diagrams to code " + "=" * 88], 0
    for package, diagrams in DIAGRAMS.items():
        out = os.path.join(ROOT, "design", "generated", package)
        for old in glob.glob(os.path.join(out, "*.py")):
            os.remove(old)
        os.makedirs(out, exist_ok=True)
        r = vp.call("generateCode", quiet=True, diagramName=", ".join(diagrams), language="python",
                    packageName=package, outputDir=out, jpa=False, accessors=False, primaryKeys="").strip()
        print(package, r[:300])
        rel = "design/generated/" + package
        names = ", ".join(diagrams)
        log.append(f'$ generateCode("{names}", "python", "{package}", "{rel}", false, false, "")\n'
                   + r.replace(out, rel.replace("/", os.sep)))
        files = glob.glob(os.path.join(out, "*.py"))
        total += len([f for f in files if not f.endswith("__init__.py")])
        for f in files:
            py_compile.compile(f, doraise=True)
    log.append(f"Result: {total} classes in {len(DIAGRAMS)} packages; every file compiles (python -m py_compile).")
    path = os.path.join(ROOT, "design", "vp_tool_log.txt")
    text = open(path, encoding="utf-8").read()
    if "==== 4." in text:
        text = text[:text.index("==== 4. Design class diagrams to code")]
    open(path, "w", encoding="utf-8").write(text + "\n".join(log) + "\n")


if __name__ == "__main__":
    {"classes": draw_classes, "layers": draw_layers, "code": generate_code}[sys.argv[1]]()
    vp.call("saveProject", quiet=True)
