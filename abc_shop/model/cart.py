"""Model: Cart and CartItem (composition, UC07).

Each line computes its own sub_total(); the cart adds the lines (calc_total), so no class
reaches inside another to multiply prices. cart_price keeps the price at the moment of adding.
"""
from dataclasses import dataclass, field


@dataclass
class CartItem:
    product_id: str
    name: str
    cart_price: float
    quantity: int

    def sub_total(self):
        return round(self.cart_price * self.quantity, 2)


@dataclass
class Cart:
    cart_id: str
    customer_id: str
    items: list = field(default_factory=list)

    def find(self, product_id):
        return next((line for line in self.items if line.product_id == product_id), None)

    def add_item(self, product, quantity=1):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        line = self.find(product.product_id)
        if line:
            line.quantity += quantity
            return line
        line = CartItem(product.product_id, product.name, product.price, quantity)
        self.items.append(line)
        return line

    def update_quantity(self, product_id, quantity):
        line = self.find(product_id)
        if line is None:
            raise KeyError(product_id)
        if quantity <= 0:
            self.items.remove(line)
        else:
            line.quantity = quantity

    def remove_item(self, product_id):
        self.items = [line for line in self.items if line.product_id != product_id]

    def calc_total(self):
        return round(sum(line.sub_total() for line in self.items), 2)

    def is_empty(self):
        return not self.items

    def clear(self):
        self.items = []
