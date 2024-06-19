import requests
import xml.etree.ElementTree as ET
import csv
import logging

class RFEConnector:
    """
    A class used to interact with Azure Blob Storage through Cegid Cloud.

    Attributes
    ----------
    user : str
        Username for authentication.
    workspace : str
        Workspace name for the environment.
    password : str
        Password for authentication.
    environnement : str
        Environment name.
    container_name : str
        Name of the blob storage container.
    access_token : str, optional
        Access token for authentication.
    sas_key : str, optional
        SAS key for accessing the blob storage container.
    logger : logging.Logger
        Logger for logging information and errors.

    Methods
    -------
    get_token():
        Retrieves an access token and a SAS key from the Cegid Cloud server.
    get_blobs(file_prefixes):
        Downloads files from an Azure Blob Storage container using a SAS key, filtering by file prefixes.
    upload_blob(file_path, file_content):
        Uploads a file to an Azure Blob Storage container using a SAS key.
    """

    def __init__(self, user, workspace, password, environnement, container_name):
        """
        Initializes the RFEConnector with the given parameters.

        Parameters
        ----------
        user : str
            Username for authentication.
        workspace : str
            Workspace name for the environment.
        password : str
            Password for authentication.
        environnement : str
            Environment name.
        container_name : str
            Name of the blob storage container.
        """
        self.user = user
        self.workspace = workspace
        self.password = password
        self.environnement = environnement
        self.container_name = container_name
        self.access_token = None
        self.sas_key = None
        self.logger = logging.getLogger(__name__)

    def get_token(self):
        """
        Retrieves an access token and a SAS key from the Cegid Cloud server.

        Raises
        ------
        ValueError
            If there is an error while getting the SAS token or SAS key.
        """
        url = f"https://retail-services.cegid.cloud/{self.environnement}/as/connect/token"
        payload = f'client_id=CegidRetailResourceFlowClient&username={self.user}%40{self.workspace}&password={self.password}&grant_type=password&scope=RetailBackendApi%20offline_access'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'ASLBSA=00035295a8b8ab29b0e6e67c5e09c95f82ab249e6c3e362c44e7089e2422d1292b9641369945f7e8b5940a4a688db1f303ecd26547f2db369e4a3c4231afe28d6c8c; ASLBSACORS=00035295a8b8ab29b0e6e67c5e09c95f82ab249e6c3e362c44e7089e2422d1292b9641369945f7e8b5940a4a688db1f303ecd26547f2db369e4a3c4231afe28d6c8c'
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            self.access_token = response.json()['access_token']
            tenantID = self.container_name.split('-')[0]

            url = f"https://rfe.cegid.cloud/{self.environnement}/storage/api/{self.workspace}/RFE/V1/getsastoken/{self.container_name}"
            headers = {
                'X-TenantID': tenantID,
                'Authorization': f'Bearer {self.access_token}',
                'Cookie': 'ASLBSA=000381c0e45cf7d105034ad4c6b9fda6c02fe8f3fe9ffdf961dbb7da90a76f73b4bdf13c9168eae8166ded5e2e5e3caa04e5d4b5fb643e6b653d209ebeac6b4d0efc; ASLBSACORS=000381c0e45cf7d105034ad4c6b9fda6c02fe8f3fe9ffdf961dbb7da90a76f73b4bdf13c9168eae8166ded5e2e5e3caa04e5d4b5fb643e6b653d209ebeac6b4d0efc'
            }
            response = requests.get(url, headers=headers)
            response_json = response.json()
            self.sas_key = response_json['blobServiceUri'] + response_json['containerName'] + response_json['sasToken']

            self.logger.info('SAS key is generated successfully')

        except ValueError as e:
            self.logger.error(f'Error while getting SAS token or SAS key: {e}')

    def get_blobs(self, file_prefixes):
        """
        Downloads files from an Azure Blob Storage container using a SAS key, filtering by file prefixes.

        Parameters
        ----------
        file_prefixes : list of str
            The list of prefixes of the files to filter and download.

        Returns
        -------
        list of str
            A list of the filtered file names that were downloaded.

        Raises
        ------
        ValueError
            If an error occurs while downloading files from the blob storage.
        """
        try:
            url = f'{self.sas_key}&comp=list&restype=container'
            self.logger.info('Requesting list of blobs from RFE container')
            response = requests.get(url)
            blobserviceuri = self.sas_key.split('?')[0]
            sas_token = self.sas_key.split('?')[1]

            root = ET.fromstring(response.text)
            headers = {
                "Content-Type": "text/plain",
                "x-ms-blob-type": "BlockBlob"
            }
            filtred_files = []
            for blob in root.findall(".//Blob"):
                name = blob.find("Name").text
                if any(name.startswith(f"out/{prefix}") for prefix in file_prefixes) and name != "out/.Output folder.txt":
                    file_name = name.split('/')[1]
                    filtred_files.append(file_name)
                    if len(filtred_files) > 0:
                        url = f'{blobserviceuri}/out/{file_name}?{sas_token}'
                        self.logger.info(f'Downloading {file_name} file from blob')
                        response = requests.get(url, headers=headers)
                        lines = response.text.split("\r\n")
                        if lines and lines[-1] == '':
                            lines.pop(-1)
                        rows = [line.split(';') for line in lines]
                        output_csv = f'/tmp/{file_name}'
                        with open(output_csv, mode='w', newline='') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerows(rows)

                        self.logger.info(f'{file_name} successfully downloaded')
                        self.logger.info('----------')
                        self.logger.info(f'Deleting {file_name} from blob')
                        response = requests.delete(url, headers=headers)
                        self.logger.info(f'{file_name} successfully deleted from blob')
                    else:
                        self.logger.info("No new data found")
            return filtred_files
        except ValueError as e:
            self.logger.error(f'Error while downloading file from blob: {e}')

    def upload_blob(self, file_path, file_content):
        """
        Uploads a file to an Azure Blob Storage container using a SAS key.

        Parameters
        ----------
        file_path : str
            The path of the file to be uploaded.
        file_content : str
            The content of the file to be uploaded.

        Raises
        ------
        ValueError
            If an error occurs while uploading the file to the blob storage.
        """
        try:
            blobserviceuri = self.sas_key.split('?')[0]
            sas_token = self.sas_key.split('?')[1]
            file_name = file_path.split('/')[-1]
            url = f'{blobserviceuri}/out/{file_name}?{sas_token}'
            headers = {
                "Content-Type": "text/plain",
                "x-ms-blob-type": "BlockBlob"
            }

            file_content = ""
            with open(file_path, mode='r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    row_string = ';'.join(row)
                    file_content += row_string + "\r\n"
            payload = file_content
            response = requests.put(url, headers=headers, data=payload)
            self.logger.info(f'{file_name} successfully uploaded to blob')

        except ValueError as e:
            self.logger.error(f'Error while uploading {file_name} to blob: {e}')
