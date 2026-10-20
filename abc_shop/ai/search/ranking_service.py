"""AI / application layer: orders the retrieved candidates (retrieval is not ranking).

S(x|q) = alpha * S_text + beta * S_image + gamma * S_business
  S_text     = matched query words / number of query words      (0..1)
  S_image    = cosine similarity of the image embeddings          (0..1)
  S_business = 0.8 * in_stock + 0.2 * min(stock, 20) / 20         (0..1)
"""

WEIGHTS = {
    "text": (0.9, 0.0, 0.1),
    "voice": (0.9, 0.0, 0.1),
    "image": (0.0, 0.9, 0.1),
}
GAMMA = 0.1


class RankingService:

    def business_score(self, available):
        in_stock = 1.0 if available > 0 else 0.0
        return 0.8 * in_stock + 0.2 * min(available, 20) / 20

    def weights(self, query):
        if query["type"] == "multimodal":
            lam = query.get("weights", {"text": 0.5, "image": 0.5})
            return lam["text"] * (1 - GAMMA), lam["image"] * (1 - GAMMA), GAMMA
        return WEIGHTS[query["type"]]

    def rank(self, candidates, query, k=5):
        alpha, beta, gamma = self.weights(query)
        n_terms = max(len(query.get("terms") or []), 1)

        ranked = []
        for c in candidates:
            s_text = c["text"] / n_terms
            s_image = max(c["image"], 0.0)
            s_business = self.business_score(c["available"])
            score = alpha * s_text + beta * s_image + gamma * s_business
            ranked.append({**c, "s_text": s_text, "s_image": s_image,
                           "s_business": s_business, "score": round(score, 4)})

        ranked.sort(key=lambda r: (-r["score"], -r["text"], -r["image"], r["product"].product_id))
        return ranked[:k]
