"""
Simple example script to generate a biomechanical assessment report
"""

from report_generator import generate_biomechanical_report
import os
import subprocess
import sys
import tempfile
import json

def install_package(package):
    """Install a package using pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])




def convert_html_to_pdf_subprocess(html_path, pdf_path, method="playwright"):
    """
    Convert HTML to PDF using subprocess to avoid Streamlit conflicts
    """
    try:
        # Create a temporary Python script for PDF conversion
        script_content = f'''
import os
import sys
import subprocess

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def convert_pdf():
    html_path = r"{html_path}"
    pdf_path = r"{pdf_path}"
    method = "{method}"
    
    try:
        if method == "playwright":
            try:
                from playwright.sync_api import sync_playwright
            except ImportError:
                print("Installing playwright...")
                install_package("playwright")
                subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
                from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
                )
                page = browser.new_page()
                
                # Create proper file URL
                html_abs_path = os.path.abspath(html_path)
                if os.name == 'nt':  # Windows
                    file_url = f"file:///" + html_abs_path.replace(os.sep, "/")
                else:
                    file_url = f"file://" + html_abs_path
                
                page.goto(file_url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(2000)
                
                # Add CSS
                page.add_style_tag(content="""
                    @page {{ size: A4; margin: 1cm; }}
                    body {{ font-size: 12pt; line-height: 1.4; }}
                    .graph-text img {{ max-width: 400px !important; }}
                    table {{ font-size: 10pt; page-break-inside: avoid; }}
                """)
                
                page.pdf(
                    path=pdf_path,
                    format='A4',
                    margin={{'top': '1cm', 'right': '1cm', 'bottom': '1cm', 'left': '1cm'}},
                    print_background=True,
                    prefer_css_page_size=True,
                    display_header_footer=False
                )
                browser.close()
                
                return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0
                
        elif method == "weasyprint":
            try:
                import weasyprint
                from weasyprint import HTML, CSS
            except ImportError:
                install_package("weasyprint")
                import weasyprint
                from weasyprint import HTML, CSS
            
            pdf_css = CSS(string="""
                @page {{ size: A4; margin: 1cm; }}
                body {{ font-size: 12pt; line-height: 1.4; }}
                .graph-text img {{ max-width: 400px !important; }}
                table {{ font-size: 10pt; }}
            """)
            
            HTML(filename=html_path).write_pdf(pdf_path, stylesheets=[pdf_css])
            return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0
            
        return False
        
    except Exception as e:
        print(f"Error: {{e}}")
        return False

if __name__ == "__main__":
    success = convert_pdf()
    print("SUCCESS" if success else "FAILED")
'''

        # Write script to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_script:
            temp_script.write(script_content)
            temp_script_path = temp_script.name

        try:
            # Run the script as subprocess
            print(f"🔄 Running PDF conversion as subprocess...")
            print(f"   Method: {method}")
            print(f"   HTML: {html_path}")
            print(f"   PDF: {pdf_path}")
            
            result = subprocess.run(
                [sys.executable, temp_script_path],
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )
            
            # Check if subprocess succeeded
            if result.returncode == 0:
                if "SUCCESS" in result.stdout:
                    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
                        pdf_size = os.path.getsize(pdf_path)
                        print(f"✅ PDF created successfully via subprocess: {pdf_path} ({pdf_size} bytes)")
                        return True
                    else:
                        print("❌ Subprocess claimed success but PDF not found")
                        return False
                else:
                    print(f"❌ Subprocess failed: {result.stdout}")
                    print(f"❌ Subprocess stderr: {result.stderr}")
                    return False
            else:
                print(f"❌ Subprocess returned error code {result.returncode}")
                print(f"❌ Subprocess stdout: {result.stdout}")
                print(f"❌ Subprocess stderr: {result.stderr}")
                return False
                
        finally:
            # Clean up temporary script
            try:
                os.unlink(temp_script_path)
            except:
                pass
                
    except Exception as e:
        print(f"❌ Subprocess PDF conversion failed: {e}")
        return False

def convert_html_to_pdf(html_path, pdf_path, method="weasyprint"):
    """
    Convert HTML file to PDF - uses subprocess when running in Streamlit
    """
    print(f"🔄 Starting PDF conversion...")
    print(f"   HTML file: {html_path}")
    print(f"   PDF output: {pdf_path}")
    print(f"   Method: {method}")
    
    # Check if HTML file exists
    if not os.path.exists(html_path):
        print(f"❌ HTML file not found: {html_path}")
        return False
    
    # Ensure PDF directory exists
    pdf_dir = os.path.dirname(pdf_path)
    if pdf_dir and not os.path.exists(pdf_dir):
        print(f"📁 Creating PDF directory: {pdf_dir}")
        os.makedirs(pdf_dir, exist_ok=True)
    
    # Check if we're running in Streamlit
    try:
        import streamlit as st
        if hasattr(st, 'session_state'):
            print("🌊 Detected Streamlit environment, using subprocess approach...")
            return convert_html_to_pdf_subprocess(html_path, pdf_path, method)
    except ImportError:
        pass
    
    # Original implementation for non-Streamlit environments
    try:
        if method == "playwright":
            try:
                print("🎭 Attempting PDF conversion with Playwright...")
                from playwright.sync_api import sync_playwright, Error as PlaywrightError
                
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
                    )
                    page = browser.new_page()
                    
                    html_abs_path = os.path.abspath(html_path)
                    if os.name == 'nt':  # Windows
                        file_url = f"file:///{html_abs_path.replace(os.sep, '/')}"
                    else:
                        file_url = f"file://{html_abs_path}"
                    
                    page.goto(file_url, wait_until='networkidle', timeout=30000)
                    page.wait_for_timeout(2000)
                    
                    page.add_style_tag(content="""
                        @page { size: A4; margin: 1cm; }
                        body { font-size: 12pt; line-height: 1.4; }
                        .graph-text img { max-width: 400px !important; }
                        table { font-size: 10pt; page-break-inside: avoid; }
                    """)
                    
                    page.pdf(
                        path=pdf_path,
                        format='A4',
                        margin={'top': '1cm', 'right': '1cm', 'bottom': '1cm', 'left': '1cm'},
                        print_background=True,
                        prefer_css_page_size=True,
                        display_header_footer=False
                    )
                    browser.close()
                
                if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
                    pdf_size = os.path.getsize(pdf_path)
                    print(f"✅ PDF created successfully with Playwright: {pdf_path} ({pdf_size} bytes)")
                    return True
                else:
                    print("❌ PDF file was not created")
                    return False
                    
            except ImportError:
                print("📦 Installing Playwright...")
                install_package("playwright")
                subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
                # Retry after installation
                return convert_html_to_pdf(html_path, pdf_path, method)
                
            except Exception as e:
                print(f"❌ Playwright conversion failed: {e}")
                return False
                
        elif method == "weasyprint":
            try:
                print("🖨️ Attempting PDF conversion with WeasyPrint...")
                import weasyprint
                from weasyprint import HTML, CSS
                
                pdf_css = CSS(string='''
                    @page { size: A4; margin: 1cm; }
                    body { font-size: 12pt; line-height: 1.4; }
                    .graph-text img { max-width: 400px !important; }
                    table { font-size: 10pt; page-break-inside: avoid; }
                ''')
                
                HTML(filename=html_path).write_pdf(pdf_path, stylesheets=[pdf_css])
                
                if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
                    pdf_size = os.path.getsize(pdf_path)
                    print(f"✅ PDF created successfully with WeasyPrint: {pdf_path} ({pdf_size} bytes)")
                    return True
                else:
                    print("❌ PDF file was not created with WeasyPrint")
                    return False
                    
            except ImportError:
                print("📦 Installing WeasyPrint...")
                install_package("weasyprint")
                return convert_html_to_pdf(html_path, pdf_path, method)
                
            except Exception as e:
                print(f"❌ WeasyPrint conversion failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Unexpected error during PDF conversion: {e}")
        return False
    
    return False
def generate_biomechanical_report_with_pdf(sheet_id, output_dir="./reports/", charts_dir="./charts/", 
                                         convert_to_pdf=True, pdf_method="weasyprint", use_cache=True):
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
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate HTML report - PUT IT IN THE OUTPUT DIRECTORY
    html_filename = "biomechanical_assessment_report.html"
    # html_path = os.path.join(output_dir, html_filename)  # Fixed: put HTML in output_dir too
    html_path = html_filename  # Save HTML at root (current working directory)
    
    try:
        report_path = generate_biomechanical_report(
            sheet_id=sheet_id,
            output_file=html_path,  # Use the full path
            template_dir="./",
            charts_dir=charts_dir,
            use_cache=use_cache
        )
        
        print(f"✅ HTML report generated: {report_path}")
        
        if convert_to_pdf:
            # Generate PDF version in the same directory
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
    

# def generate_report_for_sheet(sheet_id, output_dir="./reports/", charts_dir="./charts/", 
#                              convert_to_pdf=True, pdf_method="playwright",use_cache=True):
#     """
#     Generate biomechanical assessment report for a specific sheet ID
    
