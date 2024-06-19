from ..ShopifyConnector import ShopifyConnector
import requests

class ShopifyCustomers(ShopifyConnector):
    """
    A class to manage Shopify customers through the Shopify API.

    Inherits from:
        ShopifyConnector

    Attributes:
        store_name (str): The name of the Shopify store.
        access_token (str): The access token for authenticating API requests.

    Methods:
        getCustomers(): Retrieves a list of customers from the Shopify store.
        deleteCustomer(customer_id): Deletes a customer from the Shopify store by their ID.
        addCustomer(customer_data): Adds a new customer to the Shopify store.
        updateCustomer(customer_data): Updates an existing customer in the Shopify store.
    """

    def __init__(self, store_name, access_token) -> None:
        """
        Initializes the ShopifyCustomers class with the store name and access token.

        Args:
            store_name (str): The name of the Shopify store.
            access_token (str): The access token for authenticating API requests.
        """
        super().__init__(store_name, access_token)

    def getCustomers(self):
        """
        Retrieves a list of customers from the Shopify store.

        Sends a GraphQL query to the Shopify API to get the first 10 customers.

        Returns:
            None
        """
        query = """
        {
        customers(first: 10) {
            edges {
            node {
                id
            }
            }
        }
        }
        """

        url = f"{self.store_url}graphql.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token
        }

        response = requests.post(url, json={'query': query}, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Query failed with status code {response.status_code}: {response.text}")

    def deleteCustomer(self, customer_id):
        """
        Deletes a customer from the Shopify store by their ID.

        Sends a GraphQL mutation to the Shopify API to delete a customer.

        Args:
            customer_id (str): The ID of the customer to be deleted.

        Returns:
            dict: The response data from the API if the request is successful.
        """
        mutation = """
        mutation customerDelete($id: ID!) {
          customerDelete(input: {id: $id}) {
            shop {
              id
            }
            userErrors {
              field
              message
            }
            deletedCustomerId
          }
        }
        """

        url = f"{self.store_url}graphql.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token
        }

        variables = {
            "id": customer_id
        }

        response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                print(data)
                return data
            except ValueError:
                print("Response content is not valid JSON")
        else:
            print(f"Mutation failed with status code {response.status_code}: {response.text}")

    def addCustomer(self, customer_data):
        """
        Adds a new customer to the Shopify store.

        Sends a GraphQL mutation to the Shopify API to create a new customer.

        Args:
            customer_data (dict): A dictionary containing the customer data.

        Returns:
            dict: The response data from the API if the request is successful.
        """
        mutation = """
        mutation customerCreate($input: CustomerInput!) {
          customerCreate(input: $input) {
            userErrors {
              field
              message
            }
            customer {
              id
            }
          }
        }
        """

        url = f"{self.store_url}graphql.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token
        }

        variables = {
            "input": customer_data
        }

        response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                print(data)
                return data
            except ValueError:
                print("Response content is not valid JSON")
        else:
            print(f"Mutation failed with status code {response.status_code}: {response.text}")

    def updateCustomer(self, customer_data):
        """
        Updates an existing customer in the Shopify store.

        Sends a GraphQL mutation to the Shopify API to update a customer.

        Args:
            customer_data (dict): A dictionary containing the updated customer data.

        Returns:
            dict: The response data from the API if the request is successful.
        """
        mutation = """
        mutation customerUpdate($input: CustomerInput!) {
          customerUpdate(input: $input) {
            userErrors {
              field
              message
            }
            customer {
              id
            }
          }
        }
        """

        url = f"{self.store_url}graphql.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token
        }

        variables = {
            "input": customer_data
        }

        response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                print(data)
                return data
            except ValueError:
                print("Response content is not valid JSON")
        else:
            print(f"Mutation failed with status code {response.status_code}: {response.text}")
