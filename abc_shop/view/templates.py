"""Presentation layer (view): HTML pages. A view only formats what the controller gives it."""
from html import escape


def e(value):
    return escape(str(value))


def money(value):
    return f"${value:,.2f}"


def layout(request, title, body):
    user = getattr(request, "user", None)
    flash = request.session.pop("flash", "") if hasattr(request, "session") else ""
    links = ['<a href="/">Catalogue</a>']
    if user is None:
        links += ['<a href="/login">Log in</a>', '<a href="/register">Register</a>']
    else:
        if user.role == "customer":
            links += ['<a href="/cart">Cart</a>', '<a href="/orders">My orders</a>']
        if user.role in ("sales", "warehouse"):
            links.append('<a href="/staff/orders">Order processing</a>')
        if user.role == "warehouse":
            links.append('<a href="/staff/inventory">Inventory</a>')
        if user.role == "admin":
            links.append('<a href="/admin/reviews">Review moderation</a>')
        if user.role == "manager":
            links.append('<a href="/reports">Reports</a>')
        links.append(f'<span class="who">{e(user.name)} ({e(user.role)})</span> <a href="/logout">Log out</a>')
    note = f'<div class="flash">{e(flash)}</div>' if flash else ""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} - ABC Online Shop</title><link rel="stylesheet" href="/static/style.css"></head>
<body><header><a class="brand" href="/">ABC Online Shop</a><nav>{' '.join(links)}</nav></header>
<main>{note}<h1>{e(title)}</h1>{body}</main>
<footer>ABC Online Shop - course essay prototype (BeQuocKhanh, B23DCCE049)</footer></body></html>"""


def message(request, title, text):
    return layout(request, title, f'<p class="panel">{e(text)}</p><p><a href="/">Back to the catalogue</a></p>')


def search_box(query=""):
    return f"""<form class="search" method="post" action="/search" enctype="multipart/form-data">
<input name="q" value="{e(query)}" placeholder="black running shoes under 150, where is my latest order...">
<select name="mode"><option value="text">Text</option><option value="voice">Voice (transcript)</option></select>
<input type="file" name="image" accept="image/*" title="Search by image">
<button>Search</button></form>"""


def product_card(card):
    p = card["product"]
    stock = "in" if card["available"] > 0 else "out"
    return f"""<a class="card" href="/product/{e(p.product_id)}"><img src="/{e(p.image)}" alt="">
<b>{e(p.name)}</b><span>{money(p.price)}</span><small class="{stock}">{e(card['status'])}</small></a>"""


def home(request, categories, cards, active):
    tabs = ['<a href="/"%s>All</a>' % (' class="on"' if not active else "")]
    tabs += [f'<a href="/?category={e(c.category_id)}"{" class=on" if c.category_id == active else ""}>'
             f'{e(c.name)}</a>' for c in categories]
    grid = "".join(product_card(c) for c in cards)
    return layout(request, "Catalogue", search_box() + f'<div class="tabs">{"".join(tabs)}</div>'
                  f'<div class="grid">{grid}</div>')


def search_results(request, text, mode, results, trace):
    rows = "".join(
        f"<tr><td>{i}</td><td><a href='/product/{e(r['product'].product_id)}'>{e(r['product'].name)}</a></td>"
        f"<td>{money(r['product'].price)}</td><td>{r['available']}</td><td>{r['text']}</td>"
        f"<td>{r['s_image']:.3f}</td><td><b>{r['score']:.3f}</b></td></tr>"
        for i, r in enumerate(results, 1))
    table = (f"<table><tr><th>#</th><th>Product</th><th>Price</th><th>Available</th><th>Keywords</th>"
             f"<th>Cosine</th><th>S(x|q)</th></tr>{rows}</table>") if results else \
        '<p class="panel">No product matches this search. Try fewer words or another photo.</p>'
    steps = "".join(f"<li>{e(t)}</li>" for t in trace)
    return layout(request, f"Search results ({mode})", search_box(text or "") + table +
                  f'<details open><summary>Processing steps</summary><ol class="trace">{steps}</ol></details>')


def order_search(request, text, orders, trace):
    rows = "".join(f"<tr><td><a href='/orders/{e(o.order_id)}'>{e(o.order_id)}</a></td><td>{e(o.created_at)}</td>"
                   f"<td>{e(o.status)}</td><td>{money(o.calc_total())}</td></tr>" for o in orders)
    body = (f"<table><tr><th>Order</th><th>Date</th><th>Status</th><th>Total</th></tr>{rows}</table>"
            if orders else '<p class="panel">No order of yours matches this question.</p>')
    steps = "".join(f"<li>{e(t)}</li>" for t in trace)
    return layout(request, "Order search", search_box(text) + body + f'<ol class="trace">{steps}</ol>')


def product(request, card, reviews, insight, similar):
    p = card["product"]
    aspects = "".join(
        f"<tr><td>{e(a.title())}</td><td>{s['positive']}</td><td>{s['negative']}</td>"
        f"<td><div class='bar'><i style='width:{int(s['share_positive'] * 100)}%'></i></div></td>"
        f"<td><small>{e(s['evidence'][0][1])}</small></td></tr>"
        for a, s in insight["aspects"].items())
    insight_html = (f"<p>Overall: <b>{e(insight['label'])}</b> ({insight['reviews_used']} reviews analysed, "
                    f"{insight['reviews_skipped']} skipped as noise)</p>"
                    f"<table><tr><th>Aspect</th><th>+</th><th>-</th><th>Positive share</th><th>Evidence</th></tr>"
                    f"{aspects}</table>") if aspects else "<p>Not enough reviews yet.</p>"
    review_list = "".join(f"<li><b>{'*' * r.rating}</b> {e(r.text)} <small>{e(r.created_at[:10])}</small></li>"
                          for r in reviews) or "<li>No reviews yet.</li>"
    recs = "".join(f'<a class="card small" href="/product/{e(q.product_id)}"><img src="/{e(q.image)}" alt="">'
                   f'<b>{e(q.name)}</b><span>{money(q.price)}</span><small>score {s:.2f}</small></a>'
                   for q, s, _ in similar)
    buy = (f"""<form method="post" action="/cart/add"><input type="hidden" name="product_id" value="{e(p.product_id)}">