#     Args:
#         sheet_id: Google Sheets ID to generate report for
#         output_dir: Directory for output files (default: "./reports/")
#         charts_dir: Directory for radar charts (default: "./charts/")
#         convert_to_pdf: Whether to convert HTML to PDF (default: True)
#         pdf_method: Method for PDF conversion - "weasyprint", "pdfkit", or "playwright" (default: "playwright")
    
#     Returns:
#         dict: Dictionary containing paths and status information
#         {
#             'success': bool,
#             'html_path': str or None,
#             'pdf_path': str or None,
#             'chart_files': list,
#             'message': str
#         }
#     """
    
#     # Create output directories
#     os.makedirs(output_dir, exist_ok=True)
#     os.makedirs(charts_dir, exist_ok=True)
    
#     result = {
#         'success': False,
#         'html_path': None,
#         'pdf_path': None,
#         'chart_files': [],
#         'message': ''
#     }
    
#     try:
#         print(f"Starting biomechanical assessment report generation for sheet: {sheet_id}")
        
#         # Generate both HTML and PDF reports
#         html_path, pdf_path = generate_biomechanical_report_with_pdf(
#             sheet_id=sheet_id,
#             output_dir=output_dir,
#             charts_dir=charts_dir,
#             convert_to_pdf=convert_to_pdf,
#             pdf_method=pdf_method
#         )
        
