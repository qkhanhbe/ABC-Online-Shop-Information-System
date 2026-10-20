"""Presentation layer: the WSGI application - routes a request to one controller method.

A controller translates HTTP into one service call and back; it never touches a DAO and never
calculates anything. Service errors become messages for the user (alternative flows).
"""
import mimetypes
import os
import re
import traceback

from controller.account_controller import AccountController
from controller.http import STATUS_TEXT, Request, Response
from controller.order_controller import OrderController
from controller.report_controller import ReportController
from controller.shop_controller import ShopController
from controller.staff_controller import StaffController
from service.errors import NotFound, PermissionDenied, ServiceError
from view import templates

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "view", "static")


class WebApp:

    def __init__(self, shop):
        self.shop = shop
        account = AccountController(shop)
        store = ShopController(shop)
        orders = OrderController(shop)
        staff = StaffController(shop)
        reports = ReportController(shop)
        self.routes = [
            ("GET", r"/", store.home),
            ("GET", r"/search", store.search),
            ("POST", r"/search", store.search),
            ("GET", r"/product/(?P<product_id>\w+)", store.product),
            ("GET", r"/login", account.login_form),
            ("POST", r"/login", account.login),
            ("GET", r"/logout", account.logout),
            ("GET", r"/register", account.register_form),
            ("POST", r"/register", account.register),
            ("GET", r"/cart", orders.cart),
            ("POST", r"/cart/add", orders.add_to_cart),
            ("POST", r"/cart/update", orders.update_cart),
            ("GET", r"/checkout", orders.checkout_form),
            ("POST", r"/checkout", orders.checkout),
            ("GET", r"/orders", orders.history),
            ("GET", r"/orders/(?P<order_id>\w+)", orders.track),
            ("POST", r"/orders/(?P<order_id>\w+)/cancel", orders.cancel),
            ("POST", r"/orders/(?P<order_id>\w+)/review", orders.review),
            ("GET", r"/staff/orders", staff.orders),
            ("POST", r"/staff/orders/(?P<order_id>\w+)/(?P<action>\w+)", staff.order_action),
            ("GET", r"/staff/inventory", staff.inventory),
            ("POST", r"/staff/inventory", staff.inventory_event),
            ("GET", r"/admin/reviews", staff.reviews),
            ("POST", r"/admin/reviews/(?P<review_id>\w+)", staff.moderate),
            ("GET", r"/reports", reports.dashboard),
        ]

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch(request)
        headers = list(response.headers)
        if request.session_id:
            headers.append(("Set-Cookie", f"sid={request.session_id}; Path=/; HttpOnly; SameSite=Lax"))
        start_response(STATUS_TEXT.get(response.status, "200 OK"), headers)
        return [response.body]

    def dispatch(self, request):
        if request.path.startswith(("/static/", "/images/")):
            return self.static(request.path)
        user = self.shop.dao.customers.get_user(request.session.get("user_id", ""))
        request.user = user
        for method, pattern, handler in self.routes:
            match = re.fullmatch(pattern, request.path)
            if match and method == request.method:
                try:
                    return handler(request, **match.groupdict())
                except NotFound as e:
                    return Response(templates.message(request, "Not found", str(e)), 404)
                except PermissionDenied as e:
                    if user is None:
                        return Response.redirect("/login", "Please log in first.", request)
                    return Response(templates.message(request, "Not permitted", str(e)), 403)
                except ServiceError as e:
                    return Response(templates.message(request, "Request rejected", str(e)), 400)
                except Exception:                       # pragma: no cover - last resort
                    traceback.print_exc()
                    return Response(templates.message(request, "Error", "Unexpected error."), 500)
        return Response(templates.message(request, "Not found", request.path), 404)

    def static(self, path):
        if path.startswith("/images/"):
            full = self.shop.storage.path(path.lstrip("/"))
        else:
            full = os.path.join(STATIC_DIR, os.path.basename(path))
        if not os.path.isfile(full):
            return Response("not found", 404, "text/plain")
        with open(full, "rb") as f:
            return Response(f.read(), 200, mimetypes.guess_type(full)[0] or "application/octet-stream")
