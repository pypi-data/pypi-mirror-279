import pytest
from ..lib.Convert_Soap_Rest import XML_JSON_XML
from ..lib.Handle_error_response import ErrorAPI

# Fixtures
@pytest.fixture
def converter():
    """
    Fixture to initialize an instance of XML_JSON_XML for testing.
    """
    return XML_JSON_XML()

# Path to the XML test file
file_path = (r'C:\Repos_Arion\ArionLibrary\processors\Convert_xml_json_xml\tests\Input_File_test\CERT.xml')

def test_convert_file(converter):
    """
    Test to verify if the convert_file method correctly converts an XML file to JSON.

    Args:
        converter: Instance of XML_JSON_XML.
    """
    # Convert the XML file to JSON using the convert_file method
    converter.convert_file(file_path)


# Fixture to create an instance of the ErrorAPI class
@pytest.fixture
def error_api_instance():
    """
    Fixture to create an instance of the ErrorAPI class for testing.
    """
    return ErrorAPI()

# Test to verify the behavior of the _handle_error_response method
def test_handle_error_response(error_api_instance):
    """
    Test to verify the behavior of the _handle_error_response method.
    
    :param error_api_instance: Instance of the ErrorAPI class.
    """
    # Sample response containing an error message
    response = """
    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
        <s:Body>
            <s:Fault>
                <faultcode xmlns:a="http://www.cegid.fr/fault">a:CBR_001_0003</faultcode>
                <faultstring xml:lang="en-US">Remote call failed: Code = (WP006) Message = (WP006 : Failure during message execution (TWorkerMessageProcess.TryExecuteMessage))</faultstring>
                <detail>
                    <CbpExceptionDetail xmlns="http://www.cegid.fr/fault" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
                        <InnerException i:type="CbpExceptionDetail">
                            <InnerException i:type="CbpExceptionDetail">
                                <InnerException i:type="CbpExceptionDetail">
                                    <Message>Remote call failed: Code = (CBR00009) Message = (CBR00009 : Import failed : Customer order Internal reference LZD_EC04 DOC00042 - This document already exists and cannot be re-integrated (TCbrImportHelper.InvokeImport))</Message>
                                    <Type>Cegid.Retail.Tools.Resources.Biz001Exception</Type>
                                    <Id>CBR_001_0003</Id>
                                    <ToDo/>
                                </InnerException>
                                <Message>Remote call failed: Code = (CBR00006) Message = (CBR00006 : Failed to create document (TCbrImportHelper.CreateDocument))</Message>
                                <Type>Cegid.Retail.Tools.Resources.Biz001Exception</Type>
                                <Id>CBR_001_0003</Id>
                                <ToDo/>
                            </InnerException>
                            <Message>Remote call failed: Code = (WP008) Message = (WP008 : Operation 'Cegid.Retail.Documents.Sales.Create' failed calling 'TCbrImportHelper.CreateDocument' (TWorkerOperationDispatcher.Execute))</Message>
                            <Type>Cegid.Retail.Tools.Resources.Biz001Exception</Type>
                            <Id>CBR_001_0003</Id>
                            <ToDo/>
                        </InnerException>
                        <Message>Remote call failed: Code = (WP006) Message = (WP006 : Failure during message execution (TWorkerMessageProcess.TryExecuteMessage))</Message>
                        <TrackingId>f91de7f2-0c43-4cae-b8e3-4cad3f37811a</TrackingId>
                        <Type>Cegid.Retail.Tools.Resources.Biz001Exception</Type>
                        <Id>CBR_001_0003</Id>
                        <ToDo/>
                    </CbpExceptionDetail>
                </detail>
            </s:Fault>
        </s:Body>
    </s:Envelope>"""

    # Test with a response containing an error message
    result = error_api_instance.handle_error_response(response)
    print(result)  # Output the result
