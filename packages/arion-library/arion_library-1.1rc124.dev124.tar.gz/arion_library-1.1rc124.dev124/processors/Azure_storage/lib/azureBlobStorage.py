from io import BytesIO
from datetime import datetime
import re
from .Azurestoragebaseclasse import AzureStorageConnector
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone


class AzureBlobProcessor(AzureStorageConnector):
    """
    This class allows reading from and pushing files to Azure Blob storage.

    :param str container_name: The name of the Blob container.
    :param str flow_name: The name of the flow.
    :param str connection_string: The connection string to use to connect to the Blob service. Defaults to None.
    :param str account_name: The name of the Azure storage account. Defaults to None.
    :param str account_key: The key for the Azure storage account. Defaults to None.

    :ivar str container_name: The name of the Blob container.
    :ivar str flow_name: The name of the flow.
    :ivar str connection_string: The connection string to use to connect to the Blob service.
    :ivar str account_name: The name of the Azure storage account.
    :ivar str account_key: The key for the Azure storage account.
    """

    def __init__(self, container_name, flow_name, connection_string=None, account_name=None, account_key=None):
        """
        Initializes an instance of the AzureBlobProcessor class.

        :param str container_name: The name of the Blob container.
        :param str flow_name: The name of the flow.
        :param str connection_string: The connection string to use to connect to the Blob service. Defaults to None.
        :param str account_name: The name of the Azure storage account. Defaults to None.
        :param str account_key: The key for the Azure storage account. Defaults to None.
        """
        super().__init__(connection_string, account_name, account_key)
        self.container_name = container_name
        self.flow_name = flow_name
        self.blob_service_client = None

    def connect_blob_service(self, container_name, blob_permissions=BlobSasPermissions(read=True), blob_expiry=None):
        """
        Establishes a connection with the Azure Blob service.

        :param str container_name: The name of the Blob container.
        :param BlobSasPermissions blob_permissions: The permissions for the Blob SAS. Defaults to BlobSasPermissions(read=True).
        :param datetime blob_expiry: The expiry date for the Blob SAS. Defaults to None.

        :raises ValueError: If neither a connection string nor both an account name and account key are provided.

        :return: None
        """
        try:
            if self.connection_string:
                self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                self.logger.info("Connected to Azure Blob Service using connection string")
            elif self.account_name and self.account_key:
                sas_key = self.generate_blob_sas_key(container_name, permissions=blob_permissions, expiry=blob_expiry)
                self.blob_service_client = BlobServiceClient(sas_key)
                self.logger.info("Connected to Azure Blob Service using SAS Key")
            else:
                raise ValueError("Either connection string or both account name and account key must be provided")
        except Exception as e:
            self.logger.error(f"Error connecting to Azure Blob Service: {e}")

    def generate_blob_sas_key(self, container_name, blob_name, permissions=BlobSasPermissions(read=True), expiry=None):
        """
        Generates a SAS token for Azure Blob storage.

        :param str container_name: The name of the Blob container.
        :param str blob_name: The name of the Blob.
        :param BlobSasPermissions permissions: The permissions for the Blob SAS. Defaults to BlobSasPermissions(read=True).
        :param datetime expiry: The expiry date for the Blob SAS. Defaults to None.

        :return: The generated SAS token.
        :rtype: str
        """
        expiry = expiry or datetime.now(timezone.utc) + timedelta(hours=1)
        sas_token = generate_blob_sas(
            self.account_name,
            container_name,
            account_key=self.account_key,
            blob_name=blob_name,
            permission=permissions,
            expiry=expiry
        )
        return sas_token

    def read_blob_files(self, regex_pattern=r'.*', permissions=BlobSasPermissions(read=True), expiry=None):
        """
        Retrieves files from Azure Blob storage.

        :param str regex_pattern: The regular expression pattern to filter file names. Defaults to '.*'.
        :param BlobSasPermissions permissions: The permissions for the Blob SAS. Defaults to BlobSasPermissions(read=True).
        :param datetime expiry: The expiry date for the Blob SAS. Defaults to None.

        :return: A generator containing the file information.
        :rtype: generator
        """
        self.connect_blob_service(self.container_name, blob_permissions=permissions, blob_expiry=expiry)
        container_client = self.blob_service_client.get_container_client(self.container_name)
        for blob in container_client.list_blobs():
            if re.match(regex_pattern, blob.name):
                blob_client = container_client.get_blob_client(blob.name)
                file_content = BytesIO()
                file_content.write(blob_client.download_blob().readall())
                file_content.seek(0)
                yield {'file_name': blob.name, 'file_content': file_content}

    def push_files_to_blob(self, files_info, permissions=BlobSasPermissions(write=True), expiry=None):
        """
        Pushes files to Azure Blob storage.

        :param list files_info: The list of file information to push, where each item is a tuple containing the file name and its content.
        :param BlobSasPermissions permissions: The permissions for the Blob SAS. Defaults to BlobSasPermissions(write=True).
        :param datetime expiry: The expiry date for the Blob SAS. Defaults to None.

        :return: None
        """
        self.connect_blob_service(self.container_name, blob_permissions=permissions, blob_expiry=expiry)
        container_client = self.blob_service_client.get_container_client(self.container_name)
        for file_info in files_info:
            file_name = file_info[0]
            file_content = file_info[1]
            current_date = datetime.now().strftime("%d-%m-%Y")
            folder_name = f"{self.flow_name}/{current_date}/"
            blob_name = folder_name + file_name
            container_client.upload_blob(name=blob_name, data=file_content, overwrite=True)
            self.logger.info(f"File '{file_name}' successfully pushed to Azure Blob Storage.")
