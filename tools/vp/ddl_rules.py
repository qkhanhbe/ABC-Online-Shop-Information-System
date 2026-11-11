"""CHECK and DEFAULT rules of abc_shop/dao/schema.sql as table|column|check|default lines.

The essay.gen plugin stores them in the column specifications of the ER model (mode ddl) before it writes the
SQL script, so the rules are part of the Visual Paradigm model and not only of the script.
"""
import re
import sys

text = open("../../abc_shop/dao/schema.sql", encoding="utf-8").read()
rows = []
for m in re.finditer(r"CREATE TABLE IF NOT EXISTS (\w+) \((.*?)\n\);", text, re.S):
    table = m.group(1)
    for raw in m.group(2).split("\n"):
        line = raw.strip().rstrip(",")
        if not line or line.split()[0] in ("PRIMARY", "UNIQUE", "CHECK", "--"):
            continue
        col, check = line.split()[0], ""
        i = line.find("CHECK (")
        if i >= 0:
            depth = 0
            for k in range(i + 6, len(line)):
                depth += line[k] == "("
                depth -= line[k] == ")"
                if depth == 0:
                    check = line[i + 7:k]
                    break
        default = re.search(r"DEFAULT ('[^']*'|\S+)", line)
        if table == "stock_level" and col == "reserved":
            check = "reserved >= 0 AND reserved <= physical"     # the table-level CHECK, written on its column
        if check or default:
            rows.append(f"{table}|{col}|{check}|{default.group(1) if default else ''}")
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(rows) + "\n")
print(len(rows), "rules")
