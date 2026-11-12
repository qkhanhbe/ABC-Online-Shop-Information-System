"""Version 4 (final) of the essay: six chapters in the order of the final brief.

1 System requirements determination   (business, stakeholders, process, problems, context, objectives)
2 Requirements analysis and specification (needs, FR/NFR, use cases, specifications, analysis models)
3 AI in e-commerce
4 System design                        (analysis classes, conceptual/logical/physical data, design classes, layers, code)
5 Implementation and demonstration
6 Conclusion and future work
The text of earlier versions is reused; sections are renumbered here and every "Section x.y" reference follows.
"""
import os
import re

import ch1
import ch2
import ch3
import ch4
import ch5
import extras

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = os.path.join(ROOT, "diagrams")
R = os.path.join(ROOT, "demo_results")


def fig(code, caption, width=160):
    path = next(os.path.join(D, f) for f in sorted(os.listdir(D)) if f.startswith(code + " "))
    return ("fig", path, caption + f" - VP diagram \"{os.path.basename(path)[:-4]}\"", width)


def figl(code, caption):
    path = next(os.path.join(D, f) for f in sorted(os.listdir(D)) if f.startswith(code + " "))
    return ("figl", path, caption + f" - VP diagram \"{os.path.basename(path)[:-4]}\"")


def find(blocks, kind, start):
    return next(i for i, b in enumerate(blocks) if b[0] == kind and b[1].startswith(start))


def after(blocks, kind, start, new, skip=1):
    """Insert blocks after the block found (skip = how many blocks after the heading to pass first)."""
    i = find(blocks, kind, start) + skip
    return blocks[:i] + new + blocks[i:]


# ---------------------------------------------------------------- source parts
c1 = ch1.BLOCKS
intro = c1[:find(c1, "h1", "CHAPTER 1")]
req_det = c1[find(c1, "h2", "1.1. "):find(c1, "h2", "1.10. ")]
req_spec = c1[find(c1, "h2", "1.10. "):find(c1, "h2", "1.18. ")]
c2 = ch2.BLOCKS
analysis = c2[find(c2, "h2", "2.1. "):find(c2, "h2", "2.7. ")]
data_old = c2[find(c2, "h2", "2.7. ") + 1:find(c2, "h2", "2.8. ")]
consistency = c2[find(c2, "h2", "2.8. "):find(c2, "h2", "2.9. ")]
c5 = ch5.BLOCKS
impl = c5[:find(c5, "h2", "5.13. ")]
limits = c5[find(c5, "h2", "5.13. ") + 1:find(c5, "h2", "5.14. ")]
impl_summary = c5[find(c5, "h2", "5.14. "):find(c5, "h1", "CONCLUSION")]
concl = c5[find(c5, "h1", "CONCLUSION") + 1:find(c5, "h1", "REFERENCES")]
refs = c5[find(c5, "h1", "REFERENCES"):]

# ---------------------------------------------------------------- introduction
intro = [b for b in intro if not (b[0] == "table" and b[1].startswith("Chapters of the essay"))]
intro.insert(3, ("table", "Chapters of the essay and the course work they build on", ["Chapter", "Main question", "Built on"], [
    ["1. System Requirements Determination", "What problem does the shop have, who is involved and where is the system boundary?",
     "Assignment 01 (investigation)"],
    ["2. Requirements Analysis and Specification", "What must the system do, and which behaviour, data and classes does that contain?",
     "Assignment 02 (requirements, use cases, activity diagrams), Assignment 03 (DFD, sequence, class models)"],
    ["3. AI in E-commerce", "Where does AI help the shop, and how do we know that it helps?",
     "Assignment 02 (AI review analysis), Assignment 06 (multimodal search)"],
    ["4. System Design", "How do the analysis classes become data, design classes, layers and code?",
     "Test 01 (eComDesign), Assignment 06 (three-layer architecture), lecture on analysis-to-design steps"],
    ["5. Implementation and Demonstration", "Does the design run, and can each function be traced back to its model?",
     "Assignment 06 prototype, Python application abc_shop"],
    ["6. Conclusion", "What was achieved, what is missing and what comes next?", "-"]], [42, 70, 53]))

# ---------------------------------------------------------------- chapter 1
CH1 = [("h1", "CHAPTER 1. SYSTEM REQUIREMENTS DETERMINATION"),
       ("p", "Requirement determination answers two questions before any model or code exists: what is wrong in the "
             "business, and where an information system has to stand to stop it from being wrong. This chapter "
             "summarises the investigation of Assignment 01: the business, its stakeholders, the end-to-end process, the "
             "problems and their causes, and the boundary and objectives of the system. Chapter 2 turns this picture into "
             "requirements and analysis models.")] + req_det
