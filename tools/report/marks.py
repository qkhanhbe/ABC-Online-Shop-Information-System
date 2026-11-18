"""Red numbered callouts on a diagram image (the style of the reference essay): a red frame around an element
of the diagram and a numbered red badge; the numbers are explained under the figure.

The positions come from the geometry Visual Paradigm reports for the diagram (design/geometry/<code>.txt, saved
with getDiagramGeometry). The exported PNG is the diagram cropped to its content, so the offset between model
and image coordinates is found from the first non-white pixel and the left-/top-most coordinate of the geometry.
"""
import os
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GEO = os.path.join(ROOT, "design", "geometry")
D = os.path.join(ROOT, "diagrams")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "marks")
RED = (192, 0, 0)

SHAPE = re.compile(r"^\s*(\w+): (.+?) (-?\d+),(-?\d+) (\d+)x(\d+)(?: caption|$)")
POINTS = re.compile(r"\((-?\d+),(-?\d+)\)")
CONNECTOR = re.compile(r"^\s*(\w+)(?: <<\w+>>)?(?: '([^']*)')?: (.+?) -> (.+?) points (.*)$")


HEADER = {}


def geometry(code):
    shapes, connectors, xs, ys = {}, [], [], []
    for line in open(os.path.join(GEO, code + ".txt"), encoding="utf-8"):
        c = CONNECTOR.match(line)
        if c and " -> " in line and "points" in line:
            pts = [(int(a), int(b)) for a, b in POINTS.findall(c.group(5).split(" caption ")[0])]
            connectors.append({"kind": c.group(1), "name": c.group(2) or "", "from": c.group(3).strip(),
                               "to": c.group(4).strip(), "points": pts})
            xs += [p[0] for p in pts]
            ys += [p[1] for p in pts]
            continue
        s = SHAPE.match(line)
        if s:
            x, y, w, h = map(int, s.group(3, 4, 5, 6))
            name = s.group(2).strip()
            shapes.setdefault(name, (x, y, w, h))
            cap = re.search(r"caption -?\d+,-?\d+ \d+x(\d+)", line)
            HEADER[name] = int(cap.group(1)) if cap else 19
            xs.append(x)
            ys.append(y)
    return shapes, connectors, min(xs), min(ys)


def first_ink(img):
    g = img.convert("L").point(lambda v: 255 if v < 235 else 0)
    box = g.getbbox()
    return box[0], box[1]


def fit_offset(img, shapes, dx0, dy0, window=90, step=2):
    """The offset from model to image coordinates. The first estimate (first ink against the left-/top-most
    coordinate) is off when a label lies outside every shape, so the offset is searched near it: the one where the
    borders of the shapes fall on the most dark pixels of the image."""
    import numpy as np
    dark = np.asarray(img.convert("L")) < 110
    h, w = dark.shape
    xs, ys = [], []
    for x, y, sw, sh in shapes.values():
        for t in range(0, sw, step):                  # top and bottom border
            xs += [x + t, x + t]
            ys += [y, y + sh - 1]
        for t in range(0, sh, step):                  # left and right border
            xs += [x, x + sw - 1]
            ys += [y + t, y + t]
    xs, ys = np.array(xs), np.array(ys)
    best, at = -1, (dx0, dy0)
    for dy in range(dy0 - window, dy0 + window + 1):
        yy = ys + dy
        okay = (yy >= 0) & (yy < h)
        for dx in range(dx0 - window, dx0 + window + 1):
            xx = xs + dx
            ok = okay & (xx >= 0) & (xx < w)
            score = int(dark[yy[ok], xx[ok]].sum())
            if score > best:
                best, at = score, (dx, dy)
    return at


def font(size):
    for f in ("arialbd.ttf", "segoeuib.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


def annotate(code, marks, pad=6):
    """marks: [(number, target)], target = element name, ('line', from, to) or ('rect', x, y, w, h) in model coords.
    Returns the path of the annotated copy of the diagram image."""
    src = next(os.path.join(D, f) for f in sorted(os.listdir(D)) if f.startswith(code + " "))
    img = Image.open(src).convert("RGB")
    shapes, connectors, mx, my = geometry(code)
    ix, iy = first_ink(img)
    dx, dy = fit_offset(img, shapes, ix - mx, iy - my)
    M = 40                                            # white margin, so frames and badges near the edge stay visible
    framed = Image.new("RGB", (img.width + 2 * M, img.height + 2 * M), "white")
    framed.paste(img, (M, M))
    img = framed
    ox, oy = dx + M, dy + M
    d = ImageDraw.Draw(img)
    scale = max(1, img.width // 900)
    width = 3 * scale
    f = font(15 * scale)
    for n, target in marks:
        if isinstance(target, tuple) and target[0] == "line":
            c = next(c for c in connectors if c["from"] == target[1] and c["to"] == target[2])
            px = [p[0] for p in c["points"]]
            py = [p[1] for p in c["points"]]
            x, y, w, h = min(px) - 8, min(py) - 8, max(px) - min(px) + 16, max(py) - min(py) + 16
        elif isinstance(target, tuple) and target[0] == "attr":          # one attribute row of a class
            x, y, w, h = shapes[target[1]]
            y, h = y + HEADER[target[1]] + 1 + 19 * target[2], 19
        elif isinstance(target, tuple) and target[0] == "union":         # one frame around several elements
            bs = [shapes[n] for n in target[1]]
            x, y = min(b[0] for b in bs), min(b[1] for b in bs)
            w, h = max(b[0] + b[2] for b in bs) - x, max(b[1] + b[3] for b in bs) - y
        elif isinstance(target, tuple) and target[0] == "rect":
            x, y, w, h = target[1:]
        else:
            x, y, w, h = shapes[target]
        p = 2 if isinstance(target, tuple) and target[0] == "attr" else pad
        box = (x + ox - p, y + oy - p, x + ox + w + p, y + oy + h + p)
        d.rectangle(box, outline=RED, width=width)
        r = 13 * scale
        cx, cy = box[0] - r + 2, box[1] - r + 2
        cx, cy = max(r, cx), max(r, cy)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED)
        d.text((cx, cy), str(n), fill="white", font=f, anchor="mm")
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, code + ".png")
    img.save(out)
    return out
