"""Draw the three data models in Visual Paradigm (Section 4.2): conceptual, logical, physical.

conceptual  CDM01  entities (UPPER CASE) and their relationships, no attributes
logical     LDM01  relations (Title Case) with attributes, keys and nullability, class-table mapping of the
                   product details, generic types
physical    ERD01, ERD02  the SQLite tables of abc_shop/dao/schema.sql with SQL names, types and keys
usage: python data_models.py conceptual|logical|physical
"""
import re
import sys

from vp import call, export

SCHEMA = "../../abc_shop/dao/schema.sql"


def parse(path=SCHEMA):
    """table -> {columns: [...], pk: [...], fks: [(column, parent, parent column)]} from schema.sql."""
    text = open(path, encoding="utf-8").read()
    tables = {}
    for m in re.finditer(r"CREATE TABLE IF NOT EXISTS (\w+) \((.*?)\n\);", text, re.S):
        cols, pk, fks = [], [], []
        for raw in m.group(2).split("\n"):
            line = raw.strip().rstrip(",")
            if not line or line.startswith(("--", "UNIQUE", "CHECK")):
                continue
            if line.startswith("PRIMARY KEY"):
                pk += [c.strip() for c in re.search(r"\((.*)\)", line).group(1).split(",")]
                continue
            name, typ = line.split()[:2]
            up = line.upper()
            col = {"name": name, "sqltype": typ, "notnull": "NOT NULL" in up or "PRIMARY KEY" in up,
                   "unique": " UNIQUE" in up, "pk": "PRIMARY KEY" in up}
            ref = re.search(r"REFERENCES (\w+)\((\w+)\)", line)
            if ref:
                fks.append((name, ref.group(1), ref.group(2)))
            if col["pk"]:
                pk.append(name)
            cols.append(col)
        for c in cols:
            c["pk"] = c["name"] in pk
        tables[m.group(1)] = {"columns": cols, "pk": pk, "fks": fks}
    return tables


def sql_type(table, col):
    n, t = col["name"], col["sqltype"]
    if t == "INTEGER":
        return "integer"
    if t == "REAL":
        return "decimal(10,2)"
    if n.endswith("_at") or n == "at":
        return "timestamp"
    if n in ("start_date", "end_date"):
        return "date"
    if n.endswith("_id") or n in ("code", "attempt_ref", "provider_ref", "carrier_ref", "reference",
                                  "idempotency_key", "promo_code", "kind", "status", "role", "currency",
                                  "detail_kind", "movement"):
        return "varchar(40)"
    if n in ("description", "text", "detail", "address", "note"):
        return "varchar(1000)"
    return "varchar(200)"


def logical_type(table, col):
    """Logical model: the domain of the attribute, without SQL sizes."""
    t = sql_type(table, col)
    return {"integer": "integer", "decimal(10,2)": "decimal", "timestamp": "timestamp", "date": "date"}.get(t, "varchar")


def build_tables(d, names, tables, typer, rename=lambda t: t, done=None):
    done = set() if done is None else done
    for t in names:
        call("addTable", quiet=True, diagramName=d, tableName=rename(t))
        if rename(t) in done:
            continue
        done.add(rename(t))
        for c in tables[t]["columns"]:
            call("addColumn", quiet=True, diagramName=d, tableName=rename(t), columnName=c["name"],
                 columnType=typer(t, c), length=0, scale=0, isPrimaryKey=c["pk"],
                 isNullable=not c["notnull"], isUnique=c["unique"])
    for t in names:
        for col, parent, pcol in tables[t]["fks"]:
            if parent in names:
                call("addForeignKey", diagramName=d, fromTable=rename(t), toTable=rename(parent),
                     fromColumn=col, toColumn=pcol, relationshipName=f"fk_{rename(t)}_{col}")
    return done


DETAILS = ["footwear_detail", "apparel_detail", "bag_detail", "watch_detail"]


