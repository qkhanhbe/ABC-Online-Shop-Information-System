"""Additional sections inserted before each chapter summary (numbered automatically)."""

CH1 = [
    ("h2", "1.x. Elicitation Questions and Assumptions"),
    ("p", "The investigation could not observe the shop directly, so every interpretation that goes beyond the case "
          "description was recorded with the question that would confirm or reject it. The list doubles as an interview "
          "plan for the first meeting with the shop's staff."),
    ("table", "Working assumptions and the questions that validate them", ["ID", "Working assumption", "Question / evidence required"], [
        ["A1", "ABC sells general consumer products through its own website only", "Which channels accept orders today: website, social media, marketplace, phone?"],
        ["A2", "Separate copies and batch updates cause the inconsistencies", "Where is each product, customer, order and stock item recorded, who owns it, how often is it updated?"],
        ["A3", "Available stock = physical stock minus reserved quantities", "When exactly is stock reserved, released, issued, received and adjusted?"],
        ["A4", "Order status can be derived from accepted business events", "Which status names, transition rules and customer-visible wordings are approved?"],
        ["A5", "Providers expose a reference and a status for every exchange", "Which providers are used; how are duplicates, timeouts and late updates reported?"],
        ["A6", "Only customers with a delivered order may review", "Can visitors review? Who approves or removes a review?"],
        ["A7", "Management needs sales, inventory and exception reports", "Which decision uses each report, how often, with which definitions?"]], [12, 70, 83]),
    ("h2", "1.x. From Problems to Objectives"),
    ("table", "Traceability from business problems to system objectives", ["Problem", "Objectives", "Evidence expected after implementation"], [
        ["BP01, BP06 inconsistent product and customer data", "O1, O7", "One controlled record per item; audited changes; fewer conflicting entries"],
        ["BP02 outdated inventory", "O2, O3", "Every quantity explained by events; fewer cancellations for unavailable items"],
        ["BP03 manual order processing", "O3, O5", "No re-entry; provider results matched to orders automatically"],
        ["BP04 unclear order status", "O3, O4, O5", "Timestamped status history; fewer routine status enquiries"],
        ["BP05, BP07 slow and limited management information", "O1, O6", "Reports computed from operational records with a visible refresh time"]], [55, 25, 85]),
    ("p", "The objectives deliberately avoid numeric targets such as \"reduce enquiries by 30%\". A target needs a baseline, "
          "and the shop has none yet; inventing one during the investigation would give the project a false precision. The "
          "candidate measures (status enquiries per 100 orders, stock discrepancies, orders cancelled for unavailable "
          "items, report preparation time) are recorded so that a baseline can be taken before the system goes live."),
    ("h2", "1.x. Further Use Case Specifications"),
    ("p", "UC08 depends on two use cases that carry most of the integrity rules: UC09 Make Payment and UC20 Manage "
          "Inventory. Their specifications, condensed from Assignment 02, are the source of the payment and stock code in "
          "Chapter 5."),
    ("table", "Specification of UC09 Make Payment", ["Field", "Specification"], [
        ["Actors", "Customer (primary), Payment Provider (supporting); triggered by UC08 for a Payment Pending order"],
        ["Goal", "Record an authoritative online-payment outcome without raw credentials or duplicates"],
        ["Main flow", "1 System creates a payment attempt with a unique reference. 2 System sends reference, amount and currency to the "
                      "provider. 3 Customer authorises at the provider. 4 Provider returns a verifiable result. 5 System authenticates "
                      "the source and matches reference, amount and currency. 6 System records success once and changes the order to Paid/Confirmed."],
        ["Alternative flows", "A1 declined: Payment Failed, reservations released, cart kept. A2 timeout: Pending, reconcile later, never "
                              "\"pay again\". A3 duplicate callback: acknowledge, no second effect. A4 late success on a closed order: refund exception."],
        ["Exceptions", "E1 reference, amount or currency mismatch: quarantine, order unchanged. E2 unauthenticated result: reject and alert."],
        ["Business rules", "Store status and references, never card data; a retry creates a new attempt reference; provider retries are idempotent"]], [32, 133]),
    ("table", "Specification of UC20 Manage Inventory", ["Field", "Specification"], [
        ["Actors", "Warehouse Staff (primary); UC08, UC09, UC12 and UC21 create events automatically; Supplier through UC24"],
        ["Goal", "Maintain current, explainable stock through traceable events"],
        ["Main flow", "1 Staff selects a product and an event type; system shows physical, reserved, available and recent events. "
                      "2 Staff enters quantity, reference and reason. 3 System validates role, product, quantity, unique reference "
                      "and resulting balance. 4 System records an immutable event and recalculates the balance atomically. "
                      "5 At or below threshold, system offers UC24. 6 System shows the new balance and the event id."],
        ["Alternative flows", "A1 reservation, A2 issue, A3 release (order-driven); A4 correction recorded as a reason-coded ADJUST; A5 threshold reached"],
        ["Exceptions", "E1 negative resulting balance: reject atomically. E2 duplicate reference: return the earlier event, no change."],
        ["Business rules", "available = physical - reserved; all quantities >= 0; an issue or release never exceeds its reservation"]], [32, 133]),
    ("h2", "1.x. Acceptance Criteria"),
    ("p", "For the requirements with the highest risk, acceptance criteria were written in the Given-When-Then form so that "
          "they can become tests without reinterpretation. Chapter 5 shows that each of them became exactly one test."),
    ("table", "Acceptance criteria of key requirements", ["Req.", "Given", "When", "Then"], [
        ["FR09 / A7", "a cart with one product and checkout key k-1", "the customer submits checkout twice with k-1", "one order exists and one payment attempt was made"],
        ["FR10 / NFR07", "a pending payment attempt", "the provider sends a forged result, a wrong amount, then the correct result twice", "the order is Paid/Confirmed exactly once"],
        ["FR11 / NFR05", "order O002 belongs to customer C002", "customer C001 asks for O002", "the answer is \"not found\"; C002 sees the order"],
        ["FR19", "P05 with 10 units received under reference GRN-77", "the same receipt is recorded again, then an adjustment of -20", "stock stays 10; the adjustment is rejected"],
        ["FR21", "a shipment with milestones 1 and 2", "milestone 2 arrives again and milestone 1 arrives late", "both are ignored and the status does not move back"]], [20, 45, 50, 50]),
    ("h2", "1.x. Managing Requirement Change"),
    ("p", "Requirements changed three times after Assignment 02, and each change was recorded with its reason instead of "
          "silently editing the baseline. (1) The AI requirements AI-R1 to AI-N3 were added as Release 2 extensions, so the "
          "32 Release 1 use cases stayed unchanged. (2) The order state machine gained the transition Delivery Failed "
          "→ Delivered when implementing UC23 showed that a carrier can deliver after a failed attempt without a new "
          "pick-up message. (3) The definition of a purchase (used by reviews and recommendations) was made explicit: an "
          "order counts only if it was not cancelled and its payment did not fail. Each change was propagated through the "
          "traceability matrix to the diagrams and tests that depend on it."),
]

