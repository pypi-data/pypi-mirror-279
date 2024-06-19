

"""
NOTE : https://shopify.dev/docs/api/admin-graphql/
"""
def get_orders_query(number_of_orders_to_show):
    """
    Returns the GraphQL query for getting orders.
    NOTE : customer field should be allowed on read/write mode from shopify store api
    """
    GET_ORDERS_QUERY ="""
    {{
    orders(first: {number_of_orders_to_show}) {{
        edges {{
        node {{
            id
            name
            createdAt
            totalPriceSet {{
            shopMoney {{
                amount
                currencyCode
            }}
            }}
            lineItems(first: 5) {{
            edges {{
                node {{
                title
                quantity
                originalUnitPriceSet {{
                    shopMoney {{
                    amount
                    currencyCode
                    }}
                }}
                }}
            }}
            }}
            customer {{
            firstName
            lastName
            email
            }}
        }}
        }}
    }}
    }}
    """.format(
        number_of_orders_to_show=number_of_orders_to_show
        )
    
    return GET_ORDERS_QUERY

def get_inventory_levels_query(number_of_levels_to_show):
    """
    Returns the GraphQL query to get inventory levels.
    """
    number_of_levels_to_show = str(number_of_levels_to_show)
    GET_INVENTORY_LEVEL_QUERY ="""
    query {{
    shop {{
        # Retrieves inventory at fulfillment service app locations
        fulfillmentServices {{
        location {{
            # The ID of the location.
            id
            # Retrieves the first three inventory levels associated with each location
            inventoryLevels(first: {number_of_levels_to_show}) {{
            edges {{
                node {{
                id
                }}
            }}
            }}
        }}
        }}
    }}
    }}
    """.format(
        number_of_levels_to_show=number_of_levels_to_show
        )
    
    return GET_INVENTORY_LEVEL_QUERY

def get_inventory_quantity_query(inventory_level_id:str):
    """
    Returns the GraphQL query to an inventory quantity within a single location
    """
    inventory_level_id=str(inventory_level_id)
    GET_INVENTORY_QUANTITY_QUERY ="""
    query {{
    inventoryLevel(id:"{inventory_level_id}") {{
        id
        # The quantities field takes an array of inventory states, which include the following: `incoming`, `on_hand`, `available`, `committed`, `reserved`, `damaged`, `safety_stock`, and `quality_control`.
        quantities(names: ["available"]) {{
        name
        quantity
        }}
        item {{
        id
        }}
        location {{
        id
        }}
        createdAt
        updatedAt
        canDeactivate
    }}
    }}
    """.format(inventory_level_id=inventory_level_id)
    
    return GET_INVENTORY_QUANTITY_QUERY


def get_inventory_quantity_multiple_location(
        inventoryItemId:str,
        max_levels
        ):
    """
    This query retrieve inventory quantities for an item at all locations.
    """
    inventoryItemId = str(inventoryItemId)
    max_levels = str(max_levels)
    
    GET_INVENTORY_QUANTITY_QUERY ="""
    {{
    inventoryItem(id: "{inventoryItemId}") {{
        # Retrieves the first five inventory levels.
        inventoryLevels(first: {max_levels}) {{
        edges {{
            node {{
            # The quantities field takes an array of inventory states, which include the following: `incoming`, `on_hand`, `available`, `committed`, `reserved`, `damaged`, `safety_stock`, and `quality_control`.
            quantities(names: ["available", "on_hand", "reserved", "committed"]) {{
                name
                quantity
            }}
            }}
        }}
        }}
    }}
    }}
    """.format(
        inventoryItemId=inventoryItemId,
        max_levels=max_levels
        )
    
    return GET_INVENTORY_QUANTITY_QUERY

def set_inventory_quantity_for_an_item(
        inventoryItemId:str,
        locationId:str,
        new_quantity:str
        ):
    """
    TODO : check utility of referenceDocumentUri: "gid://shopify/Order/1974482927638",

    This query have to explicitly set the quantity of inventory that's in the on_hand state.
    Example of inventoryItemId: "gid://shopify/InventoryItem/32889739542550"
               locationId     : "gid://shopify/Location/35239591958" 
    """
    inventoryItemId =str(inventoryItemId)
    locationId =str(locationId)
    new_quantity =str(new_quantity)

    UPDATE_QUANTITY_QUERY ="""
    mutation {{
    inventorySetOnHandQuantities(input: {{
        reason: "correction",
        referenceDocumentUri: "gid://shopify/Order/1974482927638",
        setQuantities: [
        {{
            inventoryItemId: "{inventoryItemId}",
            locationId: "{locationId}",
            quantity: {new_quantity}
        }}
        ]
    }}
    ) {{
        inventoryAdjustmentGroup {{
        id
        changes {{
            name
            delta
            quantityAfterChange
        }}
        reason
        referenceDocumentUri
        }},
        userErrors {{
        message
        code
        field
        }}
    }}
    }}
    """.format(
        new_quantity=new_quantity,
        inventoryItemId=inventoryItemId,
        locationId=locationId
        )
    
    return UPDATE_QUANTITY_QUERY


def get_products_query(maxlevels):

    GET_PRODUCTS_QUERY ="""
    {{
    products(first: {maxlevels}) {{
        edges {{
        node {{
            id
            title
            description
            createdAt
            variants(first: 5) {{
            edges {{
                node {{
                id
                title
                price
                sku
                displayName
                barcode
                }}
            }}
            }}
        }}
        }}
    }}
    }}
    """.format(maxlevels=maxlevels)

    return GET_PRODUCTS_QUERY


def create_product_query(
        product_title:str
        ):

    CREATE_PRODUCT_QUERY ="""
    mutation {{
    productCreate(input: {{
        title: "{product_title}"
    }}) {{
        product {{
        id
        title
        }}
    }}
    }}
    """.format(
        product_title=product_title
        )
    return CREATE_PRODUCT_QUERY

def delete_product_query(
        product_gid:str
        ):

    product_gid =str(product_gid)

    DELETE_PRODUCT_QUERY ="""
    mutation {{
    productDelete(input: {{id: "{product_gid}"}}) {{
        deletedProductId
    }}
    }}
    """.format(
        product_gid=product_gid
        )
    
    return DELETE_PRODUCT_QUERY


def update_title_for_an_item(
        new_title:str,
        product_gid:str
        ):
    """
    TODO : check utility of referenceDocumentUri: "gid://shopify/Order/1974482927638",

    This query have to explicitly set the quantity of inventory that's in the on_hand state.
    Example of inventoryItemId: "gid://shopify/InventoryItem/32889739542550"
               locationId     : "gid://shopify/Location/35239591958" 
    """
    new_title =str(new_title)
    product_gid =str(product_gid)

    UPDATE_TITLE_QUERY ="""
    mutation {{
    productUpdate(input: {{id: "{product_gid}", title: "{new_title}"}}) {{
        product {{
        id
        title
        }}
    }}
    }}
    """.format(
        product_gid=product_gid,
        new_title=new_title
        )
    
    return UPDATE_TITLE_QUERY