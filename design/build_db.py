"""Build the database from the DDL generated from the data model (Chapter 4) and check it.

Chain: data model classes DM01 + DM02 (<<ORM Persistable>>) --syncClassesToErd--> ERD01 --generateSql-->
design/create_tables.sql. This script
  [1] runs create_tables.sql on an empty SQLite file,
  [2] compares its tables, columns, primary keys and foreign keys with abc_shop/dao/schema.sql and lists what
      the application schema adds by hand (NOT NULL, CHECK, UNIQUE, DEFAULT, triggers, technical tables),
  [3] lets the real application seed one month of shop history into the generated database,
  [4] tries statements that break a rule: the generated database rejects those guarded by a key; the rules
      written as CHECK, UNIQUE or trigger are rejected by the application schema only.
usage: python design/build_db.py
"""
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(os.path.dirname(HERE), "abc_shop")
SCRIPT = os.path.join(HERE, "create_tables.sql")
APP_SCHEMA = os.path.join(APP, "dao", "schema.sql")
DB = os.path.join(HERE, "abc_design.db")
TECHNICAL = ("sequence", "audit_log")
sys.path.insert(0, APP)


def shape(conn):
    """table -> (columns, primary key, foreign keys)"""
    out = {}
    for (t,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
        info = conn.execute(f'PRAGMA table_info("{t}")').fetchall()
        out[t] = (sorted(r[1] for r in info), sorted((r[5], r[1]) for r in info if r[5]),
                  sorted((r[3], r[2], r[4]) for r in conn.execute(f'PRAGMA foreign_key_list("{t}")')))
    return out


def added_by_hand(conn, t):
    sql = conn.execute("SELECT sql FROM sqlite_master WHERE name = ?", (t,)).fetchone()[0].upper()
    info = conn.execute(f'PRAGMA table_info("{t}")').fetchall()
    return {"NOT NULL": sum(1 for r in info if r[3] and not r[5]), "CHECK": sql.count("CHECK"),
            "UNIQUE": sql.count("UNIQUE"), "DEFAULT": sql.count("DEFAULT"), "CASCADE": sql.count("CASCADE")}


def attempt(conn, label, sql):
    try:
        conn.execute(sql)
    except sqlite3.IntegrityError as e:
        print(f"    rejected  {label:<52} {str(e)[:52]}")
        return True
    print(f"    accepted  {label}")
    return False


def main():
    print("> python design/build_db.py\n")
    if os.path.exists(DB):
        os.remove(DB)
    script = open(SCRIPT, encoding="utf-8").read()
    gen = sqlite3.connect(DB)
    gen.executescript(script)
    g = shape(gen)
    fks = sum(len(v[2]) for v in g.values())
    print(f"[1] create_tables.sql (generateSql, SQLite, from ERD01) executed: {len(g)} tables, {fks} foreign keys")
    names = sorted(g)
    for i in range(0, len(names), 8):
        print("    " + ", ".join(names[i:i + 8]))

    ref = sqlite3.connect(":memory:")
    ref.executescript(open(APP_SCHEMA, encoding="utf-8").read())
    r = shape(ref)
    same = [t for t in g if t in r and g[t] == r[t]]
    print(f"\n[2] Compared with abc_shop/dao/schema.sql: {len(same)} of {len(g)} generated tables have the same "
          "columns, primary key and foreign keys")
    for t in g:
        if t not in r or g[t] != r[t]:
            print(f"    differs: {t}")
    totals = {}
    for t in g:
        for k, v in added_by_hand(ref, t).items():
            totals[k] = totals.get(k, 0) + v
    print("    added by hand in schema.sql: " + ", ".join(f"{v} {k}" for k, v in totals.items()))
    triggers = [x[0] for x in ref.execute("SELECT name FROM sqlite_master WHERE type='trigger' ORDER BY name")]
    print(f"    {len(triggers)} triggers of BR-CAT-01 ({', '.join(triggers)}); technical tables "
          f"{', '.join(t for t in r if t not in g)} (not domain classes)")
    gen.close()

    # [3] the application on the generated database: the generated DDL plus the two technical tables
    tech = "\n".join(re.search(rf"CREATE TABLE IF NOT EXISTS {t} \(.*?\);", open(APP_SCHEMA, encoding="utf-8").read(),
                               re.S).group(0) for t in TECHNICAL)
    combined = os.path.join(HERE, "generated_plus_technical.sql")
    with open(combined, "w", encoding="utf-8") as f:
        f.write("PRAGMA foreign_keys = ON;\n" + script.replace("CREATE TABLE ", "CREATE TABLE IF NOT EXISTS ") + "\n" + tech)
    import dao.database as database
    import seed
    database.SCHEMA = combined
    shop = seed.seed(DB, verbose=False)
    shop.db.close()
    os.remove(combined)
    conn = sqlite3.connect(DB)
    counts = {t: conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in names}
    print("\n[3] The application seeded one month of history into the generated database:")
    print("    " + ", ".join(f"{t}={counts[t]}" for t in ("User", "Customer", "Product", "Footwear", "Apparel", "Bag",
                                                               "Watch", "Orders")))
    print("    " + ", ".join(f"{t}={counts[t]}" for t in ("OrderItem", "StatusChange", "Payment", "Shipment",
                                                               "Milestone", "InventoryEvent", "Review")))
    row = conn.execute("""SELECT p.product_id, p.name, c.detail_kind, b.capacity_l FROM Product p
                          JOIN Category c ON c.category_id = p.category_id JOIN Bag b ON b.product_id = p.product_id
                          ORDER BY p.product_id LIMIT 1""").fetchone()
    print(f"    a bag: {row[0]} {row[1]} (category kind {row[2]}), its own row in Bag: capacity {row[3]} l")

    print("\n[4] Statements that break a rule")
    conn.execute("PRAGMA foreign_keys = ON")
    keyed = [
        ("order line for a product that does not exist", "INSERT INTO OrderItem VALUES ('x', 1.0, 1, 'O001', 'P999')"),
        ("Bag row for a product that does not exist", "INSERT INTO Bag VALUES (10, 'canvas', 0, 'P999')"),
        ("second stock level for the same product",
         "INSERT INTO StockLevel SELECT 1, 0, 3, product_id FROM StockLevel LIMIT 1"),
        ("same product twice in one cart",
         "INSERT INTO CartItem SELECT name, cart_price, 1, cart_id, product_id FROM CartItem LIMIT 1"),
        ("review of an order that does not exist",
         "INSERT INTO Review VALUES ('R-X', 5, 'x', 'published', '2026-11-01', 'P01', 'C001', 'O999')"),
    ]
    print("    generated database (keys from the ERD):")
    k = sum(attempt(conn, label, sql) for label, sql in keyed)
    conn.close()
    app = sqlite3.connect(":memory:")
    app.executescript(open(APP_SCHEMA, encoding="utf-8").read())
    app.executescript("""INSERT INTO Category VALUES ('bags', 'Bags', 'bag');
        INSERT INTO Product VALUES ('P1', 'Tote', 'Lumi', 'black', 80, '', '', 'active', 'bags');
        INSERT INTO User VALUES ('C1', 'An', 'an@x', 'h', 'customer', '2026-11-01');
        INSERT INTO Customer VALUES ('C1');
        INSERT INTO StockLevel VALUES (5, 0, 3, 'P1');
        INSERT INTO Orders VALUES ('O1', 'addr', 0, 0, 80, 'Paid', '2026-11-01', 'K1', 'C1', NULL);""")
    by_hand = [
        ("review rating 6 (CHECK)",
         "INSERT INTO Review VALUES ('R1', 6, 'x', 'published', '2026-11-01', 'P1', 'C1', 'O1')"),
        ("more reserved than physical stock (CHECK)", "UPDATE StockLevel SET reserved = 6"),
        ("user with an unknown role (CHECK)", "INSERT INTO User VALUES ('U2', 'X', 'x@x', 'h', 'guest', '2026-11-01')"),
        ("repeated idempotency key, double submit (UNIQUE)",
         "INSERT INTO Orders VALUES ('O2', 'addr', 0, 0, 80, 'Paid', '2026-11-01', 'K1', 'C1', NULL)"),
        ("Watch row for a product of a bag category (trigger)",
         "INSERT INTO Watch VALUES ('smart', 'silicone', 30, 5, 'P1')"),
    ]
    print("    application schema (rules added by hand in schema.sql):")
    h = sum(attempt(app, label, sql) for label, sql in by_hand)
    print(f"    {k} of {len(keyed)} rejected by the generated database, {h} of {len(by_hand)} by the application schema")


if __name__ == "__main__":
    main()