CH2 = [
    ("h2", "2.x. Business Rules and Decision Logic"),
    ("p", "The decision nodes of the activity diagrams hide business rules. Writing them as decision tables makes sure "
          "that every combination of conditions has exactly one outcome, which is what the code must implement."),
    ("table", "Decision table: may an order enter Processing? (UC19)", ["Rule", "Payment verified", "All lines reserved", "Blocking exception", "Outcome"], [
        ["R1", "Yes", "Yes", "No", "Processing; added to the pick list"],
        ["R2", "No", "-", "-", "On Hold: \"payment is not confirmed\""],
        ["R3", "Yes", "No", "-", "On Hold: \"product is not reserved\""],
        ["R4", "Yes", "Yes", "Yes", "On Hold with the recorded reason"]], [14, 30, 32, 32, 57]),
    ("table", "Decision table: may an order be cancelled? (UC12)", ["Current status", "Who", "Outcome"], [
        ["Payment Pending", "Owner or Sales Staff", "Cancelled; reservations released"],
        ["Paid/Confirmed, On Hold, Processing", "Owner or Sales Staff", "Cancelled; reservations released; refund initiated and audited"],
        ["Ready for Shipment, Shipped, Delivered", "anyone", "Rejected: \"can no longer be cancelled\""],
        ["any status", "another customer", "\"order not found\" (no disclosure)"]], [60, 45, 60]),
    ("table", "Promotion rule (UC32)", ["Condition", "Result"], [
        ["code unknown", "no discount; message \"promotion does not exist\"; checkout continues (A4)"],
        ["today outside [start, end] or subtotal < minimum", "no discount; message \"not valid for this order\""],
        ["valid", "discount = subtotal x percent / 100, rounded to cents; shipping calculated after discount"]], [70, 95]),
    ("h2", "2.x. Class Responsibilities"),
    ("table", "Analysis classes and their responsibilities", ["Class", "Responsibility", "Key rule"], [
        ["User / Customer", "Identity, role, contact; customer owns address, cart and orders", "Least privilege by role"],
        ["Product / Category", "What is sold and how it is grouped", "Only active products are sold"],
        ["Promotion", "A discount rule with dates and minimum total", "Valid only in its period"],
        ["Cart / CartItem", "Tentative choice with the price at the time of adding", "Revalidated before ordering"],
        ["Order / OrderItem", "Commitment with authoritative prices and address", "Lines fixed after creation"],
        ["StatusChange", "One entry of the append-only order history", "Never updated or deleted"],
        ["Payment", "One attempt with its reference and result", "At most one success per order"],
        ["StockLevel / InventoryEvent", "Current balance and the events that explain it", "available = physical - reserved >= 0"],
        ["Shipment / Milestone", "Parcel and carrier messages", "Sequence numbers only increase"],
        ["Review", "Opinion linked to a delivered purchase", "One per customer, product and order"]], [38, 75, 52]),
    ("h2", "2.x. From Classes to Tables"),
    ("table", "Mapping of the analysis model to the logical model", ["Class / relationship", "Table", "Key and foreign keys"], [
        ["User, Customer (generalisation)", "users", "PK user_id; role column distinguishes the subtypes"],
        ["Address (aggregation 1-0..1)", "address", "PK = FK customer_id"],
        ["Cart (1-1 with Customer)", "cart", "PK cart_id; FK customer_id UNIQUE"],
        ["CartItem (composition)", "cart_item", "PK (cart_id, product_id), both FK"],
        ["Order", "customer_order", "PK order_id; FK customer_id; UNIQUE idempotency_key"],
        ["OrderItem (composition)", "order_item", "PK (order_id, product_id), both FK"],
        ["StatusChange (composition)", "order_status_history", "PK id (autoincrement); FK order_id"],
        ["Payment", "payment", "PK payment_id; FK order_id; UNIQUE attempt_ref"],
        ["Shipment / Milestone", "shipment / shipment_milestone", "UNIQUE order_id / PK (shipment_id, seq)"],
        ["Product, Category", "product, category", "FK category_id"],
        ["StockLevel (1-1) / InventoryEvent", "stock_level / inventory_event", "PK = FK product_id / UNIQUE (product_id, kind, reference)"],
        ["Review", "review", "FK product_id, customer_id, order_id; UNIQUE of the three"]], [50, 45, 70]),
    ("p", "The schema is in third normal form. Every non-key column depends on the whole key and only on the key: the "
          "product name copied into order_item is not a transitive dependency but a historical fact (the name at the time "
          "of purchase), in the same way as unit_price. The order total is stored although it can be computed from the "
          "lines, because reports must reproduce the amount that was charged even if a rounding rule changes later; the "
          "service computes it once at creation and never updates it."),
    ("h2", "2.x. CRUD Matrix"),
    ("p", "The CRUD matrix crosses use cases with data entities and shows which use case creates (C), reads (R), updates "
          "(U) or deletes (D) which data. It is a completeness check: every entity must be created somewhere and read "
          "somewhere, and an entity updated by many use cases deserves a closer look at concurrency."),
    ("table", "CRUD matrix (selected use cases)", ["Use case", "Product", "Stock / Event", "Cart", "Order / History", "Payment", "Shipment", "Review"], [
        ["UC04-06 Browse, Search, View", "R", "R", "", "", "", "", "R"],
        ["UC07 Manage Cart", "R", "R", "CRU", "", "", "", ""],
        ["UC08 Place Order", "R", "RU / C", "RU", "C", "", "", ""],
        ["UC09 Make Payment", "", "U / C (release)", "", "U / C", "CU", "", ""],
        ["UC11 Track Order", "", "", "", "R", "", "R", ""],
        ["UC12 Cancel Order", "", "U / C", "", "U / C", "R", "", ""],
        ["UC13 Submit Review", "", "", "", "R", "", "", "C"],
        ["UC14 Manage Products", "CRU", "C", "", "", "", "", ""],
        ["UC18 Manage Reviews", "", "", "", "", "", "", "RU"],
        ["UC19 Process Orders", "", "R", "", "RU / C", "R", "", ""],
        ["UC20 Manage Inventory", "R", "RU / C", "", "", "", "", ""],
        ["UC21-23 Shipment", "", "U / C (issue)", "", "U / C", "", "CRU", ""],
        ["UC25-28 Reports", "R", "R", "", "R", "R", "", ""]], [37, 16, 22, 13, 24, 17, 18, 18]),
    ("p", "Two observations from the matrix shaped the design. Stock is updated by six use cases, so stock changes are "
          "funnelled through one service method (InventoryService.record) inside a transaction. And no use case deletes an "
          "order, a payment or a stock event: corrections are new records, which is what makes every figure explainable."),
]

