"""Service layer: UC01 Register Account, UC02 Login, role checks (NFR05 least privilege)."""
import hashlib
import os
import re

from model.customer import Customer, User
from service.errors import PermissionDenied, ValidationError

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.IGNORECASE)
ITERATIONS = 60_000


def hash_password(password, salt=None):
    salt = salt or os.urandom(8).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), ITERATIONS).hex()
    return f"{salt}${digest}"


def check_password(password, stored):
    salt, _ = stored.split("$", 1)
    return hash_password(password, salt) == stored


class AuthService:

    def __init__(self, db, customer_dao, audit_dao):
        self.db = db
        self.customers = customer_dao
        self.audit = audit_dao

    def register(self, name, email, password, address=None):
        email = email.strip().lower()
        problems = []
        if len(name.strip()) < 2:
            problems.append("name is required")
        if not EMAIL_RE.match(email):
            problems.append("email is not valid")
        elif self.customers.find_by_email(email):
            problems.append("email is already registered")
        if len(password) < 8:
            problems.append("password needs at least 8 characters")
        if address is not None and not address.is_complete():
            problems.append("delivery address is incomplete")
        if problems:
            raise ValidationError("; ".join(problems))
        customer = Customer(self.db.next_id("customer", "C"), name.strip(), email,
                            hash_password(password), "customer", address, self.db.now())
        self.customers.save_user(customer)
        self.audit.record(customer.user_id, "register", "user", customer.user_id)
        return customer

    def login(self, email, password):
        user = self.customers.find_by_email(email)
        if user is None or not check_password(password, user.password_hash):
            raise ValidationError("email or password is incorrect")   # no account enumeration
        return user

    def create_staff(self, user_id, name, email, password, role):
        user = User(user_id, name, email.lower(), hash_password(password), role)
        return self.customers.save_user(user)

    @staticmethod
    def require(user, permission):
        if user is None or not user.can(permission):
            raise PermissionDenied(f"'{permission}' is not permitted for this account")
        return user
