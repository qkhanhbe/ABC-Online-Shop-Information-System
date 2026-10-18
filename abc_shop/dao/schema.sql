-- Physical data model of ABC Online Shop (SQLite). Integrity rules of Chapter 2 are written
-- as constraints so that no path - not even a manual script - can break them.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sequence (
    name   TEXT PRIMARY KEY,
    value  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id        TEXT PRIMARY KEY,
    name           TEXT NOT NULL,
    email          TEXT NOT NULL UNIQUE,
    password_hash  TEXT NOT NULL,
    role           TEXT NOT NULL CHECK (role IN ('customer','sales','warehouse','admin','manager')),
    created_at     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS address (
    customer_id  TEXT PRIMARY KEY REFERENCES users(user_id),
    receiver     TEXT NOT NULL,
    phone        TEXT NOT NULL,
    street       TEXT NOT NULL,
    city         TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS category (
    category_id  TEXT PRIMARY KEY,
    name         TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product (
    product_id   TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    category_id  TEXT NOT NULL REFERENCES category(category_id),
    brand        TEXT NOT NULL,
    color        TEXT NOT NULL,
    price        REAL NOT NULL CHECK (price > 0),
    description  TEXT NOT NULL DEFAULT '',
    image        TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','unpublished'))
);

CREATE TABLE IF NOT EXISTS stock_level (
    product_id  TEXT PRIMARY KEY REFERENCES product(product_id),
    physical    INTEGER NOT NULL CHECK (physical >= 0),
    reserved    INTEGER NOT NULL CHECK (reserved >= 0),
    threshold   INTEGER NOT NULL DEFAULT 3,
    CHECK (physical >= reserved)
);

CREATE TABLE IF NOT EXISTS inventory_event (
    event_id    TEXT PRIMARY KEY,
    product_id  TEXT NOT NULL REFERENCES product(product_id),
    kind        TEXT NOT NULL CHECK (kind IN ('RECEIPT','RESERVE','RELEASE','ISSUE','ADJUST')),
    quantity    INTEGER NOT NULL,
    reference   TEXT NOT NULL,
    reason      TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL,
    UNIQUE (product_id, kind, reference)
);

CREATE TABLE IF NOT EXISTS replenishment_request (
    request_id  TEXT PRIMARY KEY,
    product_id  TEXT NOT NULL REFERENCES product(product_id),
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    status      TEXT NOT NULL DEFAULT 'Requested',
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cart (
    cart_id      TEXT PRIMARY KEY,
    customer_id  TEXT NOT NULL UNIQUE REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS cart_item (
    cart_id     TEXT NOT NULL REFERENCES cart(cart_id) ON DELETE CASCADE,
    product_id  TEXT NOT NULL REFERENCES product(product_id),
    name        TEXT NOT NULL,
    cart_price  REAL NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (cart_id, product_id)
);

CREATE TABLE IF NOT EXISTS promotion (
    code        TEXT PRIMARY KEY,
    percent     REAL NOT NULL CHECK (percent > 0 AND percent <= 50),
    min_total   REAL NOT NULL DEFAULT 0,
    start_date  TEXT NOT NULL,
    end_date    TEXT NOT NULL,
    active      INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS customer_order (
    order_id         TEXT PRIMARY KEY,
    customer_id      TEXT NOT NULL REFERENCES users(user_id),
    address          TEXT NOT NULL,
    discount         REAL NOT NULL DEFAULT 0,
    shipping_fee     REAL NOT NULL DEFAULT 0,
    total            REAL NOT NULL CHECK (total > 0),
    status           TEXT NOT NULL,
    created_at       TEXT NOT NULL,
    promo_code       TEXT NOT NULL DEFAULT '',
    idempotency_key  TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS order_item (
    order_id    TEXT NOT NULL REFERENCES customer_order(order_id),
    product_id  TEXT NOT NULL REFERENCES product(product_id),
    name        TEXT NOT NULL,
    unit_price  REAL NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS order_status_history (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id  TEXT NOT NULL REFERENCES customer_order(order_id),
    status    TEXT NOT NULL,
    actor     TEXT NOT NULL,
    at        TEXT NOT NULL,
    note      TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS payment (
    payment_id    TEXT PRIMARY KEY,
    order_id      TEXT NOT NULL REFERENCES customer_order(order_id),
    attempt_ref   TEXT NOT NULL UNIQUE,
    amount        REAL NOT NULL CHECK (amount > 0),
    currency      TEXT NOT NULL DEFAULT 'USD',
    status        TEXT NOT NULL,
    provider_ref  TEXT NOT NULL DEFAULT '',
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shipment (
    shipment_id  TEXT PRIMARY KEY,
    order_id     TEXT NOT NULL UNIQUE REFERENCES customer_order(order_id),
    carrier_ref  TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shipment_milestone (
    shipment_id  TEXT NOT NULL REFERENCES shipment(shipment_id),
    seq          INTEGER NOT NULL,
    code         TEXT NOT NULL,
    at           TEXT NOT NULL,
    location     TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (shipment_id, seq)
);

CREATE TABLE IF NOT EXISTS review (
    review_id    TEXT PRIMARY KEY,
    product_id   TEXT NOT NULL REFERENCES product(product_id),
    customer_id  TEXT NOT NULL REFERENCES users(user_id),
    order_id     TEXT NOT NULL REFERENCES customer_order(order_id),
    rating       INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    text         TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'published',
    created_at   TEXT NOT NULL,
    UNIQUE (customer_id, product_id, order_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    actor      TEXT NOT NULL,
    action     TEXT NOT NULL,
    entity     TEXT NOT NULL,
    entity_id  TEXT NOT NULL,
    detail     TEXT NOT NULL DEFAULT '',
    at         TEXT NOT NULL
);
