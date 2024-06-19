import logging 
from ..ShopifyConnector import (
    ShopifyConnector,
    GraphQLError
)
from .graphql_queries import update_title_for_an_item,delete_product_query,create_product_query,get_products_query
import requests
import json

logger= logging.getLogger(__name__)

class ShopifyProducts(ShopifyConnector):

    def __init__(self, store_name, access_token):
        """
        Initializes a new instance of the ShopifyProducts class.

        Args:
            store_name (str): The name of the Shopify store.
            access_token (str): The access token for the Shopify API.

        This method calls the __init__ method of the parent class ShopifyConnector with the provided store_name and access_token.
        """
        super().__init__(store_name, access_token)
        

    def get_products(
        self,
        max_levels:str,
        sort=False
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
                    'query': get_products_query(max_levels)
                })
            )
            if 'errors' in response.json():
                raise GraphQLError(response.json()['errors'])
            
            if sort:
                products = response.json()['data']['products']['edges']
                return sorted(products, key=lambda product: product["node"]["createdAt"])
            
            else:
                return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")


    def get_id_from_sku(
            self,
            sku:str
    )->dict:
        """
        Updates an inventory quantity of a specific item_id
        Uses Shopify's GRAPHQL Api
        """
        SKU_QUERY = """
        query getProductID($sku: String!) {
        productVariants(first: 1, query: $sku) {
            edges {
            node {
                id
                product {
                id
                title
                }
            }
            }
        }
        }
        """
        variables = {"sku": sku}  
        try:
            response = requests.post(
                self.store_url+"/graphql.json",
                headers=self.headers,
                data=json.dumps({
                    'query': SKU_QUERY,
                    "variables": variables
                }
                )
            )
            if 'errors' in response.json():
                raise GraphQLError(response.json()['errors'])
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
    

    def update_product_title(
        self,
        new_title:str,
        product_gid:str
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
                    'query': update_title_for_an_item(new_title, product_gid)
                })
            )
            if 'errors' in response.json():
                raise GraphQLError(response.json()['errors'])
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")


    def delete_product(
        self,
        product_gid:str
        )->dict:
        """
        Updates an inventory quantity of a specific item_id
        Uses Shopify's GRAPHQL Api

        deletes product's variant
        """
        try:
            response = requests.post(
                self.store_url+"/graphql.json",
                headers=self.headers,
                data=json.dumps({
                    'query': delete_product_query(product_gid)
                })
            )
            if 'errors' in response.json():
                raise GraphQLError(response.json()['errors'])
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")

    def create_product(
        self,
        product_title:str
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
                    'query': create_product_query(product_title)
                })
            )
            if 'errors' in response.json():
                raise GraphQLError(response.json()['errors'])
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")

###########
#### REST API
###########

    # def get_products(self)->list | None:
    #     """
    #     Retrieves all products from the specified collection.
    #     Uses Shopify's REST Api
    #     """
    #     url = f"{self.store_url}/products.json"
    #     products = []
    #     try :
    #         response = requests.get(url, headers=self.headers)
    #         if response.status_code == 200:
    #             products = response.json()['products']
    #             if len(products) > 0 :
    #                 return products
    #             else:
    #                 return None
    #     except requests.exceptions.RequestException as e:
    #         logger.error(f"Error: {e}")
    
    # def get_product(
    #         self,
    #         product_id:str
    #         )-> dict | None:
    #     """
    #     Retrieves a specific product by its ID.
    #     Uses Shopify's REST Api
    #     """

    #     url = f"{self.store_url}/products/{product_id}.json"
    #     product = {}
    #     try :
    #         response = requests.get(url, headers=self.headers)
    #         if response.status_code == 200:
    #             product = response.json()['product']
    #             if len(product) > 0 :
    #                 return product
    #             else:
    #                 return None
    #     except requests.exceptions.RequestException as e:
    #         logging.error(f"Error: {e}")
        
    # def update_product(
    #         self,
    #         product_id:str,
    #         data:dict
    #         )-> None:
    #     """
    #     Updates a product in the specified collection.
    #     Uses Shopify's REST Api
    #     """

    #     url = f"{self.store_url}/admin/api/2023-04/products/{product_id}.json"
    #     try :
    #         payload = json.dumps(
    #             {"product":data}
    #             )
    #         response = requests.request("PUT", url, headers=self.headers, data=payload)
    #         if response.status_code == 200:
    #             logger.info("Product updated successfully")
    #     except requests.exceptions.RequestException as e:
    #         logger.error(f"Error: {e}")

    # def extract_id_from_sku(
    #         self,
    #         target_sku:str
    #         )-> int | None:
    #     """
    #     Extracts the product ID from a given SKU.
    #     Uses Shopify's REST Api
    #     Args:
    #         target_sku (str): The SKU of the product.
    #     Returns:
    #         int | None: The product ID if found, None otherwise.
    #     Raises:
    #         requests.exceptions.RequestException: If there is an error making the API request.
    #     """
        
    #     target_sku = str(target_sku)
    #     try :
    #         products = self.get_products()
    #         for product in products:
    #             for variant in product["variants"]:
    #                 if variant["sku"] == target_sku:
    #                     product_id = product["id"]
    #                     break
    #         if product_id:
    #             return product_id
    #         else:
    #             return  None

    #     except requests.exceptions.RequestException as e:
    #         logger.error(f"Error: {e}")


    # def delete_product(
    #         self,
    #         product_id:str
    #         )-> None:
    #     """
    #     Deletes a product from the specified collection.
    #     Uses Shopify's REST Api
    #     """

    #     url = f"{self.store_url}/admin/api/2023-04/products/{product_id}.json"
    #     try :
    #         response = requests.delete(url, headers=self.headers)
    #         if response.status_code == 204:
    #             logger.info("Product deleted successfully")
    #         else:
    #             logger.error(f"Failed to delete product: {response.status_code} | {response.text}")
    #     except requests.exceptions.RequestException as e:
    #         logger.error(f"Error: {e}")

    # def create_product(self, product_data):
            
    #     url = f"{self.store_url}/products.json"

    #     response = requests.post(url, headers=self.headers, data=json.dumps(product_data))
    #     if response.status_code == 201:
    #         print("Product created successfully")
    #         return response.json()
    #     else:
    #         print(f"Failed to create product: {response.status_code}")
    #         print(response.json())
    #         return None