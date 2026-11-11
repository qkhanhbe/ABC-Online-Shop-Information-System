"""Business and requirements overview diagrams (Chapter 1 and 2.2).

BP01  high-level business process: BPMN collaboration of the customer, the shop and its partners
STK01 stakeholder map: internal and external stakeholders and the interest that ties them to the shop
PT01  problem tree: root causes, the core problem and its effects (Assignment 01 problems BP01-BP07)
UC00  general use case diagram: every actor with the main use case of each subsystem
usage: python business.py bp|stk|pt|uc
"""
import sys

from vp import call, colour, export


def bp():
    d = "BP01 High-Level Business Process"
    call("createBpmnDiagram", diagramName=d)
    call("addBpmnPool", diagramName=d, poolName="Customer", height=120)
    call("addBpmnPool", diagramName=d, poolName="ABC Online Shop")
    for lane in ("Online shop system", "Sales Staff", "Warehouse Staff", "Manager"):
        call("addBpmnLane", diagramName=d, poolName="ABC Online Shop", laneName=lane)
    call("addBpmnPool", diagramName=d, poolName="Payment Provider", height=60)
    call("addBpmnPool", diagramName=d, poolName="Shipping Provider", height=60)
    call("addBpmnPool", diagramName=d, poolName="Supplier", height=60)

    ev = lambda n, lane, pos, trig="": call("addBpmnEvent", diagramName=d, eventName=n, laneName=lane, position=pos, trigger=trig)
    task = lambda n, lane, kind="task": call("addBpmnTask", diagramName=d, taskName=n, laneName=lane, kind=kind)
    flow = lambda a, b, c="": call("addBpmnSequenceFlow", diagramName=d, fromElement=a, toElement=b, condition=c)
    msg = lambda a, b, label: call("addBpmnMessageFlow", diagramName=d, fromElement=a, toElement=b, label=label)

    ev("Wants a product", "Customer", "start")
    task("Browse and search", "Customer", "user")
    task("Fill cart and check out", "Customer", "user")
    task("Receive parcel", "Customer", "manual")
    ev("Order received", "Customer", "end")
    flow("Wants a product", "Browse and search")
    flow("Browse and search", "Fill cart and check out")
    flow("Fill cart and check out", "Receive parcel")
    flow("Receive parcel", "Order received")

    shop = "Online shop system"
    ev("Order submitted", shop, "start", "message")
    task("Validate cart, reserve stock", shop, "service")
    task("Request payment", shop, "send")
    call("addBpmnGateway", diagramName=d, gatewayName="Payment verified?", laneName=shop, kind="exclusive")
    task("Release stock", shop, "service")
    ev("Order failed", shop, "end")
    task("Process order", "Sales Staff", "user")
    task("Pick and pack", "Warehouse Staff", "user")
    task("Hand over parcel", "Warehouse Staff", "manual")
    task("Record milestones", shop, "receive")
    task("Review sales and stock", "Manager", "user")
    ev("Period closed", "Manager", "end")
    flow("Order submitted", "Validate cart, reserve stock")
    flow("Validate cart, reserve stock", "Request payment")
    flow("Request payment", "Payment verified?")
    flow("Payment verified?", "Process order", "[verified]")
    flow("Payment verified?", "Release stock", "[failed]")
    flow("Release stock", "Order failed")
    flow("Process order", "Pick and pack")
    flow("Pick and pack", "Hand over parcel")
    flow("Hand over parcel", "Record milestones")
    flow("Record milestones", "Review sales and stock")
    flow("Review sales and stock", "Period closed")

    msg("Fill cart and check out", "Order submitted", "order")
    msg("Request payment", "Payment Provider", "payment request")
    msg("Payment Provider", "Payment verified?", "signed result")
    msg("Hand over parcel", "Shipping Provider", "parcel")
    msg("Shipping Provider", "Record milestones", "milestones")
    msg("Shipping Provider", "Receive parcel", "delivery")
    msg("Pick and pack", "Supplier", "replenishment request")
    export(d)


INTERNAL = {"Administrator": "accurate catalogue and promotions", "Sales Staff": "complete, current order data",
            "Warehouse Staff": "true stock and clear pick lists", "Manager": "timely, reproducible reports"}
EXTERNAL = {"Customer": "correct price, stock and order status", "Supplier": "clear replenishment requests",
            "Payment Provider": "unambiguous payment exchange", "Shipping Provider": "correct parcels and status exchange"}


