import cx_Oracle
import logging
import math
from ...Baseconnector.BaseConnector import BaseConnector

class OracleDatabase(BaseConnector):
    """
    A class for interacting with an Oracle database.

    :param user: The username for connecting to the database.
    :param password: The password for connecting to the database.
    :param dsn: The Oracle Database Source Name (DSN).
    """

    def __init__(self, user, password, dsn):
        """
        Initialize the OracleDatabase.

        This method establishes a connection to the Oracle database.

        :param user: The username for connecting to the database.
        :param password: The password for connecting to the database.
        :param dsn: The Oracle Database Source Name (DSN).
        """
        db_connection_str = f'{user}/{password}@{dsn}'
        try:
            self.connection = cx_Oracle.connect(db_connection_str)
            self.cursor = self.connection.cursor()
            logging.info("Connection established!")
        except cx_Oracle.DatabaseError as e:
            logging.error(f"Error occurred while trying to connect to the database: {e}")

    def select_data(self, query):
        """
        Execute a SELECT query on the database.

        :param query: The SELECT query to be executed.
        :return: The result of the query.
        """
        
        # Execute the SELECT query
        self.cursor.execute(query)

        # Fetch all rows and return the result
        result = self.cursor.fetchall()
        return result
        
        # except cx_Oracle.DatabaseError as e:
        #     logging.error(f"Error during SELECT operation: {e}")
        # finally:
        #     self.cursor.close()
    
    def execute_query(self, query) : 

        # Execute the SELECT query
        self.cursor.execute(query)
        
    def insert_data(self, table_name, data, batch_size=1):
        """
        Insert data into the database.
        :param table_name: The name of the table.
        :param data: The data to be inserted (json object).
        :param batch_size: The batch size for inserting data.
        :return: A list of errors encountered during insertion, if any.
        """
        errors = []
        try:
            total_rows = len(data)
            total_batches = math.ceil(total_rows / batch_size)

            for batch_number in range(total_batches):
                start_index = batch_number * batch_size
                end_index = min((batch_number + 1) * batch_size, total_rows)

                batch_data = data[start_index:end_index]

                columns = ', '.join(batch_data[0].keys())
                placeholders = ', '.join(':' + key for key in batch_data[0])

                self.cursor.executemany(
                    f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                    batch_data
                )

                batch_errors = self.cursor.getbatcherrors()
                if batch_errors:
                    errors.extend(batch_errors)
                logging.info(f"Inserted {len(batch_data)} rows in batch {batch_number + 1}/{total_batches}")
            
            self.connection.commit()
        
        except cx_Oracle.DatabaseError as e:
            logging.error(f"Error during INSERT operation: {e}")
            self.connection.rollback()
            raise

        return errors
    

    def close_connection(self):
        """
        Close the database connection.
        """
        self.connection.close()
        self.connection = None
