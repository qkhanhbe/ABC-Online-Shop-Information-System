"""AI components of Chapter 3: search, review insights, recommender."""
import os

from model.review import Review

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def top(shop, query):
    results = shop.search.search(query)
    return results[0]["product"].product_id if results else None


def test_text_voice_and_price_filter(shop):
    assert top(shop, shop.query.text_query("black shoes")) == "P01"
    voice = shop.query.voice_query(shop.speech.transcribe("  find   nike shoes under 100 dollars "))
    assert voice["filters"] == {"max_price": 100.0}
    assert top(shop, voice) == "P05"


def test_synonyms_map_sneakers_to_shoes(shop):
    assert shop.query.text_query("nike sneakers")["terms"] == ["nike", "shoes"]


def test_image_and_multimodal_search(shop):
    emb = shop.image.encode(os.path.join(HERE, "data", "query_images", "query_red_shoe.png"))
    assert top(shop, shop.query.image_query(emb)) == "P12"
    assert top(shop, shop.query.multimodal_query("running shoes", emb)) == "P12"


def test_ranking_is_stock_aware(shop):
    results = shop.search.search(shop.query.text_query("nike shoes"))
    court = next(r for r in results if r["product"].product_id == "P05")
    assert court["s_business"] == 0.0                     # out of stock


def test_order_questions_only_see_own_orders(shop):
    q = shop.query.order_query("find my order O002", "C001")
    assert shop.search.search(q) == []
    q = shop.query.order_query("find my order O002", "C002")
    assert [o.order_id for o in shop.search.search(q)] == ["O002"]
    latest = shop.search.search(shop.query.order_query("where is my latest order?", "C001"))
    assert [o.order_id for o in latest] == ["O016"]


def test_review_insights_handle_negation_and_noise(shop):
    ins = shop.insights
    assert ins.analyse_review("Shipping was not fast at all.") == {"delivery": -1}
    assert ins.analyse_review("Affordable price and nice fabric.") == {"price": 1, "quality": 1}
    assert ins.is_noise("Click www.free-money.biz now")
    reviews = [Review("R1", "P1", "C1", "O1", 5, "Great quality, fast delivery."),
               Review("R2", "P1", "C2", "O2", 2, "Delivery was late."),
               Review("R3", "P1", "C3", "O3", 5, "!!!!!!!!")]
    result = ins.analyse(reviews)
    assert result["reviews_skipped"] == 1
    assert result["aspects"]["delivery"]["positive"] == 1 and result["aspects"]["delivery"]["negative"] == 1


def test_recommender_never_suggests_out_of_stock_or_bought_items(shop):
    shop.recommender.fit()
    similar = [p.product_id for p, _, _ in shop.recommender.similar("P01", 10)]
    assert "P05" not in similar and "P01" not in similar
    bought = {i.product_id for o in shop.dao.orders.find_by_customer("C001")
              if o.status not in ("Cancelled", "Payment Failed") for i in o.items}
    assert not {p.product_id for p, _ in shop.recommender.for_customer("C001")} & bought
