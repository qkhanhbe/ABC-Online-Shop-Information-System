-- Generated from the ER model of TieuLuan_KHANHBQ.vpp (ERD01, ERD02) by the essay.gen plugin.
-- 19 tables, 18 foreign keys; parents before children.
PRAGMA foreign_keys = ON;

CREATE TABLE users (
  user_id VARCHAR(40) NOT NULL,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  password_hash VARCHAR(200) NOT NULL,
  role VARCHAR(40) NOT NULL CHECK (role IN ('customer','sales','warehouse','admin','manager')),
  created_at TIMESTAMP NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE address (
  customer_id VARCHAR(40) NOT NULL,
  receiver VARCHAR(200) NOT NULL,
  phone VARCHAR(200) NOT NULL,
  street VARCHAR(200) NOT NULL,
  city VARCHAR(200) NOT NULL,
  PRIMARY KEY (customer_id),
  FOREIGN KEY (customer_id) REFERENCES users (user_id)
);

CREATE TABLE cart (
  cart_id VARCHAR(40) NOT NULL,
  customer_id VARCHAR(40) NOT NULL UNIQUE,
  PRIMARY KEY (cart_id),
  FOREIGN KEY (customer_id) REFERENCES users (user_id)
);

CREATE TABLE customer_order (
  order_id VARCHAR(40) NOT NULL,
  customer_id VARCHAR(40) NOT NULL,
  address VARCHAR(1000) NOT NULL,
  discount DECIMAL(10,2) NOT NULL DEFAULT 0,
  shipping_fee DECIMAL(10,2) NOT NULL DEFAULT 0,
  total DECIMAL(10,2) NOT NULL CHECK (total > 0),
  status VARCHAR(40) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  promo_code VARCHAR(40) NOT NULL DEFAULT '',
  idempotency_key VARCHAR(40) UNIQUE,
  PRIMARY KEY (order_id),
  FOREIGN KEY (customer_id) REFERENCES users (user_id)
);

CREATE TABLE order_status_history (
  id INTEGER NOT NULL,
  order_id VARCHAR(40) NOT NULL,
  status VARCHAR(40) NOT NULL,
  actor VARCHAR(200) NOT NULL,
  at TIMESTAMP NOT NULL,
  note VARCHAR(1000) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  FOREIGN KEY (order_id) REFERENCES customer_order (order_id)
);

CREATE TABLE payment (
  payment_id VARCHAR(40) NOT NULL,
  order_id VARCHAR(40) NOT NULL,
  attempt_ref VARCHAR(40) NOT NULL UNIQUE,
  amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
  currency VARCHAR(40) NOT NULL DEFAULT 'USD',
  status VARCHAR(40) NOT NULL,
  provider_ref VARCHAR(40) NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL,
  PRIMARY KEY (payment_id),
  FOREIGN KEY (order_id) REFERENCES customer_order (order_id)
);

CREATE TABLE shipment (
  shipment_id VARCHAR(40) NOT NULL,
  order_id VARCHAR(40) NOT NULL UNIQUE,
  carrier_ref VARCHAR(40) NOT NULL DEFAULT '',
  status VARCHAR(40) NOT NULL,
  PRIMARY KEY (shipment_id),
  FOREIGN KEY (order_id) REFERENCES customer_order (order_id)
);

CREATE TABLE shipment_milestone (
  shipment_id VARCHAR(40) NOT NULL,
  seq INTEGER NOT NULL,
  code VARCHAR(40) NOT NULL,
  at TIMESTAMP NOT NULL,
  location VARCHAR(200) NOT NULL DEFAULT '',
  PRIMARY KEY (shipment_id, seq),
  FOREIGN KEY (shipment_id) REFERENCES shipment (shipment_id)
);

CREATE TABLE promotion (
  code VARCHAR(40) NOT NULL,
  percent DECIMAL(10,2) NOT NULL CHECK (percent > 0 AND percent <= 50),
  min_total DECIMAL(10,2) NOT NULL DEFAULT 0,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  active INTEGER NOT NULL DEFAULT 1,
  PRIMARY KEY (code)
);

CREATE TABLE category (
  category_id VARCHAR(40) NOT NULL,
  name VARCHAR(200) NOT NULL,
  PRIMARY KEY (category_id)
);

CREATE TABLE audit_log (
  id INTEGER NOT NULL,
  actor VARCHAR(200) NOT NULL,
  action VARCHAR(200) NOT NULL,
  entity VARCHAR(200) NOT NULL,
  entity_id VARCHAR(40) NOT NULL,
  detail VARCHAR(1000) NOT NULL DEFAULT '',
  at TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE sequence (
  name VARCHAR(200) NOT NULL,
  value INTEGER NOT NULL,
  PRIMARY KEY (name)
);

CREATE TABLE product (
  product_id VARCHAR(40) NOT NULL,
  name VARCHAR(200) NOT NULL,
  category_id VARCHAR(40) NOT NULL,
  brand VARCHAR(200) NOT NULL,
  color VARCHAR(200) NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK (price > 0),
  description VARCHAR(1000) NOT NULL DEFAULT '',
  image VARCHAR(200) NOT NULL DEFAULT '',
  status VARCHAR(40) NOT NULL DEFAULT 'active' CHECK (status IN ('active','unpublished')),
  PRIMARY KEY (product_id),
  FOREIGN KEY (category_id) REFERENCES category (category_id)
);

CREATE TABLE stock_level (
  product_id VARCHAR(40) NOT NULL,
  physical INTEGER NOT NULL CHECK (physical >= 0),
  reserved INTEGER NOT NULL CHECK (reserved >= 0 AND reserved <= physical),
  threshold INTEGER NOT NULL DEFAULT 3,
  PRIMARY KEY (product_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE inventory_event (
  event_id VARCHAR(40) NOT NULL,
  product_id VARCHAR(40) NOT NULL,
  kind VARCHAR(40) NOT NULL CHECK (kind IN ('RECEIPT','RESERVE','RELEASE','ISSUE','ADJUST')),
  quantity INTEGER NOT NULL,
  reference VARCHAR(40) NOT NULL,
  reason VARCHAR(200) NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL,
  PRIMARY KEY (event_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE replenishment_request (
  request_id VARCHAR(40) NOT NULL,
  product_id VARCHAR(40) NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  status VARCHAR(40) NOT NULL DEFAULT 'Requested',
  created_at TIMESTAMP NOT NULL,
  PRIMARY KEY (request_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE review (
  review_id VARCHAR(40) NOT NULL,
  product_id VARCHAR(40) NOT NULL,
  customer_id VARCHAR(40) NOT NULL,
  order_id VARCHAR(40) NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
  text VARCHAR(1000) NOT NULL,
  status VARCHAR(40) NOT NULL DEFAULT 'published',
  created_at TIMESTAMP NOT NULL,
  PRIMARY KEY (review_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id),
  FOREIGN KEY (customer_id) REFERENCES users (user_id),
  FOREIGN KEY (order_id) REFERENCES customer_order (order_id)
);

CREATE TABLE cart_item (
  cart_id VARCHAR(40) NOT NULL,
  product_id VARCHAR(40) NOT NULL,
  name VARCHAR(200) NOT NULL,
  cart_price DECIMAL(10,2) NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (cart_id, product_id),
  FOREIGN KEY (cart_id) REFERENCES cart (cart_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE order_item (
  order_id VARCHAR(40) NOT NULL,
  product_id VARCHAR(40) NOT NULL,
  name VARCHAR(200) NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (order_id) REFERENCES customer_order (order_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id)
);