<input type="number" name="qty" value="1" min="1" max="{card['available']}"> <button>Add to cart</button></form>"""
           if card["available"] > 0 else '<p class="out">Out of stock</p>')
    return layout(request, p.name, f"""<div class="detail"><img src="/{e(p.image)}" alt="">
<div><p class="price">{money(p.price)}</p><p>{e(p.description)}</p>
<p>Brand: {e(p.brand)} &middot; Colour: {e(p.color)} &middot; Category: {e(p.category_id)}</p>
<p>Available: <b>{card['available']}</b></p>{buy}</div></div>
<h2>AI review insights</h2>{insight_html}<h2>Customer reviews</h2><ul class="reviews">{review_list}</ul>
<h2>Customers also like</h2><div class="grid">{recs}</div>""")


def cart(request, cart):
    rows = "".join(
        f"""<tr><td>{e(l.name)}</td><td>{money(l.cart_price)}</td><td><form method="post" action="/cart/update">
<input type="hidden" name="product_id" value="{e(l.product_id)}"><input type="number" name="qty" value="{l.quantity}" min="0">
<button>Update</button></form></td><td>{money(l.sub_total())}</td></tr>""" for l in cart.items)
    if not rows:
        return layout(request, "Your cart", '<p class="panel">Your cart is empty.</p>')
    return layout(request, "Your cart", f"<table><tr><th>Product</th><th>Price</th><th>Quantity</th>"
                  f"<th>Subtotal</th></tr>{rows}<tr><td colspan=3><b>Total</b></td><td><b>{money(cart.calc_total())}"
                  f"</b></td></tr></table><p><a class='button' href='/checkout'>Checkout</a></p>")


def checkout(request, customer, quote, promo, key):
    problems = "".join(f"<li>{e(p)}</li>" for p in quote["problems"])
    lines = "".join(f"<tr><td>{e(l.name)} x {l.quantity}</td><td>{money(l.sub_total())}</td></tr>"
                    for l in quote["cart"].items)
    address = customer.address.one_line() if customer.address else "missing"
    return layout(request, "Checkout", f"""{f'<ul class="problems">{problems}</ul>' if problems else ''}
