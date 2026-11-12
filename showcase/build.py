"""Builds the defence showcase: showcase/index.html and readable code pages in showcase/code/.

Every artefact link is relative to the project folder, so the page works when the folder is opened on any
computer. Markers in the texts:  {fig:CL01}  {code:service/checkout_service.py:CheckoutService.place_order}
{file:design/create_tables.sql}  {test:test_repeated_submission_returns_the_same_order}
usage: python showcase/build.py
"""
import ast
import html
import os
import re

from content import ANSWERS, DIAGRAMS, EVOLUTION, PHASES, SCRIPT, TRACE, DECISIONS, kind

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APP = os.path.join(ROOT, "abc_shop")
CODE_DIR = os.path.join(HERE, "code")
code_pages = {}


def diagram_file(code):
    for f in sorted(os.listdir(os.path.join(ROOT, "diagrams"))):
        if f.startswith(code + " "):
            return f
    raise KeyError(code)


def locate(rel, symbol):
    """Line of `def symbol` / `class symbol` / Class.method in an application file."""
    path = os.path.join(APP, rel) if not rel.startswith(("design/", "tools/")) else os.path.join(ROOT, rel)
    text = open(path, encoding="utf-8").read()
    if not rel.endswith(".py") or not symbol:
        return 1
    tree = ast.parse(text)
    parts = symbol.split(".")
    nodes = tree.body
    node = None
    for p in parts:
        node = next(n for n in nodes if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == p)
        nodes = node.body
    return node.lineno


def code_page(rel):
    """Write showcase/code/<rel>.html with numbered, anchored lines; return its relative URL."""
    if rel in code_pages:
        return code_pages[rel]
    src = os.path.join(APP, rel) if not rel.startswith(("design/", "tools/")) else os.path.join(ROOT, rel)
    lines = open(src, encoding="utf-8").read().split("\n")
    name = rel.replace("/", "__") + ".html"
    body = "".join(f'<tr id="L{i}"><td class="n"><a href="#L{i}">{i}</a></td><td><pre>{html.escape(l) or " "}</pre></td></tr>'
                   for i, l in enumerate(lines, 1))
    os.makedirs(CODE_DIR, exist_ok=True)
    depth = "../" * (rel.count("/") + 0)
    open(os.path.join(CODE_DIR, name), "w", encoding="utf-8").write(f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(rel)}</title>
