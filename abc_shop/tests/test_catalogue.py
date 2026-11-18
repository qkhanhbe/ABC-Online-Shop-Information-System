"""UC06 View Product Details, UC14 Manage Products: attributes every product has live in Product, and each
kind of product (Footwear, Apparel, Bag, Watch) is a subclass with the attributes of its kind; the category
says which kind a product is (BR-CAT-01)."""
import sqlite3

import pytest

from model.product import Apparel, Bag, Footwear, Product, Watch
from service.errors import ValidationError


def test_each_product_is_of_the_kind_of_its_category(shop):
    kinds = {c.category_id: c.detail_kind for c in shop.dao.products.list_categories()}
    expected = {"footwear": Footwear, "apparel": Apparel, "bag": Bag, "watch": Watch}
    products = shop.dao.products.list_products(active_only=False)
    assert len(products) == 16
    for p in products:
        assert type(p) is expected[kinds[p.category_id]], p.product_id
        assert isinstance(p, Product)                       # a kind is a Product (generalization)


def test_product_page_shows_the_attributes_of_the_kind(shop):
    rows = dict(shop.catalog.product_detail("P16")["product"].spec_rows())
    assert rows["Capacity (litres)"] == "25" and rows["Laptop sleeve"] == "yes"
    watch = dict(shop.catalog.product_detail("P11")["product"].spec_rows())
    assert "Battery (days)" not in watch              # an analog watch has no battery figure


def test_service_rejects_a_product_of_the_wrong_kind(shop, users):
    shoe = Watch("P90", "Trail Shoes", "shoes", "Salomon", "grey", 130, movement="smart", strap="silicone",
                 water_resistance_m=30, battery_days=5)
    with pytest.raises(ValidationError):
        shop.catalog.save_product(users["A01"], shoe)
    assert shop.dao.products.get_product("P90") is None


def test_database_trigger_rejects_a_kind_row_of_the_wrong_kind(shop, users):
    shop.catalog.save_product(users["A01"], Footwear("P91", "Trail Shoes", "shoes", "Salomon", "grey", 130,
                                                     sizes="40-46", upper_material="mesh", sole="lugged",
                                                     purpose="trail"))
    with pytest.raises(sqlite3.IntegrityError, match="watch category"):
        shop.db.execute("INSERT INTO Watch(product_id, movement, strap, water_resistance_m) "
                        "VALUES ('P91', 'smart', 'silicone', 30)")
    assert type(shop.dao.products.get_product("P91")) is Footwear


def test_search_uses_the_attributes_of_the_kind(shop):
    results = shop.search.search(shop.query.text_query("backpack with laptop sleeve"))
    assert results[0]["product"].product_id == "P16"        # only P16 has a laptop sleeve