<table>{lines}<tr><td>Subtotal</td><td>{money(quote['subtotal'])}</td></tr>
<tr><td>Discount {e(quote['promo_note'])}</td><td>-{money(quote['discount'])}</td></tr>
<tr><td>Shipping</td><td>{money(quote['shipping'])}</td></tr><tr><td><b>Total</b></td><td><b>{money(quote['total'])}</b></td></tr></table>
<p>Deliver to: {e(address)}</p>
<form method="get" action="/checkout"><input name="promo" value="{e(promo)}" placeholder="Promotion code"><button>Apply</button></form>
<form method="post" action="/checkout"><input type="hidden" name="promo" value="{e(promo)}"><input type="hidden" name="key" value="{e(key)}">
<label>Payment (simulated provider) <select name="card"><option value="tok_visa">Card accepted</option>
<option value="tok_declined">Card declined</option><option value="tok_timeout">Provider timeout</option></select></label>
<button {'disabled' if problems else ''}>Place order and pay</button></form>""")


def order_history(request, orders, picks):
    rows = "".join(f"<tr><td><a href='/orders/{e(o.order_id)}'>{e(o.order_id)}</a></td><td>{e(o.created_at[:16])}</td>"
                   f"<td>{e(', '.join(i.name for i in o.items))}</td><td>{money(o.calc_total())}</td>"
                   f"<td><span class='status'>{e(o.status)}</span></td></tr>" for o in orders)
    recs = "".join(f'<a class="card small" href="/product/{e(p.product_id)}"><img src="/{e(p.image)}" alt="">'
                   f'<b>{e(p.name)}</b><span>{money(p.price)}</span></a>' for p, _ in picks)
    return layout(request, "My orders", f"<table><tr><th>Order</th><th>Date</th><th>Items</th><th>Total</th>"
                  f"<th>Status</th></tr>{rows}</table><h2>Recommended for you</h2><div class='grid'>{recs}</div>")


def track(request, t):
    o = t["order"]
    steps = "".join(f"<li><b>{e(s)}</b> <small>{e(at)}</small> {e(note)}</li>" for at, s, note in t["timeline"])
    items = "".join(f"<tr><td>{e(i.name)}</td><td>{i.quantity}</td><td>{money(i.sub_total())}</td></tr>" for i in o.items)
    cancel = (f'<form method="post" action="/orders/{e(o.order_id)}/cancel"><button class="ghost">Cancel order</button></form>'
              if o.can_cancel() else "")
    review = ""
    if o.status == "Delivered":
        options = "".join(f'<option value="{e(i.product_id)}">{e(i.name)}</option>' for i in o.items)
        review = f"""<h2>Review a product</h2><form method="post" action="/orders/{e(o.order_id)}/review">
<select name="product_id">{options}</select> <select name="rating">{''.join(f'<option>{n}</option>' for n in (5, 4, 3, 2, 1))}</select>
<input name="text" placeholder="What did you think?" size="50"> <button>Submit review</button></form>"""
    carrier = f" &middot; carrier ref {e(t['carrier_ref'])}" if t["carrier_ref"] else ""
    return layout(request, f"Order {o.order_id}", f"""<p class="panel">Status: <span class="status">{e(o.status)}</span>
&middot; last update {e(t['last_update'])}{carrier}</p><table><tr><th>Item</th><th>Qty</th><th>Subtotal</th></tr>{items}
<tr><td colspan=2>Total (incl. shipping, discount)</td><td><b>{money(o.calc_total())}</b></td></tr></table>
<h2>Timeline</h2><ol class="timeline">{steps}</ol>{cancel}{review}""")


def login(request, error=""):
    err = f'<p class="problems">{e(error)}</p>' if error else ""
    return layout(request, "Log in", f"""{err}<form class="stack" method="post" action="/login">
<input name="email" placeholder="Email" value="{e(request.get('email'))}"><input name="password" type="password" placeholder="Password">
<button>Log in</button></form><p class="hint">Demo accounts: khanh@example.com / khanh2026, sales@abc.vn / sales2026,
warehouse@abc.vn / stock2026, admin@abc.vn / admin2026, manager@abc.vn / report2026</p>""")


def register(request, error=""):
    err = f'<p class="problems">{e(error)}</p>' if error else ""
    fields = "".join(f'<input name="{n}" placeholder="{p}" value="{e(request.get(n)) if n != "password" else ""}"'
                     f'{" type=password" if n == "password" else ""}>'
                     for n, p in (("name", "Full name"), ("email", "Email"), ("password", "Password (8+ characters)"),
                                  ("phone", "Phone"), ("street", "Street address"), ("city", "City")))
    return layout(request, "Create an account", f'{err}<form class="stack" method="post" action="/register">{fields}'
                  f'<button>Register</button></form>')


def staff_orders(request, queue, picks, ready):
    def rows(orders, actions):
        return "".join(
            f"<tr><td>{e(o.order_id)}</td><td>{e(o.customer_id)}</td><td>{e(o.created_at[:16])}</td>"
            f"<td>{e(', '.join(f'{i.name} x{i.quantity}' for i in o.items))}</td><td>{e(o.status)}</td><td>"
            + "".join(f'<form class="inline" method="post" action="/staff/orders/{e(o.order_id)}/{a}">'
                      f'<button>{label}</button></form>' for a, label in actions)
            + "</td></tr>" for o in orders) or "<tr><td colspan=6>Nothing to do.</td></tr>"
    head = "<tr><th>Order</th><th>Customer</th><th>Date</th><th>Items</th><th>Status</th><th>Action</th></tr>"
    body = ""
    if request.user.can("process_orders"):
        body += f"<h2>Processing queue (UC19)</h2><table>{head}{rows(queue, [('process', 'Confirm processing'), ('hold', 'Hold')])}</table>"
    if request.user.can("shipment"):
        body += f"<h2>Pick list (UC21)</h2><table>{head}{rows(picks, [('pack', 'Mark packed')])}</table>"
        body += f"<h2>Ready for shipment (UC22)</h2><table>{head}{rows(ready, [('ship', 'Hand to carrier')])}</table>"
    return layout(request, "Order processing", body)


def inventory(request, rows, low):
    table = "".join(f"<tr class='{'low' if s.is_low() else ''}'><td>{e(p.product_id)}</td><td>{e(p.name)}</td>"
                    f"<td>{s.physical}</td><td>{s.reserved}</td><td><b>{s.available}</b></td><td>{s.threshold}</td></tr>"
                    for p, s in rows)
    options = "".join(f'<option value="{e(p.product_id)}">{e(p.product_id)} {e(p.name)}</option>' for p, _ in rows)
    return layout(request, "Inventory (UC20)", f"""<table><tr><th>ID</th><th>Product</th><th>Physical</th><th>Reserved</th>
