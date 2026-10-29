"""Build the database from the SQL script generated from the ER model (Section 4.2.3).

1. create_tables.sql (generated from ERD01/ERD02 of TieuLuan_KHANHBQ.vpp) runs on an empty SQLite file.
2. Its structure is compared with abc_shop/dao/schema.sql, the schema the application ships with.
3. The real application seeds one month of shop history into the generated database.
4. Statements that break a business rule must be rejected by the database itself.
usage: python build_db.py
"""
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(os.path.dirname(HERE), "abc_shop")
SCRIPT = os.path.join(HERE, "create_tables.sql")
DB = os.path.join(HERE, "abc_design.db")
sys.path.insert(0, APP)


def structure(conn):
    """table -> (columns {name: (notnull, pk)}, foreign keys, unique column sets, has CHECK)"""
    out = {}
    for (name, sql) in conn.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
        cols = {r[1]: (bool(r[3]) or r[5] > 0, r[5] > 0) for r in conn.execute(f"PRAGMA table_info({name})")}
        fks = sorted((r[3], r[2], r[4]) for r in conn.execute(f"PRAGMA foreign_key_list({name})"))
        uniq = sorted(tuple(r2[2] for r2 in conn.execute(f"PRAGMA index_info({r[1]})"))
                      for r in conn.execute(f"PRAGMA index_list({name})") if r[2] and r[3] == "u")
        out[name] = (cols, fks, uniq, "CHECK" in sql.upper())
    return out


def compare(gen, ref):
    same, notes = 0, []
    for t in sorted(ref):
        if t not in gen:
            notes.append(f"{t}: missing in the generated script")
            continue
        (gc, gf, gu, gk), (rc, rf, ru, rk) = gen[t], ref[t]
        diff = []
        if gc != rc:
            diff.append("columns/NOT NULL/PK")
        if gf != rf:
            diff.append("foreign keys")
        if gu != ru:
            extra = [u for u in ru if u not in gu]
            diff.append("UNIQUE " + ", ".join("(" + ", ".join(u) + ")" for u in extra))
        if gk != rk:
            diff.append("CHECK")
        if diff:
            notes.append(f"{t}: differs in " + "; ".join(diff))
        else:
            same += 1
    return same, notes


def must_fail(conn, label, sql, params=()):
    try:
        conn.execute(sql, params)
    except sqlite3.IntegrityError as e:
        print(f"  rejected: {label:<44} -> {str(e)[:60]}")
        return 1
    print(f"  ACCEPTED (unexpected): {label}")
    return 0


def main():
    print("> python build_db.py\n")
    if os.path.exists(DB):
        os.remove(DB)
    script = open(SCRIPT, encoding="utf-8").read()
    conn = sqlite3.connect(DB)
    conn.executescript(script)
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    fks = sum(len(conn.execute(f"PRAGMA foreign_key_list({t})").fetchall()) for t in tables)
    print(f"[1] create_tables.sql (generated from ERD01 + ERD02) executed: {len(tables)} tables, {fks} foreign keys")
    for i in range(0, len(tables), 6):
        print("    " + ", ".join(tables[i:i + 6]))
    conn.close()

    ref = sqlite3.connect(":memory:")
    ref.executescript(open(os.path.join(APP, "dao", "schema.sql"), encoding="utf-8").read())
    gen = sqlite3.connect(DB)
    same, notes = compare(structure(gen), structure(ref))
    print(f"\n[2] Compared with abc_shop/dao/schema.sql: {same} of {len(structure(ref))} tables identical "
          "(columns, NOT NULL, keys, foreign keys, UNIQUE, CHECK)")
    for n in notes:
        print("    " + n)
    gen.close()

    import dao.database as database
    import seed
    database.SCHEMA = SCRIPT                         # the application now builds on the generated script
    shop = seed.seed(DB, verbose=False)
    conn = sqlite3.connect(DB)
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}
    print("\n[3] The application seeded one month of history into the generated database:")
    line = []
    for t in ("users", "product", "customer_order", "order_item", "payment", "shipment", "inventory_event", "review"):
        line.append(f"{t}={counts[t]}")
    print("    " + ", ".join(line[:4]) + ",\n    " + ", ".join(line[4:]))
    row = conn.execute("""SELECT o.order_id, u.name, COUNT(i.product_id), o.total, p.status, s.status
                          FROM customer_order o JOIN users u ON u.user_id = o.customer_id
                          JOIN order_item i ON i.order_id = o.order_id
                          LEFT JOIN payment p ON p.order_id = o.order_id AND p.status = 'Succeeded'
                          LEFT JOIN shipment s ON s.order_id = o.order_id
                          GROUP BY o.order_id ORDER BY o.order_id LIMIT 1""").fetchone()
    print(f"    first order: {row[0]} of {row[1]}, {row[2]} line(s), total {row[3]:.2f}, payment {row[4]}, shipment {row[5]}")
    shop.db.close()

    print("\n[4] Rules the database enforces by itself:")
    conn.execute("PRAGMA foreign_keys = ON")
    ok = 0
    ok += must_fail(conn, "order line for a product that does not exist",
                    "INSERT INTO order_item VALUES ('O001', 'P999', 'x', 1.0, 1)")
    ok += must_fail(conn, "second cart for the same customer",
                    "INSERT INTO cart SELECT 'CART-X', customer_id FROM cart LIMIT 1")
    ok += must_fail(conn, "more reserved than physical stock",
                    "UPDATE stock_level SET reserved = physical + 1 WHERE product_id = (SELECT MIN(product_id) FROM stock_level)")
    ok += must_fail(conn, "review rating 6",
                    "UPDATE review SET rating = 6 WHERE review_id = (SELECT MIN(review_id) FROM review)")
    ok += must_fail(conn, "repeated idempotency key (double submit)",
                    "INSERT INTO customer_order SELECT 'O-X', customer_id, address, 0, 0, total, status, created_at, '', "
                    "idempotency_key FROM customer_order WHERE idempotency_key IS NOT NULL LIMIT 1")
    ok += must_fail(conn, "user with an unknown role",
                    "INSERT INTO users VALUES ('U-X', 'X', 'x@x', 'h', 'guest', '2026-10-01')")
    print(f"    {ok} of 6 rejected")
    conn.close()


if __name__ == "__main__":
    main()
