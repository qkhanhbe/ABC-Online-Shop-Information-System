"""PKG02: the layers of the design as a package diagram (packages = layers, classes by name, <<use>> downwards).
Each class is the design class drawn on DCL01..DCL06 (the package owns it, so the box is a view of it)."""
import vp
from v5_design_spec import classes

D = "PKG01 Layers and Packages (Design)"
ORDER = ["controller", "service", "ai", "dao", "model"]
USES = [("controller", "service"), ("controller", "ai"), ("service", "dao"), ("ai", "dao"),
        ("service", "model"), ("ai", "model"), ("dao", "model"), ("controller", "model")]

vp.call("createPackageDiagram", quiet=True, diagramName=D)
for p in ORDER:
    vp.call("addPackageElement", quiet=True, diagramName=D, packageName=p)
    for c in classes(p):
        vp.call("addClassInPackage", quiet=True, diagramName=D, packageName=p, className=c)
for a, b in USES:
    vp.call("addPackageDependency", quiet=True, diagramName=D, fromPackage=a, toPackage=b, kind="use")
vp.call("autoLayoutDiagram", quiet=True, diagramName=D)
print(vp.call("getElementCounts", quiet=True, diagramName=D).replace("\n", " "))
vp.call("exportDiagramImage", quiet=True, diagramName=D, filePath=vp.PNG + D + ".png")
vp.call("saveProject", quiet=True)
