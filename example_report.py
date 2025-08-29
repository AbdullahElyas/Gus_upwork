"""
Simple example script to generate a biomechanical assessment report
"""

from report_generator import generate_biomechanical_report
import os
import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def convert_html_to_pdf(html_path, pdf_path, method="weasyprint"):
    """
    Convert HTML file to PDF using various methods
    
    Args:
        html_path: Path to the HTML file
        pdf_path: Path for the output PDF file
        method: Conversion method ("weasyprint", "pdfkit", "playwright")
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        if method == "weasyprint":
            # Method 1: WeasyPrint (Recommended for complex CSS)
            try:
                import weasyprint
                from weasyprint import HTML, CSS
                
                print(f"Converting HTML to PDF using WeasyPrint...")
                
                # Create CSS for better PDF formatting
                pdf_css = CSS(string='''
                    @page {
                        size: A4;
                        margin: 1cm;
                    }
                    body {
                        font-size: 10pt;
                        line-height: 1.4;
                    }
                    .graph-text img {
                        max-width: 400px !important;
                        max-height: 400px !important;
                    }
                    table {
                        font-size: 8pt;
                    }
                    .section-divider {
                        page-break-after: avoid;
                    }
                ''')
                
                HTML(filename=html_path).write_pdf(pdf_path, stylesheets=[pdf_css])
                return True
                
            except ImportError:
                print("WeasyPrint not installed. Installing...")
                install_package("weasyprint")
                import weasyprint
                from weasyprint import HTML, CSS
                
                pdf_css = CSS(string='''
                    @page {
                        size: A4;
                        margin: 1cm;
                    }
                    body {
                        font-size: 10pt;
                        line-height: 1.4;
                    }
                    .graph-text img {
                        max-width: 400px !important;
                        max-height: 400px !important;
                    }
                    table {
                        font-size: 8pt;
                    }
                ''')
                
                HTML(filename=html_path).write_pdf(pdf_path, stylesheets=[pdf_css])
                return True
                
        elif method == "pdfkit":
            # Method 2: pdfkit (requires wkhtmltopdf)
            try:
                import pdfkit
                
                print(f"Converting HTML to PDF using pdfkit...")
                
                options = {
                    'page-size': 'A4',
                    'margin-top': '1cm',
                    'margin-right': '1cm',
                    'margin-bottom': '1cm',
                    'margin-left': '1cm',
                    'encoding': "UTF-8",
                    'no-outline': None,
                    'enable-local-file-access': None
                }
                
                pdfkit.from_file(html_path, pdf_path, options=options)
                return True
                
            except ImportError:
                print("pdfkit not installed. Installing...")
                install_package("pdfkit")
                import pdfkit
                
                options = {
                    'page-size': 'A4',
                    'margin-top': '1cm',
                    'margin-right': '1cm',
                    'margin-bottom': '1cm',
                    'margin-left': '1cm',
                    'encoding': "UTF-8",
                    'no-outline': None,
                    'enable-local-file-access': None
                }
                
                pdfkit.from_file(html_path, pdf_path, options=options)
                return True
                
            except Exception as e:
                print(f"pdfkit error (may need wkhtmltopdf installed): {e}")
                return False
                
        elif method == "playwright":
            # Method 3: Playwright (modern browser engine)
            try:
                from playwright.sync_api import sync_playwright
                
                print(f"Converting HTML to PDF using Playwright...")
                
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    
                    # Navigate to the HTML file
                    page.goto(f"file://{os.path.abspath(html_path)}")
                    
                    # Wait for the page to fully load
                    page.wait_for_load_state('networkidle')
                    
                    # Wait a bit more to ensure all content is rendered
                    page.wait_for_timeout(2000)  # 2 seconds
                    
                    # Optional: Wait for specific content to be visible
                    try:
                        page.wait_for_selector('table', timeout=5000)
                    except:
                        print("Warning: Tables not found, continuing with PDF generation...")
                    
                    # Generate PDF with better settings
                    page.pdf(
                        path=pdf_path,
                        format='A4',
                        margin={'top': '1cm', 'right': '1cm', 'bottom': '1cm', 'left': '1cm'},
                        print_background=True,
                        prefer_css_page_size=True,
                        display_header_footer=False
                    )
                    browser.close()
                return True
                
            except ImportError:
                print("Playwright not installed. Installing...")
                install_package("playwright")
                subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
                
                from playwright.sync_api import sync_playwright
                
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    
                    # Navigate to the HTML file
                    page.goto(f"file://{os.path.abspath(html_path)}")
                    
                    # Wait for the page to fully load
                    page.wait_for_load_state('networkidle')
                    page.wait_for_timeout(2000)
                    
                    # Wait for tables to be visible
                    try:
                        page.wait_for_selector('table', timeout=5000)
                    except:
                        print("Warning: Tables not found, continuing with PDF generation...")
                    
                    page.pdf(
                        path=pdf_path,
                        format='A4',
                        margin={'top': '1cm', 'right': '1cm', 'bottom': '1cm', 'left': '1cm'},
                        print_background=True,
                        prefer_css_page_size=True,
                        display_header_footer=False
                    )
                    browser.close()
                return True
                
    except Exception as e:
        print(f"Error converting HTML to PDF with {method}: {e}")
        return False

def generate_biomechanical_report_with_pdf(sheet_id, output_dir="./reports/", charts_dir="./charts/", 
                                         convert_to_pdf=True, pdf_method="weasyprint"):
    """
    Generate both HTML and PDF versions of the biomechanical assessment report
    
    Args:
        sheet_id: Google Sheets ID
        output_dir: Directory for output files
        charts_dir: Directory for radar charts
        convert_to_pdf: Whether to convert HTML to PDF
        pdf_method: Method for PDF conversion ("weasyprint", "pdfkit", "playwright")
    
    Returns:
        tuple: (html_path, pdf_path) or (html_path, None) if PDF conversion fails
    """
    # Generate HTML report
    html_filename = "biomechanical_assessment_report.html"
    # html_path = os.path.join(output_dir, html_filename)
    html_path = html_filename
    
    try:
        report_path = generate_biomechanical_report(
            sheet_id=sheet_id,
            output_file=html_path,
            template_dir="./",
            charts_dir=charts_dir
        )
        
        print(f"✅ HTML report generated: {report_path}")
        
        if convert_to_pdf:
            # Generate PDF version
            pdf_filename = "biomechanical_assessment_report.pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)
            
            # Try different PDF conversion methods
            methods_to_try = [pdf_method]
            if pdf_method != "weasyprint":
                methods_to_try.append("weasyprint")
            if pdf_method != "playwright":
                methods_to_try.append("playwright")
            
            pdf_success = False
            for method in methods_to_try:
                print(f"Attempting PDF conversion with {method}...")
                if convert_html_to_pdf(html_path, pdf_path, method):
                    print(f"✅ PDF report generated: {pdf_path}")
                    pdf_success = True
                    break
                else:
                    print(f"❌ PDF conversion failed with {method}")
            
            if not pdf_success:
                print("❌ All PDF conversion methods failed. HTML report is still available.")
                return html_path, None
            
            return html_path, pdf_path
        
        return html_path, None
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return None, None

def main():
    # Your Google Sheets ID
    sheet_id = "1wu2ZWK_Em_2Hsj7unMD3s0gB2QqZz6GHYb00oDhtGjw"
    
    # Create output directories
    os.makedirs("./charts", exist_ok=True)
    os.makedirs("./reports", exist_ok=True)
    
    try:
        print("Starting biomechanical assessment report generation...")
        
        # Generate both HTML and PDF reports
        html_path, pdf_path = generate_biomechanical_report_with_pdf(
            sheet_id=sheet_id,
            output_dir="./reports/",
            charts_dir="./charts/",
            convert_to_pdf=True,
            pdf_method="playwright"  # Options: "weasyprint", "pdfkit", "playwright"
        )
        
        if html_path:
            print(f"\n✅ Success! HTML report generated at: {html_path}")
            
        if pdf_path:
            print(f"✅ Success! PDF report generated at: {pdf_path}")
            
        print("\n📊 Charts generated in: ./charts/")
        print("\n🌐 Open the HTML file in your web browser to view the complete report")
        if pdf_path:
            print("📄 Open the PDF file for a print-ready version")
        
        # List generated files
        print("\nGenerated files:")
        if html_path and os.path.exists(html_path):
            print(f"  📄 {html_path}")
        if pdf_path and os.path.exists(pdf_path):
            print(f"  📄 {pdf_path}")
        
        chart_files = [
            "./charts/ankle_radar_chart.png",
            "./charts/knee_radar_chart.png", 
            "./charts/hip_radar_chart.png",
            "./charts/shoulder_radar_chart.png"
        ]
        
        for chart_file in chart_files:
            if os.path.exists(chart_file):
                print(f"  📈 {chart_file}")
                
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        print("Make sure you have:")
        print("  1. Valid Google Sheets credentials (credentials.json)")
        print("  2. All required dependencies installed (jinja2, matplotlib, etc.)")
        print("  3. The HTML template file (biomechanical_report_template.html)")

def convert_existing_html_to_pdf(html_file_path, pdf_output_path=None, method="weasyprint"):
    """
    Convert an existing HTML file to PDF
    
    Args:
        html_file_path: Path to existing HTML file
        pdf_output_path: Output path for PDF (optional, will use same name with .pdf extension)
        method: Conversion method ("weasyprint", "pdfkit", "playwright")
    
    Returns:
        str: Path to generated PDF file or None if failed
    """
    if not os.path.exists(html_file_path):
        print(f"❌ HTML file not found: {html_file_path}")
        return None
    
    if pdf_output_path is None:
        # Generate PDF path from HTML path
        pdf_output_path = os.path.splitext(html_file_path)[0] + ".pdf"
    
    print(f"Converting {html_file_path} to {pdf_output_path}...")
    
    if convert_html_to_pdf(html_file_path, pdf_output_path, method):
        print(f"✅ PDF generated successfully: {pdf_output_path}")
        return pdf_output_path
    else:
        print("❌ PDF conversion failed")
        return None

if __name__ == "__main__":
    main()
#     pdf_path = convert_existing_html_to_pdf(
#     "biomechanical_report.html",
#     "biomechanical_report.pdf",
#     method="playwright"
# )
    
    # Example of converting an existing HTML file to PDF
    # Uncomment the lines below if you want to convert an existing HTML file
    # existing_html = "./reports/biomechanical_assessment_report.html"
    # convert_existing_html_to_pdf(existing_html)