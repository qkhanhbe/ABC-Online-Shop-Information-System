"""Draws the catalogue photos (data/images) and the customer query photos (data/query_images).

The shop has no real product photography, so each product is drawn as a studio-style illustration: shaded
shapes on a warm backdrop, drawn at three times the final size and scaled down for smooth edges. The query
photos show the same kinds of objects as a customer would photograph them: another backdrop, a slightly
different scale, position, angle and light, and sensor noise. The image search must still find the right
product (python evaluate.py).

The backdrops are chosen so that every product colour, white and silver included, differs from the backdrop by
more than the threshold the image encoder uses to separate object from background.
usage: python tools/make_images.py   (from the abc_shop folder)
"""
import os

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SS = 3                    # supersampling factor
N = 600 * SS              # drawing canvas

BACKDROP = ((236, 225, 212), (224, 211, 196))       # centre, edge: warm studio paper


def font(size, bold=False):
    for name in (("segoeuib.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")):
        try:
            return ImageFont.truetype(name, size * SS)
        except OSError:
            pass
    return ImageFont.load_default()


def tone(c, k):
    """k > 0 mixes toward white, k < 0 toward black."""
    t = (255, 255, 255) if k > 0 else (0, 0, 0)
    k = abs(k)
    return tuple(int(round(a + (b - a) * k)) for a, b in zip(c, t))


class Path:
    def __init__(self, x, y):
        self.pts = [(x, y)]

    def l(self, x, y):
        self.pts.append((x, y))
        return self

    def c(self, x1, y1, x2, y2, x, y, n=28):
        x0, y0 = self.pts[-1]
        for i in range(1, n + 1):
            t = i / n
            m = 1 - t
            self.pts.append((m ** 3 * x0 + 3 * m * m * t * x1 + 3 * m * t * t * x2 + t ** 3 * x,
                             m ** 3 * y0 + 3 * m * m * t * y1 + 3 * m * t * t * y2 + t ** 3 * y))
        return self


def P(pts):
    return [(x * SS, y * SS) for x, y in pts]


