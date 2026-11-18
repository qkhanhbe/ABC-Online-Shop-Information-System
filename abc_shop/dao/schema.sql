-- Physical data model of ABC Online Shop (SQLite).
-- Tables, columns, primary keys and foreign keys are the ones of ERD01, which syncClassesToErd generated from
-- the data model classes (DM01, DM02); design/create_tables.sql is the DDL generateSql wrote from it.
-- Added here by hand, because the ERD does not carry them: NOT NULL, CHECK, UNIQUE, DEFAULT, ON DELETE CASCADE,
-- the triggers of BR-CAT-01 and the two technical tables sequence and audit_log.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sequence (
    name   TEXT PRIMARY KEY,
    value  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS User (
    user_id        TEXT NOT NULL,
    name           TEXT NOT NULL,
    email          TEXT NOT NULL UNIQUE,
    password_hash  TEXT NOT NULL,
    role           TEXT NOT NULL CHECK (role IN ('customer','sales','warehouse','admin','manager')),
    created_at     TEXT NOT NULL,
    CONSTRAINT pk_User PRIMARY KEY (user_id)
);

-- Customer is a subclass of User: its table shares the User key (table per subclass).
CREATE TABLE IF NOT EXISTS Customer (
    user_id  TEXT NOT NULL,
    CONSTRAINT pk_Customer PRIMARY KEY (user_id),
    CONSTRAINT fk_Customer_User FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Address (
    receiver     TEXT NOT NULL,
    phone        TEXT NOT NULL,
    street       TEXT NOT NULL,
    city         TEXT NOT NULL,
    customer_id  TEXT NOT NULL,
    CONSTRAINT pk_Address PRIMARY KEY (customer_id),
    CONSTRAINT fk_Address_Customer FOREIGN KEY (customer_id) REFERENCES Customer (user_id)
);

-- A category says which kind its products are, and therefore which kind table holds their own attributes.
CREATE TABLE IF NOT EXISTS Category (
    category_id  TEXT NOT NULL,
    name         TEXT NOT NULL,
    detail_kind  TEXT NOT NULL CHECK (detail_kind IN ('footwear','apparel','bag','watch')),
    CONSTRAINT pk_Category PRIMARY KEY (category_id)
);

CREATE TABLE IF NOT EXISTS Product (
    product_id   TEXT NOT NULL,
    name         TEXT NOT NULL,
    brand        TEXT NOT NULL,
    color        TEXT NOT NULL,
    price        REAL NOT NULL CHECK (price > 0),
    description  TEXT NOT NULL DEFAULT '',
    image        TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','unpublished')),
    category_id  TEXT NOT NULL,
    CONSTRAINT pk_Product PRIMARY KEY (product_id),
    CONSTRAINT fk_Product_Category FOREIGN KEY (category_id) REFERENCES Category (category_id)
);

-- The four kinds of Product (table per subclass): the key is also the foreign key to Product.
CREATE TABLE IF NOT EXISTS Footwear (
    sizes           TEXT NOT NULL,
    upper_material  TEXT NOT NULL,
    sole            TEXT NOT NULL,
    purpose         TEXT NOT NULL,
    product_id      TEXT NOT NULL,
    CONSTRAINT pk_Footwear PRIMARY KEY (product_id),
    CONSTRAINT fk_Footwear_Product FOREIGN KEY (product_id) REFERENCES Product (product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Apparel (
    sizes       TEXT NOT NULL,
    material    TEXT NOT NULL,
    fit         TEXT NOT NULL,
    product_id  TEXT NOT NULL,
    CONSTRAINT pk_Apparel PRIMARY KEY (product_id),
    CONSTRAINT fk_Apparel_Product FOREIGN KEY (product_id) REFERENCES Product (product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Bag (
    capacity_l     REAL NOT NULL CHECK (capacity_l > 0),
    material       TEXT NOT NULL,
    laptop_sleeve  INTEGER NOT NULL DEFAULT 0 CHECK (laptop_sleeve IN (0, 1)),
    product_id     TEXT NOT NULL,
    CONSTRAINT pk_Bag PRIMARY KEY (product_id),
    CONSTRAINT fk_Bag_Product FOREIGN KEY (product_id) REFERENCES Product (product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Watch (
    movement            TEXT NOT NULL CHECK (movement IN ('smart','quartz','automatic')),
    strap               TEXT NOT NULL,
    water_resistance_m  INTEGER NOT NULL CHECK (water_resistance_m >= 0),
    battery_days        INTEGER,
    product_id          TEXT NOT NULL,
    CONSTRAINT pk_Watch PRIMARY KEY (product_id),
    CONSTRAINT fk_Watch_Product FOREIGN KEY (product_id) REFERENCES Product (product_id) ON DELETE CASCADE
);

-- BR-CAT-01: a product is of the kind its category names. A foreign key cannot say this, because product_id
-- is the key of all four kind tables; each kind table checks it before a row is inserted.
CREATE TRIGGER IF NOT EXISTS footwear_kind BEFORE INSERT ON Footwear
WHEN (SELECT c.detail_kind FROM Product p JOIN Category c ON c.category_id = p.category_id
      WHERE p.product_id = NEW.product_id) IS NOT 'footwear'
BEGIN SELECT RAISE(ABORT, 'the category of this product is not a footwear category'); END;

CREATE TRIGGER IF NOT EXISTS apparel_kind BEFORE INSERT ON Apparel
WHEN (SELECT c.detail_kind FROM Product p JOIN Category c ON c.category_id = p.category_id
      WHERE p.product_id = NEW.product_id) IS NOT 'apparel'
BEGIN SELECT RAISE(ABORT, 'the category of this product is not an apparel category'); END;

CREATE TRIGGER IF NOT EXISTS bag_kind BEFORE INSERT ON Bag
WHEN (SELECT c.detail_kind FROM Product p JOIN Category c ON c.category_id = p.category_id
      WHERE p.product_id = NEW.product_id) IS NOT 'bag'
BEGIN SELECT RAISE(ABORT, 'the category of this product is not a bag category'); END;

CREATE TRIGGER IF NOT EXISTS watch_kind BEFORE INSERT ON Watch
WHEN (SELECT c.detail_kind FROM Product p JOIN Category c ON c.category_id = p.category_id
      WHERE p.product_id = NEW.product_id) IS NOT 'watch'
BEGIN SELECT RAISE(ABORT, 'the category of this product is not a watch category'); END;

CREATE TABLE IF NOT EXISTS StockLevel (
    physical    INTEGER NOT NULL CHECK (physical >= 0),
    reserved    INTEGER NOT NULL CHECK (reserved >= 0),
    threshold   INTEGER NOT NULL DEFAULT 3,
    product_id  TEXT NOT NULL,
    CHECK (physical >= reserved),
    CONSTRAINT pk_StockLevel PRIMARY KEY (product_id),
    CONSTRAINT fk_StockLevel_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE IF NOT EXISTS InventoryEvent (
    event_id    TEXT NOT NULL,
    kind        TEXT NOT NULL CHECK (kind IN ('RECEIPT','RESERVE','RELEASE','ISSUE','ADJUST')),
    quantity    INTEGER NOT NULL,
    reference   TEXT NOT NULL,
    reason      TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL,
    product_id  TEXT NOT NULL,
    UNIQUE (product_id, kind, reference),
    CONSTRAINT pk_InventoryEvent PRIMARY KEY (event_id),
    CONSTRAINT fk_InventoryEvent_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE IF NOT EXISTS ReplenishmentRequest (
    request_id  TEXT NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    status      TEXT NOT NULL DEFAULT 'Requested',
    created_at  TEXT NOT NULL,
    product_id  TEXT NOT NULL,
    CONSTRAINT pk_ReplenishmentRequest PRIMARY KEY (request_id),
    CONSTRAINT fk_ReplenishmentRequest_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE IF NOT EXISTS Cart (
    cart_id      TEXT NOT NULL,
    customer_id  TEXT NOT NULL UNIQUE,
    CONSTRAINT pk_Cart PRIMARY KEY (cart_id),
    CONSTRAINT fk_Cart_Customer FOREIGN KEY (customer_id) REFERENCES Customer (user_id)
);

CREATE TABLE IF NOT EXISTS CartItem (
    name        TEXT NOT NULL,
    cart_price  REAL NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    cart_id     TEXT NOT NULL,
    product_id  TEXT NOT NULL,
    CONSTRAINT pk_CartItem PRIMARY KEY (cart_id, product_id),
    CONSTRAINT fk_CartItem_Cart FOREIGN KEY (cart_id) REFERENCES Cart (cart_id) ON DELETE CASCADE,
    CONSTRAINT fk_CartItem_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE IF NOT EXISTS Promotion (
    code        TEXT NOT NULL,
    percent     REAL NOT NULL CHECK (percent > 0 AND percent <= 50),
    min_total   REAL NOT NULL DEFAULT 0,
    start_date  TEXT NOT NULL,
    end_date    TEXT NOT NULL,
    active      INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT pk_Promotion PRIMARY KEY (code)
);

-- ORDER is an SQL keyword, so the table of Order is named Orders.
CREATE TABLE IF NOT EXISTS Orders (
    order_id         TEXT NOT NULL,
    address          TEXT NOT NULL,
    discount         REAL NOT NULL DEFAULT 0,
    shipping_fee     REAL NOT NULL DEFAULT 0,
    total            REAL NOT NULL CHECK (total > 0),
    status           TEXT NOT NULL,
    created_at       TEXT NOT NULL,
    idempotency_key  TEXT UNIQUE,
    customer_id      TEXT NOT NULL,
    promo_code       TEXT,
    CONSTRAINT pk_Orders PRIMARY KEY (order_id),
    CONSTRAINT fk_Orders_Customer FOREIGN KEY (customer_id) REFERENCES Customer (user_id),
    CONSTRAINT fk_Orders_Promotion FOREIGN KEY (promo_code) REFERENCES Promotion (code)
);

CREATE TABLE IF NOT EXISTS OrderItem (
    name        TEXT NOT NULL,
    unit_price  REAL NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    order_id    TEXT NOT NULL,
    product_id  TEXT NOT NULL,
    CONSTRAINT pk_OrderItem PRIMARY KEY (order_id, product_id),
    CONSTRAINT fk_OrderItem_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id),
    CONSTRAINT fk_OrderItem_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE IF NOT EXISTS StatusChange (
    ID        INTEGER NOT NULL,
    status    TEXT NOT NULL,
    actor     TEXT NOT NULL,
    at        TEXT NOT NULL,
    note      TEXT NOT NULL DEFAULT '',
    order_id  TEXT NOT NULL,
    CONSTRAINT pk_StatusChange PRIMARY KEY (ID),
    CONSTRAINT fk_StatusChange_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

CREATE TABLE IF NOT EXISTS Payment (
    payment_id    TEXT NOT NULL,
    attempt_ref   TEXT NOT NULL UNIQUE,
    amount        REAL NOT NULL CHECK (amount > 0),
    currency      TEXT NOT NULL DEFAULT 'USD',
    status        TEXT NOT NULL,
    provider_ref  TEXT NOT NULL DEFAULT '',
    created_at    TEXT NOT NULL,
    order_id      TEXT NOT NULL,
    CONSTRAINT pk_Payment PRIMARY KEY (payment_id),
    CONSTRAINT fk_Payment_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

CREATE TABLE IF NOT EXISTS Shipment (
    shipment_id  TEXT NOT NULL,
    carrier_ref  TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL,
    order_id     TEXT NOT NULL UNIQUE,
    CONSTRAINT pk_Shipment PRIMARY KEY (shipment_id),
    CONSTRAINT fk_Shipment_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

CREATE TABLE IF NOT EXISTS Milestone (
    seq          INTEGER NOT NULL,
    code         TEXT NOT NULL,
    at           TEXT NOT NULL,
    location     TEXT NOT NULL DEFAULT '',
    shipment_id  TEXT NOT NULL,
    CONSTRAINT pk_Milestone PRIMARY KEY (shipment_id, seq),
    CONSTRAINT fk_Milestone_Shipment FOREIGN KEY (shipment_id) REFERENCES Shipment (shipment_id)
);

CREATE TABLE IF NOT EXISTS Review (
    review_id    TEXT NOT NULL,
    rating       INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    text         TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'published',
    created_at   TEXT NOT NULL,
    product_id   TEXT NOT NULL,
    customer_id  TEXT NOT NULL,
    order_id     TEXT NOT NULL,
    UNIQUE (customer_id, product_id, order_id),
    CONSTRAINT pk_Review PRIMARY KEY (review_id),
    CONSTRAINT fk_Review_Product FOREIGN KEY (product_id) REFERENCES Product (product_id),
    CONSTRAINT fk_Review_Customer FOREIGN KEY (customer_id) REFERENCES Customer (user_id),
    CONSTRAINT fk_Review_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id)
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
