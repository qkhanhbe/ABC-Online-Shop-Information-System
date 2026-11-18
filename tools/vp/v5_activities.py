"""Activity diagrams of the use cases that had none (analysis, Chapter 2), drawn from the code paths:
AD05 Search Products (ShopController.search), AD06 Manage Cart (CartService), AD07 Track Order
(OrderService.track), AD08 Manage Products (CatalogService.save_product).

    python tools/vp/v5_activities.py
"""
import vp

# diagram: (lanes, nodes, flows); node = (kind, name, lane); kind action | initial | final | decision | merge
DIAGRAMS = {
    "AD05 Search Products (Swimlane)": (
        ["Customer", "System"],
        [("initial", "Start", "Customer"),
         ("action", "Type words, speak or upload a photo", "Customer"),
         ("decision", "Kind of input?", "System"),
         ("action", "Transcribe the recording (Whisper)", "System"),
         ("action", "Encode the photo as a vector", "System"),
         ("merge", "Input ready", "System"),
         ("decision", "About an order?", "System"),
         ("action", "Find the customer's own orders", "System"),
         ("action", "Read terms, synonyms and price limit", "System"),
         ("action", "Retrieve candidates by keyword and vector", "System"),
         ("action", "Rank by text, image and stock", "System"),
         ("decision", "Any result?", "System"),
         ("action", "Suggest fewer words or another photo", "System"),
         ("action", "Show ranked products with scores", "System"),
         ("action", "Open a product", "Customer"),
         ("final", "End", "Customer"),
         ("final", "End #2", "System"),
         ("final", "End #3", "System")],
        [("Start", "Type words, speak or upload a photo", ""),
         ("Type words, speak or upload a photo", "Kind of input?", ""),
         ("Kind of input?", "Transcribe the recording (Whisper)", "voice"),
         ("Kind of input?", "Encode the photo as a vector", "photo"),
         ("Kind of input?", "Input ready", "text"),
         ("Transcribe the recording (Whisper)", "Input ready", ""),
         ("Encode the photo as a vector", "Input ready", ""),
         ("Input ready", "About an order?", ""),
         ("About an order?", "Find the customer's own orders", "yes"),
         ("Find the customer's own orders", "End #2", ""),
         ("About an order?", "Read terms, synonyms and price limit", "no"),
         ("Read terms, synonyms and price limit", "Retrieve candidates by keyword and vector", ""),
         ("Retrieve candidates by keyword and vector", "Rank by text, image and stock", ""),
         ("Rank by text, image and stock", "Any result?", ""),
         ("Any result?", "Suggest fewer words or another photo", "no"),
         ("Suggest fewer words or another photo", "End #3", ""),
         ("Any result?", "Show ranked products with scores", "yes"),
         ("Show ranked products with scores", "Open a product", ""),
         ("Open a product", "End", "")]),
    "AD06 Manage Cart (Swimlane)": (
        ["Customer", "System"],
        [("initial", "Start", "Customer"),
         ("action", "Choose a product and a quantity", "Customer"),
         ("decision", "Product for sale?", "System"),
         ("action", "Report the product is not available", "System"),
         ("action", "Add the quantity already in the cart", "System"),
         ("decision", "Enough available stock? (UC30)", "System"),
         ("action", "Show the available quantity", "System"),
         ("action", "Add a line with the current price", "System"),
         ("action", "Save the cart", "System"),
         ("action", "Review the cart", "Customer"),
         ("decision", "Next step?", "Customer"),
         ("action", "Change a quantity (0 removes the line)", "Customer"),
         ("action", "Proceed to checkout", "Customer"),
         ("final", "End", "Customer"),
         ("final", "End #2", "System"),
         ("final", "End #3", "System")],
        [("Start", "Choose a product and a quantity", ""),
         ("Choose a product and a quantity", "Product for sale?", ""),
         ("Product for sale?", "Report the product is not available", "no"),
         ("Report the product is not available", "End #2", ""),
         ("Product for sale?", "Add the quantity already in the cart", "yes"),
         ("Add the quantity already in the cart", "Enough available stock? (UC30)", ""),
         ("Enough available stock? (UC30)", "Show the available quantity", "no"),
         ("Show the available quantity", "End #3", ""),
         ("Enough available stock? (UC30)", "Add a line with the current price", "yes"),
         ("Add a line with the current price", "Save the cart", ""),
         ("Save the cart", "Review the cart", ""),
         ("Review the cart", "Next step?", ""),
         ("Next step?", "Change a quantity (0 removes the line)", "change"),
         ("Change a quantity (0 removes the line)", "Enough available stock? (UC30)", ""),
         ("Next step?", "Proceed to checkout", "checkout"),
         ("Proceed to checkout", "End", "")]),
    "AD07 Track Order (Swimlane)": (
        ["Customer", "System"],
        [("initial", "Start", "Customer"),
         ("action", "Open My orders and choose an order", "Customer"),
         ("decision", "Logged in as a customer?", "System"),
         ("action", "Send to the login page", "System"),
         ("action", "Load the order by its id", "System"),
         ("decision", "Order exists and is the customer's?", "System"),
         ("action", "Answer order not found", "System"),
         ("action", "Load the shipment of the order", "System"),
         ("decision", "Shipment exists?", "System"),
         ("action", "Add the carrier milestones", "System"),
         ("merge", "Timeline ready", "System"),
         ("action", "Sort the timeline by time", "System"),
         ("action", "Show status, carrier reference and timeline", "System"),
         ("action", "Read the progress of the order", "Customer"),
         ("final", "End", "Customer"),
         ("final", "End #2", "System"),
         ("final", "End #3", "System")],
        [("Start", "Open My orders and choose an order", ""),
         ("Open My orders and choose an order", "Logged in as a customer?", ""),
         ("Logged in as a customer?", "Send to the login page", "no"),
         ("Send to the login page", "End #2", ""),
         ("Logged in as a customer?", "Load the order by its id", "yes"),
         ("Load the order by its id", "Order exists and is the customer's?", ""),
         ("Order exists and is the customer's?", "Answer order not found", "no"),
         ("Answer order not found", "End #3", ""),
         ("Order exists and is the customer's?", "Load the shipment of the order", "yes"),
         ("Load the shipment of the order", "Shipment exists?", ""),
         ("Shipment exists?", "Add the carrier milestones", "yes"),
         ("Shipment exists?", "Timeline ready", "no"),
         ("Add the carrier milestones", "Timeline ready", ""),
         ("Timeline ready", "Sort the timeline by time", ""),
         ("Sort the timeline by time", "Show status, carrier reference and timeline", ""),
         ("Show status, carrier reference and timeline", "Read the progress of the order", ""),
         ("Read the progress of the order", "End", "")]),
    "AD08 Manage Products (Swimlane)": (
        ["Administrator", "System"],
        [("initial", "Start", "Administrator"),
         ("action", "Choose a category and enter the product", "Administrator"),
         ("decision", "Allowed to manage the catalogue?", "System"),
         ("action", "Refuse the request", "System"),
         ("decision", "Name given and price positive?", "System"),
         ("decision", "Kind of the category? (BR-CAT-01)", "System"),
         ("action", "Show what to correct", "System"),
         ("action", "Save Product and its kind row in one transaction", "System"),
         ("decision", "New product?", "System"),
         ("action", "Create an empty stock level", "System"),
         ("merge", "Saved", "System"),
         ("action", "Record the change in the audit log", "System"),
         ("action", "See the product in the catalogue", "Administrator"),
         ("final", "End", "Administrator"),
         ("final", "End #2", "System")],
        [("Start", "Choose a category and enter the product", ""),
         ("Choose a category and enter the product", "Allowed to manage the catalogue?", ""),
         ("Allowed to manage the catalogue?", "Refuse the request", "no"),
         ("Refuse the request", "End #2", ""),
         ("Allowed to manage the catalogue?", "Name given and price positive?", "yes"),
         ("Name given and price positive?", "Show what to correct", "no"),
         ("Name given and price positive?", "Kind of the category? (BR-CAT-01)", "yes"),
         ("Kind of the category? (BR-CAT-01)", "Show what to correct", "different"),
         ("Show what to correct", "Choose a category and enter the product", ""),
         ("Kind of the category? (BR-CAT-01)", "Save Product and its kind row in one transaction", "same"),
         ("Save Product and its kind row in one transaction", "New product?", ""),
         ("New product?", "Create an empty stock level", "yes"),
         ("New product?", "Saved", "no"),
         ("Create an empty stock level", "Saved", ""),
         ("Saved", "Record the change in the audit log", ""),
         ("Record the change in the audit log", "See the product in the catalogue", ""),
         ("See the product in the catalogue", "End", "")]),
}


def draw(d, lanes, nodes, flows):
    vp.call("createActivityDiagram", quiet=True, diagramName=d)
    for lane in lanes:
        vp.call("addActivityPartition", quiet=True, diagramName=d, partitionName=lane)
    for kind, name, lane in nodes:
        if kind == "action":
            vp.call("addActivityAction", quiet=True, diagramName=d, actionName=name, partitionName=lane)
        else:
            vp.call("addActivityControlNode", quiet=True, diagramName=d, kind=kind, nodeName=name, partitionName=lane)
    for a, b, guard in flows:
        vp.call("addActivityFlow", quiet=True, diagramName=d, fromNode=a, toNode=b, guard=guard, twoWay=False)
    print(vp.call("getElementCounts", quiet=True, diagramName=d).replace("\n", " "))
    vp.call("exportDiagramImage", quiet=True, diagramName=d, filePath=vp.PNG + d + ".png")


if __name__ == "__main__":
    for d, spec in DIAGRAMS.items():
        draw(d, *spec)
    vp.call("saveProject", quiet=True)
