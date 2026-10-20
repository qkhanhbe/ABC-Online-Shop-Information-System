"""AI / application layer: aspect-based review insights (UC33 View Review Insights).

Assignment 02 proposed a PhoBERT aspect-based sentiment model for this job. The prototype
keeps the same interface - analyse(reviews) -> per-aspect sentiment + evidence - but uses a
transparent lexicon with negation handling, so it runs offline and every label can be
explained. A trained model can replace classify_clause() without changing any caller.

    review -> noise filter -> clauses -> aspect detection -> polarity -> aggregation
"""
import re
from collections import defaultdict

ASPECTS = {
    "quality": {"quality", "material", "durable", "sole", "stitching", "fabric", "leather",
                "battery", "strap", "comfortable", "comfort", "fit", "fits", "size", "build",
                "chat luong", "ben"},
    "price": {"price", "cheap", "expensive", "value", "money", "worth", "cost", "overpriced",
              "affordable", "gia"},
    "delivery": {"delivery", "shipping", "arrived", "late", "package", "packaging", "courier",
                 "shipped", "days", "giao hang"},
    "service": {"service", "support", "staff", "seller", "refund", "answered", "reply",
                "helpful", "rude", "tu van"},
}
POSITIVE = {"good", "great", "excellent", "love", "perfect", "fast", "quick", "comfortable",
            "durable", "nice", "worth", "cheap", "affordable", "helpful", "friendly", "solid",
            "recommend", "happy", "soft", "well", "beautiful", "tot", "dep", "nhanh"}
NEGATIVE = {"bad", "poor", "slow", "late", "broken", "expensive", "overpriced", "rude",
            "terrible", "cheaply", "worst", "damaged", "faded", "tight", "uncomfortable",
            "disappointed", "never", "loose", "wrong", "te", "cham", "hong"}
NEGATIONS = {"not", "no", "never", "isn't", "wasn't", "don't", "didn't", "khong"}
SPAM = re.compile(r"(https?://|www\.|\bclick\b|\bfree money\b|\bpromo code\b|\d{9,})", re.I)


class ReviewInsightService:

    def is_noise(self, text):
        """Noise filter: spam links, phone numbers, or text without any real words."""
        words = re.findall(r"[a-zA-Z]{2,}", text)
        return bool(SPAM.search(text)) or len(words) < 2 or bool(re.search(r"(.)\1{5,}", text))

    def split_clauses(self, text):
        return [c.strip() for c in re.split(r"[.!?;,]|\bbut\b|\bhowever\b", text.lower()) if c.strip()]

    def classify_clause(self, clause):
        """Return (aspects, polarity) for one clause; polarity is +1, -1 or 0."""
        tokens = re.findall(r"[a-z']+", clause)
        aspects = [a for a, words in ASPECTS.items()
                   if any(w in tokens or (" " in w and w in clause) for w in words)]
        score = 0
        for i, t in enumerate(tokens):
            value = 1 if t in POSITIVE else -1 if t in NEGATIVE else 0
            if value and any(n in tokens[max(0, i - 3):i] for n in NEGATIONS):
                value = -value
            score += value
        return aspects, (score > 0) - (score < 0)

    def analyse_review(self, text, rating=None):
        """{aspect: +1/-1} for one review; the star rating breaks ties for unmarked clauses."""
        result = {}
        for clause in self.split_clauses(text):
            aspects, polarity = self.classify_clause(clause)
            if polarity == 0 and rating is not None:
                polarity = 1 if rating >= 4 else -1 if rating <= 2 else 0
            for a in aspects:
                if polarity:
                    result[a] = polarity
        return result

    def analyse(self, reviews):
        """Aggregate published reviews of one product into per-aspect statistics + evidence."""
        stats = defaultdict(lambda: {"positive": 0, "negative": 0, "evidence": []})
        used, skipped = 0, 0
        for r in reviews:
            if self.is_noise(r.text):
                skipped += 1
                continue
            used += 1
            for aspect, polarity in self.analyse_review(r.text, r.rating).items():
                key = "positive" if polarity > 0 else "negative"
                stats[aspect][key] += 1
                if len(stats[aspect]["evidence"]) < 2:
                    stats[aspect]["evidence"].append((key, r.text))
        aspects = {}
        for a in ASPECTS:
            s = stats.get(a)
            if s and s["positive"] + s["negative"]:
                total = s["positive"] + s["negative"]
                aspects[a] = {**s, "share_positive": round(s["positive"] / total, 2)}
        return {"reviews_used": used, "reviews_skipped": skipped, "aspects": aspects,
                "label": self.label(aspects, used)}

    @staticmethod
    def label(aspects, used):
        if used < 2:
            return "Not enough reviews"
        pos = sum(a["positive"] for a in aspects.values())
        neg = sum(a["negative"] for a in aspects.values())
        if pos + neg == 0:
            return "Not enough reviews"
        share = pos / (pos + neg)
        return "Mostly positive" if share >= 0.7 else "Mixed" if share >= 0.4 else "Mostly negative"
