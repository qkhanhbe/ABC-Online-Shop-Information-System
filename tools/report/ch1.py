import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = os.path.join(ROOT, "diagrams")

FRONT = [
    ("h1x", "ABSTRACT"),
    ("p", "This essay is the final version (V4) of the course essay. It follows one information system, the "
          "<b>ABC Online Shop</b>, from requirement determination through requirements analysis, artificial intelligence in "
          "e-commerce and system design to a working, demonstrated implementation. "
          "The material was built up during the semester. Assignment 01 investigated the shop and its problems, "
          "Assignment 02 turned them into a requirements baseline with 32 use cases, Assignment 03 and Test 01 practised "
          "the data-flow, interaction, class and data models, and Assignment 06 produced a three-layer multimodal search "
          "prototype. The essay joins these pieces into one path from a business problem to a running program and explains "
          "the decision taken at each joint."),
    ("p", "The main results are: a requirements baseline of 7 business problems, 14 stakeholder needs, 24 functional and "
          "12 non-functional requirements traced to 32 use cases; an analysis model with activity, data-flow, sequence, "
          "class, state and entity-relationship diagrams; three AI components (multimodal search, aspect-based review "
          "insights and a stock-aware recommender) analysed as ordinary requirements with their own risks and fallbacks; "
          "an updated analysis class model and a layered design (typed design classes, six packages, data access "
          "objects), with a conceptual, logical and physical data model in which product details depend on the category, "
          "from which a database of 23 tables and 28 Python classes were generated; and a working Python application with a web "
          "interface, a SQLite database, 45 automated tests and an evaluation script. All 36 diagrams are kept in one Visual Paradigm project "
          "(TieuLuan_KHANHBQ.vpp). On the test sets, the search returns the expected item first for 25 of 26 queries "
          "(96.2%), the review analyser reaches an aspect F1 of 0.96, and every order-state and stock rule of the "
          "requirements is checked by a test."),
    ("p", "<i>Keywords: requirements engineering, use case, data flow diagram, UML, data modeling, DAO, MVC, layered "
          "architecture, multimodal search, aspect-based sentiment analysis, recommendation, Python.</i>"),
    ("h2", "Abbreviations"),
    ("table", "Abbreviations used in the essay", ["Abbreviation", "Meaning"], [
        ["ABSA", "Aspect-based sentiment analysis"], ["AI", "Artificial intelligence"],
        ["BCE", "Boundary, control, entity (analysis object stereotypes)"], ["BP", "Business problem (Assignment 01)"],
        ["DAO", "Data access object"], ["DFD", "Data flow diagram"], ["ERD", "Entity relationship diagram"],
        ["FR / NFR", "Functional / non-functional requirement"], ["MoSCoW", "Must, Should, Could, Won't (prioritisation)"],
        ["MVC", "Model, view, controller"], ["SN", "Stakeholder need"], ["TF-IDF", "Term frequency, inverse document frequency"],
        ["UC", "Use case"], ["UML", "Unified Modeling Language"], ["VP", "Visual Paradigm, the modeling tool of all diagrams"],
        ["WSGI", "Web Server Gateway Interface (Python web standard)"]], [35, 130]),
]