#         # Update result with paths
#         result['html_path'] = html_path
#         result['pdf_path'] = pdf_path
        
#         if html_path:
#             print(f"\n✅ Success! HTML report generated at: {html_path}")
#             result['success'] = True
#             result['message'] += f"HTML report: {html_path}\n"
            
#         if pdf_path:
#             print(f"✅ Success! PDF report generated at: {pdf_path}")
#             result['message'] += f"PDF report: {pdf_path}\n"
            
#         print(f"\n📊 Charts generated in: {charts_dir}")
#         print("\n🌐 Open the HTML file in your web browser to view the complete report")
#         if pdf_path:
#             print("📄 Open the PDF file for a print-ready version")
        
#         # Check for generated chart files
#         chart_files = [
#             os.path.join(charts_dir, "ankle_radar_chart.png"),
#             os.path.join(charts_dir, "knee_radar_chart.png"), 
#             os.path.join(charts_dir, "hip_radar_chart.png"),
#             os.path.join(charts_dir, "shoulder_radar_chart.png")
#         ]
        
#         existing_charts = []
#         print("\nGenerated files:")
#         if html_path and os.path.exists(html_path):
#             print(f"  📄 {html_path}")
#         if pdf_path and os.path.exists(pdf_path):
#             print(f"  📄 {pdf_path}")
        
#         for chart_file in chart_files:
#             if os.path.exists(chart_file):
#                 print(f"  📈 {chart_file}")
#                 existing_charts.append(chart_file)
        
#         result['chart_files'] = existing_charts
#         result['message'] += f"Charts: {len(existing_charts)} generated\n"
        
#         if not result['success']:
#             result['message'] = "Failed to generate report"
            
#     except Exception as e:
#         error_msg = f"❌ Error generating report: {e}"
#         print(error_msg)
#         print("Make sure you have:")
#         print("  1. Valid Google Sheets credentials (credentials.json)")
#         print("  2. All required dependencies installed (jinja2, matplotlib, etc.)")
#         print("  3. The HTML template file (biomechanical_report_template.html)")
        
#         result['success'] = False
#         result['message'] = str(e)
    
