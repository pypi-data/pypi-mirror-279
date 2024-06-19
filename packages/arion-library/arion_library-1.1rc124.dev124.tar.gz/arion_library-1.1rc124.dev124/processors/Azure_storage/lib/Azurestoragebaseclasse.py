import logging
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.data.tables import TableServiceClient, generate_table_sas, TableSasPermissions
from datetime import datetime, timezone, timedelta
from azure.core.credentials import AzureNamedKeyCredential
from ...Baseconnector.BaseConnector import BaseConnector

class AzureStorageConnector(BaseConnector):
    """
    This class allows establishing a connection with Azure Blob and Azure Table storage services.

    :param connection_string: The connection string to use to connect to the service. Defaults to None.
    :type connection_string: str, optional
    :param account_name: The name of the Azure storage account. Defaults to None.
    :type account_name: str, optional
    :param account_key: The key for the Azure storage account. Defaults to None.
    :type account_key: str, optional

    :ivar connection_string: The connection string to use to connect to the service.
    :vartype connection_string: str
    :ivar account_name: The name of the Azure storage account.
    :vartype account_name: str
    :ivar account_key: The key for the Azure storage account.
    :vartype account_key: str
    :ivar logger: The logger for recording messages.
    :vartype logger: logging.Logger
    """

    def __init__(self, connection_string=None, account_name=None, account_key=None):
        """
        Initializes an instance of the AzureStorageConnector class.

        :param connection_string: The connection string to use to connect to the service. Defaults to None.
        :type connection_string: str, optional
        :param account_name: The name of the Azure storage account. Defaults to None.
        :type account_name: str, optional
        :param account_key: The key for the Azure storage account. Defaults to None.
        :type account_key: str, optional
        """
        self.connection_string = connection_string
        self.account_name = account_name
        self.account_key = account_key
        self.logger = logging.getLogger('AzureStorageConnector')