CH1 = after(CH1, "table", "Stakeholders, interests and evidence", [
    ("p", "The stakeholder map groups the same eight stakeholders by their position. The four internal roles work inside "
          "the shop and change its data; the four external parties exchange information with it across the system "
          "boundary. Each box carries the one interest that the system must serve for that stakeholder, so the map "
          "doubles as a checklist for the requirements of Chapter 2: every interest returns as at least one need."),
    fig("STK01", "Stakeholder map: internal and external stakeholders and their interest in the shop", 165)], skip=1)
CH1 = after(CH1, "h2", "1.5. ", [
    ("p", "The BPMN collaboration diagram shows the same process as message exchanges between five participants. The "
          "customer's pool holds what the customer does; the shop's pool is divided into the online system and the "
          "three staff lanes; payment provider, shipping provider and supplier are separate pools, because the shop does "
          "not control their work, only the messages it sends and receives (dashed message flows). The exclusive gateway "
          "<i>Payment verified?</i> is the point where the shop's information either becomes trustworthy or the order is "
          "stopped and the reserved stock is released."),
    figl("BP01", "High-level business process of ABC Online Shop as a BPMN collaboration: customer, shop lanes and partner pools")],
    skip=2)
i = find(CH1, "h2", "1.8. ")
CH1 = CH1[:i] + [
    ("p", "The problem tree is read from top to bottom, from causes to effects. The top row holds the root causes, the "
          "second row the six observable problems of Assignment 01 (BP01-BP06) that they produce. All six lead to one core "
          "problem: order, stock and payment information is fragmented and late. At the bottom are the effects the business "
          "feels: customers lose trust, sales are lost or cancelled, and management decides late. The root causes, not the symptoms, are what "
          "the requirements of Chapter 2 address: a single product source, stock as typed events, verified payment "
          "results, defined order states, carrier milestones with references and reports computed from records."),
    fig("PT01", "Problem tree: root causes, the six business problems, the core problem and its effects", 165)] + CH1[i:]
CH1 += extras.CH1[:extras.CH1.index(("h2", "1.x. Further Use Case Specifications"))]
CH1 += [("h2", "1.x. Chapter Summary"),
        ("p", "The shop's difficulty is not the lack of a website but fragmented and delayed information. Eight stakeholders "
              "were identified and mapped, the order-to-feedback process was modelled as a BPMN collaboration, and six "
              "problems were traced in a problem tree to their root causes. The context diagram fixes the boundary: the "
              "system owns catalogue, orders, stock, payments records, shipments and reports, and exchanges messages with "
              "the payment provider, the shipping provider and suppliers. The objectives give each root cause a measurable "
              "target.")]

# ---------------------------------------------------------------- chapter 2
CH2 = [("h1", "CHAPTER 2. REQUIREMENTS ANALYSIS AND SPECIFICATION"),
       ("p", "This chapter turns the investigation of Chapter 1 into a requirements baseline and analyses it. The first "
             "half states what the system must do: stakeholder needs, functional and non-functional requirements, their "
             "priority, the actors and the use case model with its specifications. The second half analyses how the "
             "requirements behave: activity and data flow diagrams, analysis sequence diagrams with boundary, control and "
             "entity objects, the analysis class model and the order state machine. The analysis models stay "
             "independent of technology; Chapter 4 decides how they are built.")]
CH2 += req_spec
CH2 = after(CH2, "h2", "1.14. ", [
    ("p", "The general use case diagram gives the overview on one page: every actor and the main use case of each "
          "package, with Customer as a specialisation of Visitor and the include relationship between checkout and "
          "payment. The four detailed diagrams that follow give the complete model, package by package."),
    fig("UC00", "General use case diagram: all actors and the main use case of each package", 150)], skip=2)
CH2 += extras.CH1[extras.CH1.index(("h2", "1.x. Further Use Case Specifications")):]
analysis = [b for b in analysis]
j = find(analysis, "table", "Analysis questions")
t = analysis[j]
analysis[j] = (t[0], t[1], t[2], [r for r in t[3] if not r[0].startswith("How is the data stored")], t[4])
analysis = after(analysis, "fig", os.path.join(D, "CL01"), [
    ("p", "Following the lecturer's remark on the first version, the catalogue part of the class model no longer keeps "
          "every attribute of every product kind in one Product class. Product holds what all products share: name, "
          "brand, colour, price, description, image and status. What only one group of products has lives in a detail "
          "class: sizes, upper material, sole and purpose for footwear; sizes, material and fit for apparel; capacity, "
          "material and laptop sleeve for bags; movement, strap, water resistance and battery life for watches. "
          "ProductDetail is abstract, so a product is always described by exactly one concrete kind, and "
          "Category.detailKind says which kind its products use. A new product group means a new detail class and a "
          "new category, not a new column that is empty for all other products.")], skip=1)