#     return result
def generate_report_for_sheet(sheet_id, output_dir="./reports/", charts_dir="./charts/", 
                             convert_to_pdf=True, pdf_method="playwright",use_cache=True):
    """
    Generate biomechanical assessment report for a specific sheet ID
    
    Args:
        sheet_id: Google Sheets ID to generate report for
        output_dir: Directory for output files (default: "./reports/")
        charts_dir: Directory for radar charts (default: "./charts/")
        convert_to_pdf: Whether to convert HTML to PDF (default: True)
        pdf_method: Method for PDF conversion - "weasyprint", "pdfkit", or "playwright" (default: "playwright")
    
    Returns:
        dict: Dictionary containing paths and status information
        {
            'success': bool,
            'html_path': str or None,
            'pdf_path': str or None,
            'chart_files': list,
            'message': str
        }
    """
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(charts_dir, exist_ok=True)
    
    result = {
        'success': False,
        'html_path': None,
        'pdf_path': None,
        'chart_files': [],
        'message': ''
    }
    
    try:
        print(f"🔄 Starting biomechanical assessment report generation for sheet: {sheet_id}")
        print(f"📁 Output directory: {output_dir}")
        print(f"📈 Charts directory: {charts_dir}")
        print(f"📄 PDF conversion: {'Enabled' if convert_to_pdf else 'Disabled'}")
        if convert_to_pdf:
            print(f"🔧 PDF method: {pdf_method}")
        
        # Generate both HTML and PDF reports
        html_path, pdf_path = generate_biomechanical_report_with_pdf(
            sheet_id=sheet_id,
            output_dir=output_dir,
            charts_dir=charts_dir,
            convert_to_pdf=convert_to_pdf,
            pdf_method=pdf_method,
            use_cache=use_cache
        )
        
        print(f"\n📋 Report generation completed:")
        print(f"   HTML path returned: {html_path}")
        print(f"   PDF path returned: {pdf_path}")
        
        # Update result with paths
        result['html_path'] = html_path
        result['pdf_path'] = pdf_path
        
        # Check if HTML was actually created
        if html_path and os.path.exists(html_path):
            html_size = os.path.getsize(html_path)
            print(f"✅ HTML report verified: {html_path} ({html_size} bytes)")
            result['success'] = True
            result['message'] += f"HTML report: {html_path} ({html_size} bytes)\n"
        elif html_path:
            print(f"❌ HTML report file not found: {html_path}")
            result['message'] += f"HTML report file not found: {html_path}\n"
        else:
            print("❌ No HTML path returned from report generation")
            result['message'] += "No HTML path returned from report generation\n"
            
        # Check if PDF was created (only if requested)
        if convert_to_pdf:
            if pdf_path and os.path.exists(pdf_path):
                pdf_size = os.path.getsize(pdf_path)
                print(f"✅ PDF report verified: {pdf_path} ({pdf_size} bytes)")
                result['message'] += f"PDF report: {pdf_path} ({pdf_size} bytes)\n"
            elif pdf_path:
                print(f"❌ PDF report file not found: {pdf_path}")
                result['message'] += f"PDF report file not found: {pdf_path}\n"
                
                # Try to convert again with better error handling
                print(f"🔄 Attempting manual PDF conversion...")
                if html_path and os.path.exists(html_path):
                    expected_pdf_path = os.path.join(output_dir, "biomechanical_assessment_report.pdf")
                    print(f"   HTML source: {html_path}")
                    print(f"   PDF target: {expected_pdf_path}")
                    
                    # Try conversion with all methods
                    methods_to_try = ["playwright", "weasyprint", "pdfkit"]
                    for method in methods_to_try:
                        print(f"   Trying {method}...")
                        try:
                            if convert_html_to_pdf(html_path, expected_pdf_path, method):
                                if os.path.exists(expected_pdf_path):
                                    pdf_size = os.path.getsize(expected_pdf_path)
                                    print(f"✅ PDF created with {method}: {expected_pdf_path} ({pdf_size} bytes)")
                                    result['pdf_path'] = expected_pdf_path
                                    result['message'] += f"PDF report (retry): {expected_pdf_path} ({pdf_size} bytes)\n"
                                    break
                                else:
                                    print(f"❌ {method} claimed success but no file created")
                            else:
                                print(f"❌ {method} conversion failed")
                        except Exception as e:
                            print(f"❌ {method} error: {e}")
                    
                    if not result['pdf_path']:
                        print("❌ All PDF conversion methods failed")
                        result['message'] += "All PDF conversion methods failed\n"
                else:
                    print("❌ Cannot retry PDF conversion - HTML file missing")
                    result['message'] += "Cannot retry PDF conversion - HTML file missing\n"
            else:
                print("❌ No PDF path returned from report generation")
                result['message'] += "No PDF path returned from report generation\n"
        
        print(f"\n📊 Checking charts in: {charts_dir}")
        
        # Check for generated chart files
        chart_files = [
            os.path.join(charts_dir, "ankle_radar_chart.png"),
            os.path.join(charts_dir, "knee_radar_chart.png"), 
            os.path.join(charts_dir, "hip_radar_chart.png"),
            os.path.join(charts_dir, "shoulder_radar_chart.png")
        ]
        
        existing_charts = []
        print("📈 Chart verification:")
        for chart_file in chart_files:
            if os.path.exists(chart_file):
                chart_size = os.path.getsize(chart_file)
                print(f"   ✅ {chart_file} ({chart_size} bytes)")
                existing_charts.append(chart_file)
            else:
                print(f"   ❌ {chart_file} (not found)")
        
        result['chart_files'] = existing_charts
        result['message'] += f"Charts: {len(existing_charts)}/{len(chart_files)} generated\n"
        
        # Final success determination
        if result['html_path'] and os.path.exists(result['html_path']):
            result['success'] = True
            if convert_to_pdf and not (result['pdf_path'] and os.path.exists(result['pdf_path'])):
                result['message'] += "⚠️ HTML generated successfully but PDF conversion failed\n"
        else:
            result['success'] = False
            result['message'] = "❌ Failed to generate HTML report\n" + result['message']
            
        print(f"\n📋 Final result: {'✅ Success' if result['success'] else '❌ Failed'}")
        
    except Exception as e:
        error_msg = f"❌ Error generating report: {e}"
        print(error_msg)
        print("Make sure you have:")
        print("  1. Valid Google Sheets credentials (credentials.json)")
        print("  2. All required dependencies installed (jinja2, matplotlib, etc.)")
        print("  3. The HTML template file (biomechanical_report_template.html)")
        
        # Print full traceback for debugging
        import traceback
        print("\n🐛 Full error traceback:")
        traceback.print_exc()
        
        result['success'] = False
        result['message'] = str(e)
    
    return result
    
