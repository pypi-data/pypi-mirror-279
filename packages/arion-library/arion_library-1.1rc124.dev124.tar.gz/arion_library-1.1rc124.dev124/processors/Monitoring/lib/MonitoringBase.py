import logging
import base64
from azure.data.tables import TableServiceClient, TableSasPermissions, TableClient
from ...Azure_storage.lib.TableStorage import AzureDataTablesClient  # Ensure the import path is correct
from ...Baseconnector.BaseConnector import BaseConnector
from datetime import datetime
from azure.communication.email import EmailClient
from typing import List
from azure.core.credentials import AzureKeyCredential

class MonitoringBase(BaseConnector):
    """
    Base class for monitoring functionalities.
    """
    
    def __init__(self):
        """
        Initializes an instance of the MonitoringBase class.
        """
        super().__init__()

    def handleTableStorageLogs(self, table_name, connection_string=None, account_name=None, account_key=None):
        """
        Handles log storage in an Azure Data Table.

        :param table_name: The name of the table in Azure Data Tables.
        :type table_name: str
        :param connection_string: The connection string to use to connect to the service. Defaults to None.
        :type connection_string: str, optional
        :param account_name: The name of the Azure storage account. Defaults to None.
        :type account_name: str, optional
        :param account_key: The key for the Azure storage account. Defaults to None.
        :type account_key: str, optional

        :return: None
        """
        # Initialize AzureDataTablesClient
        data_tables_client = AzureDataTablesClient(table_name, connection_string, account_name, account_key)
        
        # Connect to the table service
        data_tables_client.connect_table_service(table_name)
        
        # Check if table exists, create if it does not
        try:
            table_service_client = data_tables_client.table_service_client
            table_client = table_service_client.create_table_if_not_exists(table_name)
            table_exists = table_client is not None

            if not table_exists:
                table_client.create_table()
                logging.info(f"Table {table_name} created successfully.")
            else:
                logging.info(f"Table {table_name} already exists.")
        except Exception as e:
            logging.error(f"An error occurred while checking or creating the table: {e}")
            return

        # Define columns
        columns = ["type", "filename", "flowname", "record", "status", "execTime", "error", "nb_insertedLines", "nb_failedLines"]

        # Example log entry
        log_entries = [{
            "type": "Error",
            "filename": "example.csv",
            "flowname": "DataFlow1",
            "record": "Record1",
            "status": "Failed",
            "execTime": datetime.utcnow().isoformat(),
            "error": "Example error message",
            "nb_insertedLines": 0,
            "nb_failedLines": 1
        }]

        # Insert log entries
        try:
            data_tables_client.insert_batch_entities(log_entries, PartitionKey="LogPartition", RowKey="record", columnstoinsert=columns)
            logging.info("Log entries inserted successfully.")
        except Exception as e:
            logging.error(f"An error occurred while inserting log entries: {e}")

    def send_email_with_attachment(self, connection_string: str, file_bytes: bytes, subject: str, body: str, recipient: str, sender: str, cc: List[str] = None ):
        """
        Sends an email with an Excel file attachment.

        :param connection_string: The connection string for Azure Communication Services EmailClient.
        :type connection_string: str
        :param file_bytes: The bytes of the Excel file to attach.
        :type file_bytes: bytes
        :param subject: The subject of the email.
        :type subject: str
        :param body: The body of the email (plain text).
        :type body: str
        :param recipient: The recipient email address.
        :type recipient: str
        :param sender: The sender email address.
        :type sender: str
        :param cc: List of CC email addresses. Defaults to None.
        :type cc: list, optional

        :return: None
        """
        logging.info("Initializing EmailClient.")
        email_client = EmailClient.from_connection_string(connection_string)
        if len(file_bytes) > 0:
            try:
                logging.info("Encoding file to base64.")
                file_bytes_b64 = base64.b64encode(file_bytes).decode()

                message = {
                    "content": {
                        "subject": subject,
                        "plainText": body,
                        "html": f"<html><p>{body}</p></html>"
                    },
                    "recipients": {
                        "to": [
                            {"address": recipient }
                        ],
                        "cc": [{"address": cc_email} for cc_email in cc] if len(cc) > 0 else []
                    },
                    "senderAddress": sender,
                    "attachments": [
                        {
                            "name": "attachment.xlsx",
                            "contentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            "contentInBase64": file_bytes_b64
                        }
                    ]
                }

                logging.info("Sending email.")
                poller = email_client.begin_send(message)
                result = poller.result()
                logging.info(f"Email sent successfully: {result}")
            except Exception as e:
                logging.error(f"An error occurred while sending the email: {e}")
        else:
            logging.info("Skipping email sending because the file is empty.")