import pytest
from datetime import datetime
from ..lib.MonitoringBase import MonitoringBase  # Replace with the actual import path

@pytest.fixture(scope="module")
def azure_config():
    return {
        "table_name": "testlogstable",
        "connection_string": "",
        "account_name": "",
        "account_key": ""
    }

@pytest.fixture
def monitoring_base():
    return MonitoringBase()

def test_handle_table_storage_logs(monitoring_base, azure_config):
    """
    Test the handleTableStorageLogs method.
    """
    # Invoke the method
    monitoring_base.handleTableStorageLogs(
        table_name=azure_config["table_name"],
        connection_string=azure_config["connection_string"],
        account_name=azure_config["account_name"],
        account_key=azure_config["account_key"]
    )

    # Assuming the handleTableStorageLogs method does not return anything,
    # you can verify its effect by checking the existence of the table
    # and the inserted log entry.
    from azure.data.tables import TableServiceClient

    table_service_client = TableServiceClient.from_connection_string(azure_config["connection_string"])
    table_client = table_service_client.get_table_client(azure_config["table_name"])

    # Check if the table exists


    # Query the inserted log entry
    entities = list(table_client.list_entities())
    assert len(entities) > 0, "No entities found in the table."

    # Validate the content of the inserted log entry
    log_entry = entities[0]
    assert log_entry["type"] == "Error"
    assert log_entry["filename"] == "example.csv"
    assert log_entry["flowname"] == "DataFlow1"
    assert log_entry["record"] == "Record1"
    assert log_entry["status"] == "Failed"
    assert "execTime" in log_entry
    assert log_entry["error"] == "Example error message"
    assert log_entry["nb_insertedLines"] == 0
    assert log_entry["nb_failedLines"] == 1