def generate_multiple_reports(sheet_ids, output_base_dir="./reports/", charts_base_dir="./charts/",
                            convert_to_pdf=True, pdf_method="playwright", use_cached=True):
    """
    Generate reports for multiple sheet IDs
    
    Args:
        sheet_ids: List of Google Sheets IDs or list of dicts with 'id' and 'name' keys
        output_base_dir: Base directory for output files
        charts_base_dir: Base directory for charts
        convert_to_pdf: Whether to convert HTML to PDF
        pdf_method: Method for PDF conversion
    
    Returns:
        dict: Summary of all generated reports
    """
    
    results = {}
    
    for i, sheet_info in enumerate(sheet_ids):
        # Handle both string IDs and dict objects
        if isinstance(sheet_info, dict):
            sheet_id = sheet_info['id']
            sheet_name = sheet_info.get('name', f'Sheet_{i+1}')
        else:
            sheet_id = sheet_info
            sheet_name = f'Sheet_{i+1}'
        
        print(f"\n{'='*60}")
        print(f"Processing {sheet_name} ({i+1}/{len(sheet_ids)})")
        print(f"{'='*60}")
        
        # Create individual directories for each sheet
        sheet_output_dir = os.path.join(output_base_dir, sheet_name)
        sheet_charts_dir = os.path.join(charts_base_dir, sheet_name)
        
        # Generate report for this sheet
        result = generate_report_for_sheet(
            sheet_id=sheet_id,
            output_dir=sheet_output_dir,
            charts_dir=sheet_charts_dir,
            convert_to_pdf=convert_to_pdf,
            pdf_method=pdf_method,
            use_cache=use_cached
        )
        
        results[sheet_name] = result
        
        if result['success']:
            print(f"✅ Successfully generated report for {sheet_name}")
        else:
            print(f"❌ Failed to generate report for {sheet_name}: {result['message']}")
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for r in results.values() if r['success'])
    total = len(results)
    
    print(f"Successfully generated: {successful}/{total} reports")
    
    for sheet_name, result in results.items():
        status = "✅" if result['success'] else "❌"
        print(f"  {status} {sheet_name}")
        if result['success'] and result['html_path']:
            print(f"    📄 HTML: {result['html_path']}")
        if result['success'] and result['pdf_path']:
            print(f"    📄 PDF: {result['pdf_path']}")
    
    return results

# ...existing code...

def main():
    # Your Google Sheets ID
    sheet_id = "1XLHc0boxOxkn18ECPTJKK-FvL0_zHtqz4Awavz1Qo4c"

    # Generate report for the specified sheet
    result = generate_report_for_sheet(
        sheet_id=sheet_id,
        output_dir="./reports/",
        charts_dir="./charts/",
        convert_to_pdf=True,
        pdf_method="playwright",
        use_cache=True
    )

    if result['success']:
        print(f"✅ Report generated successfully: {result['html_path']}")
        if result['pdf_path']:
            print(f"✅ PDF generated successfully: {result['pdf_path']}")
    else:
        print(f"❌ Failed to generate report: {result['message']}")


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