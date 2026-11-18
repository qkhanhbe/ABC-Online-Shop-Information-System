"""Brings the operations drawn on the design diagrams in line with the code (v5_design_spec.py): an operation
whose parameters or return type differ is removed and added again."""
import json

import vp
from v5_design_build import DIAGRAMS
from v5_design_spec import classes

fixed = 0
for package, diagrams in DIAGRAMS.items():
    spec = classes(package)
    for d in diagrams:
        drawn = json.loads(vp.call("getRelationshipDetails", quiet=True, diagramName=d))["classes"]
        for c in drawn:
            want = {o[0]: o for o in spec.get(c["name"], {}).get("ops", [])}
            have = {o["name"]: (", ".join(o.get("params", [])), o.get("returnType", "")) for o in c["operations"]}
            for name, o in want.items():
                if have.get(name) != (o[1], o[2]):
                    vp.call("removeOperation", quiet=True, diagramName=d, className=c["name"], operationName=name)
                    vp.call("addOperation", quiet=True, className=c["name"], operationName=name, returnType=o[2],
                            params=o[1], visibility="public", isAbstract=bool(o[4] and spec[c["name"]].get("interface")),
                            diagramName=d)
                    fixed += 1
                    print("fixed", d[:6], c["name"], name, have.get(name), "->", (o[1], o[2]))
print("operations fixed:", fixed)
vp.call("saveProject", quiet=True)
