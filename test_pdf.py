# Test script - save as test_pdf.py
from example_report import convert_html_to_pdf
import os

# Test with an existing HTML file
html_file = "biomechanical_assessment_report.html"  # Use your actual HTML file
pdf_file = "test_output.pdf"

if os.path.exists(html_file):
    print("Testing PDF conversion...")
    success = convert_html_to_pdf(html_file, pdf_file, "playwright")
    if success:
        print("✅ PDF conversion test successful!")
    else:
        print("❌ PDF conversion test failed")
else:
    print(f"❌ HTML file not found: {html_file}")