<th>Available</th><th>Threshold</th></tr>{table}</table><p>{len(low)} product(s) at or below threshold.</p>
<h2>Record an inventory event</h2><form class="inline" method="post" action="/staff/inventory">
<select name="product_id">{options}</select><select name="kind"><option>RECEIPT</option><option>ADJUST</option>
<option value="REPLENISH">Replenishment request</option></select><input name="qty" type="number" value="10">
<input name="reference" placeholder="Reference (GRN-...)"><input name="reason" placeholder="Reason"><button>Record</button></form>""")


def moderation(request, queue):
    rows = "".join(f"""<tr><td>{e(r.review_id)}</td><td>{e(r.product_id)}</td><td>{r.rating}</td><td>{e(r.text)}</td><td>
<form class="inline" method="post" action="/admin/reviews/{e(r.review_id)}"><button name="decision" value="approve">Publish</button>
<button name="decision" value="reject" class="ghost">Reject</button></form></td></tr>""" for r in queue)
    return layout(request, "Review moderation (UC18)", "<p>Reviews flagged as noise by the AI wait here for a person.</p>"
                  f"<table><tr><th>ID</th><th>Product</th><th>Rating</th><th>Text</th><th>Decision</th></tr>"
                  f"{rows or '<tr><td colspan=5>No review is waiting.</td></tr>'}</table>")


def reports(request, dash, sales, stock, exceptions):
    kpis = "".join(f'<div class="kpi"><small>{e(k)}</small><b>{e(v)}</b></div>' for k, v in (
        ("Orders", dash["orders"]), ("Revenue", money(dash["revenue"])),
        ("Average order", money(dash["average_order"])), ("Open exceptions", dash["exceptions"]),
        ("Low-stock products", len(dash["low_stock"]))))
    status = "".join(f"<tr><td>{e(s)}</td><td>{n}</td></tr>" for s, n in sorted(dash["by_status"].items()))
    peak = max(sales["by_day"].values(), default=1)
    days = "".join(f"<tr><td>{e(d)}</td><td>{money(v)}</td><td><div class='bar'><i style='width:{int(v / peak * 100)}%'>"
                   f"</i></div></td></tr>" for d, v in sales["by_day"].items())
    cats = "".join(f"<tr><td>{e(c)}</td><td>{money(v)}</td></tr>" for c, v in sales["by_category"].items())
    low = "".join(f"<tr><td>{e(r['product_id'])}</td><td>{e(r['name'])}</td><td>{r['available']}</td></tr>"
                  for r in stock if r["low"])
    exc = "".join(f"<tr><td>{e(o)}</td><td>{e(s)}</td><td>{e(n)}</td></tr>" for o, s, n in exceptions["orders"])
    return layout(request, "Management dashboard", f"""<div class="kpis">{kpis}</div>
<p class="hint">Computed from operational records at {e(dash['refreshed_at'])}.</p>
<div class="cols"><div><h2>Sales by day (UC26)</h2><table>{days}</table></div>
<div><h2>Orders by status</h2><table>{status}</table><h2>Sales by category</h2><table>{cats}</table></div></div>
<div class="cols"><div><h2>Low stock (UC27)</h2><table><tr><th>ID</th><th>Product</th><th>Available</th></tr>{low}</table></div>
<div><h2>Exceptions (UC28)</h2><table><tr><th>Order</th><th>Status</th><th>Last note</th></tr>{exc}</table></div></div>""")
