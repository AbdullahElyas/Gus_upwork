import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from sheetid_fetch import get_sheet_ids_from_folder, save_sheet_ids_to_file, read_sheet_ids_from_file
from example_report import generate_report_for_sheet  # Import the report generation function
import os
import sys
from io import StringIO
import contextlib
import json

def show_assessment_editor(sheet_id, sheet_name):
    """Show assessment editor UI and handle state management"""
    st.markdown("---")
    st.subheader("📝 Assessment Texts")
    
    # Ensure we have a place for edited assessments
    if "edited_assessments" not in st.session_state:
        st.session_state.edited_assessments = {}
    
    # Cache file path
    cache_file = os.path.join("./cache", f"{sheet_id}_assessments.json")
    
    # Load cached data if we haven't already
    if sheet_id not in st.session_state.edited_assessments:
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    st.session_state.edited_assessments[sheet_id] = json.load(f)
                    st.success("✅ Loaded assessment data from cache")
            except Exception as e:
                st.error(f"Error loading assessment data: {str(e)}")
                st.session_state.edited_assessments[sheet_id] = {}
        else:
            st.warning("No cached assessments found. Generate a report first.")
            st.session_state.edited_assessments[sheet_id] = {}
    
    # Now access the data (or empty dict if nothing loaded)
    assessments = st.session_state.edited_assessments.get(sheet_id, {})
    
    if assessments:
        # For stability, use fixed tab names
        tab_names = ["posture", "core", "ankle", "knee", "hip", "shoulder", "conclusion"]
        tab_labels = ["📊 Posture", "🏋️ Core", "🦶 Ankle", "🦵 Knee", "🍑 Hip", "💪 Shoulder", "📋 Conclusion"]
        
        # Create tabs
        assessment_tabs = st.tabs(tab_labels)
        
        # Define a common function for updating edited text
        def handle_edit(tab_idx, field_name):
            text = assessments.get(field_name, "")
            if text:
                # Display text in a human-readable format
                display_text = text.replace('<br>', '\n')
                edited = st.text_area(
                    f"Edit {tab_labels[tab_idx].split(' ')[1]} Assessment",
                    value=display_text,
                    height=300,
                    key=f"edit_{field_name}_{sheet_id}"
                )
                if edited != display_text:
                    # Store edited text back to session state
                    assessments[field_name] = edited.replace('\n', '<br>')
                    st.session_state.edited_assessments[sheet_id] = assessments
                    # Add a visual confirmation
                    st.success("Changes detected! Click 'Save Edited Assessments' below to save.")
            else:
                st.info(f"No {tab_labels[tab_idx].split(' ')[1]} assessment available")
        
        # Handle each tab
        with assessment_tabs[0]:
            st.markdown("### Posture Assessment")
            handle_edit(0, "posture")
            
        with assessment_tabs[1]:
            st.markdown("### Core Function Assessment")
            handle_edit(1, "core")
            
        with assessment_tabs[2]:
            st.markdown("### Ankle Assessment")
            handle_edit(2, "ankle")
            
        with assessment_tabs[3]:
            st.markdown("### Knee Assessment")
            handle_edit(3, "knee")
            
        with assessment_tabs[4]:
            st.markdown("### Hip Assessment")
            handle_edit(4, "hip")
            
        with assessment_tabs[5]:
            st.markdown("### Shoulder Assessment")
            handle_edit(5, "shoulder")
            
        with assessment_tabs[6]:
            st.markdown("### Overall Conclusion")
            handle_edit(6, "overall_conclusion")
        
        # Add a save button outside the tabs
        st.markdown("### Save Changes")
        
        # Add save button outside the tabs - more reliable than in the tab container
        save_col1, save_col2 = st.columns([1, 3])
        with save_col1:
            # Properly define the button using the standard st.button pattern
            save_button = st.button(
                "💾 Save Edited Assessments", 
                key=f"save_assessments_{sheet_id}",
                help="Save edited assessment texts to cache file"
            )
            
            # Check if button was clicked
            if save_button:
                try:
                    # Ensure directory exists
                    os.makedirs("./cache", exist_ok=True)
                    
                    # Write the data
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        json.dump(assessments, f, ensure_ascii=False, indent=2)
                    
                    # Verify it saved
                    if os.path.exists(cache_file):
                        st.success("✅ Successfully saved edited assessments!")
                        st.balloons()
                    else:
                        st.error("Failed to save assessments - file not created")
                except Exception as e:
                    st.error(f"Error saving assessments: {str(e)}")
        
        with save_col2:
            st.info("💡 Click to save any edited assessment texts back to cache. This will affect future reports.")
    else:
        st.warning("No assessment data available for editing. Generate a report first.")
        
