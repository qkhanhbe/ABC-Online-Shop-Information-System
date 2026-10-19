"""Service layer: UC07 Manage Shopping Cart, UC29 Validate Cart, UC30 Check Product Availability."""
from service.errors import NotFound, ValidationError


class CartService:

    def __init__(self, cart_dao, product_dao, inventory_dao):
        self.carts = cart_dao
        self.products = product_dao
        self.inventory = inventory_dao

    def view(self, customer_id):
        return self.carts.get_cart(customer_id)

    def add_item(self, customer_id, product_id, quantity=1):
        product = self.products.get_product(product_id)
        if product is None or not product.is_active():
            raise NotFound("product is not available for sale")
        cart = self.carts.get_cart(customer_id)
        line = cart.find(product_id)
        wanted = quantity + (line.quantity if line else 0)
        self.check_availability(product_id, wanted)              # UC30 (included)
        cart.add_item(product, quantity)
        return self.carts.update_cart(cart)

    def update_quantity(self, customer_id, product_id, quantity):
        cart = self.carts.get_cart(customer_id)
        if quantity > 0:
            self.check_availability(product_id, quantity)
        cart.update_quantity(product_id, quantity)
        return self.carts.update_cart(cart)

    def remove_item(self, customer_id, product_id):
        cart = self.carts.get_cart(customer_id)
        cart.remove_item(product_id)
        return self.carts.update_cart(cart)

    def check_availability(self, product_id, quantity):
        available = self.inventory.get_stock(product_id).available
        if quantity > available:
            raise ValidationError(f"only {available} item(s) of {product_id} are available")
        return available

    def validate_cart(self, cart):
        """UC29: every line must be active and orderable; prices become authoritative here.

        Returns a list of problems (A1/A2 of UC08). A changed price is refreshed in the cart
        and reported, so the customer confirms the real amount before paying.
        """
        problems = []
        if cart.is_empty():
            return ["the cart is empty"]
        for line in cart.items:
            product = self.products.get_product(line.product_id)
            if product is None or not product.is_active():
                problems.append(f"{line.name} is no longer sold")
                continue
            available = self.inventory.get_stock(line.product_id).available
            if line.quantity > available:
                problems.append(f"{line.name}: only {available} available")
            if abs(product.price - line.cart_price) > 0.001:
                problems.append(f"{line.name}: price changed {line.cart_price} -> {product.price}")
                line.cart_price = product.price
        if problems:
            self.carts.update_cart(cart)
        return problems
