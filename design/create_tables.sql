-- Written by the plugin's SQLITE generator: Visual Paradigm's own generator needs the database set up in Tools > DB > Database Configuration (Dialect class not found:)

-- CREATE (SQLite)
CREATE TABLE User (
  user_id TEXT NOT NULL,
  name TEXT,
  email TEXT,
  password_hash TEXT,
  role TEXT,
  created_at TEXT,
  CONSTRAINT pk_User PRIMARY KEY (user_id)
);

CREATE TABLE Customer (
  user_id TEXT NOT NULL,
  CONSTRAINT pk_Customer PRIMARY KEY (user_id),
  CONSTRAINT fk_Customer_User FOREIGN KEY (user_id) REFERENCES User (user_id)
);

CREATE TABLE Address (
  receiver TEXT,
  phone TEXT,
  street TEXT,
  city TEXT,
  customer_id TEXT NOT NULL,
  CONSTRAINT pk_Address PRIMARY KEY (customer_id),
  CONSTRAINT fk_Address_Customer FOREIGN KEY (customer_id) REFERENCES Customer (user_id)
);

CREATE TABLE Cart (
  cart_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  CONSTRAINT pk_Cart PRIMARY KEY (cart_id),
  CONSTRAINT fk_Cart_Customer FOREIGN KEY (customer_id) REFERENCES Customer (user_id)
);

CREATE TABLE Category (
  category_id TEXT NOT NULL,
  name TEXT,
  detail_kind TEXT,
  CONSTRAINT pk_Category PRIMARY KEY (category_id)
);

CREATE TABLE Product (
  product_id TEXT NOT NULL,
  name TEXT,
  brand TEXT,
  color TEXT,
  price REAL,
  description TEXT,
  image TEXT,
  status TEXT,
  category_id TEXT NOT NULL,
  CONSTRAINT pk_Product PRIMARY KEY (product_id),
  CONSTRAINT fk_Product_Category FOREIGN KEY (category_id) REFERENCES Category (category_id)
);

CREATE TABLE CartItem (
  name TEXT,
  cart_price REAL,
  quantity INTEGER,
  cart_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  CONSTRAINT pk_CartItem PRIMARY KEY (cart_id, product_id),
  CONSTRAINT fk_CartItem_Cart FOREIGN KEY (cart_id) REFERENCES Cart (cart_id),
  CONSTRAINT fk_CartItem_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE Footwear (
  sizes TEXT,
  upper_material TEXT,
  sole TEXT,
  purpose TEXT,
  product_id TEXT NOT NULL,
  CONSTRAINT pk_Footwear PRIMARY KEY (product_id),
  CONSTRAINT fk_Footwear_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE Apparel (
  sizes TEXT,
  material TEXT,
  fit TEXT,
  product_id TEXT NOT NULL,
  CONSTRAINT pk_Apparel PRIMARY KEY (product_id),
  CONSTRAINT fk_Apparel_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE Bag (
  capacity_l REAL,
  material TEXT,
  laptop_sleeve INTEGER,
  product_id TEXT NOT NULL,
  CONSTRAINT pk_Bag PRIMARY KEY (product_id),
  CONSTRAINT fk_Bag_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE Watch (
  movement TEXT,
  strap TEXT,
  water_resistance_m INTEGER,
  battery_days INTEGER,
  product_id TEXT NOT NULL,
  CONSTRAINT pk_Watch PRIMARY KEY (product_id),
  CONSTRAINT fk_Watch_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE Promotion (
  code TEXT NOT NULL,
  percent REAL,
  min_total REAL,
  start_date TEXT,
  end_date TEXT,
  active INTEGER,
  CONSTRAINT pk_Promotion PRIMARY KEY (code)
);

CREATE TABLE Orders (
  order_id TEXT NOT NULL,
  address TEXT,
  discount REAL,
  shipping_fee REAL,
  total REAL,
  status TEXT,
  created_at TEXT,
  idempotency_key TEXT,
  customer_id TEXT NOT NULL,
  promo_code TEXT,
  CONSTRAINT pk_Orders PRIMARY KEY (order_id),
  CONSTRAINT fk_Orders_Customer FOREIGN KEY (customer_id) REFERENCES Customer (user_id),
  CONSTRAINT fk_Orders_Promotion FOREIGN KEY (promo_code) REFERENCES Promotion (code)
);

CREATE TABLE OrderItem (
  name TEXT,
  unit_price REAL,
  quantity INTEGER,
  order_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  CONSTRAINT pk_OrderItem PRIMARY KEY (order_id, product_id),
  CONSTRAINT fk_OrderItem_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id),
  CONSTRAINT fk_OrderItem_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE Payment (
  payment_id TEXT NOT NULL,
  attempt_ref TEXT,
  amount REAL,
  currency TEXT,
  status TEXT,
  provider_ref TEXT,
  created_at TEXT,
  order_id TEXT NOT NULL,
  CONSTRAINT pk_Payment PRIMARY KEY (payment_id),
  CONSTRAINT fk_Payment_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

CREATE TABLE Shipment (
  shipment_id TEXT NOT NULL,
  carrier_ref TEXT,
  status TEXT,
  order_id TEXT NOT NULL,
  CONSTRAINT pk_Shipment PRIMARY KEY (shipment_id),
  CONSTRAINT fk_Shipment_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

CREATE TABLE StatusChange (
  ID INTEGER NOT NULL,
  status TEXT,
  actor TEXT,
  at TEXT,
  note TEXT,
  order_id TEXT NOT NULL,
  CONSTRAINT pk_StatusChange PRIMARY KEY (ID),
  CONSTRAINT fk_StatusChange_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

CREATE TABLE Milestone (
  seq INTEGER NOT NULL,
  code TEXT,
  at TEXT,
  location TEXT,
  shipment_id TEXT NOT NULL,
  CONSTRAINT pk_Milestone PRIMARY KEY (seq, shipment_id),
  CONSTRAINT fk_Milestone_Shipment FOREIGN KEY (shipment_id) REFERENCES Shipment (shipment_id)
);

CREATE TABLE StockLevel (
  physical INTEGER,
  reserved INTEGER,
  threshold INTEGER,
  product_id TEXT NOT NULL,
  CONSTRAINT pk_StockLevel PRIMARY KEY (product_id),
  CONSTRAINT fk_StockLevel_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE InventoryEvent (
  event_id TEXT NOT NULL,
  kind TEXT,
  quantity INTEGER,
  reference TEXT,
  reason TEXT,
  created_at TEXT,
  product_id TEXT NOT NULL,
  CONSTRAINT pk_InventoryEvent PRIMARY KEY (event_id),
  CONSTRAINT fk_InventoryEvent_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE ReplenishmentRequest (
  request_id TEXT NOT NULL,
  quantity INTEGER,
  status TEXT,
  created_at TEXT,
  product_id TEXT NOT NULL,
  CONSTRAINT pk_ReplenishmentRequest PRIMARY KEY (request_id),
  CONSTRAINT fk_ReplenishmentRequest_Product FOREIGN KEY (product_id) REFERENCES Product (product_id)
);

CREATE TABLE Review (
  review_id TEXT NOT NULL,
  rating INTEGER,
  text TEXT,
  status TEXT,
  created_at TEXT,
  product_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  order_id TEXT NOT NULL,
  CONSTRAINT pk_Review PRIMARY KEY (review_id),
  CONSTRAINT fk_Review_Product FOREIGN KEY (product_id) REFERENCES Product (product_id),
  CONSTRAINT fk_Review_Customer FOREIGN KEY (customer_id) REFERENCES Customer (user_id),
  CONSTRAINT fk_Review_Orders FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