<style>body{{margin:0;font:13px/1.45 Consolas,monospace;background:#fffdf9;color:#1e1b18}}
header{{position:sticky;top:0;background:#f6f3ee;border-bottom:1px solid #e2dbd1;padding:10px 16px;font:14px Segoe UI,sans-serif}}
header a{{color:#b5532c}}table{{border-collapse:collapse;width:100%}}td{{padding:0 10px;vertical-align:top}}
td.n{{text-align:right;color:#a39a8f;user-select:none;width:1%;border-right:1px solid #e2dbd1}}td.n a{{color:inherit;text-decoration:none}}
pre{{margin:0;white-space:pre-wrap}}tr:target{{background:#f6e4da}}</style></head><body>
<header><a href="../index.html">&larr; Showcase</a> &nbsp; <b>{html.escape(rel)}</b> &nbsp; <a href="../../{'abc_shop/' if not rel.startswith(('design/','tools/')) else ''}{rel}">tệp gốc</a></header>
<table>{body}</table></body></html>""")
    code_pages[rel] = "code/" + name
    return code_pages[rel]


TESTS = {}
for f in os.listdir(os.path.join(APP, "tests")):
    if f.startswith("test_"):
        for i, line in enumerate(open(os.path.join(APP, "tests", f), encoding="utf-8"), 1):
            m = re.match(r"def (test_\w+)", line)
            if m:
                TESTS[m.group(1)] = (f, i)


def expand(text):
    def rep(m):
        kind, arg = m.group(1), m.group(2)
        if kind == "fig":
            f = diagram_file(arg)
            return f'<a class="fig" href="../diagrams/{f}" data-lbx>{arg}</a>'
        if kind == "code":
            rel, _, sym = arg.partition(":")
            line = locate(rel, sym)
            return f'<a class="code" href="{code_page(rel)}#L{line}" title="{rel}:{line}">{sym or rel}</a>'
        if kind == "file":
            return f'<a class="file" href="../{arg}">{arg}</a>'
        if kind == "test":
            f, line = TESTS[arg]
            return f'<a class="test" href="{code_page("tests/" + f)}#L{line}" title="tests/{f}:{line}">{arg}</a>'
        return m.group(0)
    return re.sub(r"\{(fig|code|file|test):([^}]+)\}", rep, text)


def section(id_, letter, title, lead, body):
    return (f'<section id="{id_}"><p class="eyebrow">{letter}</p><h2>{title}</h2>'
            f'{f"<p class=lead>{expand(lead)}</p>" if lead else ""}{body}</section>')


def gallery():
    out = []
    n = 0
    for phase, items in DIAGRAMS:
        cards = []
        for code, caption in items:
            f = diagram_file(code)
            n += 1
            k = kind(code)
            cards.append(f'<figure><a href="../diagrams/{f}" data-lbx data-cap="{html.escape(code + " (" + k + ") · " + caption)}">'
                         f'<img loading="lazy" src="../diagrams/{f}" alt="{html.escape(code)}"></a>'
                         f'<figcaption><b>{code}</b> <span class="kind">({html.escape(k)})</span> {html.escape(caption)}</figcaption></figure>')
        out.append(f'<h3>{phase} <span class="muted">({len(items)})</span></h3><div class="gallery">{"".join(cards)}</div>')
    return n, "".join(out)


def source_path(rel):
    return os.path.join(APP, rel) if not rel.startswith(("design/", "tools/")) else os.path.join(ROOT, rel)


def code_excerpt(rel, symbols, pick=None):
    """Real lines of the source: for a class, its header, typed fields and method signatures;
    for a function, its signature and the lines matching `pick`. Never hand-written."""
    lines = open(source_path(rel), encoding="utf-8").read().split("\n")
    tree = ast.parse("\n".join(lines))
    out = []
    for symbol in symbols:
        nodes, node = tree.body, None
        for part in symbol.split("."):
            node = next(n for n in nodes if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == part)
            nodes = node.body
        if isinstance(node, ast.ClassDef):
            out.append(lines[node.lineno - 1])
            for stmt in node.body:
                if isinstance(stmt, (ast.AnnAssign, ast.FunctionDef)):
                    out.append(lines[stmt.lineno - 1])
        else:
            body = lines[node.lineno - 1:node.end_lineno]
            out += [l for i, l in enumerate(body) if i == 0 or (pick and re.search(pick, l))]
        out.append("")
    indent = min(len(l) - len(l.lstrip()) for l in out if l.strip())
    return [l[indent:] for l in out[:-1]], locate(rel, symbols[0])


def highlight(lines, comment="#"):
    out = []
    for l in lines:
        code, _, note = l.partition(comment) if comment in l else (l, "", "")
        code = html.escape(code.rstrip() if note else code)
        code = re.sub(r"\b(class|def|with|return|if|for|in|not|is|None|True|False|CREATE TABLE|PRIMARY KEY|FOREIGN KEY|"
                      r"REFERENCES|NOT NULL|DEFAULT|CHECK)\b", r'<span class="k">\1</span>', code)
        out.append(code + (f'  <span class="c">{html.escape(comment + note)}</span>' if note else ""))
    return "\n".join(out)


def evo_step(step):
    label = html.escape(step["label"])
    if "fig" in step:
        f, code = diagram_file(step["fig"]), step["fig"]
        link = f'<a href="../diagrams/{f}" data-lbx data-cap="{html.escape(f[:-4])}">{code}</a>'
        thumb = (f'<a class="thumb" href="../diagrams/{f}" data-lbx data-cap="{html.escape(f[:-4])}">'
                 f'<img src="../diagrams/{f}" alt="{html.escape(f[:-4])}" loading="lazy"></a>')
    elif "shot" in step:
        name = os.path.basename(step["shot"])
        link = f'<a href="../{step["shot"]}" data-lbx data-cap="{html.escape(step["cap"][:80])}">{name}</a>'
        thumb = (f'<a class="thumb shot" href="../{step["shot"]}" data-lbx data-cap="{html.escape(name)}">'
                 f'<img src="../{step["shot"]}" alt="{html.escape(name)}" loading="lazy"></a>')
    elif "code" in step:
        rel, symbols = step["code"]
        lines, line = code_excerpt(rel, symbols, step.get("pick"))
        link = f'<a href="{code_page(rel)}#L{line}" title="{rel}:{line}">{os.path.basename(rel)}</a>'
        thumb = f'<a class="thumb code" href="{code_page(rel)}#L{line}">{highlight(lines)}</a>'
    else:
        rel, table = step["sql"]
        text = open(source_path(rel), encoding="utf-8").read()
        block = re.search(rf"CREATE TABLE {table} \(.*?\);", text, re.S).group(0)
        line = text[:text.index(block)].count("\n") + 1
        link = f'<a href="{code_page(rel)}#L{line}">{os.path.basename(rel)}</a>'
        thumb = f'<a class="thumb code" href="{code_page(rel)}#L{line}">{highlight(block.split(chr(10)), "--")}</a>'
    return (f'<div class="step"><div class="label"><span>{label}</span>{link}</div>{thumb}'
            f'<div class="cap">{expand(step["cap"])}</div></div>')


def evolution():
    out = []
    for chain in EVOLUTION:
        steps = chain["steps"]
        cols = " 30px ".join(["minmax(0,1fr)"] * len(steps))
        row = '<div class="arrow" aria-hidden="true">→</div>'.join(evo_step(s) for s in steps)
        changes = "".join(f'<div><h4>{h}</h4><ul>{"".join(f"<li>{expand(x)}</li>" for x in chain[k])}</ul></div>'
                          for h, k in (("Thay đổi gì", "what"), ("Vì sao", "why"), ("Lợi ích", "gain")))
        out.append(f'<div class="evo"><div class="evo-title"><h3>{chain["title"]}</h3><span class="note">{chain["note"]}</span></div>'
                   f'<div class="steps" style="grid-template-columns:{cols}">{row}</div><div class="changes">{changes}</div></div>')
    return "".join(out)


def trace():
    out = []
    for uc, rows in TRACE:
        body = "".join(f"<tr><th>{k}</th><td>{expand(v)}</td></tr>" for k, v in rows)
        out.append(f'<div class="trace"><h3>{uc}</h3><table>{body}</table></div>')
    return "".join(out)


def answers():
    out, group = [], None
    for n, (g, q, a) in enumerate(ANSWERS, 1):
        if g != group:
            if group is not None:
                out.append("</div>")
            out.append(f'<h3>{g}</h3><div class="qa">')
            group = g
        out.append(f'<details id="q{n}"><summary><span class="qn">{n}</span>{html.escape(q)}</summary>'
                   f'<div class="ans">{expand(a)}</div></details>')
    out.append("</div>")
    return "".join(out)


def read(rel):
    return html.escape(open(os.path.join(ROOT, rel), encoding="utf-8").read())


def build():
    count, gal = gallery()
    phases = "".join(f'<div class="phase"><span class="n">{i}</span><h3>{t}</h3><p>{expand(p)}</p></div>'
                     for i, (t, p) in enumerate(PHASES, 1))
    script = "".join(f"<tr><td class='t'>{t}</td><td>{expand(s)}</td><td>{expand(o)}</td></tr>" for t, s, o in SCRIPT)
    decisions = "".join(f"<tr><td><b>{d}</b></td><td>{expand(w)}</td><td>{expand(a)}</td><td>{expand(c)}</td></tr>"
                        for d, w, a, c in DECISIONS)
    values = dict(
        count=count, gallery=gal, phases=phases, evolution=evolution(), trace=trace(), answers=answers(),
        script=script, decisions=decisions,
        build_db=read("design/build_db_output.txt"), check_code=read("design/check_code_output.txt"),
        tests=html.escape("\n".join(open(os.path.join(ROOT, "demo_results/test_output.txt"), encoding="utf-8").read().split("\n")[-4:])),
        evaluation=read("demo_results/evaluation_output.txt"),
        ddl=html.escape(re.search(r"CREATE TABLE category.*?\);\n\nCREATE TABLE product .*?\);\n\nCREATE TABLE bag_detail.*?\);",
                                  open(os.path.join(ROOT, "design/create_tables.sql"), encoding="utf-8").read(), re.S).group(0)),
        place_order=code_page("service/checkout_service.py") + "#L" + str(locate("service/checkout_service.py", "CheckoutService.place_order")),
    )
    page = TEMPLATE
    for k, v in values.items():
        page = page.replace("%%" + k + "%%", str(v))
    page = expand(page)
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    print(f"showcase/index.html: {count} diagrams, {len(ANSWERS)} answers, {len(code_pages)} code pages")


TEMPLATE = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()

if __name__ == "__main__":
    build()
