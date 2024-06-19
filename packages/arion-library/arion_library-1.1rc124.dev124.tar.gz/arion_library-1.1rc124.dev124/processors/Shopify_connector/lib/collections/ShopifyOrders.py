from ..ShopifyConnector import ShopifyConnector
import requests
import json
from processors.Shopify_connector.lib.collections.graphql_queries import (
    get_orders_query
)
import logging

logger = logging.getLogger(__name__)

class ShopifyOrders(ShopifyConnector):
    """
    This class servers as abstracction for the shopify orders collection
    NOTE : 
        For REST API: https://shopify.dev/docs/api/admin-rest/2023-10/resources/order
        For GRAPHQL Api: https://shopify.dev/docs/api/admin-graphql/latest/objects/Order
    """
    def __init__(self, store_name, access_token):
        super().__init__(store_name, access_token)
    
    def fetch_orders(
        self,
        cursor:str=None,
        number_of_orders_to_show=10
        )->dict:
        """
        Retrieves all orders from the specified collection.
        Uses Shopify's GRAPHQL Api
        """
        variables = {'cursor': cursor}
        response = requests.post(
            self.store_url+"/graphql.json",
            headers=self.headers,
            data=json.dumps({
                'query': get_orders_query(number_of_orders_to_show),
                'variables': variables
            })
        )
        
        return response.json()
    
    def get_orders(self)->list | None:
        """
        Retrieves all products from the specified collection.
        Uses Shopify's REST Api
        """
        url = f"{self.store_url}/orders.json"
        orders = []
        try :
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                orders = response.json()['orders']
                if len(orders) > 0 :
                    return orders
                else:
                    return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
        
    