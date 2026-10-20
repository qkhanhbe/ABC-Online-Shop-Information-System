"""Generates the sample product images and the query 'photos' used by the demo (from A6).

Product images: flat drawings on a white background. Query photos: the same kind of object
re-drawn at a different size/position, on a tinted background, with sensor noise - so an
image query is never a copy of a catalogue image.

    python tools/make_images.py
"""
import json
import os
import random

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
COLORS = {"black": (30, 30, 34), "white": (238, 238, 232), "blue": (40, 90, 200),
          "red": (205, 35, 40), "silver": (170, 172, 178)}
OUTLINE = (90, 90, 90)


def shoe(d, c, s, ox, oy):
    d.polygon([(ox + 10 * s, oy + 60 * s), (ox + 20 * s, oy + 30 * s), (ox + 45 * s, oy + 28 * s),
               (ox + 60 * s, oy + 45 * s), (ox + 92 * s, oy + 52 * s), (ox + 95 * s, oy + 66 * s),
               (ox + 10 * s, oy + 66 * s)], fill=c, outline=OUTLINE)
    d.rectangle([ox + 8 * s, oy + 66 * s, ox + 97 * s, oy + 73 * s], fill=(120, 120, 120))


def bag(d, c, s, ox, oy):
    d.arc([ox + 32 * s, oy + 10 * s, ox + 68 * s, oy + 50 * s], 180, 360, fill=OUTLINE,
          width=max(2, int(4 * s)))
    d.rectangle([ox + 18 * s, oy + 30 * s, ox + 82 * s, oy + 85 * s], fill=c, outline=OUTLINE)


def backpack(d, c, s, ox, oy):
    d.rounded_rectangle([ox + 25 * s, oy + 12 * s, ox + 75 * s, oy + 90 * s], radius=int(14 * s),
                        fill=c, outline=OUTLINE)
    d.rectangle([ox + 33 * s, oy + 55 * s, ox + 67 * s, oy + 80 * s], outline=OUTLINE)


def shirt(d, c, s, ox, oy):
    d.polygon([(ox + 30 * s, oy + 12 * s), (ox + 70 * s, oy + 12 * s), (ox + 95 * s, oy + 32 * s),
               (ox + 82 * s, oy + 44 * s), (ox + 72 * s, oy + 36 * s), (ox + 72 * s, oy + 90 * s),
               (ox + 28 * s, oy + 90 * s), (ox + 28 * s, oy + 36 * s), (ox + 18 * s, oy + 44 * s),
               (ox + 5 * s, oy + 32 * s)], fill=c, outline=OUTLINE)


def cap(d, c, s, ox, oy):
    d.chord([ox + 20 * s, oy + 25 * s, ox + 80 * s, oy + 85 * s], 180, 360, fill=c, outline=OUTLINE)
    d.rectangle([ox + 50 * s, oy + 53 * s, ox + 97 * s, oy + 60 * s], fill=c, outline=OUTLINE)


def watch(d, c, s, ox, oy):
    d.rectangle([ox + 40 * s, oy + 5 * s, ox + 60 * s, oy + 95 * s], fill=c, outline=OUTLINE)
    d.ellipse([ox + 28 * s, oy + 32 * s, ox + 72 * s, oy + 76 * s], fill=c, outline=OUTLINE,
              width=max(2, int(3 * s)))


SHAPES = {"shoes": shoe, "bag": bag, "shirt": shirt, "cap": cap, "watch": watch,
          "backpack": backpack}


def draw(shape, color, size=200, scale=2.0, offset=(0, 0), bg=(255, 255, 255)):
    img = Image.new("RGB", (size, size), bg)
    SHAPES.get(shape, shape)(ImageDraw.Draw(img), COLORS[color], scale, *offset)
    return img


def noisy(img, sigma, seed):
    rng = np.random.default_rng(seed)
    a = np.asarray(img, dtype=float) + rng.normal(0, sigma, (img.height, img.width, 3))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


QUERIES = [  # file, shape, colour  (photo of an object the customer has)
    ("query_black_shoe.png", "shoes", "black"),
    ("query_red_shoe.png", "shoes", "red"),
    ("query_white_shoe.png", "shoes", "white"),
    ("query_black_bag.png", "bag", "black"),
    ("query_blue_cap.png", "cap", "blue"),
    ("query_silver_watch.png", "watch", "silver"),
    ("query_black_tshirt.png", "shirt", "black"),
    ("query_blue_shoe.png", "shoes", "blue"),
    ("query_red_cap.png", "cap", "red"),
    ("query_blue_backpack.png", "backpack", "blue"),
]


def main():
    products = json.load(open(os.path.join(ROOT, "seed.json")))["products"]
    for p in products:
        shape = backpack if p["name"].endswith("Backpack") else p["category"]
        draw(shape, p["color"]).save(os.path.join(ROOT, p["image"]))

    rnd = random.Random(6)
    for i, (name, shape, color) in enumerate(QUERIES):
        bg = tuple(rnd.randint(200, 250) for _ in range(3))
        img = draw(shape, color, size=240, scale=rnd.uniform(1.7, 2.2),
                   offset=(rnd.randint(5, 30), rnd.randint(5, 30)), bg=bg)
        noisy(img, 8, i).save(os.path.join(ROOT, "query_images", name))
    print(f"{len(products)} product images, {len(QUERIES)} query images")


if __name__ == "__main__":
    main()
