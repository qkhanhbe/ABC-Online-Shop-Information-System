"""Draw the DFD-type diagrams (CTX01, DFD0, DFD1) from the layout stored in the VP project.

Visual Paradigm Community Edition cannot open or export Data Flow Diagrams, so the shapes and
routed flows are dumped from the project (plugin mode "dumpdfd") and drawn here as SVG in the
same notation and colours, then rendered to PNG with headless Edge.
usage: python render_dfd.py DUMP.jsonl OUT_DIR
"""
import html
import json
import os
import subprocess
import sys
from collections import defaultdict

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FONT = "font-family:Arial,Helvetica,sans-serif"


def esc(s):
    return html.escape(s)


def wrap(text, width_px, size):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) * size * 0.55 > width_px and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def shape_svg(s):
    x, y, w, h = s["b"]
    name, kind = s["name"], s["k"]
    out = []
    if kind == "DFExternalEntity":
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFF2CC" stroke="#2F5597" stroke-width="1.2"/>')
        for i, line in enumerate(wrap(name, w - 10, 12)):
            out.append(f'<text x="{x + w / 2}" y="{y + 17 + i * 14}" text-anchor="middle" style="{FONT};font-size:12px;font-weight:bold">{esc(line)}</text>')
    elif kind == "DFProcess":
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="#DCF0FC" stroke="#2F5597" stroke-width="1.2"/>')
        out.append(f'<line x1="{x}" y1="{y + 18}" x2="{x + w}" y2="{y + 18}" stroke="#2F5597"/>')
        out.append(f'<line x1="{x + 34}" y1="{y}" x2="{x + 34}" y2="{y + 18}" stroke="#2F5597"/>')
        out.append(f'<line x1="{x}" y1="{y + h - 14}" x2="{x + w}" y2="{y + h - 14}" stroke="#2F5597"/>')
        out.append(f'<text x="{x + 6}" y="{y + 13}" style="{FONT};font-size:10px;font-weight:bold">{esc(s["id"])}</text>')
        lines = wrap(name, w - 12, 12)
        top = y + 18 + (h - 32 - len(lines) * 14) / 2 + 12
        for i, line in enumerate(lines):
            out.append(f'<text x="{x + w / 2}" y="{top + i * 14}" text-anchor="middle" style="{FONT};font-size:12px;font-weight:bold">{esc(line)}</text>')
    elif kind == "DFDataStore":
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#E2F0D9" stroke="none"/>')
        out.append(f'<rect x="{x}" y="{y}" width="30" height="{h}" fill="#D0D0D0" stroke="none"/>')
        out.append(f'<polyline points="{x + w},{y} {x},{y} {x},{y + h} {x + w},{y + h}" fill="none" stroke="#2F5597" stroke-width="1.2"/>')
        out.append(f'<line x1="{x + 30}" y1="{y}" x2="{x + 30}" y2="{y + h}" stroke="#2F5597"/>')
        out.append(f'<text x="{x + 15}" y="{y + h / 2 + 4}" text-anchor="middle" style="{FONT};font-size:11px;font-weight:bold">D{esc(s["id"])}</text>')
        out.append(f'<text x="{x + 30 + (w - 30) / 2}" y="{y + h / 2 + 4}" text-anchor="middle" style="{FONT};font-size:12px;font-weight:bold">{esc(name)}</text>')
    return "\n".join(out)


def flow_svg(f, shapes):
    pts = [tuple(p) for p in f["pts"]]
    if len(pts) < 2:
        a, b = shapes[f["from"]], shapes[f["to"]]
        pts = [(a[0] + a[2] / 2, a[1] + a[3] / 2), (b[0] + b[2] / 2, b[1] + b[3] / 2)]
    tb = shapes.get(f["to"])
    if tb:                               # make sure the polyline ends at the target shape
        cx, cy = tb[0] + tb[2] / 2, tb[1] + tb[3] / 2
        d0 = abs(pts[0][0] - cx) + abs(pts[0][1] - cy)
        d1 = abs(pts[-1][0] - cx) + abs(pts[-1][1] - cy)
        if d0 < d1:
            pts = pts[::-1]
    poly = " ".join(f"{x},{y}" for x, y in pts)
    out = [f'<polyline points="{poly}" fill="none" stroke="#000" stroke-width="1" marker-end="url(#arr)"/>']
    best, seg = -1, (pts[0], pts[1])
    for p, q in zip(pts, pts[1:]):
        length = abs(q[0] - p[0]) + abs(q[1] - p[1])
        if length > best:
            best, seg = length, (p, q)
    (x1, y1), (x2, y2) = seg
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if abs(y2 - y1) < 2:                 # horizontal segment: label above the line
        out.append(f'<text x="{mx}" y="{my - 5}" text-anchor="middle" style="{FONT};font-size:12px">{esc(f["name"])}</text>')
    else:
        out.append(f'<text x="{mx + 5}" y="{my}" style="{FONT};font-size:12px">{esc(f["name"])}</text>')
    return "\n".join(out)


def render(diagram, items, out_dir):
    shapes = {s["name"]: s["b"] for s in items if s["k"] != "flow"}
    xs = [b[0] for b in shapes.values()] + [p[0] for f in items if f["k"] == "flow" for p in f["pts"]]
    ys = [b[1] for b in shapes.values()] + [p[1] for f in items if f["k"] == "flow" for p in f["pts"]]
    x2 = [b[0] + b[2] for b in shapes.values()] + [p[0] + 160 for f in items if f["k"] == "flow" for p in f["pts"]]
    y2 = [b[1] + b[3] for b in shapes.values()]
    minx, miny, maxx, maxy = min(xs) - 20, min(ys) - 20, max(x2) + 20, max(y2) + 30
    w, h = int(maxx - minx), int(maxy - miny)
    body = [shape_svg(s) for s in items if s["k"] != "flow"] + [flow_svg(f, shapes) for f in items if f["k"] == "flow"]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{minx} {miny} {w} {h}">'
           '<defs><marker id="arr" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto" markerUnits="userSpaceOnUse">'
           '<path d="M0,0 L11,5 L0,10" fill="none" stroke="#000" stroke-width="1"/></marker></defs>'
           f'<rect x="{minx}" y="{miny}" width="{w}" height="{h}" fill="#fff"/>' + "\n".join(body) + "</svg>")
    page = os.path.join(out_dir, diagram + ".html")
    with open(page, "w", encoding="utf-8") as fh:
        fh.write(f'<!doctype html><html><body style="margin:0;background:#fff">{svg}</body></html>')
    png = os.path.join(out_dir, diagram + ".png")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    "--force-device-scale-factor=1", f"--screenshot={png}", "file:///" + page.replace("\\", "/")],
                   check=True, capture_output=True, timeout=60)
    os.remove(page)
    print("rendered", png, w, h)


def main(dump, out_dir):
    groups = defaultdict(list)
    for line in open(dump, encoding="utf-8"):
        item = json.loads(line)
        if item["k"] in ("DFExternalEntity", "DFProcess", "DFDataStore", "flow"):
            groups[item["d"]].append(item)
    os.makedirs(out_dir, exist_ok=True)
    for diagram, items in groups.items():
        render(diagram, items, out_dir)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
