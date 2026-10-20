"""Presentation layer: UC01 Register Account, UC02 Login."""
from controller.http import Response
from model.customer import Address
from service.errors import ValidationError
from view import templates


class AccountController:

    def __init__(self, shop):
        self.auth = shop.auth

    def login_form(self, request):
        return Response(templates.login(request))

    def login(self, request):
        try:
            user = self.auth.login(request.get("email"), request.get("password"))
        except ValidationError as e:
            return Response(templates.login(request, str(e)), 400)
        request.session["user_id"] = user.user_id
        home = {"customer": "/", "sales": "/staff/orders", "warehouse": "/staff/inventory",
                "admin": "/admin/reviews", "manager": "/reports"}[user.role]
        return Response.redirect(home, f"Welcome, {user.name}.", request)

    def logout(self, request):
        request.session.clear()
        return Response.redirect("/", "You are logged out.", request)

    def register_form(self, request):
        return Response(templates.register(request))

    def register(self, request):
        address = Address(request.get("name"), request.get("phone"), request.get("street"),
                          request.get("city"))
        try:
            customer = self.auth.register(request.get("name"), request.get("email"),
                                          request.get("password"), address)
        except ValidationError as e:
            return Response(templates.register(request, str(e)), 400)
        request.session["user_id"] = customer.user_id
        return Response.redirect("/", f"Account {customer.user_id} created.", request)
