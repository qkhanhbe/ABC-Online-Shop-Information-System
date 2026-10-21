"""Offline evaluation of the three AI components (Chapter 3, Section "Evaluation").

  1. Search      - top-1 success rate on 26 test queries (the 20 of Assignment 06 + 6 new)
  2. Insights    - aspect detection precision / recall and polarity accuracy on 30 labelled reviews
  3. Recommender - category hit rate of the top-3 similar products, catalogue coverage

    python evaluate.py
"""
import json
import os
from collections import Counter

from main import HERE
from seed import seed

Q = os.path.join(HERE, "data", "query_images")

# mode, text, image, expected top-1 (product id, or order id for order questions)
SEARCH_TESTS = [
    ("text", "black shoes", None, "P01"),
    ("text", "white polo shirt", None, "P08"),
    ("text", "find Nike shoes under 100 dollars", None, "P05"),
    ("text", "red bag", None, "P06"),
    ("text", "cheap watch under 60", None, "P11"),
    ("text", "leather handbag", None, "P03"),
    ("voice", "find running shoes", None, "P02"),
    ("voice", "show me a blue cap", None, "P09"),
    ("voice", "i want a smart watch", None, "P10"),
    ("image", None, "query_black_shoe.png", "P01"),
    ("image", None, "query_red_shoe.png", "P12"),
    ("image", None, "query_white_shoe.png", "P02"),
    ("image", None, "query_black_bag.png", "P03"),
    ("image", None, "query_blue_cap.png", "P09"),
    ("image", None, "query_silver_watch.png", "P11"),
    ("image", None, "query_black_tshirt.png", "P07"),
    ("multimodal", "running shoes", "query_red_shoe.png", "P12"),
    ("multimodal", "nike", "query_white_shoe.png", "P05"),
    ("text", "find my order O001", None, "O001"),
    ("voice", "where is my latest order", None, "O016"),
    # new in the essay
    ("text", "white sneakers", None, "P05"),
    ("voice", "blue smartwatch", None, "P15"),
    ("image", None, "query_red_cap.png", "P14"),
    ("image", None, "query_blue_backpack.png", "P16"),
    ("multimodal", "cap", "query_blue_cap.png", "P09"),
    ("text", "find my order O002", None, None),          # O002 belongs to C002: must stay hidden
]


def evaluate_search(shop, out=print):
    out(f" {'#':>2}  {'Mode':<10} {'Query':<38} {'Top-1 result':<24} {'Score':>6}  Success")
    ok, per_mode = 0, Counter()
    for i, (mode, text, image, expected) in enumerate(SEARCH_TESTS, 1):
        if text and shop.query.is_order_question(text):
            orders = shop.search.search(shop.query.order_query(text, "C001", mode))
            got, score = (orders[0].order_id if orders else None), "-"
        else:
            if image:
                emb = shop.image.encode(os.path.join(Q, image))
                query = shop.query.multimodal_query(text, emb) if text else shop.query.image_query(emb)
            else:
                query = shop.query.voice_query(text) if mode == "voice" else shop.query.text_query(text)
            results = shop.search.search(query)
            got = results[0]["product"].product_id if results else None
            score = f"{results[0]['score']:.3f}" if results else "-"
        success = got == expected
        ok += success
        per_mode[(mode if not (text and "order" in text) else "order", success)] += 1
        label = " + ".join(x for x in (text, image) if x)
        name = (shop.dao.products.get_product(got).name if got and got.startswith("P") else got) or "(nothing)"
        out(f" {i:>2}  {mode:<10} {label[:38]:<38} {name[:24]:<24} {score:>6}  "
            f"{'Yes' if success else 'No (expected ' + str(expected) + ')'}")
    out(f"\n Total queries: {len(SEARCH_TESTS)}   Successful: {ok}   "
        f"Success rate: {ok / len(SEARCH_TESTS) * 100:.1f}%")
    modes = sorted({m for m, _ in per_mode})
    out(" Per mode: " + ", ".join(f"{m} {per_mode[(m, True)]}/{per_mode[(m, True)] + per_mode[(m, False)]}"
                                   for m in modes))
    return ok, len(SEARCH_TESTS)


def evaluate_insights(shop, out=print):
    with open(os.path.join(HERE, "data", "reviews_labeled.json"), encoding="utf-8") as f:
        data = json.load(f)
    tp = fp = fn = polarity_ok = 0
    errors = []
    for r in data:
        predicted = shop.insights.analyse_review(r["text"], r["rating"])
        gold = r["labels"]
        for aspect in set(predicted) | set(gold):
            if aspect in predicted and aspect in gold:
                tp += 1
                polarity_ok += predicted[aspect] == gold[aspect]
                if predicted[aspect] != gold[aspect]:
                    errors.append((r["text"], aspect, "polarity"))
            elif aspect in predicted:
                fp += 1
                errors.append((r["text"], aspect, "extra aspect"))
            else:
                fn += 1
                errors.append((r["text"], aspect, "missed aspect"))
    precision, recall = tp / (tp + fp), tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    out(f" Reviews: {len(data)}   gold aspect labels: {tp + fn}   predicted: {tp + fp}")
    out(f" Aspect detection  precision {precision:.2f}  recall {recall:.2f}  F1 {f1:.2f}")
    out(f" Polarity accuracy on detected aspects: {polarity_ok}/{tp} = {polarity_ok / tp:.2f}")
    out(" Errors:")
    for text, aspect, kind in errors:
        out(f"   - {kind:<13} {aspect:<9} \"{text}\"")
    return precision, recall, polarity_ok / tp


def evaluate_recommender(shop, out=print):
    shop.recommender.fit()
    products = shop.dao.products.list_products()
    hits = total = 0
    shown = set()
    for p in products:
        recs = shop.recommender.similar(p.product_id, 3)
        shown |= {q.product_id for q, _, _ in recs}
        hits += sum(q.category_id == p.category_id for q, _, _ in recs)
        total += len(recs)
    in_stock = [p for p in products if shop.dao.inventory.get_stock(p.product_id).available > 0]
    out(f" Same-category hit rate of top-3 similar products: {hits}/{total} = {hits / total:.2f}")
    out(f" Catalogue coverage: {len(shown)}/{len(in_stock)} in-stock products appear in some top-3 list")
    out(f" Out-of-stock products recommended: "
        f"{sum(1 for p in shown if shop.dao.inventory.get_stock(p).available <= 0)}")
    return hits / total


def main(out=print):
    shop = seed(":memory:", verbose=False)
    out("=== 1. Multimodal search ===")
    evaluate_search(shop, out)
    out("\n=== 2. Review insights (aspect-based sentiment) ===")
    evaluate_insights(shop, out)
    out("\n=== 3. Recommender ===")
    evaluate_recommender(shop, out)


if __name__ == "__main__":
    main()
