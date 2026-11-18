"""Builds minorThesisV5_04_KhanhBQ.049.pdf (A6 report style: Times New Roman, light-blue tables).

Content lives in chapters.py as lists of blocks:
  ("h1", title) ("h2", title) ("h3", title) ("p", html) ("bullets", [html]) ("code", text)
  ("table", caption, header, rows, widths_mm) ("fig", path, caption, width_mm) ("term", file_or_text, caption, width_mm)
  ("pagebreak",) ("eq", html)
"""
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, Image as RLImage, KeepTogether,
                                PageBreak, PageTemplate, Paragraph, Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "minorThesisV5_04_KhanhBQ.049.pdf")
FONTS = r"C:\Windows\Fonts"

pdfmetrics.registerFont(TTFont("TNR", os.path.join(FONTS, "times.ttf")))
pdfmetrics.registerFont(TTFont("TNR-B", os.path.join(FONTS, "timesbd.ttf")))
pdfmetrics.registerFont(TTFont("TNR-I", os.path.join(FONTS, "timesi.ttf")))
pdfmetrics.registerFont(TTFont("TNR-BI", os.path.join(FONTS, "timesbi.ttf")))
pdfmetrics.registerFont(TTFont("CN", os.path.join(FONTS, "cour.ttf")))
pdfmetrics.registerFont(TTFont("CN-B", os.path.join(FONTS, "courbd.ttf")))
from reportlab.pdfbase.pdfmetrics import registerFontFamily  # noqa: E402
registerFontFamily("TNR", normal="TNR", bold="TNR-B", italic="TNR-I", boldItalic="TNR-BI")
registerFontFamily("CN", normal="CN", bold="CN-B", italic="CN", boldItalic="CN-B")

HEAD_BG = colors.HexColor("#DDEBF7")
GRID = colors.HexColor("#8EA9C1")

BODY = ParagraphStyle("body", fontName="TNR", fontSize=12, leading=16.2, alignment=TA_JUSTIFY, spaceAfter=6)
BULLET = ParagraphStyle("bullet", parent=BODY, leftIndent=16, bulletIndent=4, spaceAfter=3)
H1 = ParagraphStyle("h1", fontName="TNR-B", fontSize=16, leading=20, spaceBefore=6, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="TNR-B", fontSize=13.5, leading=17, spaceBefore=10, spaceAfter=5)
H3 = ParagraphStyle("h3", fontName="TNR-B", fontSize=12, leading=15, spaceBefore=6, spaceAfter=3)
CAP = ParagraphStyle("cap", fontName="TNR-I", fontSize=11, leading=13.5, alignment=TA_CENTER, spaceBefore=3, spaceAfter=9)
TCAP = ParagraphStyle("tcap", fontName="TNR-I", fontSize=11, leading=13.5, alignment=TA_CENTER, spaceBefore=4, spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="TNR", fontSize=10.5, leading=12.8, alignment=TA_LEFT)
CELLH = ParagraphStyle("cellh", parent=CELL, fontName="TNR")
NOTE = ParagraphStyle("note", fontName="TNR", fontSize=11, leading=14.5, leftIndent=8, spaceAfter=2)
CODE = ParagraphStyle("code", fontName="CN", fontSize=8.6, leading=10.4, leftIndent=18, spaceBefore=2, spaceAfter=8)
EQ = ParagraphStyle("eq", fontName="TNR-I", fontSize=12, leading=16, alignment=TA_CENTER, spaceBefore=2, spaceAfter=6)
TOC1 = ParagraphStyle("toc1", fontName="TNR-B", fontSize=12, leading=16, leftIndent=0)
TOC2 = ParagraphStyle("toc2", fontName="TNR", fontSize=11.5, leading=14.5, leftIndent=18)

FIG_LIST, TAB_LIST = [], []


