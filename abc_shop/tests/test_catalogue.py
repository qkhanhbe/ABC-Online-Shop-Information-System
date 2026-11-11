"""UC06 View Product Details, UC14 Manage Products: common attributes in Product, group attributes in
one detail record chosen by the category (BR-CAT-01)."""
import sqlite3

import pytest

from model.product import ApparelDetail, BagDetail, FootwearDetail, Product, WatchDetail
from service.errors import ValidationError


def test_each_product_loads_the_detail_kind_of_its_category(shop):
    kinds = {c.category_id: c.detail_kind for c in shop.dao.products.list_categories()}
    expected = {"footwear": FootwearDetail, "apparel": ApparelDetail, "bag": BagDetail, "watch": WatchDetail}
    products = shop.dao.products.list_products(active_only=False)
    assert len(products) == 16
    for p in products:
        assert isinstance(p.detail, expected[kinds[p.category_id]]), p.product_id


def test_product_page_shows_the_group_specific_attributes(shop):
    card = shop.catalog.product_detail("P16")
    rows = dict(card["product"].detail.spec_rows())
    assert rows["Capacity (litres)"] == "25" and rows["Laptop sleeve"] == "yes"
    watch = dict(shop.catalog.product_detail("P11")["product"].detail.spec_rows())
    assert "Battery (days)" not in watch              # an analog watch has no battery figure


def test_service_rejects_a_detail_of_the_wrong_group(shop, users):
    shoe = Product("P90", "Trail Shoes", "shoes", "Salomon", "grey", 130,
                   detail=WatchDetail("P90", "smart", "silicone", 30, 5))
    with pytest.raises(ValidationError):
        shop.catalog.save_product(users["A01"], shoe)
    assert shop.dao.products.get_product("P90") is None


def test_database_trigger_rejects_a_detail_of_the_wrong_group(shop, users):
    shop.catalog.save_product(users["A01"], Product("P91", "Trail Shoes", "shoes", "Salomon", "grey", 130,
                                                   detail=FootwearDetail("P91", "40-46", "mesh", "lugged", "trail")))
    with pytest.raises(sqlite3.IntegrityError, match="watch details"):
        shop.db.execute("INSERT INTO watch_detail(product_id, movement, strap, water_resistance_m) "
                        "VALUES ('P91', 'smart', 'silicone', 30)")
    assert isinstance(shop.dao.products.get_product("P91").detail, FootwearDetail)


def test_search_uses_the_detail_attributes(shop):
    results = shop.search.search(shop.query.text_query("backpack with laptop sleeve"))
    assert results[0]["product"].product_id == "P16"        # only P16 has a laptop sleeve
