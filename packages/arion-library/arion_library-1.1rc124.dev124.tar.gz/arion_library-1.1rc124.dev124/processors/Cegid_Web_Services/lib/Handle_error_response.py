import logging
import xml.etree.ElementTree as ET
from ...Baseconnector.BaseConnector import BaseConnector

class ErrorAPI(BaseConnector):
    """

    This class provides a method for handling error responses in XML format.

    """

    def handle_error_response(self, response):
        """Handle the error response and extract the error message.

        Args:
            response (str): The XML response containing error information.

        Returns:
            str: Extracted error message or original response if no error message found.

        """
        try:
            root = ET.fromstring(response)

            # Modified this line to directly access the root of the XML tree
            error_message_element = root.find(".//{http://www.cegid.fr/fault}Message")

            if error_message_element is not None:
                error_message = error_message_element.text
                error_message = error_message.split(":")[-1].strip()
                index = error_message.find("(TCbrImportHelper")

                if index != -1:
                    error_message = error_message[:index]
                    if "-" in error_message:
                        error_message = error_message.split('- ')[1].strip()

                    return error_message
                else:
                    return error_message  # Return error message if it's not None
            else:
                return response  # Return response text if no error message found
        except Exception as e:
            logging.error(f"Error handling response for: {str(e)}")
            return f'error message : {response}'

# Static response for testing
response = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
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


