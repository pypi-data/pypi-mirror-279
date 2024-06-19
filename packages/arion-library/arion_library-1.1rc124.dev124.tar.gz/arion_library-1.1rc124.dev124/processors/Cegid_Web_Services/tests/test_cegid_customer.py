import pytest
from ..lib.CegidCustomer import CegidCustomer

@pytest.fixture
def cegid_customer():
    """
    Fixture for initializing the CegidCustomer instance.

    This fixture replaces the values with your actual WSDL URL, username, and password.

    Returns:
        CegidCustomer: An instance of the CegidCustomer class.
    """
    # Replace these values with your actual WSDL URL, username, and password
    wsdl_url = ''
    username = ''
    password = ''
    return CegidCustomer(wsdl_url, username, password)

def test_get_customer_id_by_reference(cegid_customer):
    """
    Test for the GetCustomerIdByReference method of CegidCustomer.

    Args:
        cegid_customer (CegidCustomer): The CegidCustomer instance.

    This test verifies that the GetCustomerIdByReference method returns a valid response
    and contains the expected attributes.

    """
    customerReference = ""
    DatabaseId = ""

    # Call the GetCustomerIdByReference method
    response = cegid_customer.GetCustomerIdByReference(customerReference, DatabaseId)

    # Print the response for debugging purposes
    print(response)

    # Add assertions based on expected response structure and content
    assert response is not None
    assert hasattr(response, 'CustomerId')
    # Add more assertions as needed to validate the response

def test_add_new_customer(cegid_customer):
    """
    Test for the AddNewCustomer method of CegidCustomer.

    Args:
        cegid_customer (CegidCustomer): The CegidCustomer instance.

    This test verifies that the AddNewCustomer method returns a valid response when
    adding a new customer with specified data.

    """
    customerData = {
        'AddressData': {
            'AddressLine1': '123 Main St',
            'City': 'Marseille',
            'CountryId': 'FRA',
            'ZipCode': '13000'
        },
        'FirstName': 'John',
        'LastName': 'Doe',
        'EmailData': {
            'Email': 'john.doe@example.com'
        },
        'PhoneData': {
            'CellularPhoneNumber': '555-1234'
        }
    }
    DatabaseId = ""

    # Call the AddNewCustomer method
    response = cegid_customer.AddNewCustomer(customerData, DatabaseId)

    # Print the response for debugging purposes
    print(response)

    # Add assertions based on expected response structure and content
    assert response is not None
    # Add more assertions as needed to validate the response