def stk():
    d = "STK01 Stakeholder Map"
    call("createClassDiagram", diagramName=d)
    call("addClass", diagramName=d, className="ABC Online Shop", stereotype="business", modelPackage="Stakeholders")
    for group, members, colour_ in (("Internal stakeholders", INTERNAL, "#C5E0B4"), ("External stakeholders", EXTERNAL, "#FBE5D6")):
        for name, interest in members.items():
            cls = name                          # owned by the frame package, so no clash with the model classes
            call("addClass", diagramName=d, className=cls, packageName=group, packageColor=colour_,
                 stereotype="stakeholder", modelPackage="")
            call("addAttribute", className=cls, attributeName="interest", attributeType=interest,
                 visibility="public", diagramName=d)
            call("addAssociation", diagramName=d, fromClass=cls, toClass="ABC Online Shop",
                 fromMultiplicity="", toMultiplicity="", name="")
    colour(d, ["ABC Online Shop"], "#7ACFF5")
    export(d)


EFFECTS = ["Customers lose trust", "Lost and cancelled sales", "Management decides late"]
CORE = "Order, stock and payment information is fragmented and late"
CAUSES = {"Inconsistent product data (BP01)": "Catalogue and stock kept by different people",
          "Overselling and stock errors (BP02)": "Stock edited as one number, no event history",
          "Unverified payment status (BP03)": "Payment results typed in by hand",
          "Unclear order status (BP04)": "No defined order states",
          "Untracked deliveries (BP05)": "Carrier updates by phone and e-mail",
          "Reports built by hand (BP06)": "No single source for sales data"}


def pt():
    d = "PT01 Problem Tree"
    call("createFlowchart", diagramName=d)
    for e in EFFECTS:
        call("addFlowchartShape", quiet=True, diagramName=d, shapeName=e, kind="document")
    call("addFlowchartShape", diagramName=d, shapeName=CORE, kind="process")
    for problem, root in CAUSES.items():
        call("addFlowchartShape", quiet=True, diagramName=d, shapeName=problem, kind="process")
        call("addFlowchartShape", quiet=True, diagramName=d, shapeName=root, kind="predefinedProcess")
    for e in EFFECTS:
        call("addFlowchartFlow", quiet=True, diagramName=d, fromShape=CORE, toShape=e, label="")
    for problem, root in CAUSES.items():
        call("addFlowchartFlow", quiet=True, diagramName=d, fromShape=problem, toShape=CORE, label="")
        call("addFlowchartFlow", quiet=True, diagramName=d, fromShape=root, toShape=problem, label="")
    export(d)


ACTORS = ["Visitor", "Customer", "Administrator", "Sales Staff", "Warehouse Staff", "Manager",
          "Payment Provider", "Shipping Provider", "Supplier"]
LINKS = [("Visitor", "UC04 Browse Products"), ("Visitor", "UC05 Search Products"), ("Visitor", "UC01 Register Account"),
         ("Customer", "UC07 Manage Shopping Cart"), ("Customer", "UC08 Place Order / Checkout"),
         ("Customer", "UC11 Track Order"), ("Customer", "UC13 Submit Review"),
         ("Administrator", "UC14 Manage Products"), ("Administrator", "UC16 Manage Promotions"),
         ("Sales Staff", "UC19 Process Orders"), ("Warehouse Staff", "UC20 Manage Inventory"),
         ("Warehouse Staff", "UC21 Prepare Shipment"), ("Manager", "UC25 View Management Dashboard"),
         ("Payment Provider", "UC09 Make Payment"), ("Shipping Provider", "UC23 Update Shipment Status"),
         ("Supplier", "UC24 Manage Replenishment")]


def uc():
    d = "UC00 General Use Case Diagram"
    call("createUseCaseDiagram", diagramName=d)
    for a in ACTORS:
        call("addActor", quiet=True, actorName=a, diagramName=d)
    for _, u in LINKS:
        call("addUseCase", quiet=True, useCaseName=u, diagramName=d)
    call("addRelationship", diagramName=d, sourceName="Customer", targetName="Visitor", relationshipType="Generalization")
    call("addRelationship", diagramName=d, sourceName="UC08 Place Order / Checkout", targetName="UC09 Make Payment",
         relationshipType="Include")
    for a, u in LINKS:
        call("addRelationship", quiet=True, diagramName=d, sourceName=a, targetName=u, relationshipType="Association")
    call("addSystemBoundary", diagramName=d, systemName="ABC Online Shop")
    export(d)


if __name__ == "__main__":
    {"bp": bp, "stk": stk, "pt": pt, "uc": uc}[sys.argv[1]]()
