"""The web layer end to end: WSGI requests through controller -> service -> DAO."""
import io
from urllib.parse import urlencode
from wsgiref.util import setup_testing_defaults

import pytest

from controller.router import WebApp


class Client:

    def __init__(self, app):
        self.app, self.cookie = app, ""

    def request(self, method, path, data=None):
        path, _, qs = path.partition("?")
        body = urlencode(data or {}).encode()
        env = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": qs,
               "CONTENT_TYPE": "application/x-www-form-urlencoded", "CONTENT_LENGTH": str(len(body)),
               "wsgi.input": io.BytesIO(body), "HTTP_COOKIE": self.cookie}
        setup_testing_defaults(env)
        status, headers = {}, {}

        def start_response(s, h):
            status["code"] = int(s.split()[0])
            headers.update(h)
        page = b"".join(self.app(env, start_response)).decode()
        if "Set-Cookie" in headers:
            self.cookie = headers["Set-Cookie"].split(";")[0]
        return status["code"], headers, page

    def login(self, email, password):
        return self.request("POST", "/login", {"email": email, "password": password})


@pytest.fixture
def client(shop):
    return Client(WebApp(shop))


def test_catalogue_and_product_page_with_ai_sections(client):
    code, _, page = client.request("GET", "/")
    assert code == 200 and "Nike Running Shoes" in page
    code, _, page = client.request("GET", "/product/P01")
    assert "AI review insights" in page and "Customers also like" in page


def test_search_shows_the_processing_steps(client):
    code, _, page = client.request("GET", "/search?q=black+shoes")
    assert code == 200 and "RankingService.rank" in page and "Nike Running Shoes" in page


def test_customer_buys_through_the_web(client, shop):
    assert client.login("khanh@example.com", "khanh2026")[0] == 302
    client.request("POST", "/cart/add", {"product_id": "P09", "qty": "1"})
    _, _, page = client.request("GET", "/cart")
    assert "Blue Denim Cap" in page
    code, headers, _ = client.request("POST", "/checkout", {"card": "tok_visa", "key": "web-1"})
    assert code == 302 and headers["Location"].startswith("/orders/O017")
    _, _, page = client.request("GET", "/orders/O017")
    assert "Paid/Confirmed" in page


def test_roles_are_enforced_on_screens(client):
    code, headers, _ = client.request("GET", "/reports")
    assert code == 302 and headers["Location"] == "/login"
    client.login("khanh@example.com", "khanh2026")
    assert client.request("GET", "/reports")[0] == 403
    assert client.request("GET", "/orders/O002")[0] == 404
    client.request("GET", "/logout")
    client.login("manager@abc.vn", "report2026")
    code, _, page = client.request("GET", "/reports")
    assert code == 200 and "Management dashboard" in page
