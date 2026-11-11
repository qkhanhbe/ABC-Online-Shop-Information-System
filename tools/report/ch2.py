import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = os.path.join(ROOT, "diagrams")

BLOCKS = [
    ("h1", "CHAPTER 2. ANALYSIS"),
    ("p", "Analysis describes the problem domain without deciding how the software will be built. It answers three "
          "questions about the requirements of Chapter 1: what happens and in which order (behaviour), which data moves "
          "where (information), and which concepts exist and how they are related (structure). The chapter uses one "
          "model family for each question and closes with a check that the models agree with each other."),
    ("h2", "2.1. From Requirements to Analysis Models"),
    ("table", "Analysis questions, models and the requirements they refine", ["Question", "Model (VP diagram)", "Refines"], [
        ["Who does what, in which order?", "Activity and swimlane diagrams (AD01-AD03)", "UC08, UC19-23, UC20"],
        ["Which data flows between processes and stores?", "DFD level 0 and level 1 (DFD0, DFD1)", "Context diagram CTX01"],
        ["Which objects collaborate in a scenario?", "Sequence diagrams with BCE lifelines (SD01, SD02)", "UC08, UC11"],
        ["Which concepts and relationships exist?", "Analysis class diagram (CL01)", "Information catalogue"],
        ["Which states can an order be in?", "State machine (ST01)", "FR12, FR13, FR18"],
        ["How is the data stored?", "Physical ER diagrams (ERD01, ERD02)", "Integrity requirements NFR06-07"]], [55, 65, 45]),
    ("h2", "2.2. Activity Modeling"),
    ("p", "An activity diagram shows the control flow of one use case; a swimlane adds who performs each action. The "
          "swimlane version is the more useful one for this shop, because most of its problems are hand-offs between "
          "parties. The checkout diagram has three lanes: Customer, System and Payment Provider. It makes two facts "
          "visible that the text of UC08 only implies. First, the system reserves stock <i>before</i> it asks for "
          "payment, so that a paid order can always be fulfilled. Second, the payment result is a decision of the "
          "system, not of the provider: the provider returns a signed result and the system decides whether it is a "
          "verified success."),
    ("fig", os.path.join(D, "AD01 Place Order (Swimlane).png"), "Place order activity with swimlanes - VP diagram \"AD01 Place Order (Swimlane)\"", 150),
    ("p", "The diagram has two decision nodes; the question of each decision is written into the guards of its outgoing "
          "flows ([valid]/[invalid], [verified]/[failed]), so every flow carries exactly one condition. The failure branches end in "
          "their own final nodes rather than looping back, because the use case specification says that after a "
          "validation failure the customer returns to the cart, which is a different use case (UC07). On the [failed] branch "
          "after payment, the system releases the reservation and records Payment Failed before the customer sees the "
          "failure, which is the order of the statements in PaymentService.handle_result (Chapter 5)."),
    ("p", "Fulfilment crosses four parties, which is exactly where Assignment 01 located the delays of BP03 and BP04. "
          "The second swimlane diagram follows a paid order from the processing queue of the sales staff to the "
          "milestones of the carrier. The eligibility decision checks two facts that come from earlier use cases: a "
          "verified payment (UC09) and complete reservations (UC08 step 6). An order that fails either check is put "
          "On Hold with a recorded reason instead of being silently skipped."),
    ("fig", os.path.join(D, "AD02 Process and Ship Order (Swimlane).png"), "Order processing and shipment - VP diagram \"AD02 Process and Ship Order (Swimlane)\"", 160),
    ("p", "Inventory management is a single-actor use case and is drawn without lanes. Its interest lies in the order of "
          "the checks: the duplicate-reference check comes first, so that a repeated goods-receipt note can never add "
          "stock twice (NFR07); the balance check comes second, so that no event can produce a negative quantity; and "
          "the threshold check comes last, after the event is recorded, and only offers replenishment (UC24) instead of "
          "starting it, because a person decides how much to order."),
    ("fig", os.path.join(D, "AD03 Manage Inventory.png"), "Manage inventory - VP diagram \"AD03 Manage Inventory\"", 105),
    ("h2", "2.3. Data Flow Modeling"),
    ("p", "The context diagram of Chapter 1 treats the system as one process. The level 0 DFD opens it into eight "
          "processes and six data stores. The decomposition follows the business process of Section 1.5, so each "
          "process has one clear owner of its data. Two rules of DFD notation were checked on every flow: a data store "
          "is never connected directly to another store or to an external entity, and every process has at least one "
          "input and one output. A flow is named after the data it carries, never after an action (<i>payment "
          "request</i>, not <i>send payment</i>)."),
    ("fig", os.path.join(D, "DFD0 Level 0 Diagram.png"), "Level 0 data flow diagram - VP diagram \"DFD0 Level 0 Diagram\"", 165),
    ("p", "The level 0 diagram also shows where the shop's information becomes inconsistent today. The Products store D1 "
          "is read by process 2.0 (search) and by checkout, and written only by 1.0; the Inventory store D4 is written "
          "by 4.0 (reservations) and 6.0 (receipts) and read by everyone. With one writer per kind of change, two copies "
          "of the same fact cannot exist, which is the analysis form of objective O1."),
    ("p", "Process 4.0 Place Order and Pay is the most complex one and is decomposed at level 1 into five processes. The "
          "decomposition is balanced: the level 1 diagram has the same external flows as process 4.0 on level 0 "
          "(checkout request and confirmation with the customer, payment request and result with the provider, order, "
          "reservation and payment written to D3, D4 and D5). Two stores appear only at level 1, Carts and Promotions, "
          "because they are internal to the checkout."),
    ("fig", os.path.join(D, "DFD1 Level 1 - 4.0 Place Order and Pay.png"), "Level 1 DFD of process 4.0 - VP diagram \"DFD1 Level 1 - 4.0 Place Order and Pay\"", 160),
    ("h2", "2.4. Interaction Modeling"),
    ("p", "A sequence diagram assigns the steps of a scenario to objects. In analysis the objects are typed with the "
          "boundary, control and entity stereotypes: a <b>boundary</b> object talks to an actor or to an external system "
          "(CheckoutForm, PaymentGateway), a <b>control</b> object coordinates one use case (CheckoutController), and an "
          "<b>entity</b> object holds information that outlives the scenario (Cart, StockLevel, Order). The rule that an "
          "actor only talks to boundaries, and entities only answer, keeps the scenario readable and already suggests "
          "the layers of the design."),
    ("fig", os.path.join(D, "SD01 Place Order (Analysis).png"), "Sequence diagram of the main checkout scenario - VP diagram \"SD01 Place Order (Analysis)\"", 165),
    ("p", "The sixteen messages follow the main flow of UC08 in order. Messages 3-6 are the included use cases UC29-UC31; "
          "message 8 reserves stock before payment (step 6); messages 9-12 are UC09, where the PaymentGateway boundary "
          "is the only object that knows the provider. Message 13 changes the order status only after message 12 has "
          "reported a verified success. An alternative flow such as A5 (payment declined) is a different scenario and is "
          "therefore not drawn into this diagram; it is covered by the activity diagram and by a test."),
    ("fig", os.path.join(D, "SD02 Track Order (Analysis).png"), "Sequence diagram of order tracking - VP diagram \"SD02 Track Order (Analysis)\"", 120),
    ("p", "Tracking looks simple but contains the privacy rule of NFR05: message 5, checkOwner(customerId), happens "
          "before any shipment data is read. If the order belongs to someone else, the controller answers exactly as if "
          "the order did not exist, so that a customer cannot learn which order numbers are in use (UC11 E2)."),
    ("h2", "2.5. Analysis Class Model"),
    ("p", "The classes were found by the noun-phrase method applied to the use case specifications and the information "
          "catalogue, then filtered: nouns that name an actor (Manager), a screen (checkout page) or a single attribute "
          "(price) were removed. Eighteen classes remained, and the product detail hierarchy added five more (Section 2.5). They carry attributes but no operations yet; operations are "
          "added in the first design step (Section 4.3)."),
    ("fig", os.path.join(D, "CL01 Analysis Class Diagram.png"), "Analysis class diagram - VP diagram \"CL01 Analysis Class Diagram\"", 165),
    ("table", "Relationships of the analysis model and their justification", ["Relationship", "Kind", "Justification"], [
        ["Customer - User", "Generalisation", "A customer is a user with an address and order history; staff are users with other roles"],
        ["Customer - Address", "Aggregation 1 - 0..1", "The address exists for delivery and can be replaced; old orders keep a copy of it"],
        ["Cart - CartItem", "Composition 1 - 0..*", "A cart line has no meaning outside its cart and is deleted with it"],
        ["Order - OrderItem", "Composition 1 - 1..*", "An order has at least one line; lines are fixed after creation"],
        ["Order - StatusChange", "Composition 1 - 1..*", "The append-only history that explains the current status (BP04)"],
        ["Order - Payment", "Association 1 - 0..*", "Several attempts are possible (A5 retry); at most one succeeds"],
        ["Order - Shipment", "Association 1 - 0..1", "A shipment exists only after packing"],
        ["Shipment - Milestone", "Composition 1 - 0..*", "Milestones are carrier messages about one shipment"],
        ["Product - StockLevel", "Association 1 - 1", "Stock is kept apart from the catalogue so that two roles do not edit one record"],
        ["StockLevel - InventoryEvent", "Association 1 - 0..*", "Every quantity is explained by events (FR19)"],
        ["Review - Order, Product", "Association", "A review is verified by a delivered order of that product (FR14)"]], [40, 38, 87]),
    ("p", "Two modelling decisions deserve a comment. CartItem stores its own <i>cartPrice</i> and OrderItem its own "
          "<i>unitPrice</i> instead of reading Product.price, because the price at the time of adding and the price paid "
          "are historical facts; if the administrator changes a price, old orders must not change. And StockLevel is a "
          "separate class rather than an attribute of Product: in Assignment 01 the catalogue and the stock were "
          "maintained by different people, and putting both in one class would recreate the conflict of BP01 and BP02. "
          "The derived attribute <i>/available</i> (physical minus reserved) is marked with a slash because it is never "
          "stored."),
    ("h2", "2.6. Order State Machine"),
    ("p", "BP04, unclear order status, is in the end a missing state model. The state machine makes the allowed "
          "transitions explicit; any transition that is not drawn is forbidden. Each transition is labelled with "
          "<i>event [guard] / action</i>, so the diagram also says when stock is reserved, released or issued."),
    ("fig", os.path.join(D, "ST01 Order State Machine.png"), "Order state machine - VP diagram \"ST01 Order State Machine\"", 115),
    ("p", "The state machine resolves several questions that the use cases left open. A cancellation is possible until "
          "packing (Payment Pending, Paid/Confirmed, On Hold, Processing) and impossible afterwards, which makes FR13's "
          "\"eligible order\" precise. Payment Failed is a final state: a new attempt creates a new order instead of "
          "reviving the old one. An order On Hold returns to Processing once the reason is resolved, and a delivery that "
          "fails once can still end in Delivered when the carrier's next attempt succeeds. The same table of "
          "transitions appears in the code as a dictionary, and a model test checks that a skipped state is rejected."),
    ("h2", "2.7. Data Modeling"),
    ("p", "Data modelling followed the three levels practised in Assignment 03 and Test 01. The <b>conceptual</b> model is "
          "the analysis class diagram: entities, attributes and multiplicities, independent of any database. The "
          "<b>logical</b> model maps it to relations: each class becomes a table with a primary key, each one-to-many "
          "association a foreign key on the many side, each composition a foreign key that is part of the child's key, "
          "and the generalisation User-Customer a single table <i>users</i> with a role column (the subclass adds no "
          "columns except the address, which has its own table). The <b>physical</b> model adds types, NOT NULL, UNIQUE "
          "and CHECK constraints for SQLite."),
    ("p", "The complete physical model, its two ER diagrams and the database generated from them are the subject of "
          "Section 4.2; the table below lists the integrity rules it carries."),
    ("table", "Integrity rules expressed as database constraints", ["Constraint", "Table", "Requirement"], [
        ["CHECK (physical >= 0, reserved >= 0, physical >= reserved)", "stock_level", "FR19, BR20: never negative"],
        ["UNIQUE (product_id, kind, reference)", "inventory_event", "NFR07: an event is recorded once"],
        ["UNIQUE (idempotency_key)", "customer_order", "UC08 A7: one order per submission"],
        ["UNIQUE (attempt_ref)", "payment", "FR10: one result per attempt"],
        ["UNIQUE (order_id)", "shipment", "One shipment per order (Release 1)"],
        ["PRIMARY KEY (shipment_id, seq)", "shipment_milestone", "UC23: duplicate milestones ignored"],
        ["UNIQUE (customer_id, product_id, order_id); CHECK rating 1-5", "review", "FR14: one review per purchase"],
        ["CHECK (total > 0), price > 0", "customer_order, product", "Valid amounts"]], [72, 35, 58]),
    ("p", "The order table is called <i>customer_order</i> because ORDER is a reserved word in SQL. The status history is "
          "a table of its own with an auto-increment key, so rows are only ever appended. The audit_log table has no "
          "foreign keys on purpose: it must keep its rows even if the referenced record is later removed."),
    ("h2", "2.8. Consistency Across Models"),
    ("table", "Cross-model consistency checks", ["Check", "Result"], [
        ["Every lifeline of SD01/SD02 is a class of CL01 or a boundary/control of the use case", "Passed (Cart, StockLevel, Order, Shipment are entities)"],
        ["Every data store of DFD0 corresponds to classes of CL01 and tables of ERD01", "Passed (D1 Products = product, category; D4 Inventory = stock_level, inventory_event)"],
        ["Every state of ST01 is a value of Order.status and every transition is reachable from a use case", "Passed; Delivery Failed reached only from UC23"],
        ["Every message of SD01 corresponds to an action of AD01", "Passed; message 6 groups UC31 and UC32"],
        ["Multiplicities of CL01 match foreign keys of ERD01", "Passed; Customer-Cart 0..1 became UNIQUE(customer_id)"],
        ["DFD1 is balanced with process 4.0 of DFD0", "Passed (same external flows)"]], [95, 70]),
    ("h2", "2.9. Chapter Summary"),
    ("p", "Eleven analysis diagrams refine the requirements: three activity diagrams, two DFD levels, two sequence "
          "diagrams, one class diagram, one state machine, one physical ERD and the context diagram of Chapter 1. The "
          "models agree on six checks. The analysis made two rules concrete that the design must keep: stock and "
          "status are explained by events, and every external exchange is matched by a unique reference."),
]
