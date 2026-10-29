"""Generate Python code from the layered design model in Visual Paradigm (Section 4.5).

The model is read from TieuLuan_KHANHBQ.vpp through the Visual Paradigm MCP plugin (Visual Paradigm
must be running with the project open) and stored in model_export.json; without --live the stored
export is used, so the code can be regenerated without Visual Paradigm.
Mapping rules (Table 4.x): package -> folder, model sub-package -> module, class -> class (a model
class becomes a dataclass), <<interface>> -> ABC, generalization -> base class, attribute -> field,
navigable association end -> field named after the role (role ending in _id/_code: the key of the
other object), composition -> list field, operation -> method that raises NotImplementedError,
<<use>> -> import of the supplier for type checking.
usage: python generate_code.py [--live]
"""
import json
import os
import re
import shutil
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.join(HERE, "model_export.json")
OUT = os.path.join(HERE, "generated", "abc_shop_design")
DIAGRAMS = ["DCL01 Design Classes - Customers, Carts and Orders", "DCL02 Design Classes - Payment, Shipment and Review",
            "DCL03 Design Classes - Catalogue and Inventory", "DCL04 Layer Slice - Add a Product to the Cart"]
PACKAGES = "PKG01 Layers, Packages and Classes"
LAYERS = ["view", "controller", "service", "ai", "dao", "model"]


def vp(tool, **args):
    body = json.dumps({"toolName": tool, "arguments": args}).encode("utf-8")
    req = urllib.request.Request("http://localhost:2026/api/execute", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))["result"]


def export():
    """Read classes, members, relationships and package owners from the open VP project."""
    classes, rels = {}, []
    for d in DIAGRAMS:
        data = json.loads(vp("getRelationshipDetails", diagramName=d))
        for c in data["classes"]:
            old = classes.get(c["name"])
            size = len(c["attributes"]) + len(c["operations"])
            if old is None or size > len(old["attributes"]) + len(old["operations"]):
                classes[c["name"]] = {k: c[k] for k in ("name", "owner", "abstract", "stereotypes", "attributes", "operations")}
        for r in data["relationships"]:
            r = {k: r.get(k) for k in ("type", "from", "to", "name", "fromEnd", "toEnd")}
            if r not in rels:
                rels.append(r)
    model = {"source": "TieuLuan_KHANHBQ.vpp", "diagrams": DIAGRAMS + [PACKAGES], "classes": classes, "relationships": rels}
    with open(EXPORT, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=1)
    return model


def snake(name):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).lower().replace("d_a_o", "dao")


def location(c):
    """(layer, module) of a class: model sub-packages become modules of model."""
    owner = c["owner"]
    if owner not in LAYERS:
        return "model", owner
    if owner == "dao" and "interface" in c["stereotypes"]:
        return "dao", "interfaces"
    if "module" in c["stereotypes"]:
        return owner, c["name"]
    return owner, snake(c["name"])


def generate(model):
    classes, rels = model["classes"], model["relationships"]
    fields, bases, uses = {}, {}, {}
    for r in rels:
        if r["type"] == "Generalization":                 # VP reports from = parent, to = child
            bases[r["to"]] = r["from"]
        elif r["type"] in ("Usage", "Dependency"):
            uses.setdefault(r["from"], set()).add(r["to"])
        elif r["type"] == "Association":
            end, other = r["toEnd"], r["to"]
            role, mult, kind = end["role"], end["multiplicity"], r["fromEnd"]["aggregation"]
            if not role:
                continue
            if role.endswith("_id") or role.endswith("_code"):
                fields.setdefault(r["from"], []).append((role, "str", '""', f"key of {other} [{mult}]"))
            elif mult.endswith("*"):
                what = "composition" if kind == "composite" else "association"
                fields.setdefault(r["from"], []).append((role, f"list[{other}]", "field(default_factory=list)", f"{what} {mult}"))
            else:
                fields.setdefault(r["from"], []).append((role, f"Optional[{other}]", "None", f"association {mult}"))
    modules = {}
    for c in classes.values():
        if c["owner"] is None or not (c["attributes"] or c["operations"] or c["name"] in fields):
            if location(c)[0] != "model":
                continue                                    # name-only box of the package diagram
        modules.setdefault(location(c), []).append(c)
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    written = []
    for (layer, module), members in sorted(modules.items()):
        path = os.path.join(OUT, layer, module + ".py")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        for d in (OUT, os.path.dirname(path)):
            open(os.path.join(d, "__init__.py"), "a").close()
        members.sort(key=lambda c: (c["name"] in bases, c["name"]))
        with open(path, "w", encoding="utf-8") as f:
            f.write(module_source(layer, module, members, classes, fields, bases, uses))
        written.append((layer, module, [c["name"] for c in members]))
    return written