CH2 += analysis
CH2 += [b for b in extras.CH2 if True]
CH2 = [b for b in CH2]
k = find(CH2, "h2", "2.x. From Classes to Tables")
k2 = find(CH2, "h2", "2.x. CRUD Matrix")
CH2 = CH2[:k] + CH2[k2:]
CH2 += consistency
CH2 += [("h2", "2.x. Chapter Summary"),
        ("p", "The baseline has 14 stakeholder needs, 24 functional and 12 non-functional requirements, 9 AI "
              "requirements and 32 use cases, shown in a general and four detailed use case diagrams and specified in "
              "full for the use cases that carry the business. The analysis refines them with four activity diagrams, two "
              "DFD levels, two sequence diagrams, the analysis class diagram with the product detail hierarchy and the "
              "order state machine, and the models agree on six cross-checks. Two rules that the design must keep are now "
              "precise: stock and status are explained by events, and every external exchange carries a unique reference.")]

# ---------------------------------------------------------------- chapter 3
CH3 = extras.insert(ch3.BLOCKS, extras.CH3, "3.")

# ---------------------------------------------------------------- chapter 4
c4 = list(ch4.BLOCKS)
c4[0] = ("h1", "CHAPTER 4. SYSTEM DESIGN")
i = find(c4, "h3", "4.2.1. ")
c4 = c4[:i] + [
    ("h3", "4.2.0. Conceptual data model"),
    ("p", "The conceptual model names the things the shop keeps data about and how they are related, without attributes "
          "or keys. It is drawn in Visual Paradigm's ER notation (crow's foot): a bar is one, a circle zero, a foot many. "
          "Nineteen entities appear. Three of them show decisions that are not visible in the class model. ORDER_LINE and "
          "CART_LINE are entities of their own, because a line has a quantity and a price of its own. STAFF is related to "
          "STATUS_CHANGE (0..1 to 0..*), because a status change is made either by a staff member or by the system. And "
          "PRODUCT is related to PRODUCT_DETAIL one to one: every product has exactly one description of its own kind."),
    figl("CDM01", "Conceptual data model: entities and relationships with their multiplicities"),
    ("h3", "4.2.0. Logical data model"),
    ("p", "The logical model gives every entity its attributes and keys, still without a particular database: generic types, "
          "primary keys, foreign keys, optional (N) and unique (U) columns. The names are the names of the relations; the "
          "physical model of Section 4.2.2 turns them into SQL names and types. Three mapping decisions shape it."),
    ("table", "Decisions of the logical model", ["Question", "Decision", "Why"], [
        ["How is the generalization User-Customer stored?", "One relation UserAccount with a role column (single table)",
         "The subclass adds no attribute that needs its own relation; login stays in one place"],
        ["How are the product details stored?", "One relation per detail kind whose key product_id is also the foreign key to Product (class table)",
         "No empty columns; each kind has its own NOT NULL rules; a new kind is a new relation, not an ALTER of Product"],
        ["How does a product know which detail relation to read?", "Category.detail_kind names the kind",
         "The application reads Product joined with Category and then exactly one detail relation"],
        ["Where do order lines get their price?", "OrderItem keeps name and unit_price", "A historical fact that must not change with the catalogue (3NF exception by intent)"]],
     [42, 62, 61]),
    figl("LDM01", "Logical data model: relations with attributes, keys, optional and unique attributes"),
    ("p", "The rule that a product's detail row lives in the relation named by its category (BR-CAT-01) cannot be expressed "
          "by a foreign key alone, because the key product_id is the same in all four detail relations. It is enforced "
          "twice: CatalogService refuses a product whose detail kind differs from its category, and the database has a "
          "trigger on each detail table that rejects such a row. Both are tested.")] + c4[i:]
i = find(c4, "h2", "4.2. ")
c4[i + 1] = ("p", "The data model decides what is stored and how the stored records are linked. It was built in three levels, "
             "each drawn in Visual Paradigm: a conceptual model of entities and relationships, a logical model of relations "
             "with keys, and a physical model of SQLite tables. The SQL script was then generated from the physical model "
             "and a working database was created from it (Section 4.2.3).")
j = find(c4, "h3", "4.2.1. From classes")
c4 = c4[:j + 3] + data_old[2:] + c4[j + 3:]
CH4 = c4

