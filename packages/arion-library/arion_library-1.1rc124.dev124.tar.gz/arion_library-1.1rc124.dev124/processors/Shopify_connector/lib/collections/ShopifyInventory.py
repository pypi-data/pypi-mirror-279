from ..ShopifyConnector import (
    ShopifyConnector,
    GraphQLError
)
import requests
import json
from processors.Shopify_connector.lib.collections.graphql_queries import (
    get_inventory_levels_query,
    get_inventory_quantity_query,
    get_inventory_quantity_multiple_location,
    set_inventory_quantity_for_an_item
)
import logging

logger = logging.getLogger(__name__)

class ShopifyInventory(ShopifyConnector):
    """
    This class servers as abstracction for the shopify inventory collection
    NOTE : https://shopify.dev/docs/apps/fulfillment/inventory-management-apps/quantities-states#set-inventory-quantities-on-hand
    """

    def __init__(self, store_name, access_token):
        """
        Initializes a new instance of the ShopifyInventory class.

        Args:
            store_name (str): The name of the Shopify store.
            access_token (str): The access token for the Shopify API.

        This method calls the __init__ method of the parent class ShopifyConnector with the provided store_name and access_token.
        """
        super().__init__(store_name, access_token)
    
    def fetch_inventory_levels(
        self,
        number_of_levels_to_show=3
        )->dict:
        """
        Retrieves all inventory levels from the specified collection.
        Uses Shopify's GRAPHQL Api
        """
        try:
                
            response = requests.post(
                self.store_url+"/graphql.json",
                headers=self.headers,
                data=json.dumps({
                    'query': get_inventory_levels_query(number_of_levels_to_show)
                })
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
    
    def fetch_item_quantity_single_location(
        self,
        number_of_levels_to_show=3
        )->dict:
        """
        Retrieves all inventory quantity within a single location
        Uses Shopify's GRAPHQL Api
        """
        try:
                
            response = requests.post(
                self.store_url+"/graphql.json",
                headers=self.headers,
                data=json.dumps({
                    'query': get_inventory_quantity_query(number_of_levels_to_show)
                })
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")

    def fetch_item_quantity_multiple_location(
        self,
        inventoryItemId,
        number_of_levels_to_show=3
        )->dict:
        """
        Retrieves all inventory quantity within multiple locations
        Uses Shopify's GRAPHQL Api
        """
        try:
                
            response = requests.post(
                self.store_url+"/graphql.json",
                headers=self.headers,
                data=json.dumps({
                    'query': get_inventory_quantity_multiple_location(inventoryItemId,number_of_levels_to_show)
                })
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
        
    def set_item_quantity(
        self,
        inventoryItemId:str,
        location_id:str,
        quantity:int
        )->dict:
        """
        Updates an inventory quantity of a specific item_id
        Uses Shopify's GRAPHQL Api
        """
        try:
            response = requests.post(
                self.store_url+"/graphql.json",
                headers=self.headers,
                data=json.dumps({
                    'query': set_inventory_quantity_for_an_item(inventoryItemId, location_id, quantity)
                })
            )
            if 'errors' in response.json():
                raise GraphQLError(response.json()['errors'])
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
        
    