CH3 = [
    ("h2", "3.x. AI Component Specifications"),
    ("table", "AI component specifications", ["ID / component", "Input → output", "Interface", "Fallback"], [
        ["AIC-01 SpeechService", "audio → text", "transcribe(audio) -> str", "Text box; message \"please type your search\""],
        ["AIC-02 QueryService", "text → {type, terms, filters} or order query", "text_query, voice_query, image_query, multimodal_query, order_query", "Raw words as terms"],
        ["AIC-03 ImageService + VectorIndex", "image → 128-d vector → top-k ids", "encode(path); VectorIndex.search(z, k)", "Category browsing"],
        ["AIC-04 Search + RankingService", "query → ranked products with scores", "search(query, k) -> [result]", "Keyword-only ranking"],
        ["AIC-05 ReviewInsightService", "reviews → aspects, counts, evidence, label", "analyse(reviews); is_noise(text)", "Plain review list"],
        ["AIC-06 RecommenderService", "product / customer → products with scores", "fit(); similar(id, k); for_customer(id, k)", "Same-category products"]], [38, 45, 52, 30]),
    ("h2", "3.x. Worked Example: Ranking a Combined Query"),
    ("p", "The combined query \"running shoes\" with a photo of a red shoe shows how the formula of Section 3.5 decides. "
          "With λ<sub>t</sub> = λ<sub>i</sub> = 0.5 the weights are α = β = 0.45 and γ = 0.1. All three running shoes "
          "match both query words, so S<sub>text</sub> = 2/2 = 1 for each of them; the photo separates them."),
    ("table", "Score components of the top three results", ["Product", "S_text", "S_image (cosine)", "Available", "S_business", "S(x|q)"], [
        ["Red Running Shoes", "1.00", "0.959", "7", "0.8 + 0.2·7/20 = 0.870", "0.45 + 0.432 + 0.087 = 0.969"],
        ["Nike Running Shoes", "1.00", "0.504", "6", "0.8 + 0.2·6/20 = 0.860", "0.45 + 0.227 + 0.086 = 0.763"],
        ["Adidas Running Shoes", "1.00", "0 (not in image top-5)", "14", "0.8 + 0.2·14/20 = 0.940", "0.45 + 0 + 0.094 = 0.544"]], [38, 15, 30, 18, 34, 30]),
    ("p", "The example also shows a limit: Adidas Running Shoes receives no image score at all because the image retrieval "
          "keeps only the five most similar pictures, and the red cap and red backpack are more similar in colour than a "
          "white shoe. With a larger k, or with a neural encoder that captures shape better than colour, it would get a "
          "small positive score. The order of the results would not change, which is why k = 5 was kept."),
    ("h2", "3.x. Worked Example: Analysing One Review"),
    ("p", "The review \"Comfortable shoes but delivery was late by four days.\" (3 stars) is processed as follows. It is "
          "not noise (more than two words, no link). It is split at <i>but</i> into \"comfortable shoes\" and \"delivery was "
          "late by four days\". The first clause contains the quality word <i>comfortable</i>, which is also a positive word: "
          "quality +1. The second contains the delivery word <i>delivery</i> and the negative word <i>late</i>: delivery "
          "−1. The star rating is not needed because both clauses carry an opinion. On the product page, this review adds "
          "one positive quality count and one negative delivery count, and may be shown as evidence for either aspect."),
    ("h2", "3.x. Business Evaluation"),
    ("p", "Technical metrics say whether a component works; business metrics say whether it helps the shop. The prototype "
          "cannot measure the second kind, because it has no real customers, so the metrics are defined now and attached to "
          "the AI requirements, to be collected with an A/B comparison after release."),
    ("table", "Business metrics of the AI features", ["Feature", "Metric", "Linked problem / need"], [
        ["Multimodal search", "Search-to-cart rate; share of searches with no click; voice/photo usage", "SN01, BP01"],
        ["Order questions", "Status enquiries to staff per 100 orders", "BP04, SN04"],
        ["Review insights", "Return rate of products with negative aspects; time to resolve a recurring complaint", "SN06, SN10"],
        ["Noise filter", "Share of spam that reaches the product page; moderation time", "SN06"],
        ["Recommendations", "Click-through and add-to-cart rate of recommended items; items per order", "Business objective (sales)"]], [35, 85, 45]),
    ("h2", "3.x. AI Traceability"),
    ("table", "From problem to AI requirement, component, metric and test", ["Need / problem", "AI requirement", "Component", "Measured by", "Test"], [
        ["SN01 find products", "AI-R1, AI-R3", "AIC-01..04", "Top-1 success 92.3%", "test_image_and_multimodal_search"],
        ["BP04, NFR05 status, privacy", "AI-R2", "AIC-02, OrderDAO", "3/3 order queries", "test_order_questions_only_see_own_orders"],
        ["SN06 controlled reviews", "AI-R4, AI-R5", "AIC-05", "F1 0.96", "test_review_insights_handle_negation_and_noise"],
        ["Sales objective", "AI-R6", "AIC-06", "Coverage 15/15", "test_recommender_never_suggests_..."],
        ["NFR09 maintainability", "AI-N1", "all", "Interfaces fixed", "test_dependencies_only_point_downwards"]], [32, 25, 28, 30, 50]),
]