class Doc(BaseDocTemplate):

    def __init__(self, path):
        super().__init__(path, pagesize=A4, leftMargin=25 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                         bottomMargin=20 * mm, title="ABC Online Shop - From Requirements to Code",
                         author="Be Quoc Khanh (B23DCCE049)", subject="Information System Analysis and Design - course essay")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        lw, lh = landscape(A4)
        frame_l = Frame(20 * mm, 18 * mm, lw - 40 * mm, lh - 36 * mm, id="fl")
        self.addPageTemplates([PageTemplate("cover", [frame], onPage=draw_cover),
                               PageTemplate("plain", [frame], onPage=lambda c, d: None),
                               PageTemplate("normal", [frame], onPage=self.decorate),
                               PageTemplate("landscape", [frame_l], onPage=self.decorate_l, pagesize=landscape(A4))])

    def decorate_l(self, canvas, doc):
        lw, lh = landscape(A4)
        canvas.saveState()
        canvas.setFont("TNR-I", 9.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawRightString(lw - 20 * mm, lh - 11 * mm, "Information System Analysis and Design - ABC Online Shop")
        canvas.setFont("TNR", 10.5)
        canvas.setFillColor(colors.black)
        canvas.drawCentredString(lw / 2, 9 * mm, str(doc.page - 1))
        canvas.restoreState()

    def decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("TNR-I", 9.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 12 * mm, "Information System Analysis and Design - ABC Online Shop")
        canvas.setStrokeColor(colors.HexColor("#B0B0B0"))
        canvas.line(25 * mm, A4[1] - 13.5 * mm, A4[0] - 20 * mm, A4[1] - 13.5 * mm)
        canvas.setFont("TNR", 10.5)
        canvas.setFillColor(colors.black)
        canvas.drawCentredString((A4[0] + 5 * mm) / 2, 11 * mm, str(doc.page - 1))
        canvas.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and getattr(f, "_toc", None) is not None:
            level, text = f._toc
            key = "h%d" % id(f)
            self.canv.bookmarkPage(key)
            self.notify("TOCEntry", (level, text, self.page - 1, key))
            self.canv.addOutlineEntry(re.sub("<[^>]+>", "", text), key, level=level, closed=level > 0)


def cell(text, header=False):
    text = str(text)
    if header:
        return Paragraph(text, CELLH)
    return Paragraph(text, CELL)


def make_table(caption, header, rows, widths):
    TAB_LIST.append(caption)
    total = 165.0
    widths = [w * mm for w in widths] if widths else [total / len(header) * mm] * len(header)
    data = [[cell(h, True) for h in header]] + [[cell(c) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("GRID", (0, 0), (-1, -1), 0.5, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    cap = Paragraph(f"Table {len(TAB_LIST)}. {caption}", TCAP)
    if len(rows) <= 9:
        return [KeepTogether([cap, t]), Spacer(1, 7)]
    return [CondPageBreak(60 * mm), cap, t, Spacer(1, 7)]


def trim(path):
    """Crop uniform margins of screenshots (white page background)."""
    im = Image.open(path).convert("RGB")
    bg = im.getpixel((im.width - 2, im.height - 2))
    mask = Image.new("RGB", im.size, bg)
    from PIL import ImageChops
    box = ImageChops.difference(im, mask).convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
    if box:
        box = (max(0, box[0] - 8), max(0, box[1] - 8), min(im.width, box[2] + 8), min(im.height, box[3] + 8))
        im = im.crop(box)
    out = os.path.join(HERE, "cache", "trim_" + os.path.basename(path))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)
    return out


def make_figure(path, caption, width_mm, crop=False):
    FIG_LIST.append(caption)
    src = trim(path) if crop else path
    with Image.open(src) as im:
        w, h = im.size
    width = min(width_mm * mm, 165 * mm)
    height = width * h / w
    max_h = 225 * mm
    if height > max_h:
        width, height = width * max_h / height, max_h
    img = RLImage(src, width=width, height=height)
    img.hAlign = "CENTER"
    return [KeepTogether([img, Paragraph(f"Figure {len(FIG_LIST)}. {caption}", CAP)])]


TERM_FONT = r"C:\Windows\Fonts\consola.ttf"


def terminal_png(text, name, title="$ "):
    """Render program output like a dark terminal window (as in the Assignment 06 report)."""
    font = ImageFont.truetype(TERM_FONT, 17)
    lines = text.rstrip("\n").split("\n")
    cw = font.getbbox("M")[2]
    width = max(60, max(len(l) for l in lines)) * cw + 40
    lh = 22
    height = len(lines) * lh + 60
    im = Image.new("RGB", (width, height), (40, 42, 46))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, width, 26], fill=(58, 60, 64))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([12 + i * 20, 7, 24 + i * 20, 19], fill=c)
    y = 38
    for line in lines:
        color = (225, 228, 232)
        if line.startswith("$"):
            color = (126, 231, 135)
        elif line.startswith(("---", "===")):
            color = (121, 192, 255)
        elif "FAILED" in line or " No (" in line:
            color = (255, 140, 140)
        d.text((20, y), line, font=font, fill=color)
        y += lh
    out = os.path.join(HERE, "cache", name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)
    return out


def toc_paragraph(text, style, level):
    p = Paragraph(text, style)
    p._toc = (level, text)
    return p


def render(blocks):
    story = []
    for b in blocks:
        kind = b[0]
        if kind == "h1":
            story += [PageBreak(), toc_paragraph(b[1], H1, 0)]
        elif kind == "h1x":                                   # numbered-less (Abstract etc.)
            story += [PageBreak(), toc_paragraph(b[1], H1, 0)]
        elif kind == "h2":
            story += [CondPageBreak(55 * mm), toc_paragraph(b[1], H2, 1)]
        elif kind == "h3":
            story += [CondPageBreak(40 * mm), Paragraph(b[1], H3)]
        elif kind == "p":
            story.append(Paragraph(b[1], BODY))
        elif kind == "eq":
            story.append(Paragraph(b[1], EQ))
        elif kind == "bullets":
            story += [Paragraph(x, BULLET, bulletText="\u2022") for x in b[1]]
            story.append(Spacer(1, 4))
        elif kind == "code":
            story.append(Preformatted(b[1].strip("\n"), CODE))
        elif kind == "table":
            story += make_table(b[1], b[2], b[3], b[4] if len(b) > 4 else None)
        elif kind == "fig":
            story += make_figure(b[1], b[2], b[3] if len(b) > 3 else 160, crop=b[4] if len(b) > 4 else False)
        elif kind == "figl":                                  # wide diagram on its own landscape page
            from reportlab.platypus import NextPageTemplate
            FIG_LIST.append(b[2])
            with Image.open(b[1]) as im:
                w, h = im.size
            width = 255 * mm
            height = width * h / w
            if height > 148 * mm:
                width, height = width * 148 * mm / height, 148 * mm
            img = RLImage(b[1], width=width, height=height)
            img.hAlign = "CENTER"
            if len(story) >= 2 and getattr(story[-2], "_figl_end", False):
                del story[-2:]                            # two landscape figures in a row: no portrait page between
                story += [PageBreak(), img]
            else:
                story += [NextPageTemplate("landscape"), PageBreak(), img]
            end = NextPageTemplate("normal")
            end._figl_end = True
            story += [
                      Paragraph(f"Figure {len(FIG_LIST)}. {b[2]}", CAP), end, PageBreak()]
        elif kind == "figm":                                  # figure with red numbered callouts and their notes
            from reportlab.platypus import NextPageTemplate
            path, caption, width_mm, notes, landscape = b[1], b[2], b[3], b[4], b[5]
            note_par = [Paragraph(f'<font backColor="#C00000" color="white"><b>&nbsp;{i}&nbsp;</b></font>&nbsp; {t}', NOTE)
                        for i, t in enumerate(notes, 1)]
            with Image.open(path) as im:
                ratio = im.size[0] / im.size[1]
            if not landscape or ratio < 1.3:                 # square or tall diagrams fit a portrait page better
                FIG_LIST.append(caption)
                with Image.open(path) as im:
                    w, h = im.size
                width = 165 * mm
                height = width * h / w
                max_h = (222 - 9 * len(notes)) * mm
                if height > max_h:
                    width, height = width * max_h / height, max_h
                img = RLImage(path, width=width, height=height)
                img.hAlign = "CENTER"
                story += [KeepTogether([img, Paragraph(f"Figure {len(FIG_LIST)}. {caption}", CAP)] + note_par),
                          Spacer(1, 4)]
                continue
            FIG_LIST.append(caption)
            with Image.open(path) as im:
                w, h = im.size
            # the image gets what the caption and the notes leave of the landscape frame (174 mm less its padding)
            fw = 257 * mm - 12
            cap = Paragraph(f"Figure {len(FIG_LIST)}. {caption}", CAP)
            used = sum(p.wrap(fw, 1000)[1] + p.getSpaceBefore() + p.getSpaceAfter() for p in [cap] + note_par)
            max_h = 174 * mm - 12 - used - 6 * mm
            width = 255 * mm
            height = width * h / w
            if height > max_h:
                width, height = width * max_h / height, max_h
            img = RLImage(path, width=width, height=height)
            img.hAlign = "CENTER"
            end = NextPageTemplate("normal")
            story += [NextPageTemplate("landscape"), PageBreak(), img,
                      Paragraph(f"Figure {len(FIG_LIST)}. {caption}", CAP)] + note_par + [end, PageBreak()]
        elif kind == "term":
            text = open(b[1], encoding="utf-8").read() if os.path.isfile(b[1]) else b[1]
            name = "term_%d.png" % (len(FIG_LIST) + 1)
            story += make_figure(terminal_png(text, name), b[2], b[3] if len(b) > 3 else 160)
        elif kind == "pagebreak":
            story.append(PageBreak())
        elif kind == "spacer":
            story.append(Spacer(1, b[1] * mm))
        else:
            raise ValueError(kind)
    return story


LOGO = os.path.join(HERE, "ptit_logo.png")


def draw_cover(canvas, doc):
    """The cover in the layout of the reference essay: institute and faculty, the PTIT logo, the course, the title,
    the scope, the version, the student block and the place and date, all in Times New Roman, black, centred.
    Each y is the bottom of the line in points from the top of the A4 page."""
    W, H = A4
    canvas.saveState()

    def centred(text, font, size, bottom):
        canvas.setFont(font, size)
        canvas.drawCentredString(W / 2, H - bottom + 0.216 * size, text)

    centred("POSTS AND TELECOMMUNICATIONS INSTITUTE OF TECHNOLOGY", "TNR-B", 13, 66)
    centred("FACULTY OF INFORMATION TECHNOLOGY 1", "TNR-B", 13, 82)
    canvas.drawImage(LOGO, W / 2 - 35.5, H - 216, width=71, height=91, mask="auto")
    centred("INFORMATION SYSTEM ANALYSIS AND DESIGN", "TNR-B", 17.2, 310)
    centred("ABC ONLINE SHOP", "TNR-B", 25.9, 387)
    centred("Requirements, AI Integration Analysis, Data Model, Design, and Implementation", "TNR", 14.3, 430)
    centred("Footwear, Apparel, Bags and Watches Online Retail Specialization", "TNR", 13, 462)
    centred("Version 5", "TNR-B", 14.3, 503)
    rows = [("Student", "Bế Quốc Khánh"), ("Student ID", "B23DCCE049"), ("Class", "04"),
            ("Lecturer", "PGS.TS. Trần Đình Quế")]
    canvas.setFont("TNR", 13)
    for i, (label, value) in enumerate(rows):
        y = H - (568 + 18 * i) + 0.216 * 13
        canvas.drawString(201, y, label)
        canvas.drawString(268, y, value)
    centred("Hanoi, November 2026", "TNR", 13, 788)
    canvas.restoreState()


def cover():
    c1 = ParagraphStyle("c1", fontName="TNR-B", fontSize=14, leading=18, alignment=TA_CENTER)
    from reportlab.platypus import NextPageTemplate
    # the cover itself is drawn by draw_cover; the instructor's page that follows is a plain page
    s = [Spacer(1, 1), NextPageTemplate("plain"), PageBreak()]
    dots = ParagraphStyle("dots", fontName="TNR", fontSize=12, leading=24)
    s += [Paragraph("INSTRUCTOR'S COMMENTS", ParagraphStyle("ic", parent=c1, fontSize=15)), Spacer(1, 8 * mm)]
    s += [Paragraph("." * 150, dots) for _ in range(16)]
    s += [Spacer(1, 8 * mm), Paragraph("<b>Score:</b> ............ (In words: ................................)", dots),
          Paragraph("Hanoi, date ...... month ...... year 2026", ParagraphStyle("d", parent=dots, alignment=2)),
          Paragraph("<b>Instructor</b>", ParagraphStyle("in", parent=dots, alignment=2, rightIndent=28 * mm))]
    return s


def build():
    sys.path.insert(0, HERE)
    import chapters
    from reportlab.platypus import NextPageTemplate
    front = render(chapters.FRONT)
    body = render(chapters.BLOCKS)
    figures, tables = list(FIG_LIST), list(TAB_LIST)
    toc = TableOfContents()
    toc.levelStyles = [TOC1, TOC2]
    lst = ParagraphStyle("lf", parent=BODY, fontSize=11, leading=13.5, spaceAfter=1.5, alignment=TA_LEFT)
    story = cover() + [NextPageTemplate("normal")] + front
    story += [PageBreak(), Paragraph("CONTENTS", H1), toc]
    story += [PageBreak(), Paragraph("LIST OF FIGURES", H1)]
    story += [Paragraph(f"Figure {i}. {c}", lst) for i, c in enumerate(figures, 1)]
    story += [Spacer(1, 6 * mm), Paragraph("LIST OF TABLES", H1)]
    story += [Paragraph(f"Table {i}. {c}", lst) for i, c in enumerate(tables, 1)]
    story += body
    doc = Doc(OUT)
    doc.multiBuild(story)
    print("written", OUT)


if __name__ == "__main__":
    build()
