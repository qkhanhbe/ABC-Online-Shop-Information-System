"""Check the code generated from the design model (Section 4.5).

[1] packages and classes generated, [2] every module compiles and imports, [3] the hand-written
application in abc_shop/ is compared class by class with the generated skeleton (fields and methods
of the model must exist in the code), [4] the members of one generated class.
usage: python check_code.py
"""
import dataclasses
import importlib
import inspect
import os
import py_compile
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, "generated", "abc_shop_design")
APP = os.path.join(os.path.dirname(HERE), "abc_shop")


def modules(root):
    out = []
    for d, _, files in os.walk(root):
        for f in sorted(files):
            if f.endswith(".py") and f != "__init__.py":
                rel = os.path.relpath(os.path.join(d, f), root)[:-3]
                out.append(rel.replace(os.sep, "."))
    return sorted(out)


def load(root, name):
    """Import module `name` with `root` as the top of the import path (both trees use the same names)."""
    for m in [m for m in sys.modules if m.split(".")[0] in ("model", "dao", "service", "controller", "view", "ai")]:
        del sys.modules[m]
    sys.path.insert(0, root)
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(root)


def members(obj):
    if inspect.isclass(obj):
        meth = {n for n, v in vars(obj).items() if not n.startswith("_") and (callable(v) or isinstance(v, (property, classmethod, staticmethod)))}
        for base in obj.__mro__[1:]:
            if base.__module__.split(".")[0] in ("model", "dao", "service", "controller", "view"):
                meth |= members(base)[1]
        if dataclasses.is_dataclass(obj):
            fields = {f.name for f in dataclasses.fields(obj)}
        else:
            src = inspect.getsource(obj.__init__) if "__init__" in vars(obj) else ""
            fields = set(re.findall(r"self\.(\w+)\s*=", src))
        return fields, meth
    return set(), {n for n, v in vars(obj).items() if inspect.isfunction(v) and not n.startswith("_")}


def main():
    print("> python check_code.py\n")
    names = modules(GEN)
    print("[1] Packages and classes generated from the model (root abc_shop_design)")
    by_layer = {}
    gen_classes = {}
    for n in names:
        mod = load(GEN, n)
        cls = [c for c, v in vars(mod).items() if inspect.isclass(v) and v.__module__ == mod.__name__]
        funcs = [f for f, v in vars(mod).items() if inspect.isfunction(v) and v.__module__ == mod.__name__]
        by_layer.setdefault(n.split(".")[0], []).append((n, cls or [n.split(".")[1] + " (module)"]))
        for c in cls:
            gen_classes[c] = n
        if not cls:
            gen_classes[n.split(".")[1]] = n
    total = sum(len(c) for v in by_layer.values() for _, c in v)
    for layer in ("view", "controller", "service", "dao", "model"):
        for n, cls in by_layer.get(layer, []):
            print(f"  {n:<24} {', '.join(cls)}")
    files = [os.path.join(GEN, *n.split(".")) + ".py" for n in names]
    for f in files:
        py_compile.compile(f, doraise=True)
    print(f"\n[2] py_compile and import of {len(files)} modules ({total} classes): no errors")

    print("\n[3] Design model against the hand-written code in abc_shop/")
    print(f"  {'class':<16} {'module':<28} {'fields':>7} {'methods':>8}  difference")
    ok = 0
    for cname, n in sorted(gen_classes.items(), key=lambda kv: (kv[1], kv[0])):
        gmod = load(GEN, n)
        gobj = getattr(gmod, cname, gmod)
        gf, gm = members(gobj)
        rmod = load(APP, n)
        robj = getattr(rmod, cname, rmod) if inspect.isclass(gobj) else rmod
        rf, rm = members(robj)
        miss_f, miss_m = sorted(gf - rf), sorted(gm - rm)
        diff = ", ".join([f"field {x} missing" for x in miss_f] + [f"method {x} missing" for x in miss_m])
        extra = sorted((rm - gm) - {"available"}) if inspect.isclass(gobj) and gobj.__module__.startswith("model") else []
        if not diff:
            ok += 1
        if extra:
            diff = (diff + "; " if diff else "") + "code only: " + ", ".join(extra)
        print(f"  {cname:<16} {n:<28} {len(gf & rf):>3}/{len(gf):<3} {len(gm & rm):>3}/{len(gm):<4}  {diff or '-'}")
    print(f"  {ok} of {len(gen_classes)} classes: every field and method of the model exists in the code")

    print("\n[4] Members of the generated class model.order.Order")
    order = load(GEN, "model.order").Order
    for f in dataclasses.fields(order):
        print(f"  field  {f.name}: {f.type}")
    for name, fn in vars(order).items():
        if inspect.isfunction(fn) and not name.startswith("__"):
            print(f"  method {name}{inspect.signature(fn)}")


if __name__ == "__main__":
    main()
