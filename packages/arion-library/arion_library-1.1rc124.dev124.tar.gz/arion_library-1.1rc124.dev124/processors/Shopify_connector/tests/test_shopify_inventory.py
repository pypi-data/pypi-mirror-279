import pytest
from ..lib.collections.ShopifyInventory import ShopifyInventory
from ..lib.collections.ShopifyProducts import ShopifyProducts

from unittest.mock import patch, Mock

STORE_NAME = ""
ACCESS_TOKEN = ""

@pytest.fixture
def shopify_inventory():
    """
    Returns an instance of the ShopifyInventory class initialized with the given STORE_NAME and ACCESS_TOKEN.
    
    :return: An instance of the ShopifyInventory class.
    :rtype: ShopifyInventory
    """
    return ShopifyInventory(STORE_NAME, ACCESS_TOKEN)


@pytest.fixture
def shopify_products():
    """
    Fixture for creating an instance of the ShopifyProducts class.

    Returns:
        ShopifyProducts: An instance of the ShopifyProducts class with the specified store name and access token.
    """
    return ShopifyProducts(STORE_NAME, ACCESS_TOKEN)

def test_fetch_inventory_levels(shopify_inventory):
    response = shopify_inventory.fetch_inventory_levels()

    assert 'data' in response
    assert 'inventoryLevels' in str(response['data']) # Null inventory level case

    ## case we have set invetory level
    # assert 'inventoryLevels' in response['data']['shop']['fulfillmentServices']['location']['inventoryLevels']

def test_set_item_quantity(
        shopify_inventory,
        shopify_products
        ):

    # ## inventory_item_id tekhdhou
    # # You need to provide a valid item_id and location_id for this test to work
    # inventoryItemId = "9545300345106"
    # location_id = "gid://shopify/Location/98855649554"
    # response = shopify_inventory.set_item_quantity(inventoryItemId, location_id, 50)
    # assert 'data' in response
    # assert 'inventoryAdjustQuantity' in response['data'] 

    products = shopify_products.get_products()
    assert products is not None and len(products) > 0, "No products found"
    
    if products:
        product_id = products[0]['id']
        inventoryItemId = products[0]['variants'][0]['inventory_item_id']
        inventory = shopify_inventory.fetch_inventory_levels()
        edges = inventory['data']['shop']['fulfillmentServices'][0]['location']['inventoryLevels']['edges']
        inventory_levels = [item['node']['id'] for item in edges]


# def test_set_item_quantity_success(shopify_inventory):
#     with patch('requests.post') as mock_post:
#         mock_response = Mock()
#         mock_response.json.return_value = {
#             "data": {
#                 "inventoryAdjustQuantity": {
#                     "inventoryLevel": {
#                         "available": 100
#                     },
#                     "userErrors": []
#                 }
#             }
#         }
#         mock_response.status_code = 200
#         mock_post.return_value = mock_response

#         response = shopify_inventory.set_item_quantity("inventory_item_id", "location_id", 100)
#         assert response["data"]["inventoryAdjustQuantity"]["inventoryLevel"]["available"] == 100
#         assert mock_post.called_once()
#         assert mock_post.call_args[1]["headers"] == shopify_inventory.headers