def save_assessment_to_cache(sheet_id, assessments):
    """Save assessment texts to the cache file"""
    cache_file = os.path.join("./cache", f"{sheet_id}_assessments.json")
    try:
        # Make sure the cache directory exists
        os.makedirs("./cache", exist_ok=True)
        
        # Make sure we have valid data to save
        if not isinstance(assessments, dict):
            return False
            
        # Save the data
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(assessments, f, ensure_ascii=False, indent=2)
            
        # Verify the file was created
        if os.path.exists(cache_file):
            return True
        return False
    except Exception as e:
        print(f"Error saving assessments: {e}")
        return False

def setup_drive_service():
    """Set up Google Drive service with credentials."""
    try:
        SERVICE_ACCOUNT_FILE = 'credentials.json'
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            st.error(f"Credentials file '{SERVICE_ACCOUNT_FILE}' not found!")
            return None
            
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        drive_service = build('drive', 'v3', credentials=creds)
        return drive_service
    except Exception as e:
        st.error(f"Error setting up Google Drive service: {e}")
        return None

@contextlib.contextmanager
def capture_output():
    """Capture stdout and stderr for debugging"""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    stdout_capture = StringIO()
    stderr_capture = StringIO()
    try:
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        yield stdout_capture, stderr_capture
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def main():
    st.set_page_config(
        page_title="Google Sheets Selector & Report Generator",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Google Sheets Selector & Report Generator")
    st.markdown("---")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Folder ID input
    folder_id = st.sidebar.text_input(
        "Google Drive Folder ID:",
        value="1Tp9NL94dqQVD8XiZVjNH4_yT4CGhFER4",
        help="Enter the Google Drive folder ID containing the sheets"
    )
    
    # Report generation settings
    st.sidebar.subheader("Report Settings")
    
    convert_to_pdf = st.sidebar.checkbox(
        "Generate PDF",
        value=True,
        help="Convert HTML report to PDF"
    )
    
    pdf_method = st.sidebar.selectbox(
        "PDF Conversion Method:",
        options=["playwright", "weasyprint", "pdfkit"],
        index=0,
        help="Choose the method for PDF conversion"
    )
    
    output_dir = st.sidebar.text_input(
        "Output Directory:",
        value="./reports/",
        help="Directory to save generated reports"
    )
    
    charts_dir = st.sidebar.text_input(
        "Charts Directory:",
        value="./charts/",
        help="Directory to save radar charts"
    )
    
    # Debug mode toggle
    debug_mode = st.sidebar.checkbox(
        "Debug Mode",
        value=False,
        help="Show detailed console output"
    )
    
    # Initialize session state
    if 'sheets_data' not in st.session_state:
        st.session_state.sheets_data = []
    if 'last_folder_id' not in st.session_state:
        st.session_state.last_folder_id = ""
    if 'report_results' not in st.session_state:
        st.session_state.report_results = {}
    if 'edited_assessments' not in st.session_state:
        st.session_state.edited_assessments = {}

# Then make these fixes to your Assessment Editing Section
    
    # Buttons for actions
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        fetch_button = st.button("🔄 Fetch", help="Fetch sheets from Google Drive")
    
    with col2:
        save_button = st.button("💾 Save", help="Save current sheet list to file")
    
    with col3:
        load_button = st.button("📂 Load", help="Load sheet list from file")
    
    # Main content area
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("Available Sheets")
        
        # Fetch sheets from Google Drive
        if fetch_button and folder_id:
            with st.spinner("Fetching sheets from Google Drive..."):
                drive_service = setup_drive_service()
                if drive_service:
                    try:
                        sheets = get_sheet_ids_from_folder(folder_id, drive_service)
                    except Exception as e:
                        st.error(f"Error fetching sheet IDs from folder: {e}")
                        # Fallback: read from text file
                        try:
                            sheets = read_sheet_ids_from_file()
                        except Exception as e2:
                            st.error(f"Error reading sheet IDs from sheetid_fetch.txt: {e2}")
                            sheets = []
                    if sheets:
                        st.session_state.sheets_data = sheets
                        st.session_state.last_folder_id = folder_id
                        st.success(f"✅ Fetched {len(sheets)} sheets successfully!")
                    else:
                        st.warning("No sheets found in the specified folder.")
                else:
                    st.error("Failed to connect to Google Drive.")
        
        # Save sheets to file
        if save_button and st.session_state.sheets_data:
            try:
                save_sheet_ids_to_file(st.session_state.sheets_data)
                st.success("✅ Sheets saved to 'sheetid_fetch.txt'!")
            except Exception as e:
                st.error(f"Error saving file: {e}")
        
        # Load sheets from file
        if load_button:
            try:
                loaded_sheets = read_sheet_ids_from_file()
                if loaded_sheets:
                    st.session_state.sheets_data = loaded_sheets
                    st.success(f"✅ Loaded {len(loaded_sheets)} sheets from file!")
                else:
                    st.warning("No sheets found in file or file doesn't exist.")
            except Exception as e:
                st.error(f"Error loading file: {e}")
        
        # Display sheets list
        if st.session_state.sheets_data:
            st.info(f"📋 Total sheets: {len(st.session_state.sheets_data)}")
            
            # Create a selectbox with sheet names
            sheet_names = [sheet['name'] for sheet in st.session_state.sheets_data]
            selected_sheet_name = st.selectbox(
                "Select a sheet:",
                options=sheet_names,
                index=0,
                key="sheet_selector"
            )
            
            # Find selected sheet data
            selected_sheet = next(
                (sheet for sheet in st.session_state.sheets_data if sheet['name'] == selected_sheet_name),
                None
            )
            
        else:
            st.info("👆 Use the buttons above to fetch or load sheet data.")
            selected_sheet = None
    
    with col_right:
        st.subheader("Selected Sheet Details")
        
        if selected_sheet:
            # Display selected sheet information
            st.success(f"📄 **Sheet Selected:** {selected_sheet['name']}")
            
            # Sheet ID display with copy button
            st.markdown("**Sheet ID:**")
            sheet_id_container = st.container()
            with sheet_id_container:
                col_id, col_copy = st.columns([3, 1])
                with col_id:
                    st.code(selected_sheet['id'], language=None)
                with col_copy:
                    if st.button("📋 Copy", key="copy_id"):
                        st.write("ID copied to clipboard!")
                        # Note: Actual clipboard copying requires additional setup
            
            # Report Generation Section
            st.markdown("---")
            st.markdown("**🚀 Generate Report**")
            
            # Use cached response checkbox
            use_cached = st.checkbox(
                "Use Cached Response", 
                value=True,
                help="Use cached assessment data if available. Uncheck to force regeneration."
            )
            # Generate Report Button
            generate_button = st.button(
                "📄 Generate Biomechanical Report",
                type="primary",
                help=f"Generate report for {selected_sheet['name']}"
            )
            
            if generate_button:
                # Create unique output directories for this sheet
                sheet_output_dir = os.path.join(output_dir, selected_sheet['name'])
                sheet_charts_dir = os.path.join(charts_dir, selected_sheet['name'])
                
                # Show the directories that will be used
                st.info(f"📁 Output: `{sheet_output_dir}`")
                st.info(f"📈 Charts: `{sheet_charts_dir}`")
                
                with st.spinner(f"Generating report for {selected_sheet['name']}..."):
                    try:
                        # Capture console output for debugging
                        with capture_output() as (stdout_capture, stderr_capture):
                            # Call the report generation function
                            result = generate_report_for_sheet(
                                sheet_id=selected_sheet['id'],
                                output_dir=sheet_output_dir,
                                charts_dir=sheet_charts_dir,
                                convert_to_pdf=convert_to_pdf,
                                pdf_method=pdf_method,
                                use_cache=use_cached
                                
                            )
                        
                        # Get captured output
                        stdout_text = stdout_capture.getvalue()
                        stderr_text = stderr_capture.getvalue()
                        
                        # Store result in session state
                        st.session_state.report_results[selected_sheet['name']] = result
                        
                        # Display results
                        if result['success']:
                            st.success("✅ Report generated successfully!")
                            
                            # Display file paths and check if files actually exist
                            if result['html_path']:
                                html_exists = os.path.exists(result['html_path'])
                                status_icon = "✅" if html_exists else "❌"
                                st.markdown(f"**📄 HTML Report:** {status_icon} `{result['html_path']}`")
                                if html_exists:
                                    html_size = os.path.getsize(result['html_path'])
                                    st.write(f"   📏 Size: {html_size} bytes")
                            
                            if result['pdf_path']:
                                pdf_exists = os.path.exists(result['pdf_path'])
                                status_icon = "✅" if pdf_exists else "❌"
                                st.markdown(f"**📄 PDF Report:** {status_icon} `{result['pdf_path']}`")
                                if pdf_exists:
                                    pdf_size = os.path.getsize(result['pdf_path'])
                                    st.write(f"   📏 Size: {pdf_size} bytes")
                                elif convert_to_pdf:
                                    st.warning("⚠️ PDF was supposed to be generated but file not found!")
                            
                            if result['chart_files']:
                                st.markdown(f"**📈 Charts Generated:** {len(result['chart_files'])} files")
                                with st.expander("View Chart Files"):
                                    for chart in result['chart_files']:
                                        chart_exists = os.path.exists(chart)
                                        status_icon = "✅" if chart_exists else "❌"
                                        st.write(f"{status_icon} {chart}")

                                                        # Assessment Editing Section

                            show_assessment_editor(selected_sheet['id'], selected_sheet['name'])
                        else:
                            st.error(f"❌ Report generation failed: {result['message']}")
                        
                        # Show debug output if enabled
                        if debug_mode and (stdout_text or stderr_text):
                            with st.expander("🐛 Debug Output"):
                                if stdout_text:
                                    st.text_area("Console Output:", stdout_text, height=200)
                                if stderr_text:
                                    st.text_area("Error Output:", stderr_text, height=200)
                        
                        # Always show PDF-specific debug info if PDF generation was requested
                        if convert_to_pdf and not result.get('pdf_path'):
                            st.warning("🔍 PDF Debug Information:")
                            st.write(f"PDF Method: {pdf_method}")
                            st.write(f"Expected PDF path: {os.path.join(sheet_output_dir, 'biomechanical_assessment_report.pdf')}")
                            
                            if stdout_text:
                                pdf_lines = [line for line in stdout_text.split('\n') if 'pdf' in line.lower() or 'error' in line.lower()]
                                if pdf_lines:
                                    st.code('\n'.join(pdf_lines))
                            
                    except Exception as e:
                        st.error(f"❌ Error generating report: {e}")
                        import traceback
                        st.code(traceback.format_exc())
                        st.session_state.report_results[selected_sheet['name']] = {
                            'success': False,
                            'message': str(e)
                        }
            
            # Display previous report results if available
            if selected_sheet['name'] in st.session_state.report_results:
                st.markdown("---")
                st.markdown("**📋 Previous Report Results**")
                
                result = st.session_state.report_results[selected_sheet['name']]
                
                if result['success']:
                    st.success("✅ Last generation was successful")
                    
                    # Show file links if they exist
                    if result.get('html_path'):
                        html_exists = os.path.exists(result['html_path'])
                        status_icon = "✅" if html_exists else "❌"
                        st.markdown(f"📄 HTML: {status_icon} `{result['html_path']}`")
                    
                    if result.get('pdf_path'):
                        pdf_exists = os.path.exists(result['pdf_path'])
                        status_icon = "✅" if pdf_exists else "❌"
                        st.markdown(f"📄 PDF: {status_icon} `{result['pdf_path']}`")
                        
                    if result.get('chart_files'):
                        with st.expander(f"📈 Charts ({len(result['chart_files'])})"):
                            for chart in result['chart_files']:
                                if os.path.exists(chart):
                                    st.write(f"✅ {chart}")
                                else:
                                    st.write(f"❌ {chart} (file not found)")
                else:
                    st.error(f"❌ Last generation failed: {result.get('message', 'Unknown error')}")
            
            # Additional information
            st.markdown("---")
            st.markdown("**Additional Information:**")
            
            # Sheet URL (for reference)
            sheet_url = f"https://docs.google.com/spreadsheets/d/{selected_sheet['id']}/edit"
            st.markdown(f"🔗 [Open in Google Sheets]({sheet_url})")
            
            # JSON format for API usage
            with st.expander("📋 JSON Format (for API usage)"):
                st.json({
                    "name": selected_sheet['name'],
                    "id": selected_sheet['id'],
                    "url": sheet_url
                })
            
            # Raw data display
            with st.expander("🔍 Raw Sheet Data"):
                st.write(selected_sheet)
                
        else:
            st.info("👈 Select a sheet from the list to view its details.")
    
    # Footer with report summary
    if st.session_state.report_results:
        st.markdown("---")
        st.subheader("📊 Report Generation Summary")
        
        successful_reports = sum(1 for r in st.session_state.report_results.values() if r['success'])
        total_reports = len(st.session_state.report_results)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Reports", total_reports)
        with col2:
            st.metric("Successful", successful_reports)
        with col3:
            st.metric("Failed", total_reports - successful_reports)
        
        # Show detailed results
        with st.expander("📋 Detailed Results"):
            for sheet_name, result in st.session_state.report_results.items():
                status = "✅" if result['success'] else "❌"
                st.write(f"{status} **{sheet_name}**")
                if result['success']:
                    if result.get('html_path'):
                        st.write(f"   📄 HTML: {result['html_path']}")
                    if result.get('pdf_path'):
                        st.write(f"   📄 PDF: {result['pdf_path']}")
                else:
                    st.write(f"   ❌ Error: {result.get('message', 'Unknown error')}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Google Sheets Selector & Report Generator | Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()