import xmltodict
import json
import os
from ...Baseconnector.BaseConnector import BaseConnector

class XML_JSON_XML(BaseConnector):
    """
    Class for conversion between XML and JSON formats.
    """

    def detect_file_type(self, file_path):
        """
        Determine the file type based on its extension.

        Args:
            file_path (str): Path of the file.

        Returns:
            str: File type ('xml', 'json') or None if the type is not supported.
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.xml':
            return 'xml'
        elif file_extension == '.json':
            return 'json'
        else:
            return None

    def convert_xml_to_json(self, xml_content):
        """
        Convert XML content to JSON.

        Args:
            xml_content (str): XML content as a string.

        Returns:
            str: Resulting JSON content.
        """
        data_dict = xmltodict.parse(xml_content)
        json_data = json.dumps(data_dict, indent=4)
        return json_data

    def convert_json_to_xml(self, json_content):
        """
        Convert JSON content to XML.

        Args:
            json_content (str): JSON content as a string.

        Returns:
            str: Resulting XML content.
        """
        # Replace "None" with "null" in the JSON content
        json_content = json_content.replace("None", "null")

        # Parse JSON content
        data_list = json.loads(json_content)

        # Create XML string for each root item
        xml_data_list = []
        for item in data_list:
            xml_data_list.append(xmltodict.unparse({"root": item}, pretty=True))

        # Join XML strings
        xml_data = "\n".join(xml_data_list)
        return xml_data

    def convert_file(self, file_path):
        """
        Convert a file from the source format (XML or JSON) to the target format (JSON or XML).

        Args:
            file_path (str): Path of the source file.

        Raises:
            ValueError: If the file type is not supported.
        """
        file_type = self.detect_file_type(file_path)
        if file_type == 'xml':
            with open(file_path, 'r') as xml_file:
                xml_content = xml_file.read()
                json_data = self.convert_xml_to_json(xml_content)
                with open('Output.json', 'w') as json_file:
                    json_file.write(json_data)
            print("XML to JSON conversion successful.")
            print(json_data)
        elif file_type == 'json':
            with open(file_path, 'r') as json_file:
                json_content = json_file.read()
                xml_data = self.convert_json_to_xml(json_content)
                with open('Output.xml', 'w') as xml_file:
                    xml_file.write(xml_data)
            print("JSON to XML conversion successful.")
            print(xml_data)
        else:
            raise ValueError("Unsupported file type.")

# # Example of using the class
# xml_json_xml_instance = XML_JSON_XML()
# xml_json_xml_instance.convert_file(r'C:\Repos_Arion\ArionLibrary\processors\Convert_xml_json_xml\tests\Input_File_test\CERT.xml')