def physical():
    """ERD02 gets category.detail_kind and the four detail tables (ERD01 is unchanged)."""
    tables = parse()
    d = "ERD02 Physical Data Model - Catalogue, Stock and Reviews"
    col = next(c for c in tables["category"]["columns"] if c["name"] == "detail_kind")
    call("addColumn", diagramName=d, tableName="category", columnName="detail_kind",
         columnType=sql_type("category", col), length=0, scale=0, isPrimaryKey=False, isNullable=False, isUnique=False)
    for t in DETAILS:
        call("addTable", quiet=True, diagramName=d, tableName=t)
        for c in tables[t]["columns"]:
            call("addColumn", quiet=True, diagramName=d, tableName=t, columnName=c["name"],
                 columnType=sql_type(t, c), length=0, scale=0, isPrimaryKey=c["pk"],
                 isNullable=not c["notnull"], isUnique=c["unique"])
        call("addForeignKey", diagramName=d, fromTable=t, toTable="product", fromColumn="product_id",
             toColumn="product_id", relationshipName=f"fk_{t}_product_id")
    export(d)


LOGICAL = {"users": "UserAccount", "address": "Address", "cart": "Cart", "cart_item": "CartItem",
           "customer_order": "CustomerOrder", "order_item": "OrderItem", "order_status_history": "StatusChange",
           "payment": "Payment", "shipment": "Shipment", "shipment_milestone": "Milestone", "promotion": "Promotion",
           "review": "Review", "category": "Category", "product": "Product", "footwear_detail": "FootwearDetail",
           "apparel_detail": "ApparelDetail", "bag_detail": "BagDetail", "watch_detail": "WatchDetail",
           "stock_level": "StockLevel", "inventory_event": "InventoryEvent", "replenishment_request": "Replenishment"}


def logical():
    tables = parse()
    d = "LDM01 Logical Data Model"
    call("createErd", diagramName=d)
    build_tables(d, list(LOGICAL), tables, logical_type, rename=lambda t: LOGICAL[t])
    export(d)


# conceptual entity -> (parent entity, parent multiplicity, child multiplicity); the verbs are in CDM_VERBS
CONCEPTUAL = [
    ("CUSTOMER", "ADDRESS", "1", "0..1"), ("CUSTOMER", "CART", "1", "0..1"), ("CUSTOMER", "ORDER", "1", "0..*"),
    ("CUSTOMER", "REVIEW", "1", "0..*"), ("CART", "CART_LINE", "1", "0..*"), ("ORDER", "ORDER_LINE", "1", "1..*"),
    ("ORDER", "STATUS_CHANGE", "1", "1..*"), ("ORDER", "PAYMENT", "1", "0..*"), ("ORDER", "SHIPMENT", "1", "0..1"),
    ("SHIPMENT", "MILESTONE", "1", "0..*"), ("PROMOTION", "ORDER", "0..1", "0..*"), ("ORDER", "REVIEW", "1", "0..*"),
    ("CATEGORY", "PRODUCT", "1", "0..*"), ("PRODUCT", "PRODUCT_DETAIL", "1", "1"), ("PRODUCT", "CART_LINE", "1", "0..*"),
    ("PRODUCT", "ORDER_LINE", "1", "0..*"), ("PRODUCT", "STOCK_LEVEL", "1", "1"), ("STOCK_LEVEL", "INVENTORY_EVENT", "1", "0..*"),
    ("PRODUCT", "REPLENISHMENT", "1", "0..*"), ("PRODUCT", "REVIEW", "1", "0..*"), ("STAFF", "STATUS_CHANGE", "0..1", "0..*"),
]
ENTITIES = ["CUSTOMER", "STAFF", "ADDRESS", "CART", "CART_LINE", "ORDER", "ORDER_LINE", "STATUS_CHANGE", "PAYMENT",
            "SHIPMENT", "MILESTONE", "PROMOTION", "REVIEW", "CATEGORY", "PRODUCT", "PRODUCT_DETAIL", "STOCK_LEVEL",
            "INVENTORY_EVENT", "REPLENISHMENT"]


def conceptual():
    d = "CDM01 Conceptual Data Model"
    call("createErd", diagramName=d)
    for e in ENTITIES:
        call("addTable", quiet=True, diagramName=d, tableName=e)
    for parent, child, pm, cm in CONCEPTUAL:
        call("addTableRelationship", diagramName=d, fromTable=parent, toTable=child, type="nonIdentifying",
             fromMultiplicity=pm, toMultiplicity=cm)
    export(d)


if __name__ == "__main__":
    {"physical": physical, "logical": logical, "conceptual": conceptual}[sys.argv[1]]()
