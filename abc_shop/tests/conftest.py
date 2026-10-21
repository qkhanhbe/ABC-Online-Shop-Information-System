import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed import seed  # noqa: E402


@pytest.fixture
def shop():
    """A fresh in-memory shop with the seeded October history."""
    return seed(":memory:", verbose=False)


@pytest.fixture
def users(shop):
    get = shop.dao.customers.get_user
    return {uid: get(uid) for uid in ("C001", "C002", "C003", "C004", "S01", "W01", "A01", "M01")}
