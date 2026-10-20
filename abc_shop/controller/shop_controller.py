"""Presentation layer: UC04 Browse Products, UC05 Search Products (text / voice / image /
text + image, Chapter 3), UC06 View Product Details with review insights and recommendations."""
from controller.http import Response
from view import templates


class ShopController:

    def __init__(self, shop):
        self.catalog = shop.catalog
        self.query = shop.query
        self.speech = shop.speech
        self.image = shop.image
        self.search_service = shop.search
        self.storage = shop.storage
        self.reviews = shop.reviews
        self.insights = shop.insights
        self.recommender = shop.recommender

    def home(self, request):
        category = request.get("category") or None
        return Response(templates.home(request, self.catalog.categories(),
                                       self.catalog.browse(category), category))

    def search(self, request):
        """SearchUI of Assignment 06: every mode becomes one common query object."""
        mode = request.get("mode", "text")
        text = request.get("q")
        trace = []
        if mode == "voice":
            text = self.speech.transcribe(text)
            trace.append(f"SpeechService.transcribe -> '{text}' (simulated speech-to-text)")
        if text and self.query.is_order_question(text):
            if request.user is None:
                return Response.redirect("/login", "Log in to search your orders.", request)
            query = self.query.order_query(text, request.user.user_id, mode)
            trace.append(f"QueryService -> order query (order_id={query['order_id']}, "
                         f"latest={query['latest']})")
            orders = self.search_service.search(query)
            return Response(templates.order_search(request, text, orders, trace))
        upload = request.files.get("image")
        if upload:
            path = self.storage.save_upload(*upload)
            embedding = self.image.encode(path)
            trace.append("ImageService.encode -> 128-d embedding")
            query = (self.query.multimodal_query(text, embedding) if text
                     else self.query.image_query(embedding))
        elif text:
            query = self.query.voice_query(text) if mode == "voice" else self.query.text_query(text)
        else:
            return Response.redirect("/", "Type, say or upload something to search.", request)
        if query.get("terms") is not None and query["type"] != "image":
            trace.append(f"QueryService -> terms={query['terms']} filters={query['filters']}")
        results = self.search_service.search(query)
        trace.append(f"SearchService.retrieve + RankingService.rank -> {len(results)} result(s)")
        return Response(templates.search_results(request, text, query["type"], results, trace))

    def product(self, request, product_id):
        card = self.catalog.product_detail(product_id)
        reviews = self.reviews.published(product_id)
        insight = self.insights.analyse(reviews)
        similar = self.recommender.similar(product_id, 4)
        return Response(templates.product(request, card, reviews, insight, similar))
