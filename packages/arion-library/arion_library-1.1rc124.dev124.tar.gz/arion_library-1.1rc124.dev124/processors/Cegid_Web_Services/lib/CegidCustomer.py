from .CegidBase import CegidBase

class CegidCustomer(CegidBase):
    """
    A class to interact with the Cegid Customer SOAP web service.

    Inherits from CegidBase to utilize the SOAP client creation.

    Attributes:
        wsdl_url (str): The URL to the WSDL of the web service.
        username (str): The username for authentication.
        password (str): The password for authentication.
        client (zeep.client.ServiceProxy): The service proxy object for SOAP operations.
    """

    def __init__(self, wsdl_url, username, password) -> None:
        """
        Initializes the CegidCustomer with the given WSDL URL, username, and password.

        Args:
            wsdl_url (str): The URL to the WSDL of the web service.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        super().__init__(wsdl_url, username, password)
        self.client = super().createSoapConnector()

    def GetCustomerIdByReference(self, customerReference="", DatabaseId=""):
        """
        Retrieves a customer ID by reference from the Cegid web service.

        Args:
            customerReference (str): The reference of the customer to retrieve.
            DatabaseId (str): The database ID for the context.

        Returns:
            dict: The response from the GetCustomerIdByReference operation.
        """
        request_data = {
            'customerReference': customerReference,
            'clientContext': {
                'DatabaseId': DatabaseId
            }
        }

        # Call the GetCustomerIdByReference operation
        response = self.client.GetCustomerIdByReference(**request_data)

        return response

    def AddNewCustomer(self, customerData, DatabaseId=""):
        """
        Adds a new customer to the Cegid system.

        Args:
            customerData (dict): The data for the new customer.
            DatabaseId (str): The database ID for the context.

        Returns:
            dict: The response from the AddNewCustomer operation.
        """
        request_data = {
            'customerData': customerData,
            'clientContext': {
                'DatabaseId': DatabaseId
            }
        }

        # Call the AddNewCustomer operation
        response = self.client.AddNewCustomer(**request_data)

        # Print the response
        print(response)
        return response
