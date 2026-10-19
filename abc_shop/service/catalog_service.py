"""Service layer: UC04 Browse Products, UC06 View Product Details, UC14 Manage Products,
UC16 Manage Promotions (Administrator, audited - NFR06)."""
from model.product import Product
from service.auth_service import AuthService
from service.errors import NotFound, ValidationError


class CatalogService:

    def __init__(self, db, product_dao, inventory_dao, promotion_dao, audit_dao):
        self.db = db
        self.products = product_dao
        self.inventory = inventory_dao
        self.promotions = promotion_dao
        self.audit = audit_dao

    def browse(self, category_id=None):
        """Active products with their current available quantity (one controlled source)."""
        return [self._card(p) for p in self.products.list_products(category_id)]

    def categories(self):
        return self.products.list_categories()

    def product_detail(self, product_id):
        product = self.products.get_product(product_id)
        if product is None or not product.is_active():
            raise NotFound("product not found")
        return self._card(product)

    def _card(self, product):
        stock = self.inventory.get_stock(product.product_id)
        return {"product": product, "available": stock.available,
                "status": "In stock" if stock.available > 0 else "Out of stock"}

    def save_product(self, admin, product):
        AuthService.require(admin, "catalogue")
        if not product.name.strip() or product.price <= 0:
            raise ValidationError("name and a positive price are required")
        old = self.products.get_product(product.product_id)
        with self.db.transaction():
            self.products.save_product(product)
            if old is None:                       # a new product starts with an empty stock level
                self.inventory.save_stock(self.inventory.get_stock(product.product_id))
            detail = f"price {old.price} -> {product.price}" if old else "created"
            self.audit.record(admin.user_id, "save_product", "product", product.product_id, detail)
        return product

    def change_price(self, admin, product_id, new_price):
        product = self.products.get_product(product_id)
        if product is None:
            raise NotFound("product not found")
        updated = Product(**{**product.__dict__})
        updated.update_price(new_price)
        return self.save_product(admin, updated)

    def set_status(self, admin, product_id, status):
        AuthService.require(admin, "catalogue")
        product = self.products.get_product(product_id)
        if product is None:
            raise NotFound("product not found")
        product.status = status
        self.products.save_product(product)
        self.audit.record(admin.user_id, "set_status", "product", product_id, status)
        return product

    def save_promotion(self, admin, promotion):
        AuthService.require(admin, "promotions")
        self.promotions.save_promotion(promotion)
        self.audit.record(admin.user_id, "save_promotion", "promotion", promotion.code,
                          f"{promotion.percent}% {promotion.start}..{promotion.end}")
        return promotion
