import pytest
from ..lib.collections.ShopifyOrders import ShopifyOrders

STORE_NAME = ""
ACCESS_TOKEN = ""

@pytest.fixture
def shopify_orders():
    return ShopifyOrders(STORE_NAME, ACCESS_TOKEN)

def test_fetch_orders(shopify_orders):
    s=0
    response = shopify_orders.fetch_orders()
    assert 'data' in response
    assert 'orders' in response['data']

def test_get_orders(shopify_orders):
    orders = shopify_orders.get_orders()
    assert isinstance(orders, list)
    if orders:
        assert 'id' in orders[0]
        assert 'name' in orders[0]