import pytest
import logging
from ..lib.MonitoringBase import MonitoringBase  # Replace with your actual import path
from io import BytesIO

@pytest.fixture
def monitoring_base():
    return MonitoringBase()

def test_send_email_with_attachment(monitoring_base, caplog):
    caplog.set_level(logging.INFO)
    
    # Create a small sample Excel file in memory
    excel_content = BytesIO()
    excel_content.write(b'Test content for Excel file')
    excel_content.seek(0)
    
    file_bytes = excel_content.read()
    subject = "Test Subject"
    body = "This is a test email body."
    recipient = "email@email.com"
    sender = "donotreply@***.azurecomm.net"
    logging.info(sender)
    cc = ["email@email.com"]
    connection_string = "connection_string"

    # Call the method
    monitoring_base.send_email_with_attachment(connection_string, file_bytes, subject, body, recipient, sender, cc )

    # Check logs for what happened during the email sending process
    for record in caplog.records:
        print(record.levelname, record.message)
    
    # Ensure the test actually checked the relevant logging messages
    assert any("Initializing EmailClient" in record.message for record in caplog.records)
    assert any("Encoding file to base64" in record.message for record in caplog.records)
    assert any("Sending email" in record.message for record in caplog.records)
    assert any("Email sent successfully" in record.message for record in caplog.records)