BLOCKS = [
    ("h1", "INTRODUCTION"),
    ("p", "ABC Online Shop is a medium-sized retailer that sells consumer products online and works with a payment "
          "provider, a shipping provider and suppliers. Its central difficulty, established in Assignment 01, is not the "
          "absence of a website but fragmented and delayed information: product data differs between places, stock "
          "figures lag behind the warehouse, orders are re-entered by hand, customers cannot see where their order is, "
          "and reports arrive after the decisions they were meant to support. Every assignment of the course looked at "
          "this shop from a different angle. Written as one essay, they become a single path from a business problem to "
          "a running program."),
    ("p", "The interesting part of that path is the joints. A requirement written vaguely in the second week turns "
          "into an ambiguous use case, then into a class without a clear responsibility, and finally into code that "
          "nobody can test. A requirement written well can be followed all the way down: the essay shows this with "
          "several threads, for example the rule <i>a payment result changes an order only once</i>, which starts as "
          "NFR07 in Chapter 1, becomes alternative flow A3 of UC09, a guard on the order state machine in Chapter 2, an "
          "idempotent method in the design of Chapter 4 and finally a test in Chapter 5."),
    ("table", "Chapters of the essay and the course work they build on", ["Chapter", "Main question", "Built on"], [
        ["1. Requirement Determination", "What problem does the shop have, and what must the system do about it?",
         "Assignment 01 (investigation), Assignment 02 (requirements, use cases)"],
        ["2. Analysis", "Which behaviour, data and classes does the problem contain?",
         "Assignment 02 (activity diagrams), Assignment 03 (DFD, sequence, class, data models), Test 01"],
        ["3. AI in E-commerce", "Where does AI help the shop, and how do we know that it helps?",
         "Assignment 02 (AI review analysis), Assignment 06 (multimodal search)"],
        ["4. Design", "How do the analysis classes become software components?",
         "Test 01 (eComDesign), Assignment 06 (three-layer architecture), lecture on analysis-to-design steps"],
        ["5. Code", "Does the design survive contact with a compiler and a test suite?",
         "Assignment 06 prototype, new Python application abc_shop"]], [38, 62, 65]),
    ("p", "Three conventions hold throughout. First, identifiers are the ones fixed in Assignment 02 (BP, SN, FR, NFR, "
          "UC), so FR10 in Chapter 1 is the same FR10 that appears in a test name in Chapter 5. Second, every diagram is "
          "a Visual Paradigm diagram of the project TieuLuan_KHANHBQ.vpp, and the figure caption gives its name in the "
          "project. The diagrams were exported with Visual Paradigm Community Edition; because Community Edition "
          "cannot open data flow diagrams, the three DFD-type diagrams (CTX01, DFD0, DFD1) are drawn from the shapes "
          "and routes stored in the same project, in the notation Visual Paradigm uses. Third, every number in Chapters 3 and 5 comes from a program that was run: the outputs are stored in "
          "the folder demo_results and can be reproduced with the commands of Section 5.8."),
    ("p", "The AI chapter sits in the middle on purpose. AI functions are often presented as separate products. In this "
          "essay they are treated as one more set of requirements, with stakeholders, use cases, components, risks and "
          "tests like every other part of the shop. The design and the code therefore contain them from the start "
          "rather than as an attachment."),

    # ------------------------------------------------------------------ Chapter 1
    ("h1", "CHAPTER 1. REQUIREMENT DETERMINATION"),
    ("p", "Requirement determination answers two questions before any model or code exists: what is wrong in the "
          "business, and what must an information system do so that it stops being wrong. This chapter summarises the "
          "investigation of Assignment 01 and the requirements engineering of Assignment 02 and adds what the later "
          "chapters need: an explicit system boundary, measurable quality requirements and the requirements of the AI "
          "extensions."),
    ("h2", "1.1. Requirements in the Development Life Cycle"),
    ("p", "In the system development life cycle, requirements are the hinge between the business and the software. "
          "Errors made here are the most expensive ones, because every later artifact inherits them: an analysis class "
          "models a misunderstood concept, a test confirms the wrong behaviour, and the shop receives a program that "
          "works but does not help. The course follows a chain that keeps each step traceable:"),
    ("eq", "Business problems → Stakeholder needs → System requirements → Use cases → Validation"),
    ("p", "The chain is used in both directions. Forwards, each problem must lead to at least one requirement; "
          "backwards, each requirement must be justified by a need, so that nothing is built only because it is "
          "technically interesting. Section 1.16 checks both directions with a traceability matrix."),
    ("h2", "1.2. Investigation Approach"),
    ("p", "The evidence is the case description of the assignment brief, analysed in Assignment 01. Where the brief only "
          "states a symptom (for example <i>order status is unclear</i>), the cause was written down as a hypothesis "
          "and an elicitation question rather than as a fact, because inventing causes produces requirements for "
          "problems the shop may not have. Four techniques were used: document analysis of the case, stakeholder "
          "analysis, process modeling of the order-to-feedback flow, and problem-cause-consequence analysis summarised "
          "as a problem tree. Questions that only the shop can answer were collected as assumptions to validate "
          "(for example which payment provider is used and how it reports timeouts); they appear again as the "
          "assumptions of Section 1.13."),
    ("h2", "1.3. Business Context"),
    ("table", "Business profile of ABC Online Shop", ["Item", "Description"], [
        ["Organisation", "Medium-sized business-to-consumer online retailer"],
        ["Products", "General consumer products organised in categories; the prototype uses shoes, bags, shirts, caps and watches"],
        ["Customers", "Visitors who browse without an account; registered customers who order, pay, track and review"],
        ["Sales channel", "Own website (responsive web storefront); no marketplace, no physical store"],
        ["Partners", "Payment provider (authorises payments), shipping provider (delivers parcels), suppliers (replenish stock)"],
        ["Staff roles", "Administrator, sales staff, warehouse staff, manager"],
        ["Business objective", "Increase reliable online sales while controlling fulfilment cost and keeping customer trust"]], [40, 125]),
    ("p", "The business model is information-intensive. In a physical shop a customer sees the item on the shelf; online, "
          "the customer relies entirely on a description, a price, an availability flag, reviews, a payment confirmation "
          "and a delivery status. The shop's promise is therefore only as good as the information that connects "
          "customers, staff and the three external partners."),
    ("h2", "1.4. Stakeholder Analysis"),
    ("p", "A stakeholder has an interest in the system; an actor interacts with it directly. Keeping the two apart "
          "prevents a common error, drawing a department or a database as an actor. The table below lists the stakeholders with "
          "the evidence that would show that the system serves them."),
    ("table", "Stakeholders, interests and evidence of success", ["Stakeholder", "Type", "Main interest", "Evidence of success"], [
        ["Visitor / Customer", "External", "Find accurate products, pay safely, know where the order is", "Fewer status enquiries; checkout without help"],
        ["Administrator", "Internal", "One controlled source for catalogue, promotions and reviews", "Audited changes; no conflicting product data"],
        ["Sales staff", "Internal", "Process orders without re-entering data", "Processing queue with complete order facts"],
        ["Warehouse staff", "Internal", "Current stock, clear pick lists", "Stock explained by events; no negative balance"],
        ["Manager", "Internal", "Timely, reproducible reports", "Dashboard computed from operational records"],
        ["Payment provider", "External", "Uniquely referenced requests", "Every result matched to exactly one attempt"],
        ["Shipping provider", "External", "Correct delivery data", "Every milestone matched to one shipment"],
        ["Supplier", "External", "Clear replenishment requests", "Requests raised when stock reaches the threshold"]], [32, 18, 62, 53]),
    ("h2", "1.5. Business Process"),
    ("p", "The core business process runs from browsing to feedback in eight steps: (1) browse products, (2) build a cart, "
          "(3) validate the cart and create an order, (4) request payment, (5) reserve and update stock, (6) prepare and "
          "ship, (7) deliver and collect feedback, (8) report results and exceptions. Each step consumes information "
          "produced by an earlier one, which is why a delay anywhere becomes a problem everywhere: a stock figure that "
          "is one day old lets a customer order an item that no longer exists, which turns into a cancellation, a refund, "
          "an angry review and a wrong sales report."),
    ("h2", "1.6. Information Analysis"),
    ("table", "Information catalogue (from Assignment 01, Table 3)", ["Information item", "Produced by", "Used by", "Quality concern"], [
        ["Product, category, price", "Administrator", "Visitors, checkout, reports", "One version; changes audited"],
        ["Customer, address", "Customer", "Order, delivery, service", "Unique, current, access-controlled"],
        ["Cart", "Customer", "Checkout", "Revalidated before ordering"],
        ["Order, status history", "System from events", "Customer, staff, manager", "One identifier; valid states; timestamps"],
        ["Inventory event, stock level", "Warehouse, order process", "Browsing, checkout, warehouse", "Traceable to events; never negative"],
        ["Payment attempt, result", "System, payment provider", "Order, reports", "Unique reference; no card data stored"],
        ["Shipment, milestone", "Shipping provider", "Customer, staff", "Matched to one shipment; no regression"],
        ["Review", "Customer with delivered order", "Customers, administrator", "Linked to a real purchase"],
        ["Reports", "System", "Manager", "Reproducible for a stated period"]], [36, 34, 40, 55]),
    ("p", "Two controls follow from the catalogue and shape the whole design. Identifiers must link related records "
          "across order, payment, inventory and shipment information, and a status must be derived from recorded "
          "events rather than typed in: an order is <i>Paid</i> because a verified payment result exists, not because "
          "somebody expected one."),
    ("h2", "1.7. Current Problems"),
    ("table", "Business problems, likely causes and consequences", ["ID", "Problem", "Likely cause (to verify)", "Consequence"], [
        ["BP01", "Inconsistent product information", "Several copies edited without one owner", "Conflicting offers, disputes"],
        ["BP02", "Outdated inventory information", "Receipts and sales posted manually, in batches", "Orders for unavailable stock, cancellations"],
        ["BP03", "Manual order processing", "Re-entry of cart, payment and delivery data", "Delay, transcription errors"],
        ["BP04", "Unclear order status", "Milestones stored separately, no state rules", "Repeated enquiries, late detection of failures"],
        ["BP05", "Slow sales reporting", "End-of-period manual consolidation", "Late, irreproducible figures"],
        ["BP06", "Fragmented customer information", "No master identifier, duplicates", "Delivery errors, privacy exposure"],
        ["BP07", "Limited real-time management information", "Operational events disconnected", "Reactive decisions"]], [12, 40, 58, 55]),
    ("p", "The problem tree of Assignment 01 places one central problem, <i>fragmented and delayed information "
          "management</i>, between three causes (manual re-entry, separate records without shared identifiers, unclear "
          "ownership and state rules) and three groups of consequences (order and fulfilment errors, unclear status, "
          "slow reporting). The tree also explains the priorities: inventory accuracy and order status come first "
          "because they affect revenue, customer trust and staff workload at the same time, while reporting can only "
          "be as good as the operational records it reads."),
    ("h2", "1.8. Scope, Boundary and Context"),
    ("p", "The system boundary decides what the shop's software does itself and what it only exchanges with others. "
          "Inside are authentication and roles, customer profiles, catalogue and search, cart and checkout, order and "
          "payment-status coordination, inventory, shipment-status integration, promotions, reviews and reports. "
          "Outside are payment authorisation and settlement, carrier routing and physical delivery, and supplier "
          "operations: the shop sends a uniquely referenced request and records the attributable result. The figure below shows "
          "the boundary as a context diagram, in which the whole system is one process (0) and every arrow is a named "
          "data flow."),
    ("fig", os.path.join(D, "CTX01 System Context Diagram.png"), "System context diagram - VP diagram \"CTX01 System Context Diagram\"", 160),
    ("p", "The context diagram is deliberately symmetric: every external entity both sends and receives. A one-way arrow "
          "would hide a requirement. For example, the shipping provider does not only receive a delivery request; it "
          "also sends milestones, and without that return flow the system could never answer the customer's question "
          "\"where is my order?\" (BP04)."),
    ("h2", "1.9. System Objectives"),
    ("bullets", [
        "<b>O1</b> One controlled, role-authorised source for product, customer, promotion, order, stock, payment-status and shipment-status information (BP01, BP06).",
        "<b>O2</b> Record inventory events promptly and show one consistent available quantity at browsing, checkout, fulfilment and reporting (BP02).",
        "<b>O3</b> Coordinate checkout, payment, reservation, fulfilment, shipment and cancellation without re-entering data (BP03).",
        "<b>O4</b> Give customers and staff a timestamped order status derived from recorded events (BP04).",
        "<b>O5</b> Exchange uniquely referenced requests and results with the payment and shipping providers (BP03, BP04).",
        "<b>O6</b> Produce reproducible sales, inventory and exception reports from operational records (BP05, BP07).",
        "<b>O7</b> Protect personal and transaction data by data minimisation, role-based access and an audit trail (BP06)."]),
    ("h2", "1.10. Stakeholder Needs"),
    ("table", "Stakeholder need catalogue (Assignment 02)", ["ID", "Stakeholder", "Need", "Priority"], [
        ["SN01", "Visitor / Customer", "Find accurate, current product and availability information", "Must"],
        ["SN02", "Customer", "Maintain selected products and quantities before ordering", "Must"],
        ["SN03", "Customer", "Complete a clear and secure checkout and payment", "Must"],
        ["SN04", "Customer", "View order history, processing state and delivery progress", "Must"],
        ["SN05", "Customer", "Cancel an eligible order and review a verified purchase", "Should"],
        ["SN06", "Administrator", "Maintain products, categories, promotions and reviews from one source", "Must"],
        ["SN07", "Sales staff", "Process orders and answer enquiries without re-entering information", "Must"],
        ["SN08", "Warehouse staff", "See current stock and record every inventory movement promptly", "Must"],
        ["SN09", "Warehouse staff", "Prepare shipments and coordinate traceable replenishment", "Must"],
        ["SN10", "Manager", "Obtain timely dashboards and reproducible sales reports", "Should"],
        ["SN11", "Manager", "See inventory, order, payment, shipment and exception information", "Must"],
        ["SN12", "All users / ABC", "Protect personal and transaction information by role and purpose", "Must"],
        ["SN13", "Payment provider", "Receive a uniquely referenced request and return an attributable result", "Must"],
        ["SN14", "Shipping provider", "Receive correct delivery data and return traceable milestones", "Must"]], [13, 32, 102, 18]),
    ("h2", "1.11. Functional Requirements"),
    ("p", "Each functional requirement is an observable \"The system shall\" statement, has one identifier and one MoSCoW "
          "priority, and is allocated to a use case. None of them prescribes a database, a framework or a provider's "
          "internal design; those decisions belong to Chapter 4."),
    ("table", "Functional requirements", ["ID", "The system shall ...", "Pri.", "UC"], [
        ["FR01", "allow a Visitor to register a Customer account with validated identity and contact data", "M", "UC01"],
        ["FR02", "authenticate users and authorise functions according to their roles", "M", "UC02"],
        ["FR03", "allow a Customer to view and update profile and delivery address", "S", "UC03"],
        ["FR04", "display the active catalogue and categories to a Visitor", "M", "UC04"],
        ["FR05", "allow a Visitor to search and filter active products", "M", "UC05"],
        ["FR06", "display description, current price, promotion and available-to-order status", "M", "UC06"],
        ["FR07", "allow a Customer to add an available product, change its quantity or remove it", "M", "UC07"],
        ["FR08", "validate the cart, recheck availability and calculate the authoritative total before ordering", "M", "UC08, UC29-31"],
        ["FR09", "create one uniquely identified order linked to customer, lines, address, totals and status history", "M", "UC08"],
        ["FR10", "send a uniquely referenced payment request and record each attributable result once", "M", "UC09"],
        ["FR11", "allow a Customer to view own order history and details", "M", "UC10"],
        ["FR12", "show current processing and shipment status with the last update time", "M", "UC11"],
        ["FR13", "allow an eligible order to be cancelled according to status and refund rules", "S", "UC12"],
        ["FR14", "allow a Customer with a delivered order line to submit one review for that product", "C", "UC13"],
        ["FR15", "allow an Administrator to create, update, publish and categorise products", "M", "UC14-15"],
        ["FR16", "allow an Administrator to maintain promotion rules and moderate reviews", "S", "UC16, UC18"],
        ["FR17", "allow authorised staff to find and update permitted customer information with an audit trail", "S", "UC17"],
        ["FR18", "allow Sales Staff to progress orders only through valid state transitions", "M", "UC19"],
        ["FR19", "record receipts, reservations, releases, issues and adjustments and recalculate stock", "M", "UC20"],
        ["FR20", "provide a pick list and record packing against the order", "M", "UC21"],
        ["FR21", "send a uniquely referenced delivery request and record attributable milestones", "M", "UC22-23"],
        ["FR22", "issue and track a replenishment request when stock reaches its threshold", "S", "UC24"],
        ["FR23", "provide authorised dashboards and reproducible reports for a selected period", "M", "UC25-28"],
        ["FR24", "apply a promotion only when code, dates, scope and minimum total are valid", "S", "UC32"]], [12, 122, 10, 21]),
    ("h2", "1.12. Non-functional Requirements"),
    ("table", "Measurable non-functional requirements", ["ID", "Category", "Requirement / acceptance criterion"], [
        ["NFR01", "Performance", "95% of browse and search requests complete within 2 s under normal load"],
        ["NFR02", "Performance", "Checkout validation and total calculation within 3 s for 95% of requests (provider time excluded)"],
        ["NFR03", "Availability", "Monthly availability at least 99.5%; RPO 15 min, RTO 2 h"],
        ["NFR04", "Security", "Personal, authentication, payment-status and delivery data in transit use TLS 1.2 or later"],
        ["NFR05", "Access control", "Role-based least privilege; a Customer accesses only own profile and orders"],
        ["NFR06", "Auditability", "Role, order-state, inventory, price and promotion changes record actor, time, identifier, before/after"],
        ["NFR07", "Integrity", "Payment and shipment requests use unique references; a replay never duplicates a transaction, stock event or state change"],
        ["NFR08", "Usability", "90% of first-time users complete checkout in at most five screens without help"],
        ["NFR09", "Maintainability", "Automated tests cover order, payment, inventory and shipment rules; every Must rule has a regression test"],
        ["NFR10", "Privacy", "Only data needed by the task is shown; raw payment credentials are never stored"],
        ["NFR11", "Compatibility", "Essential customer functions work on the two latest versions of Chrome, Edge and Safari"],
        ["NFR12", "Scalability", "With 500 concurrent users NFR01 still holds and 30 checkouts per minute complete without loss"]], [14, 26, 125]),
    ("p", "The NFRs are written so that each can fail. \"The system should be secure\" cannot fail and therefore cannot "
          "be tested; \"a replay never duplicates a transaction\" (NFR07) can, and Chapter 5 shows the test that tries "
          "exactly that. Writing them this way early was the most useful single decision of Assignment 02, because it "
          "turned quality wishes into design constraints."),
    ("h2", "1.13. Prioritisation and Assumptions"),
    ("table", "MoSCoW baseline", ["Class", "Requirements", "Decision rule"], [
        ["Must", "FR01-02, FR04-12, FR15, FR18-21, FR23; NFR01-02, NFR04-07, NFR09-10", "Needed for a secure, traceable sales lifecycle"],
        ["Should", "FR03, FR13, FR16-17, FR22, FR24; NFR03, NFR08, NFR11", "Important; a temporary manual process can bridge Release 1"],
        ["Could", "FR14; NFR12", "Valuable once the transaction path is stable"],
        ["Won't (Release 1)", "Cash on delivery, guest checkout, native apps, marketplace integration", "Outside the first release or unresolved"]], [28, 82, 55]),
    ("p", "The baseline rests on assumptions that only the shop can confirm: authenticated checkout, online payment only, "
          "stock reserved when the order is created, controlled order states, uniquely referenced provider messages and "
          "reviews limited to delivered order lines. They are listed because each one changes the design if it is false; "
          "for example, cash on delivery would add an order state between <i>Shipped</i> and <i>Paid</i>."),
    ("h2", "1.14. Actors and the Use Case Model"),
    ("table", "Actors", ["Actor", "Type", "Use cases"], [
        ["Visitor", "External human", "UC01 Register, UC04 Browse, UC05 Search, UC06 View Product Details"],
        ["Customer (specialises Visitor)", "External human", "UC02-03, UC07-08, UC10-13"],
        ["Staff (abstract)", "Generalisation", "UC02 Login, shared by the four staff roles"],
        ["Administrator", "Internal human", "UC14-18 catalogue, categories, promotions, customers, reviews"],
        ["Sales Staff", "Internal human", "UC17 Manage Customers, UC19 Process Orders"],
        ["Warehouse Staff", "Internal human", "UC20-22, UC24 inventory, shipment, replenishment"],
        ["Manager", "Internal human", "UC25-28 dashboard and reports"],
        ["Payment Provider", "External system", "UC09 Make Payment"],
        ["Shipping Provider", "External system", "UC22 Arrange Delivery, UC23 Update Shipment Status"],
        ["Supplier", "External organisation", "UC24 Manage Replenishment"]], [45, 32, 88]),
    ("p", "Drawing 10 actors and 32 use cases in one picture produces a diagram in which every line crosses several others. "
          "The model is therefore shown in four diagrams, one per package of the use case catalogue of Assignment 02. "
          "Every use case appears in exactly one diagram; an actor appears in each diagram where it has an association."),
    ("fig", os.path.join(D, "UCD1 Account and Catalogue.png"), "Use cases of the Account and Catalogue package - VP diagram \"UCD1 Account and Catalogue\"", 105),
    ("fig", os.path.join(D, "UCD2 Cart, Order and Payment.png"), "Use cases of the Cart, Order and Payment package - VP diagram \"UCD2 Cart, Order and Payment\"", 160),
    ("fig", os.path.join(D, "UCD3 Administration.png"), "Use cases of the Administration package - VP diagram \"UCD3 Administration\"", 100),
    ("fig", os.path.join(D, "UCD4 Operations and Reporting.png"), "Use cases of the Operations and Reporting package - VP diagram \"UCD4 Operations and Reporting\"", 160),
    ("p", "The relationships follow the rules of the lecture. UC08 Place Order <i>includes</i> UC29 Validate Cart, UC30 "
          "Check Product Availability, UC31 Calculate Order Total and UC09 Make Payment, because under the Release 1 "
          "assumptions these always happen during checkout; UC07 includes UC30 because every cart change must check "
          "the orderable quantity. UC32 Apply Promotion <i>extends</i> UC08 only when the customer enters a code; UC12 "
          "Cancel Order and UC13 Submit Review extend UC10 View Order History at the point where an eligible order is "
          "selected; UC24 Manage Replenishment extends UC20 when stock reaches its threshold. The abstract Staff actor "
          "carries the single Login association so that the four staff roles keep separate, least-privilege use cases."),
    ("h2", "1.15. Use Case Specification: UC08 Place Order"),
    ("table", "Specification of UC08 Place Order / Checkout", ["Field", "Specification"], [
        ["Primary actor / supporting", "Customer / Payment Provider through UC09"],
        ["Goal", "Convert a valid cart into one paid, confirmed, traceable order"],
        ["Preconditions", "Customer authenticated; cart contains at least one active product"],
        ["Success guarantee", "One order with validated lines, address, total, payment reference, reservations and a Paid/Confirmed history entry; cart cleared"],
        ["Minimal guarantee", "No duplicate order or charge; stock released if payment fails; cart kept"],
        ["Main flow", "1 Customer selects Checkout. 2 System validates the cart (UC29) and availability (UC30). 3 Customer confirms "
                      "the delivery address. 4 Optional promotion code (UC32). 5 System calculates the total (UC31). 6 Customer "
                      "confirms; system reserves stock and creates one Payment Pending order with an idempotency key. "
                      "7 System requests payment (UC09). 8 Verified success: order Paid/Confirmed, cart cleared, confirmation shown."],
        ["Alternative flows", "A1 inactive line, A2 insufficient stock: return to cart, nothing created. A3 invalid address. "
                              "A4 invalid promotion: continue without discount. A5 payment declined: Payment Failed, "
                              "reservations released, cart kept. A6 timeout: stay Payment Pending, reconcile by reference. "
                              "A7 repeated submission: return the existing order."],
        ["Exception", "E1 reservation or order creation fails: roll back both, preserve the cart"],
        ["Requirements", "FR08-FR10, FR24; NFR02, NFR05-NFR07, NFR10"]], [38, 127]),
    ("p", "UC08 was chosen for full specification because it touches more requirements than any other use case and "
          "because its alternative flows are where the shop currently loses money. Chapter 5 implements each flow of "
          "this table and tests A2, A5, A6, A7 and E1 individually."),
    ("h2", "1.16. Validation and Traceability"),
    ("table", "Traceability from business problems to use cases", ["Problem", "Needs", "Requirements", "Use cases"], [
        ["BP01 product inconsistency", "SN01, SN06", "FR04-06, FR15, NFR06", "UC04-06, UC14-15"],
        ["BP02 outdated inventory", "SN08-09", "FR08, FR19, FR22, NFR07", "UC20, UC24, UC30"],
        ["BP03 manual order processing", "SN02-03, SN07", "FR07-10, FR18", "UC07-09, UC19, UC29-31"],
        ["BP04 unclear status", "SN04, SN14", "FR11-12, FR21", "UC10-11, UC22-23"],
        ["BP05 slow reporting", "SN10", "FR23", "UC25-28"],
        ["BP06 fragmented customer data", "SN12", "FR01-03, FR17, NFR05, NFR10", "UC01-03, UC17"],
        ["BP07 limited real-time information", "SN11", "FR23, NFR01", "UC25-28"]], [45, 25, 50, 45]),
    ("p", "The requirements were validated against five properties. <b>Clear</b>: every statement has an actor, an action, "
          "an object and a condition. <b>Consistent</b>: order states, provider references and reservation rules use the "
          "same terms everywhere. <b>Complete</b>: the matrix has no orphan problem, need, requirement or primary use "
          "case; the supporting UC29-UC32 are reached through include and extend. <b>Feasible</b>: provider-internal work "
          "is outside the boundary. <b>Verifiable</b>: every FR has an observable outcome and every NFR a threshold."),
    ("h2", "1.17. Requirements for the AI Extensions"),
    ("p", "The AI functions of Chapter 3 are specified as Release 2 requirements in the same form, so that they can be "
          "traced and tested like the rest. They extend existing use cases instead of replacing them, and each has a "
          "non-AI fallback."),
    ("table", "AI requirements", ["ID", "Requirement", "Extends", "Source"], [
        ["AI-R1", "Search products by keywords, by a spoken sentence, by a photo, or by text and photo together", "UC05", "A6"],
        ["AI-R2", "Answer order questions (\"where is my latest order?\") only from the customer's own orders", "UC10-11", "A6, FR11"],
        ["AI-R3", "Rank results by text match, image similarity and stock, and show the component scores", "UC05", "A6"],
        ["AI-R4", "Summarise published reviews per aspect (quality, price, delivery, service) with evidence", "UC06 (UC33)", "A02 AI part"],
        ["AI-R5", "Hold reviews that look like spam for moderation instead of publishing them", "UC13, UC18", "A02 AI part"],
        ["AI-R6", "Recommend similar in-stock products and products for a customer's purchase history", "UC06, UC10 (UC34)", "new"],
        ["AI-N1", "Every AI component is replaceable behind a fixed interface (transcribe, encode, analyse, similar)", "-", "NFR09"],
        ["AI-N2", "Results are deterministic and explainable: same input, same output, visible scores", "-", "NFR06"],
        ["AI-N3", "If an AI component fails or lacks data, the page still works with a non-AI fallback", "-", "NFR03"]], [14, 98, 30, 23]),
    ("h2", "1.18. Chapter Summary"),
    ("p", "The chapter turned a shop with fragmented information into a baseline of 7 problems, 14 needs, 24 functional "
          "and 12 non-functional requirements, 9 AI requirements and 32 use cases, with a context diagram that fixes "
          "the boundary and a matrix that shows that every problem is covered. The two ideas that the next chapters "
          "depend on are already visible: status comes from recorded events, and every exchange with a provider carries "
          "a unique reference."),
]
