import pytest
from io import BytesIO
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobSasPermissions
from ..lib.Azurestoragebaseclasse import AzureStorageConnector
from datetime import datetime, timedelta, timezone
from ..lib.azureBlobStorage import AzureBlobProcessor

# Test configuration - replace these with your actual values
CONNECTION_STRING = ""
ACCOUNT_NAME = ""
ACCOUNT_KEY = ""
CONTAINER_NAME = ""
FLOW_NAME = ""
BLOB_NAME=""

@pytest.fixture
def azure_blob_processor():
    """Fixture for AzureBlobProcessor instance."""
    return AzureBlobProcessor(
        container_name=CONTAINER_NAME,
        flow_name=FLOW_NAME,
        connection_string=CONNECTION_STRING,
        account_name=ACCOUNT_NAME,
        account_key=ACCOUNT_KEY
    )

def test_connect_blob_service_with_connection_string():
    """Test connecting to Azure Blob service using connection string."""
    azure_blob_processor = AzureBlobProcessor(
        container_name=CONTAINER_NAME,
        flow_name=FLOW_NAME,
        connection_string=CONNECTION_STRING,
        account_name=None,
        account_key=None
    )
    azure_blob_processor.connect_blob_service(CONTAINER_NAME)
    assert azure_blob_processor.blob_service_client is not None

def test_connect_blob_service_with_account_credentials(azure_blob_processor):
    """Test connecting to Azure Blob service using account name and account key."""
    azure_blob_processor.connect_blob_service(CONTAINER_NAME)
    assert azure_blob_processor.blob_service_client is not None


def test_generate_blob_sas_key(azure_blob_processor):
    """Test generating SAS token for Azure Blob Storage."""
    expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    azure_blob_processor.connect_blob_service(CONTAINER_NAME)
    sas_token = azure_blob_processor.generate_blob_sas_key(CONTAINER_NAME,BLOB_NAME, permissions=BlobSasPermissions(read=True), expiry=expiry)
    assert isinstance(sas_token, str)
    assert sas_token.startswith("se=")  # Simple check to ensure it looks like a SAS token

def test_read_blob_files(azure_blob_processor):
    """Test reading blob files from Azure Blob storage."""
    blobs = list(azure_blob_processor.read_blob_files())
    assert isinstance(blobs, list)
    for blob in blobs:
        assert 'file_name' in blob
        assert 'file_content' in blob

def test_push_files_to_blob(azure_blob_processor):
    """Test pushing files to Azure Blob storage."""
    files_info = [
        ("test_file_1.txt", BytesIO(b"Test content 1")),
        ("test_file_2.txt", BytesIO(b"Test content 2"))
    ]
    azure_blob_processor.push_files_to_blob(files_info)
    
    container_client = azure_blob_processor.blob_service_client.get_container_client(CONTAINER_NAME)
    for file_info in files_info:
        file_name = file_info[0]
        current_date = datetime.now().strftime("%d-%m-%Y")
        folder_name = f"{FLOW_NAME}/{current_date}/"
        blob_name = folder_name + file_name
        blob_client = container_client.get_blob_client(blob_name)
        assert blob_client.exists()