"""Client for the Visual Paradigm MCP plugin (plain HTTP endpoint of the plugin, port 2026).

Every drawing script of tools/vp calls Visual Paradigm through call(); the plugin draws inside the
running Visual Paradigm (Enterprise) with its layered, orthogonal layout.
"""
import json
import os
import re
import urllib.request

URL = "http://localhost:2026/api/execute"
HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "png") + os.sep
_schemas = None


def schemas():
    global _schemas
    if _schemas is None:
        with open(os.path.join(HERE, "tools.json"), encoding="utf-8") as f:
            _schemas = {t["name"]: t for t in json.load(f)["result"]["tools"]}
    return _schemas


_order = None


def order():
    """Parameter names in order, from the plugin's tool reference (the build exposes them as arg0..argN)."""
    global _order
    if _order is None:
        _order = {}
        with open(os.path.join(HERE, "tool_reference.md"), encoding="utf-8") as f:
            for line in f:
                m = re.match(r"\|\s*`(\w+)`\s*\|\s*([^|]*)\|", line)
                if m:
                    _order[m.group(1)] = [p.strip().split(":")[0] for p in m.group(2).split(",")
                                          if p.strip() and p.strip() != "(none)"]
    return _order


def call(tool, quiet=False, **args):
    """Call a tool by parameter NAME; parameters left out are filled with "", 0 or false."""
    props = schemas()[tool].get("inputSchema", {}).get("properties", {})
    if props and all(re.fullmatch(r"arg\d+", k) for k in props):
        names = order()[tool]
        args = {f"arg{names.index(k)}": v for k, v in args.items() if k in names} |                {k: v for k, v in args.items() if k not in names and "?" in k}
        unknown = {k for k in args if k not in props}
    else:
        unknown = set(args) - set(props)
    if unknown or (props and len(args) != len({k for k in args if k in props})):
        raise ValueError(f"{tool}: unknown parameters {unknown}")
    full = {}
    for name, p in props.items():
        t = p.get("type")
        full[name] = args.get(name, 0 if t in ("integer", "number") else (False if t == "boolean" else ""))
    body = json.dumps({"toolName": tool, "arguments": full}).encode("utf-8")
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        res = json.loads(r.read().decode("utf-8"))
    out = str(res.get("result", res.get("error")))
    bad = "error" in res or out.startswith("Error") or "not found" in out or out.startswith("Unknown")
    if bad or not quiet:
        print(("!! " if bad else "") + f"{tool}: {out[:240]}")
    return out


BLUE = "#7ACFF5"


def classes(d):
    return [c["name"] for c in json.loads(call("getRelationshipDetails", quiet=True, diagramName=d))["classes"]]


def colour(d, names=None, colour=BLUE):
    for c in names or classes(d):
        call("setClassColor", quiet=True, diagramName=d, className=c, backgroundColor=colour)


def place(d, pos, labels=True):
    """Pin shapes at (x, y) and route the lines around them."""
    for name, (x, y) in pos.items():
        call("setElementBounds", quiet=True, diagramName=d, elementName=name, x=x, y=y, width=0, height=0)
    call("rerouteConnectors", diagramName=d)
    if labels:
        call("layoutConnectorLabels", diagramName=d)


def export(d):
    os.makedirs(PNG, exist_ok=True)
    return call("exportDiagramImage", diagramName=d, filePath=PNG + d + ".png")
