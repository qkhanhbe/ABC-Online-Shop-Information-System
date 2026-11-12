"""Capture screenshots of the running web app (python abc_shop/main.py serve; SHOP_URL overrides the address) with headless Edge."""
import http.cookiejar
import os
import subprocess
import urllib.parse
import urllib.request

BASE = os.environ.get("SHOP_URL", "http://127.0.0.1:8000")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "demo_results")
TMP = os.environ.get("TEMP", os.path.dirname(os.path.abspath(__file__)))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def session():
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def fetch(opener, path, data=None):
    body = urllib.parse.urlencode(data).encode() if data else None
    return opener.open(BASE + path, body).read().decode()


def shot(html, name, height=1100):
    html = html.replace('href="/static/', f'href="{BASE}/static/').replace('src="/', f'src="{BASE}/').replace("src='/", f"src='{BASE}/")
    path = os.path.join(TMP, name + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    png = os.path.abspath(os.path.join(OUT, name + ".png"))
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size=1280,{height}", f"--screenshot={png}",
                    "file:///" + path.replace("\\", "/")], check=True, capture_output=True, timeout=60)
    os.remove(path)
    print("saved", png)


def main():
    guest = session()
    shot(fetch(guest, "/"), "web_01_catalogue", 1250)
    shot(fetch(guest, "/search?q=find+nike+sneakers+under+100+dollars&mode=voice"), "web_02_search_voice", 900)
    shot(fetch(guest, "/product/P01"), "web_03_product_ai", 1450)
    shot(fetch(guest, "/product/P16"), "web_03b_product_bag", 1250)

    khanh = session()
    fetch(khanh, "/login", {"email": "khanh@example.com", "password": "khanh2026"})
    fetch(khanh, "/cart/add", {"product_id": "P12", "qty": "1"})
    fetch(khanh, "/cart/add", {"product_id": "P09", "qty": "2"})
    shot(fetch(khanh, "/checkout?promo=WELCOME10"), "web_04_checkout", 900)
    shot(fetch(khanh, "/orders/O001"), "web_05_track_order", 1100)
    shot(fetch(khanh, "/search?q=where+is+my+latest+order"), "web_06_order_question", 650)

    sales = session()
    fetch(sales, "/login", {"email": "sales@abc.vn", "password": "sales2026"})
    shot(fetch(sales, "/staff/orders"), "web_07_process_orders", 700)
    wh = session()
    fetch(wh, "/login", {"email": "warehouse@abc.vn", "password": "stock2026"})
    shot(fetch(wh, "/staff/inventory"), "web_08_inventory", 1050)
    admin = session()
    fetch(admin, "/login", {"email": "admin@abc.vn", "password": "admin2026"})
    shot(fetch(admin, "/admin/reviews"), "web_09_moderation", 500)
    manager = session()
    fetch(manager, "/login", {"email": "manager@abc.vn", "password": "report2026"})
    shot(fetch(manager, "/reports"), "web_10_dashboard", 1250)


if __name__ == "__main__":
    main()
