"""ABC Online Shop - entry point.

    python main.py seed                 create data/abc_shop.db with one month of history
    python main.py serve [--port 8000]  run the web application (seeds first if needed)
    python main.py demo                 end-to-end scenario printed step by step
    python main.py search --text "black shoes" | --voice "..." | --image FILE [--text ...]
"""
import argparse
import os
import sys
from wsgiref.simple_server import make_server

from seed import DB_PATH, seed
from shop import build_shop

HERE = os.path.dirname(os.path.abspath(__file__))


def show_results(results, query, shop, out=print):
    alpha, beta, gamma = shop.search.ranking.weights(query)
    out(f"  RankingService.rank -> top results (alpha, beta, gamma) = ({alpha:g}, {beta:g}, {gamma:g})")
    out(f"    #  {'Product':<22}{'Price':>6}{'Avail':>6}  keyword  cosine  S(x|q)")
    for i, r in enumerate(results, 1):
        p = r["product"]
        out(f"   {i:>2}  {p.name:<22}{p.price:>6g}{r['available']:>6}  {r['text']:>7}  {r['s_image']:.3f}   {r['score']:.3f}")


def run_search(shop, text=None, voice=None, image=None, customer_id="C001", out=print):
    if voice:
        out(f"  input (voice): <audio of '{voice}'>")
        text = shop.speech.transcribe(voice)
        out(f"  SpeechService.transcribe -> '{text}' (simulated STT)")
    elif text and not image:
        out(f"  input (text): '{text}'")
    if text and shop.query.is_order_question(text):
        query = shop.query.order_query(text, customer_id, "voice" if voice else "text")
        out(f"  QueryService -> order query (order_id={query['order_id']}, latest={query['latest']}, "
            f"customer={customer_id})")
        orders = shop.search.search(query)
        for o in orders:
            out(f"  Order: {o.order_id}  Status: {o.status}  Total: {o.calc_total():g}  Date: {o.created_at[:10]}")
        if not orders:
            out("  no order of this customer matches")
        return orders
    if image:
        out(f"  input ({'text + image' if text else 'image'}): {(repr(text) + ' + ') if text else ''}{os.path.basename(image)}")
        embedding = shop.image.encode(image)
        out("  ImageService.encode -> 128-d embedding")
        query = shop.query.multimodal_query(text, embedding) if text else shop.query.image_query(embedding)
    else:
        query = shop.query.voice_query(text) if voice else shop.query.text_query(text)
    if query.get("terms"):
        out(f"  QueryService -> terms={query['terms']} filters={query['filters']}")
    candidates = shop.search.retrieve(query)
    out(f"  SearchService.retrieve -> {len(candidates)} candidates")
    results = shop.search.ranking.rank(candidates, query)
    show_results(results, query, shop, out)
    return results