CH4 = [
    ("h2", "4.x. From Analysis Classes to Design Classes"),
    ("table", "What happened to each analysis element in the design", ["Analysis element", "Design element(s)", "Package"], [
        ["Entity classes (Customer, Cart, Order, ...)", "Model classes with Step 1 methods", "model"],
        ["Boundary objects (CheckoutForm, OrderPage)", "View templates + controller methods", "view, controller"],
        ["Control objects (CheckoutController)", "Service classes (CheckoutService, ...)", "service"],
        ["PaymentGateway boundary", "PaymentGateway interface + SimulatedPaymentProvider", "service"],
        ["Data stores of the DFD", "Tables (schema.sql) + DAO interfaces and implementations", "dao"],
        ["Order state machine", "TRANSITIONS dictionary + Order.change_status", "model"],
        ["Decision tables", "OrderService.start_processing, Order.can_cancel, Promotion.discount_for", "service, model"],
        ["Search components of Assignment 06", "ai.search package + VectorIndex, ImageStorage in dao", "ai, dao"]], [55, 75, 35]),
    ("p", "The control objects of the analysis are the place where the name changes the most: an analysis control "
          "\"coordinates a use case\", and in a web application that job is split between a controller, which handles the "
          "request, and a service, which applies the rules. This split is the main reason for the extra service layer."),
    ("h2", "4.x. Service Layer Specification"),
    ("table", "Service classes", ["Service", "Responsibility", "Collaborators (constructor)", "Use cases"], [
        ["AuthService", "Register, login, password hashing, role checks", "Database, CustomerDAO, AuditDAO", "UC01-02"],
        ["CatalogService", "Browse, product details with availability, product and promotion maintenance", "ProductDAO, InventoryDAO, PromotionDAO, AuditDAO", "UC04, UC06, UC14, UC16"],
        ["CartService", "Cart lines, availability, cart validation", "CartDAO, ProductDAO, InventoryDAO", "UC07, UC29-30"],
        ["CheckoutService", "Quote, promotion, shipping, atomic order creation, payment request", "CartDAO, OrderDAO, PromotionDAO, CartService, InventoryService, PaymentService", "UC08, UC31-32"],
        ["PaymentService", "Payment attempts, verified callbacks, failure handling", "PaymentDAO, OrderDAO, InventoryService, PaymentGateway, AuditDAO", "UC09"],
        ["OrderService", "History, tracking, cancellation, processing queue", "OrderDAO, ShipmentDAO, PaymentService, InventoryService, AuditDAO", "UC10-12, UC19"],
        ["InventoryService", "Idempotent stock events, low stock, replenishment", "InventoryDAO, ProductDAO, AuditDAO", "UC20, UC24"],
        ["ShipmentService", "Pick list, packing, delivery request, milestones", "ShipmentDAO, OrderDAO, InventoryService, ShippingGateway", "UC21-23"],
        ["ReviewService", "Eligibility, noise check, moderation", "ReviewDAO, OrderDAO, ReviewInsightService", "UC13, UC18"],
        ["ReportService", "Dashboard, sales, inventory and exception reports", "OrderDAO, ProductDAO, InventoryDAO, AuditDAO", "UC25-28"]], [28, 52, 60, 25]),
    ("h2", "4.x. Interfaces to External Systems"),
    ("table", "Contracts of the provider gateways", ["Interface", "Request", "Response / callback", "Guarantees"], [
        ["PaymentGateway.authorize", "attempt_ref, amount, currency, card token", "{attempt_ref, status, provider_ref, amount, currency, signature} or no answer",
         "Signature = HMAC-SHA256 over all fields; result may repeat or arrive late"],
        ["ShippingGateway.create_delivery", "order_id, address, parcels", "carrier reference", "One reference per order; reused if called again"],
        ["Carrier milestone (UC23)", "-", "carrier_ref, seq, code, time, location", "seq increases; duplicates and older messages ignored"]], [35, 35, 55, 40]),
    ("h2", "4.x. Error Handling Design"),
    ("table", "Service exceptions and how the presentation layer shows them", ["Exception", "Raised when", "Shown as"], [
        ["NotFound", "Record missing or owned by another customer", "404 page with a neutral message"],
        ["PermissionDenied", "Role lacks the permission", "Redirect to login (no session) or 403 page"],
        ["ValidationError", "A business rule rejects the request (stock, transition, review)", "400 page or a message on the form"],
        ["CheckoutError", "Cart validation problems (list)", "Back to the cart with every problem listed"],
        ["StockError / InvalidTransition", "Model rule violated", "Converted to ValidationError by the service"]], [38, 70, 57]),
    ("h2", "4.x. Design Patterns Used"),
    ("table", "Patterns and where they appear", ["Pattern", "Where", "Why"], [
        ["Model-View-Controller", "view, controller, model packages", "Separate request handling, presentation and data"],
        ["Service layer", "service package", "One place for the rules of a use case"],
        ["Data Access Object", "dao package", "Storage can change without touching services"],
        ["Front controller / router", "WebApp.dispatch", "One entry point for routing, sessions and error mapping"],
        ["Gateway (strategy)", "PaymentGateway, ShippingGateway", "Simulated and real providers are interchangeable"],
        ["Composition root, dependency injection", "shop.build_shop", "All wiring in one place; tests replace parts"],
        ["Idempotency key", "Checkout, payment attempts, stock references", "Safe retries (NFR07)"],
        ["Event log (append-only)", "inventory_event, order_status_history", "Every figure explained by its history"]], [45, 55, 65]),
]


def insert(blocks, extra, chapter_prefix):
    """Insert extra sections before the summary of the chapter and renumber 'n.x.' headings."""
    idx = next(i for i, b in enumerate(blocks) if b[0] == "h2" and b[1].startswith(chapter_prefix) and "Chapter Summary" in b[1])
    last = int(blocks[idx][1].split(".")[1])
    out = []
    n = last
    for b in extra:
        if b[0] == "h2" and b[1].startswith(chapter_prefix + "x."):
            b = ("h2", f"{chapter_prefix}{n}." + b[1][len(chapter_prefix) + 2:])
            n += 1
        out.append(b)
    summary = ("h2", f"{chapter_prefix}{n}. Chapter Summary")
    return blocks[:idx] + out + [summary] + blocks[idx + 1:]
