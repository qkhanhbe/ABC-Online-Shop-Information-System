import ast
import os
import sys
import textwrap

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "abc_shop")
R = os.path.join(ROOT, "demo_results")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commit_plan import COMMITS  # noqa: E402


def code(rel, name, cls=None, strip_doc=False):
    """Source of a function or method, exactly as in the file."""
    path = os.path.join(SRC, rel)
    text = open(path, encoding="utf-8").read()
    tree = ast.parse(text)
    nodes = tree.body
    if cls:
        nodes = next(n for n in nodes if isinstance(n, ast.ClassDef) and n.name == cls).body
    node = next(n for n in nodes if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Assign))
                and (getattr(n, "name", None) == name or
                     (isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == name)))
    seg = ast.get_source_segment(text, node, padded=True)
    if node.decorator_list if hasattr(node, "decorator_list") else False:
        first = node.decorator_list[0].lineno
        lines = text.splitlines()[first - 1:node.end_lineno]
        seg = "\n".join(lines)
    return textwrap.dedent(seg)


def lines_of(path):
    return sum(1 for _ in open(path, encoding="utf-8"))


def count(folder):
    total = files = 0
    for dirpath, _, names in os.walk(os.path.join(SRC, folder)):
        for n in names:
            if n.endswith(".py"):
                total += lines_of(os.path.join(dirpath, n))
                files += n != "__init__.py"
    return total, files


def section(path, start, end=None):
    text = open(path, encoding="utf-8").read()
    a = text.index(start)
    b = text.index(end, a + 1) if end else len(text)
    return text[a:b].rstrip()


SIZES = {k: count(k) for k in ("model", "dao", "service", "ai", "controller", "view", "tests")}
ROOT_LINES = sum(lines_of(os.path.join(SRC, f)) for f in ("main.py", "shop.py", "seed.py", "evaluate.py"))
APP_LINES = sum(v[0] for k, v in SIZES.items() if k != "tests") + ROOT_LINES

DEMO_FLOW = "$ python main.py demo   (sections 2-8)\n" + section(os.path.join(R, "demo_output.txt"), "--- 2.")
TESTS = open(os.path.join(R, "test_output.txt"), encoding="utf-8").read()
TEST_FIG = "$ python -m pytest -v\n" + "\n".join(
    l.replace("tests/", "") for l in TESTS.splitlines() if "::" in l or "passed" in l)

TREE = """
abc_shop/
  main.py              entry point: seed | serve | demo | search
  shop.py              composition root (creates and wires every object)
  seed.py              catalogue, accounts, October history played through the services
  evaluate.py          evaluation of the three AI components
  model/               customer, product, cart, order, payment, shipment, inventory, review
  dao/                 schema.sql, database.py, interfaces.py, sqlite_dao.py, vector_index.py, image_storage.py
  service/             auth, catalog, cart, checkout, payment, order, inventory, shipment, review, report, gateways
  ai/                  search/ (query, speech, image, search, ranking), review_insights.py, recommender.py
  controller/          http.py, router.py, account/shop/order/staff/report controllers
  view/                templates.py, static/style.css
  data/                seed.json, reviews_labeled.json, images/, query_images/
  tests/               8 test modules, 45 test cases
"""