# ---------------------------------------------------------------- chapter 5
CH5 = [("h1", "CHAPTER 5. IMPLEMENTATION AND DEMONSTRATION")] + impl[1:]
CH5 = after(CH5, "fig", os.path.join(R, "web_03_product_ai.png"), [
    ("fig", os.path.join(R, "web_03b_product_bag.png"), "Product page of a bag: the specification table comes from bag_detail, "
     "the detail table named by the category (UC06, BR-CAT-01)", 150, True)], skip=1)
CH5 += impl_summary

# ---------------------------------------------------------------- chapter 6
CH6 = [("h1", "CHAPTER 6. CONCLUSION AND FUTURE WORK"),
       ("h2", "6.1. Summary of Deliverables")] + concl[:1] + [
       ("h2", "6.2. Evaluation Against the Requirements"),
       ("table", "Requirement groups and the evidence that they are met", ["Requirement group", "Status", "Evidence"], [
           ["FR01-FR02 account, login, roles", "Met", "test_web, test_operations (permissions)"],
           ["FR04-FR07 catalogue, search, product details, cart", "Met", "test_ai, test_catalogue, test_web; screenshots 5.x"],
           ["FR08-FR10 checkout, order, payment", "Met", "test_checkout (idempotency, failure, signature), demo output"],
           ["FR11-FR14 history, tracking, cancellation, reviews", "Met", "test_operations"],
           ["FR15-FR17 catalogue, promotions, customers (administration)", "Partly", "Services and tests; no page for categories and customers"],
           ["FR18-FR22 processing, inventory, shipment, replenishment", "Met", "test_operations; staff pages"],
           ["FR23-FR24 reports, promotions", "Met", "test_operations (reports); checkout with WELCOME10"],
           ["NFR05-NFR07, NFR10 security, audit, integrity, privacy", "Met", "Permission checks, audit_log, constraints, build_db.py block [4]"],
           ["NFR09 maintainability (layers)", "Met", "test_architecture; check_code.py"],
           ["NFR01-NFR03, NFR12 performance, availability, load", "Not measured", "Prototype runs as one process on SQLite"],
           ["AI-R1 to AI-R9 search, review insights, recommendation", "Met on the test sets", "evaluate.py: 25/26 search, F1 0.96, coverage 15/15"]],
        [62, 25, 78]),
       ("h2", "6.3. Limitations")] + limits + [
       ("h2", "6.4. Lessons and Next Steps")] + concl[1:3] + [
       ("h2", "6.5. Submitted Files")] + concl[3:]

BLOCKS_RAW = intro + CH1 + CH2 + CH3 + CH4 + CH5 + CH6 + refs


# ---------------------------------------------------------------- renumbering
def renumber(blocks):
    mapping, out, chap, sec, sub = {}, [], 0, 0, 0
    for b in blocks:
        if b[0] == "h1":
            m = re.match(r"CHAPTER (\d+)\.", b[1])
            if m:
                chap, sec = int(m.group(1)), 0
            out.append(b)
            continue
        if b[0] == "h2" and chap:
            m = re.match(r"^(\d+\.(?:\d+|x))\. (.*)$", b[1])
            if m:
                sec, sub = sec + 1, 0
                if "x" not in m.group(1):
                    mapping[m.group(1)] = f"{chap}.{sec}"
                out.append(("h2", f"{chap}.{sec}. {m.group(2)}"))
                continue
        if b[0] == "h3" and chap:
            m = re.match(r"^(\d+\.\d+\.\d+)\. (.*)$", b[1])
            if m:
                sub += 1
                mapping.setdefault(m.group(1), f"{chap}.{sec}.{sub}")
                out.append(("h3", f"{chap}.{sec}.{sub}. {m.group(2)}"))
                continue
        out.append(b)
    return out, mapping


def fix_refs(text, mapping):
    def one(m):
        return re.sub(r"\d+\.\d+(?:\.\d+)?", lambda n: mapping.get(n.group(0), n.group(0)), m.group(0))
    return re.sub(r"Sections? \d+\.\d+(?:\.\d+)?(?:(?:,| and| to| or) \d+\.\d+(?:\.\d+)?)*", one, text)


def apply_refs(blocks, mapping):
    out = []
    for b in blocks:
        if b[0] in ("p", "eq"):
            b = (b[0], fix_refs(b[1], mapping)) + tuple(b[2:])
        elif b[0] == "bullets":
            b = ("bullets", [fix_refs(x, mapping) for x in b[1]])
        elif b[0] == "table":
            b = (b[0], b[1], b[2], [[fix_refs(str(c), mapping) for c in row] for row in b[3]]) + tuple(b[4:])
        out.append(b)
    return out


BLOCKS, MAP = renumber(BLOCKS_RAW)
BLOCKS = apply_refs(BLOCKS, MAP)
FRONT = apply_refs(ch1.FRONT, MAP)
