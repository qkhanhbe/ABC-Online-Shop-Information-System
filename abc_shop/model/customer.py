"""Model: users of the system (Customer and the four staff roles).

Analysis class diagram: Customer specialises User; Staff roles share Login (UC02) only.
Methods of the class itself (design Step 1): update_profile, can.
"""
from dataclasses import dataclass
from typing import Optional

ROLES = ("customer", "sales", "warehouse", "admin", "manager")

# role -> permissions (least privilege, NFR05)
PERMISSIONS = {
    "customer": {"cart", "checkout", "own_orders", "review"},
    "sales": {"process_orders", "customers"},
    "warehouse": {"inventory", "shipment"},
    "admin": {"catalogue", "promotions", "moderate_reviews", "customers"},
    "manager": {"reports"},
}


@dataclass
class Address:
    receiver: str
    phone: str
    street: str
    city: str

    def is_complete(self):
        return all(v and v.strip() for v in (self.receiver, self.phone, self.street, self.city))

    def one_line(self):
        return f"{self.receiver}, {self.phone}, {self.street}, {self.city}"


@dataclass
class User:
    user_id: str
    name: str
    email: str
    password_hash: str
    role: str = "customer"

    def can(self, permission):
        return permission in PERMISSIONS.get(self.role, set())


@dataclass
class Customer(User):
    address: Optional[Address] = None
    created_at: str = ""

    def update_profile(self, name=None, address=None):
        if name:
            self.name = name.strip()
        if address is not None:
            if not address.is_complete():
                raise ValueError("delivery address is incomplete")
            self.address = address
        return self
