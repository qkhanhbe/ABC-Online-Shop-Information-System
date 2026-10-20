"""Composition root: the only module that creates every object and connects the layers.

    controller/view (presentation) -> service + ai (application) -> dao (data)

Every class receives its collaborators through its constructor, so a test can replace any
DAO or gateway with a fake, and a real payment provider or speech engine can be plugged in
here without changing the class that uses it.
"""
from types import SimpleNamespace

from ai.recommender import RecommenderService
from ai.review_insights import ReviewInsightService
from ai.search.image_service import ImageService
from ai.search.query_service import QueryService
from ai.search.ranking_service import RankingService
from ai.search.search_service import SearchService
from ai.search.speech_service import SpeechService
from dao import sqlite_dao
from dao.database import Database
from dao.image_storage import ImageStorage
from dao.vector_index import VectorIndex
from service.auth_service import AuthService
from service.cart_service import CartService
from service.catalog_service import CatalogService
from service.checkout_service import CheckoutService
from service.gateways import SimulatedCarrier, SimulatedPaymentProvider
from service.inventory_service import InventoryService
from service.order_service import OrderService
from service.payment_service import PaymentService
from service.report_service import ReportService
from service.review_service import ReviewService
from service.shipment_service import ShipmentService


def build_shop(db_path=":memory:", clock=None, payment_gateway=None, carrier=None):
    db = Database(db_path, clock).init_schema()

    # data layer
    customers = sqlite_dao.SqliteCustomerDAO(db)
    products = sqlite_dao.SqliteProductDAO(db)
    inventory = sqlite_dao.SqliteInventoryDAO(db)
    carts = sqlite_dao.SqliteCartDAO(db)
    promotions = sqlite_dao.SqlitePromotionDAO(db)
    orders = sqlite_dao.SqliteOrderDAO(db)
    payments = sqlite_dao.SqlitePaymentDAO(db)
    shipments = sqlite_dao.SqliteShipmentDAO(db)
    reviews = sqlite_dao.SqliteReviewDAO(db)
    audit = sqlite_dao.SqliteAuditDAO(db)
    storage = ImageStorage()

    # application layer: business services
    payment_gateway = payment_gateway or SimulatedPaymentProvider()
    carrier = carrier or SimulatedCarrier()
    insight_service = ReviewInsightService()
    inventory_service = InventoryService(db, inventory, products, audit)
    payment_service = PaymentService(db, payments, orders, inventory_service, payment_gateway, audit)
    cart_service = CartService(carts, products, inventory)

    s = SimpleNamespace(db=db, storage=storage, payment_gateway=payment_gateway, carrier=carrier)
    s.dao = SimpleNamespace(customers=customers, products=products, inventory=inventory, carts=carts,
                            promotions=promotions, orders=orders, payments=payments,
                            shipments=shipments, reviews=reviews, audit=audit)
    s.auth = AuthService(db, customers, audit)
    s.catalog = CatalogService(db, products, inventory, promotions, audit)
    s.cart = cart_service
    s.inventory = inventory_service
    s.payment = payment_service
    s.checkout = CheckoutService(db, carts, orders, promotions, cart_service, inventory_service,
                                 payment_service)
    s.orders = OrderService(db, orders, shipments, payment_service, inventory_service, audit)
    s.shipping = ShipmentService(db, shipments, orders, inventory_service, carrier, audit)
    s.reviews = ReviewService(db, reviews, orders, audit, insight_service)
    s.reports = ReportService(db, orders, products, inventory, audit)

    # application layer: AI components (Chapter 3)
    s.query = QueryService()
    s.speech = SpeechService()
    s.image = ImageService()
    s.insights = insight_service
    s.recommender = RecommenderService(products, inventory, orders)
    s.rebuild_index = lambda: _rebuild_index(s)
    s.search = SearchService(products, inventory, orders, VectorIndex(), RankingService())
    s.rebuild_index()
    return s


def _rebuild_index(shop):
    """The encoder is passed into the data layer, which never imports the AI layer."""
    shop.search.vector_index = VectorIndex.build(shop.storage, shop.dao.products.list_products(),
                                                 shop.image.encode)
    return shop.search.vector_index
