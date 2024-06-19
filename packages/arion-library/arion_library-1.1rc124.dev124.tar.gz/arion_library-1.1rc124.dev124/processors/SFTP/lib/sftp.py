import pysftp
import logging
from ...Baseconnector.BaseConnector import BaseConnector

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

class SFTPClient(BaseConnector):
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.sftp = None
    
    def connect(self):

        """

        Establishes a connection to an SFTP server_______
        This method attempts to connect to an SFTP server using the provided credentials.
        If successful, it initializes a connection object that can be used for file operations.

        :raises: Any exception raised during the connection attempt is caught and logged.
                This ensures that errors are properly handled without crashing the program.

        :return: None
        """
        try:

            logging.info('Trying to connect to sftp')
            self.sftp = pysftp.Connection(self.hostname, port=self.port, username=self.username, password=self.password,cnopts=cnopts)
            logging.info("Connected to SFTP server")
        except Exception as e:
            logging.error(f"Error connecting to SFTP server: {e}")
    
    def upload_file(self, local_path, remote_path):

        """
        Uploads a file from the local system to the remote SFTP server.

        This method uploads a file from the local system to the specified location on the SFTP server.
        It uses the established SFTP connection to perform the upload operation.

        :param local_path: The local path of the file to upload.
        :type local_path: str
        :param remote_path: The remote path where the file should be uploaded on the SFTP server.
        :type remote_path: str

        :raises: Any exception raised during the file upload is caught and logged.
                This ensures that errors are properly handled without crashing the program.

        :return: None
        """

        try:
            logging.info(f'Uploading file from {local_path} to sftp {remote_path}')
            self.sftp.put(local_path, remote_path)
            logging.info(f"File uploaded successfully to {remote_path}")
        except Exception as e:
            logging.info(f"Error uploading file: {e}")
    
    def download_file(self, remote_path, local_path):

        """
        Downloads a file from the remote SFTP server to the local system.

        This method downloads a file from the specified location on the SFTP server to the local system.
        It uses the established SFTP connection to perform the download operation.

        :param remote_path: The remote path of the file to download from the SFTP server.
        :type remote_path: str
        :param local_path: The local path where the file should be saved after downloading.
        :type local_path: str

        :raises: Any exception raised during the file download is caught and logged.
                This ensures that errors are properly handled without crashing the program.

        :return: None
        """
        try:
            logging.info(f'Downloading file from {remote_path} to sftp {local_path}')
            self.sftp.get(remote_path, local_path)
            logging.info(f"File downloaded successfully to {local_path}")
        except Exception as e:
            logging.info(f"Error downloading file: {e}")
    
    def close(self):

        """
        Closes the SFTP connection.

        This method closes the SFTP connection if it is currently open.
        It checks if the connection is active before attempting to close it.

        :return: None
        """
        
        if self.sftp:
            self.sftp.close()
            self.sftp = None
            logging.info("Connection closed")