def module_source(layer, module, members, classes, fields, bases, uses):
    here = {c["name"] for c in members}
    lines = [f'"""{layer}.{module} - generated from the Visual Paradigm design model; do not edit by hand."""',
             "from __future__ import annotations", ""]
    needs = set()
    for c in members:
        text = " ".join(a["type"] or "" for a in c["attributes"]) + " " + " ".join(
            " ".join(o["params"]) + " " + (o["returnType"] or "") for o in c["operations"])
        text += " " + " ".join(t for _, t, _, _ in fields.get(c["name"], []))
        needs |= {w for w in re.findall(r"[A-Z]\w+", text) if w in classes and w not in here and w != "Optional"}
        needs |= {u for u in uses.get(c["name"], ()) if u not in here}
    model_like = layer == "model"
    std = []
    if model_like:
        std.append("from dataclasses import dataclass, field")
    if any("interface" in c["stereotypes"] for c in members):
        std.append("from abc import ABC, abstractmethod")
    if any(t.startswith("Optional") for c in members for _, t, _, _ in fields.get(c["name"], [])):
        std.append("from typing import TYPE_CHECKING, Optional")
    else:
        std.append("from typing import TYPE_CHECKING")
    lines += std
    imports = sorted(needs | ({bases[c["name"]] for c in members if c["name"] in bases} - here))
    base_imports = sorted({bases[c["name"]] for c in members if c["name"] in bases} - here)
    for b in base_imports:
        lay, mod = location(classes[b])
        lines.append(f"from {lay}.{mod} import {b}")
    typed = [n for n in imports if n not in base_imports]
    if typed:
        lines += ["", "if TYPE_CHECKING:                       # <<use>> and the types in the signatures"]
        for n in typed:
            lay, mod = location(classes[n])
            lines.append(f"    from {lay}.{mod} import {n}")
    for c in members:
        lines += ["", ""]
        if "module" in c["stereotypes"]:                  # a <<module>> holds functions
            for o in c["operations"]:
                lines += [f"def {o['name']}({', '.join(o['params'])}) -> {o['returnType'] or 'None'}:",
                          "    raise NotImplementedError", "", ""]
            lines = lines[:-2]
            continue
        interface = "interface" in c["stereotypes"]
        parent = bases.get(c["name"], "ABC" if interface else "")
        if model_like:
            lines.append("@dataclass")
        lines.append(f"class {c['name']}({parent}):" if parent else f"class {c['name']}:")
        body = []
        if model_like:
            for a in c["attributes"]:
                body.append(f"    {a['name']}: {a['type']} = {default(a['type'])}")
            for n, t, d, note in fields.get(c["name"], []):
                body.append(f"    {n}: {t} = {d}    # {note}")
            if body and c["operations"]:
                body.append("")
        elif c["attributes"]:
            args = ", ".join(f"{a['name']}: {a['type']}" for a in c["attributes"])
            body.append(f"    def __init__(self, {args}):")
            body += [f"        self.{a['name']} = {a['name']}" for a in c["attributes"]]
            body.append("")
        for o in c["operations"]:
            if interface:
                body.append("    @abstractmethod")
            params = ", ".join(["self"] + o["params"])
            body.append(f"    def {o['name']}({params}) -> {o['returnType'] or 'None'}:")
            body.append("        ..." if interface else "        raise NotImplementedError")
            body.append("")
        while body and body[-1] == "":
            body.pop()
        lines += body or ["    pass"]
    return "\n".join(lines).rstrip() + "\n"


def default(t):
    return {"str": '""', "int": "0", "float": "0.0", "bool": "False"}.get(t, "None")


def main():
    model = export() if "--live" in sys.argv else json.load(open(EXPORT, encoding="utf-8"))
    written = generate(model)
    n = sum(len(c) for _, _, c in written)
    print(f"generated {n} classes in {len(written)} modules under {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
