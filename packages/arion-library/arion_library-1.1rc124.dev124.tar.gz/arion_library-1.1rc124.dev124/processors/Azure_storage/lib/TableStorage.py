import logging
from azure.data.tables import TableSasPermissions
from .Azurestoragebaseclasse import AzureStorageConnector
from datetime import datetime, timezone, timedelta
from azure.data.tables import TableServiceClient, generate_table_sas, TableSasPermissions
from azure.core.credentials import AzureNamedKeyCredential


class AzureDataTablesClient(AzureStorageConnector):
    """
    This class allows interaction with Azure Data Tables using inheritance from AzureStorageConnector.

    :param table_name: The name of the table in Azure Data Tables.
    :type table_name: str
    :param connection_string: The connection string to use to connect to the service. Defaults to None.
    :type connection_string: str, optional
    :param account_name: The name of the Azure storage account. Defaults to None.
    :type account_name: str, optional
    :param account_key: The key for the Azure storage account. Defaults to None.
    :type account_key: str, optional

    :ivar table_name: The name of the table in Azure Data Tables.
    :vartype table_name: str
    :ivar connection_string: The connection string to use to connect to the service.
    :vartype connection_string: str
    :ivar account_name: The name of the Azure storage account.
    :vartype account_name: str
    :ivar account_key: The key for the Azure storage account.
    :vartype account_key: str
    """

    def __init__(self, table_name, connection_string=None, account_name=None, account_key=None):
        """
        Initializes an instance of the AzureDataTablesClient class.

        :param table_name: The name of the table in Azure Data Tables.
        :type table_name: str
        :param connection_string: The connection string to use to connect to the service. Defaults to None.
        :type connection_string: str, optional
        :param account_name: The name of the Azure storage account. Defaults to None.
        :type account_name: str, optional
        :param account_key: The key for the Azure storage account. Defaults to None.
        :type account_key: str, optional
        """
        super().__init__(connection_string, account_name, account_key)
        self.table_name = table_name
        self.table_service_client = None

    def connect_table_service(self, table_name, table_permissions=TableSasPermissions(read=True), table_expiry=None):
        """
        Establishes a connection with the Azure Table service.

        :param table_name: The name of the table.
        :type table_name: str
        :param table_permissions: The permissions for the table SAS. Defaults to TableSasPermissions(read=True).
        :type table_permissions: TableSasPermissions, optional
        :param table_expiry: The expiry date for the table SAS. Defaults to None.
        :type table_expiry: datetime, optional

        :raises ValueError: If neither a connection string nor both account name and key are provided.

        :return: None
        """
        try:
            if self.connection_string:
                self.table_service_client = TableServiceClient.from_connection_string(self.connection_string)
                self.logger.info("Connected to Azure Table Service using connection string")
            elif self.account_name and self.account_key:
                sas_key = self.generate_table_sas_key(table_name, permissions=table_permissions, expiry=table_expiry)
                self.table_service_client = TableServiceClient(sas_key)
                self.logger.info("Connected to Azure Table Service using SAS token")
            else:
                raise ValueError("Either connection string or both account name and account key must be provided")
        except Exception as e:
            self.logger.error(f"Error connecting to Azure Table Service: {e}")

    def generate_table_sas_key(self, credentials, table_name="test", permissions=TableSasPermissions(read=True), expiry=None):
        """
        Generates a SAS token for Azure Table storage.

        :param table_name: The name of the table.
        :type table_name: str
        :param permissions: The permissions for the table SAS. Defaults to TableSasPermissions(read=True).
        :type permissions: TableSasPermissions, optional
        :param expiry: The expiry date for the table SAS. Defaults to None.
        :type expiry: datetime, optional

        :return: The generated SAS token.
        :rtype: str
        """
        expiry = expiry or datetime.now(timezone.utc) + timedelta(hours=1)
        sas_token = generate_table_sas(
            credentials,
            table_name=table_name,
            permission=permissions,
            expiry=expiry
        )
        return sas_token

    def insert_batch_entities(self, entities, PartitionKey, RowKey, columnstoinsert, batch_size=1,
                              table_permissions=TableSasPermissions(read=True), table_expiry=None):
        """
        Inserts entities into an Azure Data Table in batches.

        :param entities: The list of entities to insert into the table.
        :type entities: list
        :param PartitionKey: The partition key for the entities.
        :type PartitionKey: str
        :param RowKey: The row key for the entities.
        :type RowKey: str
        :param columnstoinsert: The list of columns to insert into the table.
        :type columnstoinsert: list
        :param batch_size: The size of each batch for batch insertion. Defaults to 1.
        :type batch_size: int
        :param table_permissions: The permissions for the table SAS. Defaults to TableSasPermissions(read=True).
        :type table_permissions: azure.data.tables.TableSasPermissions, optional
        :param table_expiry: The expiry date for the table SAS. Defaults to None.
        :type table_expiry: datetime, optional

        :raises ValueError: If an error occurs during data insertion.

        :return: None
        """
        try:
            logging.info(f'Preparing data to insert into {self.table_name} table')
            table_client = self.table_service_client.get_table_client(self.table_name)
            entities_to_insert = []
            for row in entities:
                entity = {'PartitionKey': PartitionKey, 'RowKey': row[RowKey]}
                for col in columnstoinsert:
                    entity[col] = row[col]
                entities_to_insert.append(("upsert", entity))
                if len(entities_to_insert) == batch_size:
                    logging.info(f'batch to insert : {entities_to_insert}')
                    table_client.submit_transaction(entities_to_insert)
                    entities_to_insert = []
            if len(entities_to_insert) > 0:
                logging.info(f'batch to insert : {entities_to_insert}')
                table_client.submit_transaction(entities_to_insert)
            logging.info(f'All lines are successfully inserted into {self.table_name} table.')
        except ValueError as e:
            logging.error(f'An error occurred while trying to insert data into {self.table_name} table: {e}')

    def query_entities(self, filter_condition, batch_size=1,
                       table_permissions=TableSasPermissions(read=True), table_expiry=None):
        """
        Executes a query to retrieve entities from an Azure Data Table.

        :param filter_condition: The filter condition to apply to the query.
        :type filter_condition: str
        :param batch_size: The number of results per page. Defaults to 1.
        :type batch_size: int
        :param table_permissions: The permissions for the table SAS. Defaults to TableSasPermissions(read=True).
        :type table_permissions: azure.data.tables.TableSasPermissions, optional
        :param table_expiry: The expiry date for the table SAS. Defaults to None.
        :type table_expiry: datetime, optional

        :return: A list of entities retrieved from the table.
        :rtype: list
        """
        try:
            table_client = self.table_service_client.get_table_client(self.table_name)
            entities = []
            logging.info(f'Executing query: {filter_condition}')
            for entity_page in table_client.query_entities(query_filter=filter_condition, results_per_page=batch_size).by_page():
                entities.extend(list(entity_page))
                break
            logging.info(f'Query Results: {entities}')
            return entities
        except ValueError as e:
            logging.error(f'An error occurred while trying to query data from {self.table_name} table: {e}')