BLOCKS = [
    ("h1", "CHAPTER 5. CODE"),
    ("p", "The last activity tests every earlier decision against reality. A requirement can be ambiguous and a diagram "
          "can be inconsistent without anyone noticing; a program either runs or it does not, and its tests either pass "
          "or fail. This chapter presents the application <b>abc_shop</b>, written for this essay on top of the "
          "Assignment 06 search prototype. It shows how the code follows the design, how it was run and tested, and what "
          "writing it taught about the earlier models."),
    ("h2", "5.1. Implementation Strategy and Environment"),
    ("p", "The application implements the Release 1 transaction path end to end (account, catalogue, cart, checkout, "
          "payment, processing, packing, delivery, tracking, cancellation, reviews, inventory, reports) and the three AI "
          "components, rather than every screen of all 32 use cases. A vertical slice through all layers is a better test "
          "of the architecture than a complete but shallow user interface: if a checkout can travel from a web form "
          "through the controller, the service and the DAO to the database and back, the remaining use cases follow the "
          "same path. Python was chosen to keep the Assignment 06 code without translation, and only the standard library "
          "plus numpy and Pillow are used, so the program runs offline on any machine with Python 3.9 or later."),
    ("table", "Environment and size of the code base", ["Item", "Value"], [
        ["Language and libraries", "Python 3.11 (tested), standard library: sqlite3, wsgiref, hashlib, hmac; numpy, Pillow; pytest for tests"],
        ["Database", "SQLite file data/abc_shop.db (or in memory for tests and the demo)"],
        ["Web server", "wsgiref (standard library WSGI server); pages rendered by view/templates.py"],
        ["Application code", f"{APP_LINES} lines: model {SIZES['model'][0]}, dao {SIZES['dao'][0]}, service {SIZES['service'][0]}, "
                             f"ai {SIZES['ai'][0]}, controller {SIZES['controller'][0]}, view {SIZES['view'][0]}, entry points {ROOT_LINES}"],
        ["Tests", f"{SIZES['tests'][0]} lines in 8 modules; 45 test cases, all passing"],
        ["Repository", "github.com/qkhanhbe/ABC-Online-Shop-Information-System"]], [40, 125]),
    ("h2", "5.2. Project Structure"),
    ("p", "The folders are the packages of the package diagram PKG01, one to one. A reader of the package diagram can find any "
          "class in the code by its package name, and a reader of the code can find any file in the diagram."),
    ("code", TREE),
    ("h2", "5.3. The Model"),
    ("p", "The model classes are Python dataclasses with the methods of Step 1. The order state machine of Section 2.6 is "
          "a dictionary in model/order.py; change_status is the only way to change a status, it appends to the history "
          "and rejects every transition that is not in the table:"),
    ("code", code("model/order.py", "change_status", "Order")),
    ("p", "The stock rule of UC20 lives in StockLevel.apply. It works on local copies and assigns the new quantities only "
          "after every check has passed, so a rejected event leaves the stock exactly as it was (minimal guarantee of UC20):"),
    ("code", code("model/inventory.py", "apply", "StockLevel")),
    ("h2", "5.4. Data Access Objects"),
    ("p", "The interfaces in dao/interfaces.py are abstract classes; the services receive them through their constructors "
          "and never import the SQLite module (an architecture test checks this). The order DAO shows how the append-only "
          "history of the analysis model reaches the database: an order is upserted, its lines are written once, and only "
          "history entries that are not stored yet are inserted."),
    ("code", code("dao/sqlite_dao.py", "save_order", "SqliteOrderDAO")),
    ("p", "Database.transaction() is a context manager that supports nesting: the outermost call opens BEGIN IMMEDIATE and "
          "commits or rolls back, inner calls join it. This let each DAO method protect its own multi-statement writes "
          "while a service can still make several DAO calls atomic."),
    ("code", code("dao/database.py", "transaction", "Database")),
    ("h2", "5.5. Services: Checkout and Payment"),
    ("p", "CheckoutService.place_order is UC08 in code; the comments carry the step and flow numbers of the specification "
          "in Section 1.15. The idempotency key comes from a hidden field of the checkout form, so pressing the button twice "
          "returns the first order (A7)."),
    ("code", code("service/checkout_service.py", "place_order", "CheckoutService")),
    ("p", "PaymentService.handle_result is the provider callback of UC09. The order of the checks is the order of the "
          "exception flows: unknown or unsigned result (E2), mismatching amount or currency (E1), already final (A3), then "
          "success or decline, with a late success on a closed order turned into a refund exception (A4)."),
    ("code", code("service/payment_service.py", "handle_result", "PaymentService")),
    ("h2", "5.6. Controllers and Views"),
    ("p", "The web layer uses only the standard library. WebApp in controller/router.py is a WSGI application with a table "
          "of routes (Section 4.4.4). dispatch() loads the user of the session, calls the controller method and turns "
          "service errors into readable pages: NotFound becomes 404, PermissionDenied a redirect to the login page or "
          "403, any other ServiceError a 400 page with the rule that was violated."),
    ("code", code("controller/router.py", "dispatch", "WebApp")),
    ("p", "Controllers stay thin. OrderController.checkout reads the form, calls one service method and redirects; it "
          "touches no DAO and calculates nothing:"),
    ("code", code("controller/order_controller.py", "checkout", "OrderController")),
    ("p", "The screenshots below were taken from the running application (python main.py serve) with the seeded data. "
          "The catalogue reads price and availability from the same records as the checkout; the product page combines "
          "the catalogue with the two AI sections of Chapter 3."),
    ("fig", os.path.join(R, "web_01_catalogue.png"), "Catalogue page with the multimodal search box (UC04, UC05)", 150, True),
    ("fig", os.path.join(R, "web_03_product_ai.png"), "Product page with AI review insights and recommendations (UC06, UC33, UC34)", 150, True),
    ("fig", os.path.join(R, "web_02_search_voice.png"), "Voice search result with scores and the processing trace (UC05)", 150, True),
    ("fig", os.path.join(R, "web_04_checkout.png"), "Checkout with promotion WELCOME10, shipping and simulated payment options (UC08, UC31, UC32)", 140, True),
    ("fig", os.path.join(R, "web_05_track_order.png"), "Order tracking: status timeline from order history and carrier milestones (UC11)", 145, True),
    ("fig", os.path.join(R, "web_06_order_question.png"), "Order question \"where is my latest order\" answered from the customer's own orders (AI-R2)", 140, True),
    ("fig", os.path.join(R, "web_07_process_orders.png"), "Sales staff processing queue (UC19)", 145, True),
    ("fig", os.path.join(R, "web_08_inventory.png"), "Warehouse inventory with low-stock rows and event form (UC20, UC24)", 145, True),
    ("fig", os.path.join(R, "web_09_moderation.png"), "Review moderation queue: the spam review held by the AI noise filter (UC18, AI-R5)", 140, True),
    ("fig", os.path.join(R, "web_10_dashboard.png"), "Management dashboard computed from operational records (UC25-UC28)", 150, True),
    ("h2", "5.7. AI Components in Code"),
    ("p", "The search keeps the Assignment 06 classes; the change is in where the data comes from. SearchService now reads "
          "ProductDAO and InventoryDAO, so a result shows the same available quantity as the product page, and order "
          "questions go through OrderDAO.find_by_customer, so the privacy rule is structural:"),
    ("code", code("ai/search/search_service.py", "search_orders", "SearchService")),
    ("p", "The review analyser's core is the clause classifier with the negation window of Section 3.6:"),
    ("code", code("ai/review_insights.py", "classify_clause", "ReviewInsightService")),
    ("p", "The composition root wires the AI components like every other service. The last lines show the design decision "
          "of Section 3.5: the encoder is passed into the data layer instead of being imported by it."),
    ("code", code("shop.py", "_rebuild_index")),
    ("h2", "5.8. Running the Application"),
    ("table", "Commands", ["Command", "What it does"], [
        ["pip install -r requirements.txt", "numpy, Pillow, pytest"],
        ["python main.py seed", "Create data/abc_shop.db: 16 products, 4 customers, 4 staff, 16 orders, 14 reviews"],
        ["python main.py serve --port 8000", "Run the web application on http://localhost:8000 (demo accounts on the login page)"],
        ["python main.py demo", "End-to-end scenario printed step by step (in-memory database)"],
        ["python main.py search --voice \"find running shoes\"", "One search; also --text, --image FILE, --text + --image"],
        ["python evaluate.py", "Search, review-insight and recommender evaluation"],
        ["python -m pytest -q", "All 45 tests"]], [70, 95]),
    ("p", "The seed is not inserted into the tables directly. seed.py plays one month of history through the real services "
          "with a simulated clock: customers fill carts and check out, payments succeed, fail or time out, sales staff "
          "process and hold orders, the warehouse packs, the carrier sends milestones and customers review delivered "
          "products. Every row in the demo database was therefore produced by the same rules that the tests check. The "
          "demo then continues with a new checkout, a repeated submission, a declined payment and a full fulfilment "
          "path including duplicate and out-of-order carrier messages:"),
    ("term", DEMO_FLOW, "Output of main.py demo, sections 2-8: checkout, idempotency, failure, fulfilment, AI and dashboard", 160),
    ("h2", "5.9. Testing"),
    ("p", "The tests were written from the use case specifications and the design rules, so a failing test names the "
          "requirement that is broken. The architecture test turns the package diagram into code: it parses every "
          "module with Python's ast module and fails if a layer imports a layer it must not use."),
    ("code", code("tests/test_architecture.py", "FORBIDDEN") + "\n\n" + code("tests/test_architecture.py", "test_dependencies_only_point_downwards")),
    ("p", "The payment test is the clearest example of a requirement becoming a test. NFR07 says that a replay must not "
          "duplicate a state change, and UC09 lists forged results (E2), mismatching amounts (E1) and duplicate callbacks "
          "(A3). The test sends all of them to the same payment attempt and checks that the order became Paid/Confirmed "
          "exactly once:"),
    ("code", code("tests/test_checkout.py", "test_payment_callbacks_are_verified_and_idempotent")),
    ("table", "Test modules", ["Module", "Tests", "What is checked"], [
        ["test_model.py", "5", "Cart totals, order transitions, stock rules, promotion validity, milestone ordering"],
        ["test_checkout.py", "9", "UC08 main flow and A2, A4, A5, A6, A7, price change, address; UC09 E1, E2, A3"],
        ["test_operations.py", "8", "Tracking ownership, cancellation and refund, processing roles, fulfilment path, inventory idempotency, replenishment, review rules, reports"],
        ["test_ai.py", "7", "Text/voice/image/multimodal search, synonyms, stock-aware ranking, order privacy, review negation and noise, recommender rules"],
        ["test_web.py", "4", "Pages through WSGI: catalogue, search trace, a customer buying through the web, role enforcement"],
        ["test_architecture.py", "7", "Layer rule for six packages (parametrised) and no storage import in services"]], [35, 13, 117]),
    ("term", TEST_FIG, "Output of pytest: 45 tests passed", 160),
    ("h2", "5.10. Traceability from Requirements to Code and Tests"),
    ("table", "From requirement to design element, code and test", ["Requirement", "Design element", "Code", "Checked by"], [
        ["FR08 validate before ordering", "CartService.validate_cart (UC29-30)", "service/cart_service.py", "test_changed_price_is_reported_before_payment, test_insufficient_stock_..."],
        ["FR09 + A7 one order per submission", "idempotency key, UNIQUE constraint", "checkout_service.py, schema.sql", "test_repeated_submission_returns_the_same_order"],
        ["FR10, NFR07 payment once", "PaymentService.handle_result", "service/payment_service.py", "test_payment_callbacks_are_verified_and_idempotent"],
        ["FR11-12, NFR05 own orders only", "OrderService.own_order, search_orders", "order_service.py, search_service.py", "test_customer_only_tracks_own_orders, test_order_questions_only_see_own_orders"],
        ["FR18 valid transitions", "Order.change_status, TRANSITIONS", "model/order.py", "test_order_follows_only_the_allowed_transitions"],
        ["FR19 stock never negative", "StockLevel.apply, CHECK constraints", "model/inventory.py, schema.sql", "test_inventory_events_are_idempotent_and_never_negative"],
        ["FR21 milestones, no regression", "Shipment.add_milestone", "model/shipment.py", "test_shipment_ignores_duplicate_and_older_milestones"],
        ["FR14, AI-R5 reviews", "ReviewService.submit + insight noise filter", "review_service.py", "test_reviews_only_for_delivered_purchases_and_spam_..."],
        ["NFR09 layers", "Package diagram PKG01", "all packages", "test_dependencies_only_point_downwards"]], [38, 42, 38, 47]),
    ("h2", "5.11. What Writing the Code Changed in the Models"),
    ("p", "Checking the code against the diagrams found four real mismatches. None produced a wrong result in the demo, "
          "which is exactly why they are dangerous: they appear only when someone later changes the system."),
    ("table", "Mismatches found while implementing", ["Mismatch", "How it was found", "Fix"], [
        ["Two controllers read DAOs through a service attribute (order_service.orders.find_by_status)", "Reading the controller imports against PKG01",
         "ShipmentService.ready_list and a shipment id in the redirect; no DAO access remains in controllers"],
        ["The image index was built before the catalogue was loaded, so image search returned nothing", "First run of the demo (0 candidates)",
         "seed.py rebuilds the index after loading the catalogue; composition root offers rebuild_index()"],
        ["The state machine did not allow Delivery Failed -> Delivered", "Writing the carrier milestone handler",
         "Transition added to ST01 and to TRANSITIONS; unexpected milestones are audited instead of crashing"],
        ["The recommender test counted cancelled orders as purchases", "Failing test on the seeded data",
         "The test now uses the same definition as the service and the analysis: cancelled and failed orders are not purchases"]], [55, 45, 65]),
    ("h2", "5.12. Development History"),
    ("p", "The code was developed in small commits over four days, in the order of the layers: model, DAO, services, AI, "
          "presentation, tests, models and report. The history is public in the repository."),
    ("table", "Commit history", ["Date and time", "Commit"], [[d[:16], m] for d, m, _ in COMMITS], [38, 127]),
    ("h2", "5.13. Limitations and Future Work"),
    ("bullets", [
        "<b>Scope.</b> Screens exist for the transaction path; profile editing (UC03), category and customer management (UC15, UC17) are implemented in services but not as pages.",
        "<b>Providers.</b> Payment and carrier are simulated behind PaymentGateway and ShippingGateway; a real integration needs webhooks over HTTPS and a reconciliation job for Payment Pending orders.",
        "<b>AI.</b> Speech recognition uses the small English Whisper model (no Vietnamese), the image encoder only sees colour and shape, and the review analyser is a lexicon; Section 3.12 lists the production replacements behind the same interfaces.",
        "<b>Non-functional requirements.</b> NFR01-03 and NFR12 (performance, availability, load) were not measured; the prototype runs on one process with SQLite.",
        "<b>Data.</b> 16 products and synthetic images; the AI numbers do not predict accuracy on a real catalogue."]),
    ("h2", "5.14. Chapter Summary"),
    ("p", f"The design of Chapter 4 runs as {APP_LINES} lines of Python in the same six packages, with a web interface, a "
          "SQLite database and the three AI components. The use case flows of Chapter 1 appear as comments and tests, the "
          "state machine and the integrity rules of Chapter 2 as code and constraints, and the package diagram as an "
          "architecture test. All 45 tests pass, and the demo reproduces every number quoted in the essay."),

    # ------------------------------------------------------------------ conclusion
    ("h1", "CONCLUSION"),
    ("p", "This essay followed ABC Online Shop from its business problem to a running program. Requirement determination "
          "turned fragmented and delayed information into 7 problems, 14 needs, 24 functional and 12 non-functional "
          "requirements and 32 use cases, plus 9 requirements for AI extensions. Analysis refined them with activity, "
          "data-flow, sequence, class, state and data models that agree with each other. The AI chapter treated "
          "multimodal search, review insights and recommendation as ordinary requirements with data, risks, fallbacks "
          "and measurements. The design turned the updated analysis classes into a generated database and a layered MVC "
          "architecture with services and data access objects, whose class skeletons were generated from the model, and the code implements it with 45 passing tests."),
    ("p", "The main lesson is about the joints between the activities. The rules that survived all five chapters were "
          "the ones written precisely at the start: status from recorded events, unique references for every external "
          "exchange, stock that can never become negative, customers who only see their own orders. Each of them is a "
          "sentence in Chapter 1, a guard or constraint in Chapter 2, a method or a unique key in Chapter 4 and a test in "
          "Chapter 5. Where a rule was vague, as with the definition of a purchase for recommendations, the vagueness "
          "came back as a failing test. AI did not change this lesson; it confirmed it, because an AI component is only "
          "as good as the operational data and the rules around it."),
    ("p", "Natural next steps are a real payment and carrier integration with reconciliation, measurement of the "
          "performance requirements, and replacing the prototype AI components with Whisper, CLIP and a fine-tuned "
          "PhoBERT behind the interfaces that are already in place."),
    ("table", "Submitted files", ["File / folder", "Content"], [
        ["tieuluan_V1_04_049_KHANHBQ.pdf", "This essay"],
        ["TieuLuan_KHANHBQ.vpp", "Visual Paradigm project with the 29 diagrams of the essay"],
        ["diagrams/", "PNG export of every diagram"],
        ["abc_shop/", "Source code, data, tests, README"],
        ["design/", "SQL script generated from the ERD, build_db.py, generate_code.py, check_code.py and the generated code"],
        ["demo_results/", "Demo, evaluation and test output; web screenshots"]], [60, 105]),
    ("p", "<b>Project repository:</b> <link href=\"https://github.com/qkhanhbe/ABC-Online-Shop-Information-System\" color=\"blue\">"
          "<u>https://github.com/qkhanhbe/ABC-Online-Shop-Information-System</u></link>"),

    ("h1", "REFERENCES"),
    ("p", "[1] Tran Dinh Que, <i>Information System Analysis and Design</i>, lecture slides and assignment briefs 01-06, "
          "Posts and Telecommunications Institute of Technology, 2026."),
    ("p", "[2] Tran Dinh Que, <i>Integrating AI in E-Commerce: Analysis Phase</i>, course material, PTIT, 2026."),
    ("p", "[3] J. W. Satzinger, R. B. Jackson and S. D. Burd, <i>Systems Analysis and Design in a Changing World</i>, 7th ed., Cengage Learning, 2016."),
    ("p", "[4] A. Dennis, B. H. Wixom and D. Tegarden, <i>Systems Analysis and Design: An Object-Oriented Approach with UML</i>, 5th ed., Wiley, 2015."),
    ("p", "[5] K. C. Laudon and J. P. Laudon, <i>Management Information Systems: Managing the Digital Firm</i>, 17th ed., Pearson, 2022."),
    ("p", "[6] M. Fowler, <i>Patterns of Enterprise Application Architecture</i>, Addison-Wesley, 2002."),
    ("p", "[7] Oracle, <i>Core J2EE Patterns: Data Access Object</i>, 2002."),
    ("p", "[8] A. Radford et al., \"Learning Transferable Visual Models From Natural Language Supervision (CLIP)\", ICML, 2021."),
    ("p", "[9] A. Radford et al., \"Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)\", 2022."),
    ("p", "[10] D. Q. Nguyen and A. T. Nguyen, \"PhoBERT: Pre-trained language models for Vietnamese\", Findings of EMNLP, 2020."),
    ("p", "[11] M. Pontiki et al., \"SemEval-2014 Task 4: Aspect Based Sentiment Analysis\", SemEval, 2014."),
    ("p", "[12] Visual Paradigm, <i>Visual Paradigm Open API (Plug-in) Developer's Guide</i>, version 18."),
    ("p", "[13] Be Quoc Khanh, Assignments 01, 02, 03, 06 and Test 01 of this course, 2026."),
]
