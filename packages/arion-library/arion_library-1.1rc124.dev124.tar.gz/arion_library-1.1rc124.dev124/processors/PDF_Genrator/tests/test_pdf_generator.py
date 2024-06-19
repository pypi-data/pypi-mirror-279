import pytest
from ..lib.PdfGenrator import PDFgenrator
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def test_pdf_generation():
    """Test PDF generation with real data and template."""

    # Sample data
    sample_data = [
        ['7622100690917', 'IQOS ORIGINALS ONE MOBILITY KIT - SLATE', 1, '9.600', '12', '12', '9.600'],
        ['', 'أيقوص أوريجينالز وان موبايلتي كيت - arabic', '', '', '', '', ''],
        ['', 'AKXVA31C185P', '', '', '', '', ''],
        ['2222222222222', 'shipping cost', 1, '0.000', '12', '12', '0.000'],
        # ... (remaining data can be omitted for brevity)
    ]

    # Path to the logo image (assuming the image exists)
    image_path = f"file://{BASE_DIR}/ALAB_Logo.png"

    # Configuration for PDF generation
    pdf_config = PDFgenrator(
        html_template_file="template.html",
        data={
            "data": sample_data,
            "image_path": image_path,
            "customer_name": "رايق العتيبي",
            "invoice_number": 24,
            "invoice_date": "August 05, 2023",
            "invoice_time": "02:14 PM"
        },
        output_file="output_jinja_class.pdf"
    )

    # Generate the PDF (This will create a PDF file)
    pdf  = pdf_config.generate_pdf()
    assert pdf

    # Add assertions here to verify the generated PDF content (optional)
    # You might need additional libraries to test the PDF content