class Art:
    """An object drawn on a transparent layer."""

    def __init__(self):
        self.layer = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.layer)

    # masks
    def poly(self, pts):
        m = Image.new("L", (N, N), 0)
        ImageDraw.Draw(m).polygon(P(pts.pts if isinstance(pts, Path) else pts), fill=255)
        return m

    def rrect(self, x0, y0, x1, y1, r):
        m = Image.new("L", (N, N), 0)
        ImageDraw.Draw(m).rounded_rectangle((x0 * SS, y0 * SS, x1 * SS, y1 * SS), r * SS, fill=255)
        return m

    def ellipse(self, x0, y0, x1, y1):
        m = Image.new("L", (N, N), 0)
        ImageDraw.Draw(m).ellipse((x0 * SS, y0 * SS, x1 * SS, y1 * SS), fill=255)
        return m

    @staticmethod
    def both(a, b):
        return ImageChops.multiply(a, b)

    # painting
    def fill(self, mask, top, bottom=None, horizontal=False):
        bottom = bottom or top
        box = mask.getbbox()
        if not box:
            return
        x0, y0, x1, y1 = box
        n = (x1 - x0) if horizontal else (y1 - y0)
        t = np.linspace(0, 1, n)[:, None]
        col = np.array(top, float)[None, :] * (1 - t) + np.array(bottom, float)[None, :] * t
        arr = col[None, :, :].repeat(y1 - y0, 0) if horizontal else col[:, None, :].repeat(x1 - x0, 1)
        grad = Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
        self.layer.paste(grad, (x0, y0), mask.crop(box))

    def light(self, mask, x0, y0, x1, y1, strength=0.35, blur=30, colour=(255, 255, 255)):
        """A soft highlight (or shade, with a dark colour) clipped to mask."""
        h = self.ellipse(x0, y0, x1, y1).filter(ImageFilter.GaussianBlur(blur * SS))
        h = self.both(h, mask).point(lambda v: int(v * strength))
        over = Image.new("RGBA", (N, N), colour + (255,))
        alpha = self.layer.getchannel("A")
        self.layer = Image.composite(over, self.layer, h)
        self.layer.putalpha(alpha)
        self.d = ImageDraw.Draw(self.layer)

    def line(self, pts, colour, width=2, dash=None):
        pts = pts.pts if isinstance(pts, Path) else pts
        if not dash:
            self.d.line(P(pts), fill=colour, width=int(width * SS), joint="curve")
            return
        # dashed: walk along the polyline
        seg, on, left = [], True, dash
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            length = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
            pos = 0
            while pos < length:
                step = min(left, length - pos)
                t0, t1 = pos / length, (pos + step) / length
                if on:
                    self.d.line(P([(ax + (bx - ax) * t0, ay + (by - ay) * t0),
                                   (ax + (bx - ax) * t1, ay + (by - ay) * t1)]), fill=colour, width=int(width * SS))
                pos += step
                left -= step
                if left <= 0:
                    on, left = not on, dash
        return seg

    def outline(self, pts, colour, width=1.6):
        pts = pts.pts if isinstance(pts, Path) else pts
        self.line(list(pts) + [pts[0]], colour, width)

    def dot(self, x, y, r, colour):
        self.d.ellipse(((x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS), fill=colour)

    def text(self, x, y, s, size, colour, bold=False):
        self.d.text((x * SS, y * SS), s, fill=colour, font=font(size, bold), anchor="mm")


# ---------------------------------------------------------------- shoes
def running_shoe(upper, accent, midsole, outsole, lace):
    a = Art()
    up = (Path(100, 372).c(86, 330, 88, 290, 104, 254).c(130, 260, 165, 274, 190, 270)
          .c(204, 244, 214, 224, 228, 212).c(240, 202, 258, 204, 266, 214)
          .c(306, 252, 384, 292, 452, 318).c(502, 336, 536, 360, 540, 400).l(100, 400))
    m = a.poly(up)
    a.fill(m, tone(upper, .16), tone(upper, -.22))
    a.light(m, 250, 230, 470, 330, .22, 30)
    heel = Path(98, 372).c(88, 330, 90, 292, 102, 262).c(126, 272, 146, 300, 156, 372)
    a.fill(a.both(a.poly(heel), m), tone(accent, .1), tone(accent, -.15))
    toe = Path(452, 318).c(502, 336, 536, 360, 540, 400).l(468, 400).c(470, 368, 462, 340, 452, 318)
    a.fill(a.both(a.poly(toe), m), tone(accent, .1), tone(accent, -.15))
    cage = Path(196, 372).c(230, 330, 262, 292, 286, 236).l(318, 258).c(306, 300, 292, 340, 286, 380)
    a.fill(a.both(a.poly(cage), m), tone(accent, .18), accent)
    a.line(Path(160, 300).c(260, 330, 380, 340, 470, 350), tone(upper, -.3), 1.4, dash=6)
    collar = Path(104, 256).c(130, 264, 165, 276, 190, 272).c(176, 258, 150, 248, 122, 246).c(110, 246, 105, 250, 104, 256)
    a.fill(a.poly(collar), (38, 36, 36))
    tongue = Path(226, 214).c(234, 196, 256, 192, 270, 204).c(268, 212, 264, 216, 258, 220)
    a.fill(a.poly(tongue), tone(upper, .08), tone(upper, -.1))
    for i in range(5):
        t = i / 4
        x, y = 246 + t * 92, 232 + t * 46
        a.dot(x - 13, y + 12, 3.2, tone(upper, -.45))
        a.dot(x + 13, y - 11, 3.2, tone(upper, -.45))
        a.line([(x - 13, y + 12), (x + 13, y - 11)], lace, 5)
    sole = (Path(96, 360).c(150, 368, 300, 380, 420, 390).c(480, 394, 522, 396, 540, 404)
            .c(550, 410, 544, 424, 524, 430).c(470, 440, 300, 446, 150, 444)
            .c(104, 444, 84, 432, 82, 404).c(81, 384, 86, 366, 96, 360))
    s = a.poly(sole)
    a.fill(s, tone(midsole, .04), tone(midsole, -.05))
    a.fill(a.both(s, a.rrect(0, 430, 600, 600, 0)), tone(outsole, .1), outsole)
    a.line(Path(108, 412).c(220, 420, 380, 424, 528, 414), tone(midsole, -.14), 2)
    a.outline(sole, tone(midsole, -.2), 1.2)
    return a


def court_shoe(upper, tab, sole_c, outsole, lace, straps=False):
    a = Art()
    up = (Path(98, 392).c(90, 344, 92, 302, 102, 268).c(132, 274, 170, 284, 196, 282)
          .c(210, 256, 222, 238, 236, 230).c(250, 222, 264, 224, 270, 232)
          .c(322, 268, 420, 296, 482, 312).c(522, 322, 546, 346, 548, 392).l(98, 396))
    m = a.poly(up)
    a.fill(m, tone(upper, .14), tone(upper, -.12))
    a.light(m, 260, 240, 480, 330, .25, 28)
    panel = Path(150, 392).c(170, 340, 220, 300, 300, 290).c(360, 286, 400, 330, 410, 392)
    a.line(panel, tone(upper, -.28), 1.6)
    a.line(Path(158, 392).c(178, 346, 226, 308, 300, 298).c(354, 294, 392, 334, 402, 392), tone(upper, -.2), 1.2, dash=5)
    heel = Path(102, 268).c(94, 310, 94, 350, 98, 392).l(130, 392).c(126, 350, 124, 310, 124, 274)
    a.fill(a.poly(heel), tone(tab, .1), tone(tab, -.15))
    collar = Path(104, 270).c(132, 278, 170, 288, 196, 284).c(182, 268, 150, 260, 124, 258).c(112, 258, 106, 262, 104, 270)
    a.fill(a.poly(collar), (40, 38, 38))
    tongue = Path(234, 232).c(242, 212, 262, 208, 276, 222).c(272, 228, 268, 232, 262, 236)
    a.fill(a.poly(tongue), tone(upper, .06), tone(upper, -.08))
    if straps:      # sporty version: a contrasting mudguard band around the foot
        guard = Path(96, 396).l(96, 356).c(200, 372, 330, 372, 430, 350).c(480, 340, 530, 344, 548, 366).l(548, 396)
        a.fill(a.both(a.poly(guard), m), tone(sole_c, .02), tone(sole_c, -.1))
        a.line(Path(96, 356).c(200, 372, 330, 372, 430, 350).c(480, 340, 530, 344, 548, 366), tone(upper, -.3), 1.4)
    for i in range(5):
        t = i / 4
        x, y = 254 + t * 88, 248 + t * 42
        a.line([(x - 12, y + 11), (x + 12, y - 10)], lace, 5)
    if not straps:
        for r in range(3):
            for c in range(4 - r):
                a.dot(470 + c * 16 + r * 6, 336 + r * 14, 2.4, tone(upper, -.3))
    sole = Path(92, 384).l(526, 386).c(546, 388, 554, 404, 550, 420).c(546, 436, 532, 444, 510, 444).l(112, 444).c(92, 444, 84, 432, 84, 412).c(84, 398, 86, 388, 92, 384)
    s = a.poly(sole)
    a.fill(s, tone(sole_c, .03), tone(sole_c, -.06))
    a.fill(a.both(s, a.rrect(0, 434, 600, 600, 0)), outsole)
    a.line(Path(96, 400).l(540, 402), tone(sole_c, -.18), 1.4, dash=5)
    a.outline(sole, tone(sole_c, -.22), 1.2)
    return a


# ---------------------------------------------------------------- bags
def tote(body, trim, metal):
    a = Art()
    handle = Path(222, 262).c(222, 132, 378, 132, 378, 262)
    a.line(handle, tone(body, -.2), 17)
    a.line(Path(222, 262).c(222, 140, 378, 140, 378, 262), tone(body, .25), 2)
    shape = (Path(166, 250).l(434, 250).c(446, 250, 452, 258, 454, 268).l(478, 452).c(480, 468, 470, 478, 456, 478)
             .l(144, 478).c(130, 478, 120, 468, 122, 452).l(146, 268).c(148, 258, 154, 250, 166, 250))
    m = a.poly(shape)
    a.fill(m, tone(body, .2), tone(body, -.3))
    a.light(m, 160, 250, 300, 470, .18, 34)
    a.fill(a.both(m, a.rrect(0, 250, 600, 290, 0)), tone(trim, .14), trim)
    inset = (Path(168, 262).l(432, 262).l(464, 462).l(136, 462).l(168, 262))
    a.line(inset.pts + [inset.pts[0]], tone(body, .35), 1.4, dash=6)
    for x in (222, 378):
        tab = a.rrect(x - 13, 240, x + 13, 292, 6)
        a.fill(tab, tone(trim, .12), tone(trim, -.1))
        a.dot(x, 252, 7, metal)
        a.dot(x, 252, 3.5, tone(trim, -.2))
    clasp = a.rrect(284, 284, 316, 312, 6)
    a.fill(clasp, tone(metal, .25), tone(metal, -.2))
    a.outline(shape, tone(body, -.4), 1.4)
    return a


def backpack(body, trim, patch):
    a = Art()
    for x0 in (156, 414):
        st = a.rrect(x0, 200, x0 + 30, 440, 14)
        a.fill(st, tone(trim, .05), tone(trim, -.25))
    a.line(Path(272, 172).c(272, 128, 328, 128, 328, 172), tone(trim, -.1), 13)
    m = a.rrect(180, 162, 420, 486, 78)
    a.fill(m, tone(body, .16), tone(body, -.26))
    a.light(m, 190, 170, 320, 330, .2, 32)
    a.line(Path(198, 268).c(226, 196, 374, 196, 402, 268), tone(body, -.45), 4)
    a.line(Path(198, 268).c(226, 196, 374, 196, 402, 268), tone(body, .2), 1)
    a.fill(a.rrect(392, 252, 404, 286, 4), (196, 190, 180))
    pocket = a.rrect(204, 318, 396, 472, 42)
    a.fill(pocket, tone(body, .06), tone(body, -.32))
    a.light(pocket, 210, 320, 330, 400, .16, 22)
    a.d.rounded_rectangle((204 * SS, 318 * SS, 396 * SS, 472 * SS), 42 * SS, outline=tone(body, -.5), width=int(1.6 * SS))
    a.line([(226, 340), (374, 340)], tone(body, -.5), 4)
    a.fill(a.rrect(366, 336, 378, 366, 4), (196, 190, 180))
    a.line(Path(216, 470).l(216, 352).c(216, 332, 228, 326, 240, 326).l(360, 326).c(374, 326, 384, 334, 384, 352).l(384, 470),
           tone(body, .22), 1.2, dash=5)
    a.fill(a.rrect(278, 384, 322, 414, 6), tone(patch, .1), tone(patch, -.15))
    a.d.rounded_rectangle((180 * SS, 162 * SS, 420 * SS, 486 * SS), 78 * SS, outline=tone(body, -.5), width=int(1.6 * SS))
    return a


# ---------------------------------------------------------------- shirts
SHIRT = (Path(254, 118).c(270, 140, 330, 140, 346, 118).l(420, 136).c(452, 150, 482, 178, 508, 214).l(472, 270)
         .c(456, 262, 440, 252, 426, 246).l(430, 496).c(380, 504, 220, 504, 170, 496).l(174, 246)
         .c(160, 252, 144, 262, 128, 270).l(92, 214).c(118, 178, 148, 150, 180, 136).l(254, 118))


def tshirt(cloth, light_cloth=False):
    a = Art()
    m = a.poly(SHIRT)
    k = (.04, -.06) if light_cloth else (.14, -.2)
    a.fill(m, tone(cloth, k[0]), tone(cloth, k[1]))
    shade = (40, 30, 20)
    a.light(m, 200, 280, 260, 480, .08 if light_cloth else .18, 18, shade)
    a.light(m, 330, 230, 400, 470, .07 if light_cloth else .16, 20, shade)
    a.light(m, 240, 160, 380, 260, .14, 26)
    inside = Path(258, 120).c(276, 110, 324, 110, 342, 120).c(326, 132, 274, 132, 258, 120)
    a.fill(a.poly(inside), tone(cloth, -.28 if light_cloth else -.4))
    a.line(Path(254, 118).c(270, 142, 330, 142, 346, 118), tone(cloth, -.12 if light_cloth else .12), 7)
    a.line(Path(254, 118).c(270, 142, 330, 142, 346, 118), tone(cloth, -.25), 1)
    for (x0, y0, x1, y1) in ((480, 252, 499, 226), (120, 252, 101, 226)):
        a.line([(x0, y0), (x1, y1)], tone(cloth, -.22), 1.2, dash=5)
    a.line([(176, 482), (424, 482)], tone(cloth, -.22), 1.2, dash=5)
    a.outline(SHIRT, tone(cloth, -.3), 1.3)
    return a


def polo(cloth, button):
    a = tshirt(cloth, light_cloth=True)
    a.fill(a.rrect(288, 132, 312, 238, 4), tone(cloth, .02), tone(cloth, -.06))
    a.d.rounded_rectangle((288 * SS, 132 * SS, 312 * SS, 238 * SS), 4 * SS, outline=tone(cloth, -.28), width=int(1.2 * SS))
    for y in (160, 190, 220):
        a.dot(300, y, 4.5, button)
        a.dot(300, y, 1.6, tone(button, -.35))
    for side in (-1, 1):
        wing = [(300 - side * 46, 112), (300, 136), (300 - side * 10, 170), (300 - side * 62, 150)]
        a.fill(a.poly(wing), tone(cloth, .03), tone(cloth, -.08))
        a.outline(wing, tone(cloth, -.3), 1.3)
    for (x0, y0, x1, y1) in ((486, 260, 506, 232), (114, 260, 94, 232)):
        a.line([(x0, y0), (x1, y1)], tone(cloth, -.2), 9)
    return a


# ---------------------------------------------------------------- caps
def cap(cloth, texture=False):
    a = Art()
    crown = Path(110, 386).c(98, 262, 170, 166, 264, 160).c(360, 156, 422, 240, 420, 378).c(346, 400, 186, 406, 110, 386)
    m = a.poly(crown)
    a.fill(m, tone(cloth, .18), tone(cloth, -.24))
    a.light(m, 150, 170, 290, 300, .22, 30)
    if texture:
        rng = np.random.default_rng(9)
        noise = Image.fromarray((rng.random((N // 2, N // 2)) * 255).astype(np.uint8)).resize((N, N))
        a.layer = Image.composite(Image.new("RGBA", (N, N), tone(cloth, .3) + (255,)), a.layer,
                                  ImageChops.multiply(m, noise.point(lambda v: 40 if v > 200 else 0)))
        a.d = ImageDraw.Draw(a.layer)
    for seam in (Path(264, 164).c(214, 220, 186, 300, 180, 398), Path(264, 164).c(296, 230, 312, 300, 316, 402),
                 Path(264, 164).c(360, 222, 398, 292, 412, 382)):
        a.line(seam, tone(cloth, -.42), 2)
        a.line([(x + 5, y) for x, y in seam.pts], tone(cloth, .1), 1, dash=4)
    for x, y in ((210, 246), (330, 238)):
        a.dot(x, y, 5, tone(cloth, -.5))
        a.dot(x, y, 2.4, tone(cloth, .2))
    a.d.ellipse((252 * SS, 150 * SS, 276 * SS, 170 * SS), fill=tone(cloth, -.1), outline=tone(cloth, -.45), width=SS)
    a.line(Path(112, 386).c(186, 406, 346, 400, 420, 378), tone(cloth, -.4), 4)
    a.outline(crown, tone(cloth, -.4), 1.3)
    under = Path(316, 392).c(390, 414, 480, 420, 556, 400).c(530, 428, 420, 432, 330, 410)
    a.fill(a.poly(under), tone(cloth, -.5), tone(cloth, -.62))
    brim = Path(316, 370).c(390, 344, 492, 344, 562, 376).c(572, 384, 566, 396, 556, 400).c(480, 420, 390, 414, 316, 392)
    b = a.poly(brim)
    a.fill(b, tone(cloth, .16), tone(cloth, -.2))
    a.light(b, 360, 340, 520, 380, .2, 16)
    for k in range(3):
        a.line(Path(336, 376 + k * 7).c(400, 356 + k * 7, 490, 358 + k * 6, 546, 384 + k * 2), tone(cloth, -.28), 1, dash=4)
    a.outline(brim, tone(cloth, -.42), 1.3)
    return a


# ---------------------------------------------------------------- watches
def smart_watch(strap, case, ring):
    a = Art()
    st = a.rrect(254, 36, 346, 564, 30)
    a.fill(st, tone(strap, .14), tone(strap, -.2), horizontal=True)
    a.light(st, 254, 36, 300, 564, .12, 10)
    for y in (470, 496, 522):
        a.dot(300, y, 5, tone(strap, -.55))
    a.fill(a.rrect(246, 444, 354, 460, 6), tone(strap, -.1), tone(strap, -.3))
    for y in (120, 140, 460):
        a.line([(262, y), (338, y)], tone(strap, -.25), 1)
    c = a.rrect(204, 174, 396, 426, 54)
    a.fill(c, tone(case, .35), tone(case, -.25))
    a.fill(a.rrect(394, 246, 412, 298, 7), tone(case, .3), tone(case, -.2))
    a.fill(a.rrect(394, 318, 406, 350, 5), tone(case, .2), tone(case, -.2))
    a.fill(a.rrect(214, 184, 386, 416, 46), tone(case, -.35))
    screen = a.rrect(222, 192, 378, 408, 38)
    a.fill(screen, (24, 26, 32), (10, 11, 14))
    a.light(screen, 200, 170, 330, 260, .1, 20)
    a.text(300, 262, "10:09", 46, (245, 245, 240), bold=True)
    a.text(300, 220, "WED 12", 14, (170, 172, 180))
    for i, (col, r) in enumerate(((ring, 40), (tone(ring, .35), 31), ((140, 210, 120), 22))):
        box = ((300 - r) * SS, (352 - r) * SS, (300 + r) * SS, (352 + r) * SS)
        a.d.arc(box, 0, 360, fill=tone(col, -.6), width=7 * SS)
        a.d.arc(box, -90, 200 - i * 50, fill=col, width=7 * SS)
    return a


def analog_watch(steel, dial):
    a = Art()
    br = a.rrect(258, 30, 342, 570, 10)
    a.fill(br, tone(steel, -.3), tone(steel, .4), horizontal=True)
    for y in range(44, 566, 26):
        a.line([(258, y), (342, y)], tone(steel, -.42), 1.4)
    mid = a.both(br, a.rrect(286, 0, 314, 600, 0))
    a.fill(mid, tone(steel, .45), tone(steel, -.1), horizontal=True)
    for y in range(44, 566, 26):
        a.line([(286, y), (314, y)], tone(steel, -.42), 1.4)
    a.fill(a.rrect(418, 286, 440, 314, 5), tone(steel, .3), tone(steel, -.25))
    a.fill(a.ellipse(176, 176, 424, 424), tone(steel, .4), tone(steel, -.35), horizontal=True)
    a.fill(a.ellipse(188, 188, 412, 412), tone(steel, -.3), tone(steel, .35), horizontal=True)
    d = a.ellipse(200, 200, 400, 400)
    a.fill(d, tone(dial, .05), tone(dial, -.06))
    a.light(d, 200, 200, 320, 300, .3, 24)
    for i in range(12):
        ang = np.radians(i * 30)
        r0, r1 = (78, 94) if i % 3 else (70, 94)
        w = 5 if i % 3 == 0 else 2.6
        a.line([(300 + r0 * np.sin(ang), 300 - r0 * np.cos(ang)), (300 + r1 * np.sin(ang), 300 - r1 * np.cos(ang))],
               (52, 54, 60), w)
    a.text(300, 248, "ABC", 13, (90, 92, 100), bold=True)
    a.text(300, 350, "QUARTZ", 9, (120, 122, 128))
    for ang, ln, w in ((-60, 52, 6), (60, 78, 4.5)):
        t = np.radians(ang)
        a.line([(300, 300), (300 + ln * np.sin(t), 300 - ln * np.cos(t))], (40, 42, 48), w)
    a.line([(300, 316), (300, 214)], (196, 72, 48), 1.6)
    a.dot(300, 300, 6, (40, 42, 48))
    a.dot(300, 300, 2.5, (196, 72, 48))
    return a


# ---------------------------------------------------------------- products
BLACK, WHITE, RED, BLUE = (40, 40, 44), (248, 247, 243), (196, 38, 42), (38, 84, 184)
GUM, DARK = (176, 128, 84), (46, 46, 50)

PRODUCTS = {
    "p01_nike_running_shoes": lambda: running_shoe(BLACK, (70, 72, 78), (244, 242, 236), DARK, (232, 232, 228)),
    "p02_adidas_running_shoes": lambda: running_shoe(WHITE, (150, 160, 176), (250, 249, 245), (70, 74, 82), (120, 130, 150)),
    "p03_black_leather_bag": lambda: tote((34, 33, 36), (26, 25, 28), (206, 168, 92)),
    "p04_blue_sports_shoes": lambda: court_shoe(BLUE, (24, 46, 104), (246, 245, 240), (60, 62, 68), WHITE, straps=True),
    "p05_nike_court_sneakers": lambda: court_shoe(WHITE, (30, 70, 60), (250, 249, 245), GUM, WHITE),
    "p06_red_canvas_backpack": lambda: backpack(RED, (70, 30, 30), (130, 84, 52)),
    "p07_black_cotton_tshirt": lambda: tshirt(BLACK),
    "p08_white_polo_shirt": lambda: polo(WHITE, (210, 206, 196)),
    "p09_blue_denim_cap": lambda: cap((52, 88, 150), texture=True),
    "p10_black_smart_watch": lambda: smart_watch((34, 34, 38), (70, 72, 78), (230, 70, 70)),
    "p11_silver_analog_watch": lambda: analog_watch((160, 165, 174), (246, 244, 238)),
    "p12_red_running_shoes": lambda: running_shoe(RED, (130, 24, 30), (246, 244, 238), DARK, (250, 250, 248)),
    "p13_white_cotton_tshirt": lambda: tshirt(WHITE, light_cloth=True),
    "p14_red_baseball_cap": lambda: cap(RED),
    "p15_blue_smart_watch": lambda: smart_watch(BLUE, (58, 66, 86), (90, 170, 240)),
    "p16_blue_canvas_backpack": lambda: backpack(BLUE, (24, 40, 80), (130, 84, 52)),
}

# query photo: (product it shows, backdrop centre, backdrop edge, scale, dx, dy, angle, light)
QUERIES = {
    "query_black_shoe": ("p01_nike_running_shoes", (204, 208, 212), (192, 196, 201), .9, 14, -8, 4, 1.04),
    "query_red_shoe": ("p12_red_running_shoes", (222, 214, 198), (206, 196, 178), .92, -12, 6, -3, .96),
    "query_white_shoe": ("p02_adidas_running_shoes", (196, 202, 210), (182, 189, 198), .88, 8, 10, 3, 1.0),
    "query_blue_shoe": ("p04_blue_sports_shoes", (226, 220, 206), (212, 204, 188), .9, -10, -6, -4, 1.03),
    "query_black_bag": ("p03_black_leather_bag", (218, 206, 186), (200, 186, 164), .9, 10, 4, 3, 1.05),
    "query_blue_backpack": ("p16_blue_canvas_backpack", (226, 222, 212), (212, 206, 194), .88, -8, 8, -3, .97),
    "query_black_tshirt": ("p07_black_cotton_tshirt", (214, 210, 202), (200, 195, 186), .9, 6, 6, 2, 1.04),
    "query_blue_cap": ("p09_blue_denim_cap", (230, 224, 212), (216, 208, 194), .92, -10, 4, -4, 1.0),
    "query_red_cap": ("p14_red_baseball_cap", (212, 214, 216), (198, 200, 203), .9, 12, -4, 3, .97),
    "query_silver_watch": ("p11_silver_analog_watch", (226, 216, 196), (210, 196, 172), .9, 8, -6, 5, 1.02),
}


def backdrop(centre, edge):
    y, x = np.mgrid[0:N, 0:N] / N
    d = np.clip(np.sqrt((x - .5) ** 2 + (y - .42) ** 2) / .72, 0, 1)[..., None]
    arr = np.array(centre, float) * (1 - d) + np.array(edge, float) * d
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def compose(art, centre, edge, shadow=16):
    bg = backdrop(centre, edge)
    alpha = art.layer.getchannel("A")
    sh = Image.new("L", (N, N), 0)
    sh.paste(alpha, (6 * SS, 12 * SS))
    sh = sh.filter(ImageFilter.GaussianBlur(10 * SS))
    dark = bg.point(lambda v: max(0, v - shadow))
    bg = Image.composite(dark, bg, sh)
    bg.paste(art.layer, (0, 0), alpha)
    return bg


def render_catalogue():
    out = os.path.join(DATA, "images")
    for name, draw in PRODUCTS.items():
        img = compose(draw(), *BACKDROP).resize((600, 600), Image.LANCZOS)
        img.save(os.path.join(out, name + ".png"), optimize=True)
        print("images/" + name + ".png")


def render_queries():
    rng = np.random.default_rng(2026)
    out = os.path.join(DATA, "query_images")
    for name, (product, centre, edge, scale, dx, dy, angle, light) in QUERIES.items():
        art = PRODUCTS[product]()
        layer = art.layer.rotate(angle, resample=Image.BICUBIC, center=(N / 2, N / 2))
        size = int(N * scale)
        layer = layer.resize((size, size), Image.LANCZOS)
        moved = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        moved.paste(layer, ((N - size) // 2 + dx * SS, (N - size) // 2 + dy * SS), layer)
        art.layer = moved
        img = compose(art, centre, edge, shadow=20).resize((360, 360), Image.LANCZOS)
        arr = np.asarray(img, float) * light + rng.normal(0, 3.5, (360, 360, 3))
        img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.4))
        img.save(os.path.join(out, name + ".png"), optimize=True)
        print("query_images/" + name + ".png")


if __name__ == "__main__":
    render_catalogue()
    render_queries()
