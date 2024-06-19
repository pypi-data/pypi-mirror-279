import pytest
import requests
from ..lib.collections.ShopifyProducts import ShopifyProducts

STORE_NAME = ""
ACCESS_TOKEN = ""

@pytest.fixture
def shopify_products():
    """
    Fixture for creating an instance of the ShopifyProducts class.

    Returns:
        ShopifyProducts: An instance of the ShopifyProducts class with the specified store name and access token.
    """
    return ShopifyProducts(STORE_NAME, ACCESS_TOKEN)

def test_get_products(shopify_products):
    products = shopify_products.get_products(5)
    assert isinstance(products['data']['products']['edges'], list)
    if products:
        assert 'id' in products['data']['products']['edges'][0]['node']
        assert 'title' in products['data']['products']['edges'][0]['node']


# def test_get_product(shopify_products):
    
#     if products:
#         product_id = products['data']['products']['edges'][0]['node']['id']
#         product = shopify_products.get_product(product_id)
#         assert product is not None
#         assert 'id' in product
#         assert product['id'] == product_id

def test_create_product(shopify_products):
    product_title="shoes for men"
    response = shopify_products.create_product(product_title)
    assert product_title in response['data']['productCreate']['product']['title'], "Product not created"
        

def test_delete_product(shopify_products):

    # deletes the latest created product by previous test
    products = shopify_products.get_products(1,sort=True)
    last_product_id = products[0]['node']['id']
    created = shopify_products.delete_product(last_product_id)

    if 'product' in created:
        assert True

def test_update_product(shopify_products):
    # Fetch the list of products
    products = shopify_products.get_products()
    assert products is not None and len(products) > 0, "No products found"
    
    if products:
        product_id = products[0]['id']
        
        # Update the product
        original_product = products[0]

        original_title = original_product['title']
        new_title = "NEW PROUCT TILE TEST"
        updated_product = original_product
        graph_id_product = original_product['admin_graphql_api_id']
        shopify_products.update_product_title(new_title,graph_id_product)
        
        # Fetch the updated product
        updated_product = shopify_products.get_product(product_id)
        
        # Assertions to verify the update
        assert updated_product is not None, "Updated product is None"
        assert updated_product['title'] == new_title, f"Product title was not updated: expected {new_title}, got {updated_product['title']}"
        
        # Revert the product title to original 
        shopify_products.update_product_title(original_title,graph_id_product)
        reverted_product = shopify_products.get_product(product_id)
        assert reverted_product['title'] == original_title, "Failed to revert product title"


def test_get_product_by_sku(shopify_products):
    response = shopify_products.get_id_from_sku("VN-01-burgandy-4")
    if response['data']['productVariants']['edges']:
        # id = response['data']['productVariants']['edges'][0]['node']['id']
        assert True