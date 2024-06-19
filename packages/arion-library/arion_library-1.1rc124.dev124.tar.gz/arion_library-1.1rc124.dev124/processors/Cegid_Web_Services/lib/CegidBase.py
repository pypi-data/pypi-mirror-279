from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import requests


class CegidBase:
    """
    A base class for creating a SOAP client connection to the Cegid web service.

    Attributes:
        wsdl_url (str): The URL to the WSDL of the web service.
        username (str): The username for authentication.
        password (str): The password for authentication.
    """

    def __init__(self, wsdl_url, username, password) -> None:
        """
        Initializes the CegidBase with the given WSDL URL, username, and password.

        Args:
            wsdl_url (str): The URL to the WSDL of the web service.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        self.wsdl_url = wsdl_url
        self.username = username
        self.password = password

    def createSoapConnector(self):
        """
        Creates and returns a SOAP client connected to the web service.

        This method sets up a session with basic authentication using the provided
        username and password, and then creates a SOAP client using the Zeep library.

        Returns:
            zeep.client.ServiceProxy: The service proxy object that allows interaction
            with the SOAP service.
        """
        # Create a session and set up basic authentication
        session = requests.Session()
        session.auth = HTTPBasicAuth(self.username, self.password)

        # Create a transport with the session
        transport = Transport(session=session)

        # Create the SOAP client
        client = Client(wsdl=self.wsdl_url, transport=transport)

        return client.service