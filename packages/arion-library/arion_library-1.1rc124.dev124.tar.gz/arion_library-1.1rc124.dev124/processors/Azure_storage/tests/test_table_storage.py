import pytest
from ..lib.TableStorage import AzureDataTablesClient
import logging
import os
from datetime import datetime, timezone, timedelta
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import  TableSasPermissions

CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=adfariontest;AccountKey=XQw1npD60T9P5p1NBW633V3yJ12YG3yJYcf2mHo0Boze5uthELC3miYI2ply00Q+1ceUHqmJh1wE+AStzAmxFg==;EndpointSuffix=core.windows.net"
ACCOUNT_NAME = "adfariontest"
ACCOUNT_KEY = "XQw1npD60T9P5p1NBW633V3yJ12YG3yJYcf2mHo0Boze5uthELC3miYI2ply00Q+1ceUHqmJh1wE+AStzAmxFg=="
TABLE_NAME = "test"



@pytest.fixture
def azure_data_tables_client():
    """Fixture for AzureDataTablesClient instance."""
    return AzureDataTablesClient(
        table_name=TABLE_NAME,
        connection_string=None,  # Set connection string to None to use account credentials
        account_name=ACCOUNT_NAME,
        account_key=ACCOUNT_KEY
    )

def test_connect_table_service_with_connection_string():
    """Test connecting to Azure Table service using connection string."""
    azure_data_tables_client = AzureDataTablesClient(
        table_name=TABLE_NAME,
        connection_string=CONNECTION_STRING,
        account_name=None,
        account_key=None
    )
    azure_data_tables_client.connect_table_service(TABLE_NAME)
    assert azure_data_tables_client.table_service_client is not None




def test_generate_table_sas_key(azure_data_tables_client):
    """Test generating SAS token for Azure Table Storage."""
    expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    credentials = AzureNamedKeyCredential(name=ACCOUNT_NAME, key=ACCOUNT_KEY)
    sas_token = azure_data_tables_client.generate_table_sas_key(credentials, TABLE_NAME, permissions=TableSasPermissions(read=True), expiry=expiry)
    assert isinstance(sas_token, str)

def test_insert_batch_entities(azure_data_tables_client):
    """Test inserting batch entities into Azure Table Storage."""
    entities = [
        {'RowKey': 'row1', 'column1': 'value1'},
        {'RowKey': 'row2', 'column1': 'value2'}
    ]
    columnstoinsert = ['column1']
    azure_data_tables_client = AzureDataTablesClient(
        table_name=TABLE_NAME,
        connection_string=CONNECTION_STRING,  # Set connection string to None to use account credentials
        account_name=ACCOUNT_NAME,
        account_key=ACCOUNT_KEY
    )
    azure_data_tables_client.connect_table_service(TABLE_NAME )
    azure_data_tables_client.insert_batch_entities(entities, PartitionKey="partition1", RowKey="RowKey", columnstoinsert=columnstoinsert, batch_size=1)
    
    # Validate that the entities were inserted
    table_client = azure_data_tables_client.table_service_client.get_table_client(TABLE_NAME)
    inserted_entities = table_client.query_entities("PartitionKey eq 'partition1'")

    # result_set = set(frozenset(entity.items()) for entity in result)
    # expected_set = set(frozenset(entity.items()) for entity in expected_entities)

    # assert result_set & expected_set
    assert len(list(inserted_entities)) == len(entities)

def test_query_entities(azure_data_tables_client):
    """Test querying entities from Azure Table Storage."""
    # Assuming that there are entities to be queried
    filter_condition = "PartitionKey eq 'partition1'"
    azure_data_tables_client = AzureDataTablesClient(
        table_name=TABLE_NAME,
        connection_string=CONNECTION_STRING,  # Set connection string to None to use account credentials
        account_name=ACCOUNT_NAME,
        account_key=ACCOUNT_KEY
    )
    azure_data_tables_client.connect_table_service(TABLE_NAME )
    entities = azure_data_tables_client.query_entities(filter_condition, batch_size=1)
    assert isinstance(entities, list)
    assert len(entities) > 0