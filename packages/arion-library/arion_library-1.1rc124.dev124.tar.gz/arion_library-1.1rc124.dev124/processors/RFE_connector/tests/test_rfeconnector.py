import pytest
import requests
import responses
import logging
from ..lib.rfe_connector import RFEConnector  # Assurez-vous que le module rfe_connector est dans votre PYTHONPATH

@pytest.fixture
def connector():
    user = ""
    workspace = ""
    password = ""
    environnement = ""
    container_name = ""
    return RFEConnector(user, workspace, password, environnement, container_name)

@responses.activate
def test_get_token(connector):
    token_url = f"https://retail-services.cegid.cloud/{connector.environnement}/as/connect/token"
    responses.add(
        responses.POST,
        token_url,
        json={"access_token": "fake_access_token"},
        status=200
    )

    sas_token_url = f"https://rfe.cegid.cloud/{connector.environnement}/storage/api/{connector.workspace}/RFE/V1/getsastoken/{connector.container_name}"
    responses.add(
        responses.GET,
        sas_token_url,
        json={
            "blobServiceUri": "https://fakeaccount.blob.core.windows.net/",
            "containerName": "test_container",
            "sasToken": "?fake_sas_token"
        },
        status=200
    )

    connector.get_token()
    assert connector.access_token == "fake_access_token"
    assert connector.sas_key == "https://fakeaccount.blob.core.windows.net/test_container?fake_sas_token"

@responses.activate
def test_get_blobs(connector):
    connector.sas_key = "https://fakeaccount.blob.core.windows.net/test_container?fake_sas_token"
    
    list_url = f"{connector.sas_key}&comp=list&restype=container"
    blob_xml = """<?xml version="1.0" encoding="utf-8"?>
    <EnumerationResults>
        <Blobs>
            <Blob>
                <Name>out/prefix1_file1.txt</Name>
            </Blob>
            <Blob>
                <Name>out/prefix2_file2.txt</Name>
            </Blob>
            <Blob>
                <Name>out/.Output folder.txt</Name>
            </Blob>
        </Blobs>
    </EnumerationResults>"""
    
    responses.add(
        responses.GET,
        list_url,
        body=blob_xml,
        status=200
    )

    file_url_prefix1 = "https://fakeaccount.blob.core.windows.net/test_container/out/prefix1_file1.txt?fake_sas_token"
    responses.add(
        responses.GET,
        file_url_prefix1,
        body="column1;column2\r\nvalue1;value2\r\n",
        status=200
    )

    file_url_prefix2 = "https://fakeaccount.blob.core.windows.net/test_container/out/prefix2_file2.txt?fake_sas_token"
    responses.add(
        responses.GET,
        file_url_prefix2,
        body="column1;column2\r\nvalue3;value4\r\n",
        status=200
    )

    delete_url_prefix1 = file_url_prefix1
    responses.add(
        responses.DELETE,
        delete_url_prefix1,
        status=200
    )

    delete_url_prefix2 = file_url_prefix2
    responses.add(
        responses.DELETE,
        delete_url_prefix2,
        status=200
    )

    file_prefixes = ["prefix1", "prefix2"]
    downloaded_files = connector.get_blobs(file_prefixes)
    assert "prefix1_file1.txt" in downloaded_files
    assert "prefix2_file2.txt" in downloaded_files


@responses.activate
def test_upload_blob(connector, tmp_path):
    connector.sas_key = "https://fakeaccount.blob.core.windows.net/test_container?fake_sas_token"
    
    file_content = "column1;column2\r\nvalue1;value2\r\n"
    file_path = tmp_path / "upload_test.csv"
    with open(file_path, "w") as f:
        f.write(file_content)

    upload_url = "https://fakeaccount.blob.core.windows.net/test_container/out/upload_test.csv?fake_sas_token"
    responses.add(
        responses.PUT,
        upload_url,
        status=201
    )

    connector.upload_blob(file_path, file_content)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == upload_url
    assert responses.calls[0].request.body == file_content
