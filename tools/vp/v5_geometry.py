"""Saves the geometry Visual Paradigm reports for every diagram to design/geometry/<code>.txt; the red callouts of
the report (tools/report/marks.py) are placed with it. Run it after the diagrams are exported.

    python tools/vp/v5_geometry.py
"""
import os
import re

import vp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GEO = os.path.join(ROOT, "design", "geometry")

if __name__ == "__main__":
    os.makedirs(GEO, exist_ok=True)
    for old in os.listdir(GEO):
        os.remove(os.path.join(GEO, old))
    names = re.findall(r"^\s+- (.+) \(\w+\)$", vp.call("listDiagrams", quiet=True, type=""), re.M)
    for d in names:
        g = vp.call("getDiagramGeometry", quiet=True, diagramName=d)
        open(os.path.join(GEO, d.split(" ")[0] + ".txt"), "w", encoding="utf-8").write(g)
    print(len(names), "geometries saved")
