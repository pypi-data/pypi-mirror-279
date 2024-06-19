"""
This script demonstrates the usage of the ShopifyCustomers class to manage customers in a Shopify store.

Classes:
    ShopifyCustomers: A class to interact with the Shopify API for customer-related operations.

Functions:
    main(): Executes a series of operations using the ShopifyCustomers class, including retrieving, adding, deleting, and updating customers.
"""

from ..lib.collections.ShopifyCustomers import ShopifyCustomers

def main():
    """
    Main function to demonstrate the usage of the ShopifyCustomers class.
    
    This function performs the following operations:
    1. Instantiates the ShopifyCustomers class with store name and access token.
    2. Retrieves a list of customers from the Shopify store.
    3. Prints the retrieved customers.
    4. Defines and adds a new customer.
    5. Prints the response from the customer creation.
    6. Deletes a customer by their ID.
    7. Updates an existing customer's information.
    """
    # Instantiate the ShopifyCustomers class with store name and access token
    shopify_customers = ShopifyCustomers("stor_name", "store_token")

    # Retrieve a list of customers from the Shopify store
    customers = shopify_customers.getCustomers()
    print(customers)

    # Define the data for a new customer
    customer_data = {
        "email": "steve.lastnameson@example.com",
        "phone": "+16465555555",
        "firstName": "Steve",
        "lastName": "Lastname",
        "acceptsMarketing": True,
        "addresses": [
            {
                "address1": "412 fake st",
                "city": "Ottawa",
                "province": "ON",
                "phone": "+16469999999",
                "zip": "A1A 4A1",
                "lastName": "Lastname",
                "firstName": "Steve",
                "country": "CA"
            }
        ]
    }

    # Add a new customer to the Shopify store
    response_create = shopify_customers.addCustomer(customer_data)
    print(response_create)

    # Define the ID of the customer to be deleted
    customer_id = "gid://shopify/Customer/7971972251922"

    # Delete the customer from the Shopify store
    response_delete = shopify_customers.deleteCustomer(customer_id)

    # Define the data for updating an existing customer
    customer_data = {
        "id": "gid://shopify/Customer/7971972284690",
        "firstName": "Tobi",
        "lastName": "Lutke"
    }

    # Update the existing customer in the Shopify store
    response_update = shopify_customers.updateCustomer(customer_data)


main()