def demo(out=print):
    out("=== ABC Online Shop - end-to-end demo ===")
    out("\n--- 0. Seed: catalogue, accounts and October history (played through the services) ---")
    shop = seed(":memory:", verbose=False)
    out(f"  {len(shop.dao.products.list_products())} products, {len(shop.dao.orders.list_orders())} orders, "
        f"{len(shop.dao.reviews.list_reviews())} reviews")
    users = shop.dao.customers
    khanh, sales, warehouse, manager = (users.get_user(i) for i in ("C001", "S01", "W01", "M01"))
    q = "query_images"

    out("\n--- 1. Search (Chapter 3): text, voice, image, text + image ---")
    run_search(shop, text="black shoes", out=out)
    out("")
    run_search(shop, voice="find nike sneakers under 100 dollars", out=out)
    out("")
    run_search(shop, image=os.path.join(HERE, "data", q, "query_red_shoe.png"), out=out)
    out("")
    run_search(shop, text="running shoes", image=os.path.join(HERE, "data", q, "query_red_shoe.png"), out=out)

    out("\n--- 2. UC07 + UC08 checkout with promotion WELCOME10 ---")
    shop.cart.add_item("C001", "P12", 1)
    shop.cart.add_item("C001", "P09", 2)
    quote = shop.checkout.quote("C001", "WELCOME10")
    out(f"  cart: {[(l.product_id, l.quantity) for l in quote['cart'].items]}  subtotal {quote['subtotal']:g}  "
        f"discount {quote['discount']:g}  shipping {quote['shipping']:g}  total {quote['total']:g}")
    before = shop.inventory.stock_of("P12").available
    result = shop.checkout.place_order(khanh, "WELCOME10", "tok_visa", idempotency_key="demo-key-1")
    order = result["order"]
    out(f"  CheckoutService.place_order -> {order.order_id} {order.status} (payment {result['payment']})")
    out(f"  P12 available {before} -> {shop.inventory.stock_of('P12').available} (reserved for {order.order_id})")
    again = shop.checkout.place_order(khanh, "WELCOME10", "tok_visa", idempotency_key="demo-key-1")
    out(f"  same submission again -> {again['order'].order_id}, duplicate={again['duplicate']} (no second order/charge)")

    out("\n--- 3. Payment declined: order fails, reservation released, cart kept ---")
    shop.cart.add_item("C001", "P10", 1)
    failed = shop.checkout.place_order(khanh, "", "tok_declined")
    out(f"  {failed['order'].order_id}: {failed['order'].status}; P10 available "
        f"{shop.inventory.stock_of('P10').available}; cart still has "
        f"{[l.product_id for l in shop.cart.view('C001').items]}")

    out(f"\n--- 4. UC19 -> UC21 -> UC22 -> UC23: fulfilment of {order.order_id} ---")
    shop.orders.start_processing(sales, order.order_id)
    shipment = shop.shipping.mark_packed(warehouse, order.order_id)
    ref = shop.shipping.arrange_delivery(warehouse, order.order_id).carrier_ref
    out(f"  processed by S01, packed {shipment.shipment_id}, carrier ref {ref}")
    for seq, code in ((1, "PICKED_UP"), (2, "IN_TRANSIT"), (2, "IN_TRANSIT"), (1, "PICKED_UP"), (3, "DELIVERED")):
        accepted = shop.shipping.on_milestone(ref, seq, code, shop.db.now(), "carrier hub")
        out(f"  milestone {seq} {code:<10} -> {'accepted' if accepted else 'ignored (duplicate/older)'}")
    tracking = shop.orders.track("C001", order.order_id)
    out(f"  UC11 Track Order -> {tracking['status']}, {len(tracking['timeline'])} timeline entries")

    out("\n--- 5. Order questions are limited to the customer's own orders ---")
    run_search(shop, text="where is my latest order", out=out)
    run_search(shop, text="find my order O002", out=out)

    out("\n--- 6. AI review insights for P01 Nike Running Shoes ---")
    insight = shop.insights.analyse(shop.reviews.published("P01"))
    out(f"  {insight['reviews_used']} reviews used, {insight['reviews_skipped']} skipped -> {insight['label']}")
    for aspect, s in insight["aspects"].items():
        out(f"  {aspect:<9} +{s['positive']} -{s['negative']}  positive share {s['share_positive']:.2f}")
    pending = shop.reviews.moderation_queue(users.get_user("A01"))
    out(f"  waiting for moderation: {[(r.review_id, r.text[:30]) for r in pending]}")

    out("\n--- 7. Recommendations ---")
    shop.recommender.fit()
    for p, score, co in shop.recommender.similar("P01", 3):
        out(f"  similar to P01: {p.product_id} {p.name:<22} score {score:.3f} (bought together {co}x)")
    for p, score in shop.recommender.for_customer("C001", 3):
        out(f"  for C001:       {p.product_id} {p.name:<22} score {score:.3f}")

    out("\n--- 8. UC25 management dashboard ---")
    d = shop.reports.dashboard(manager)
    out(f"  orders {d['orders']}  revenue {d['revenue']:g}  average {d['average_order']:g}  "
        f"exceptions {d['exceptions']}  low stock {d['low_stock']}")
    return shop


def serve(port):
    from controller.router import WebApp
    if not os.path.exists(DB_PATH):
        seed()
    app = WebApp(build_shop(DB_PATH))
    print(f"ABC Online Shop on http://localhost:{port}  (Ctrl+C to stop)")
    make_server("127.0.0.1", port, app).serve_forever()


def main(argv=None):
    parser = argparse.ArgumentParser(description="ABC Online Shop")
    parser.add_argument("command", nargs="?", default="demo", choices=["seed", "serve", "demo", "search"])
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--text")
    parser.add_argument("--voice")
    parser.add_argument("--image")
    parser.add_argument("--customer", default="C001")
    args = parser.parse_args(argv)
    if args.command == "seed":
        seed()
    elif args.command == "serve":
        serve(args.port)
    elif args.command == "search":
        shop = build_shop(DB_PATH) if os.path.exists(DB_PATH) else seed(":memory:", verbose=False)
        run_search(shop, args.text, args.voice, args.image, args.customer)
    else:
        demo()


if __name__ == "__main__":
    sys.exit(main())
