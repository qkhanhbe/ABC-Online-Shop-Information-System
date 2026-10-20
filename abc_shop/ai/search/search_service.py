"""AI / application layer: retrieval of candidate products and orders, then ranking.

R(q) = TopK_{x in X} s(q, x)

The service reads the shop's own DAOs, so search results show the same price and available
quantity as the catalogue page (one controlled source, BP01/BP02).
"""


def _stem(word):
    return word[:-1] if len(word) > 3 and word.endswith("s") else word


class SearchService:

    def __init__(self, product_dao, inventory_dao, order_dao, vector_index, ranking_service,
                 image_top_k=5):
        self.products = product_dao
        self.inventory = inventory_dao
        self.orders = order_dao
        self.vector_index = vector_index
        self.ranking = ranking_service
        self.image_top_k = image_top_k

    def search(self, query, k=5):
        """Products: retrieve C(q), rank it, keep the top-k. Orders: look them up."""
        if query["type"] == "order":
            return self.search_orders(query)
        return self.ranking.rank(self.retrieve(query), query, k)

    def search_text(self, terms, filters=None):
        """Keyword matching: score = number of query words found in the product text."""
        words = {_stem(w) for w in terms}
        filters = filters or {}
        results = []
        for product in self.products.list_products():
            if product.price > filters.get("max_price", float("inf")):
                continue
            text = f"{product.name} {product.category_id} {product.color} {product.brand}".lower()
            tokens = {_stem(t) for t in text.replace("-", " ").split()}
            score = sum(1 for w in words if w in tokens)
            if score > 0:
                results.append((product, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def search_image(self, query_embedding, k=None):
        """Vector similarity: [(product, cosine)] for the top-k most similar images."""
        hits = self.vector_index.search(query_embedding, k or self.image_top_k)
        found = [(self.products.get_product(pid), score) for pid, score in hits]
        return [(p, s) for p, s in found if p is not None and p.is_active()]

    def retrieve(self, query):
        """Candidate set C(q) for a common query object, still unranked."""
        candidates = {}

        def add(product, signal, value):
            entry = candidates.setdefault(product.product_id, {
                "product": product, "text": 0, "image": 0.0,
                "available": self.inventory.get_stock(product.product_id).available})
            entry[signal] = value

        if query.get("terms"):
            for product, score in self.search_text(query["terms"], query.get("filters")):
                add(product, "text", score)

        if query.get("embedding") is not None:
            for product, score in self.search_image(query["embedding"]):
                if product.price <= query.get("filters", {}).get("max_price", float("inf")):
                    add(product, "image", score)

        return list(candidates.values())

    def search_orders(self, query):
        """Order questions only ever see the orders of the customer in the session (FR11)."""
        own = self.orders.find_by_customer(query["customer_id"])
        if query.get("order_id"):
            return [o for o in own if o.order_id == query["order_id"]]
        if query.get("latest"):
            return own[:1]
        return own
