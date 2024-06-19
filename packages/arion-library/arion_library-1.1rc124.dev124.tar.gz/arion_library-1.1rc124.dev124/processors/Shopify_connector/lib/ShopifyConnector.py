import requests
import logging
import multiprocessing 
import time
import pandas as pd
import json
from urllib.parse import urljoin
from ...Baseconnector.BaseConnector import BaseConnector

logger= logging.getLogger(__name__)

class GraphQLError(Exception):
    """Custom exception for GraphQL errors."""
    def __init__(self, errors):
        super().__init__("GraphQL query failed with errors")

        self.errors = errors
class ShopifyConnector(BaseConnector):

    """
    A class used to interact with Shopify's REST API.

    This class provides methods to get and update products, as well as extract product IDs from SKUs.

    Attributes:
        store_url (str): The URL of the Shopify store.
        access_token (str): The access token for the Shopify API.
        headers (dict): The headers to be included in API requests.
        products (list): The list of all products in the store.

    Methods:
        __init__(store_url, access_token, collection_name): Initializes a new instance of the ShopifyConnector class.
        get_products(): Retrieves all products from the specified collection.
        get_product(product_id): Retrieves a specific product by its ID.
        extract_id_from_sku(target_sku): Extracts the product ID from a given SKU.
        update_product(product_id, data): Updates a specific product with the given data.

    NOTE :
        For graphql : https://shopify.dev/docs/api/admin-graphql
        For REST API: https://shopify.dev/docs/api/admin-rest
    """

    def __init__(self, store_name, access_token)->None:

        super().__init__()
        self.store_name = store_name
        self.api_version = "2023-04"
        self.store_url= urljoin(f'https://{store_name}.myshopify.com',f'admin/api/{self.api_version}')
        self.access_token = access_token
        self.headers = {}
        self.headers.update(
        {
            'X-Shopify-Access-Token': access_token,
            'Content-Type': 'application/json'
        }
        )
        self.hooks = {}
        self.hooks['response'] = []

        def rate_hook(r, *args, **kwargs):
            if "X-Shopify-Shop-Api-Call-Limit" in r.headers:
                logger.info("rate:", r.headers["X-Shopify-Shop-Api-Call-Limit"])
            if r.status_code == 429:
                time.sleep(int(float(r.headers["Retry-After"])))
                logger.info("rate limit reached, sleeping")
                
        self.hooks["response"].append(rate_hook)
        
        # self.products = self.get_products()   

    def run_task_in_parallel(
            task_func:list,
            data_list:list
            )-> tuple | float:
        
        num_processes = multiprocessing.cpu_count()
        start_time = time.time()
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.map(task_func, data_list)
        execution_time = time.time() - start_time
        return results, execution_time
    
    def location_mapping(
            file1_path:str,
            file2_path:str,
            on_field:str
            ):
        """
        Maps the locations from two CSV files based on a specified field.
        Args:
            file1_path (str): The path to the first CSV file.
            file2_path (str): The path to the second CSV file.
            on_field (str): The field to perform the inner join on.
        Returns:
            pandas.DataFrame: The merged DataFrame containing the mapped locations.
        Raises:
            Exception: If an error occurs during the mapping process.
        """
        try:
            # Load CSV files into pandas DataFrames
            df1 = pd.read_csv(file1_path)
            df2 = pd.read_csv(file2_path)
            
            # Perform inner join
            merged_df = pd.merge(df1, df2, how='inner', on=on_field)
            
            return merged_df
        
        except Exception as e:
            logger.error("An error occurred:", e)
            return None

    def create_webhook_using_rest(self ,
                                  event_name:str,
                                  callback_url:str
                                  )-> None:
        """
        Creates a webhook using the REST API.
        Args:
            event_name (str): The name of the event to subscribe to.
            callback_url (str): The URL to send the event data to.
        Returns:
            None
        """
        try:
            url = f"{self.store_url}/webhooks.json"
            payload = json.dumps({
            "webhook": {
                "address": callback_url,
                "topic": event_name
            }
            })
            response = requests.request("POST", url, headers=self.headers, data=payload)

            if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
                logger.info("Webhook created successfully")
                return response
            else:
                logger.error(f"Error: {response.text}")
                return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")

    def custom_graphql_query(self,
                     query:str
                     )->dict:
        try:  

            response = requests.post(
                self.store_url+"/graphql.json",
                headers=self.headers,
                data=json.dumps({
                    'query': query
                })
            )
            if 'errors' in response.json():
                raise GraphQLError(response.json()['errors'])
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")