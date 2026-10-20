"""AI / application layer: converts every input modality into one common query object.

    text q_t -> z_t      voice q_v -> z_v      image q_i -> z_i

Changes since Assignment 06: a small synonym table ("sneakers" -> "shoes", the main error
class found in A6) and the order query always carries the customer id of the session.
"""
import re

STOPWORDS = {
    "a", "an", "the", "find", "show", "me", "my", "i", "want", "to", "buy", "search", "for",
    "please", "some", "any", "products", "product", "similar", "this", "is", "where", "of",
    "with", "and", "dollars", "dollar", "usd", "price", "in", "looking", "need", "pair",
}
SYNONYMS = {
    "sneaker": "shoes", "sneakers": "shoes", "trainers": "shoes", "shoe": "shoes",
    "handbag": "bag", "purse": "bag", "tee": "shirt", "t-shirt": "shirt", "tshirt": "shirt",
    "hat": "cap", "smartwatch": "watch", "rucksack": "backpack",
}
PRICE_RE = re.compile(r"\b(?:under|below|less than|cheaper than|max)\s*\$?\s*(\d+(?:\.\d+)?)")
ORDER_ID_RE = re.compile(r"\b(o\d{3,})\b", re.IGNORECASE)
ORDER_RE = re.compile(r"\border\b")
LATEST_RE = re.compile(r"\b(latest|last|recent)\b")


class QueryService:

    def text_query(self, text):
        return self._parse(text, "text")

    def voice_query(self, text):
        return self._parse(text, "voice")

    def image_query(self, embedding):
        return {"type": "image", "embedding": embedding, "terms": [], "filters": {}}

    def multimodal_query(self, text, embedding, text_weight=0.5):
        query = self._parse(text, "multimodal")
        query["embedding"] = embedding
        query["weights"] = {"text": text_weight, "image": 1.0 - text_weight}
        return query

    def order_query(self, text, customer_id, mode="text"):
        lowered = text.lower()
        match = ORDER_ID_RE.search(lowered)
        return {"type": "order", "source": mode, "query": text.strip(), "customer_id": customer_id,
                "order_id": match.group(1).upper() if match else None,
                "latest": bool(LATEST_RE.search(lowered))}

    def is_order_question(self, text):
        return bool(ORDER_RE.search(text.lower()))

    def _parse(self, text, mode):
        raw = text.strip()
        lowered = raw.lower()
        filters = {}
        price = PRICE_RE.search(lowered)
        if price:
            filters["max_price"] = float(price.group(1))
            lowered = PRICE_RE.sub(" ", lowered)
        words = re.findall(r"[a-z0-9\-]+", lowered)
        terms = [SYNONYMS.get(w, w) for w in words if w not in STOPWORDS]
        return {"type": mode, "query": raw, "terms": terms, "filters": filters}
