from ftplib import FTP
import logging
from ...Baseconnector.BaseConnector import BaseConnector

logger = logging.getLogger(__name__)

class FTPconnector(BaseConnector):
    """A class to handle FTP connections and operations."""

    def __init__(
            self,
            host: str,
            port: int = 21,
            username: str = "",
            password: str = ""
            ):
        """
        Initialize FTPconnector with host, port, username, and password.

        Args:
            host (str): The hostname or IP address of the FTP server.
            port (int, optional): The port number of the FTP server (default is 21).
            username (str, optional): The username for authentication (default is an empty string).
            password (str, optional): The password for authentication (default is an empty string).
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ftp = None

    def connect(self):
        """
        Connect to the FTP server.

        This method establishes a connection to the FTP server using the provided credentials.
        """
        try:
            self.ftp = FTP()
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.username, self.password)
            logger.info(f"Connected to {self.host}")
        except Exception as e:
            logger.info(f"Error connecting to {self.host}: {e}")
            self.disconnect()

    def disconnect(self):
        """
        Disconnect from the FTP server.

        This method closes the connection to the FTP server.
        """
        if self.ftp:
            self.ftp.quit()
            logger.info(f"Disconnected from {self.host}")
            self.ftp = None

    def list_files(self):
        """
        List files in the current directory on the FTP server.

        This method retrieves a list of files present in the current directory on the FTP server.
        """
        if self.ftp:
            try:
                files = self.ftp.nlst()
                logger.info(f"Files in current directory: {files}")
                if files:
                    return files 
            except Exception as e:
                logger.info(f"Error listing files: {e}")
        else:
            logger.error("Not connected to any FTP server.")

    def change_dir(self, path: str):
        """
        Change the current directory on the FTP server.

        Args:
            path (str): The path of the directory to change to.
        """
        if self.ftp:
            try:
                self.ftp.cwd(path)
                logger.info(f"Changed directory to {path}")
            except Exception as e:
                logger.error(f"Error changing directory: {e}")
        else:
            logger.info("Not connected to any FTP server.")

    def download_file(self, remote_path: str, local_path: str):
        """
        Download a file from the FTP server.

        Args:
            remote_path (str): The path of the file on the FTP server.
            local_path (str): The path to save the downloaded file locally.
        """
        if self.ftp:
            try:
                self.ftp.retrbinary(f"RETR {remote_path}", open(local_path, 'wb').write)
                logger.info(f"Downloaded {remote_path} to {local_path}")
            except Exception as e:
                logger.error(f"Error downloading file: {e}")
        else:
            logger.info("Not connected to any FTP server.")

    def upload_file(self, local_path: str, remote_path: str):
        """
        Upload a file to the FTP server.

        Args:
            local_path (str): The path of the file to upload locally.
            remote_path (str): The path where the file will be uploaded on the FTP server.
        """
        if self.ftp:
            try:
                with open(local_path, 'rb') as f:
                    self.ftp.storbinary(f"STOR {remote_path}", f)
                logger.info(f"Uploaded {local_path} to {remote_path}")
            except Exception as e:
                logger.info(f"Error uploading file: {e}")
        else:
            logger.info("Not connected to any FTP server.")
