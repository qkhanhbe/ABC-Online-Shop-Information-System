"""AI / application layer: product recommendation (UC34 View Recommendations).

Two signals, both computed from the shop's own records:
  * content similarity  - TF-IDF vectors of name, category, brand, colour and description,
                          compared with cosine similarity ("similar products")
  * co-purchase         - how often two products were bought in the same order
                          ("customers who bought this also bought")

    score(p, q) = 0.7 * cos(tfidf_p, tfidf_q) + 0.3 * copurchase(p, q) / max_copurchase
Out-of-stock products are never recommended (stock-aware, as in the search ranking).
"""
import math
import re
from collections import Counter, defaultdict

import numpy as np

CONTENT_WEIGHT = 0.7


def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


class RecommenderService:

    def __init__(self, product_dao, inventory_dao, order_dao):
        self.products = product_dao
        self.inventory = inventory_dao
        self.orders = order_dao
        self.ids, self.matrix, self.copurchase = [], None, defaultdict(Counter)

    def fit(self):
        """Build the TF-IDF matrix and the co-purchase counts (call again after new orders)."""
        products = self.products.list_products()
        docs = [_tokens(p.search_text()) for p in products]
        vocab = sorted({t for d in docs for t in d})
        df = Counter(t for d in docs for t in set(d))
        idf = {t: math.log((1 + len(docs)) / (1 + df[t])) + 1 for t in vocab}
        col = {t: i for i, t in enumerate(vocab)}
        matrix = np.zeros((len(docs), len(vocab)))
        for row, d in enumerate(docs):
            for t, n in Counter(d).items():
                matrix[row, col[t]] = n * idf[t]
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        self.matrix = matrix / np.where(norms == 0, 1, norms)
        self.ids = [p.product_id for p in products]

        self.copurchase = defaultdict(Counter)
        for o in self.orders.list_orders():
            if o.status in ("Cancelled", "Payment Failed"):
                continue
            bought = {i.product_id for i in o.items}
            for a in bought:
                for b in bought - {a}:
                    self.copurchase[a][b] += 1
        return self

    def similar(self, product_id, k=4):
        if self.matrix is None:
            self.fit()
        if product_id not in self.ids:
            return []
        row = self.ids.index(product_id)
        content = self.matrix @ self.matrix[row]
        co = self.copurchase[product_id]
        max_co = max(co.values(), default=0) or 1
        scored = []
        for j, pid in enumerate(self.ids):
            if pid == product_id or self.inventory.get_stock(pid).available <= 0:
                continue
            score = CONTENT_WEIGHT * content[j] + (1 - CONTENT_WEIGHT) * co[pid] / max_co
            scored.append((pid, round(float(score), 3), int(co[pid])))
        scored.sort(key=lambda x: (-x[1], x[0]))
        return [(self.products.get_product(pid), s, n) for pid, s, n in scored[:k]]

    def for_customer(self, customer_id, k=4):
        """Sum the similarity to everything the customer bought; never re-recommend a purchase."""
        bought = {i.product_id for o in self.orders.find_by_customer(customer_id)
                  if o.status not in ("Cancelled", "Payment Failed") for i in o.items}
        totals = Counter()
        for pid in bought:
            for product, score, _ in self.similar(pid, k=len(self.ids)):
                if product.product_id not in bought:
                    totals[product.product_id] += score
        best = sorted(totals.items(), key=lambda x: (-x[1], x[0]))[:k]
        return [(self.products.get_product(pid), round(s, 3)) for pid, s in best]
