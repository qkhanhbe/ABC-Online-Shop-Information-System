"""DAO (data) layer: a tiny in-memory vector index - stands in for a vector database.

Kept from Assignment 06. build() receives the encoder as a function, so the data layer never
imports the application layer that owns the encoder (dependencies point downwards).
"""
import numpy as np


def cosine_similarity(a, b):
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


class VectorIndex:

    def __init__(self):
        self.vectors = {}

    @classmethod
    def build(cls, storage, products, encode):
        index = cls()
        for p in products:
            if p.image and storage.exists(p.image):
                index.add(p.product_id, encode(storage.path(p.image)))
        return index

    def add(self, product_id, embedding):
        self.vectors[product_id] = np.asarray(embedding, dtype=float)

    def __len__(self):
        return len(self.vectors)

    def search(self, query_embedding, k=None):
        """Return [(product_id, cosine)] sorted by similarity, top-k if k is given."""
        scores = [(pid, cosine_similarity(query_embedding, emb)) for pid, emb in self.vectors.items()]
        scores.sort(key=lambda x: (-x[1], x[0]))
        return scores[:k] if k else scores
