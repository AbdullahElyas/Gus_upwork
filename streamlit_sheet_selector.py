import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from sheetid_fetch import get_sheet_ids_from_folder, save_sheet_ids_to_file, read_sheet_ids_from_file
from example_report import generate_report_for_sheet
import os
import sys
from io import StringIO
import contextlib
import json

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

def save_assessment_to_cache(sheet_id, assessments):
    """Save assessment texts to the cache file"""
    try:
        # Make sure the cache directory exists
        os.makedirs("./cache", exist_ok=True)
        
        # Define cache file path
        cache_file = os.path.join("./cache", f"{sheet_id}_assessments.json")
        
        # Debug output
        print(f"Saving to: {cache_file}")
        print(f"Data type: {type(assessments)}")
        print(f"Keys: {list(assessments.keys()) if isinstance(assessments, dict) else 'Not a dict'}")
        
        # Make sure we have valid data to save
        if not isinstance(assessments, dict):
            print("Error: assessments is not a dictionary")
            return False
            
        # Save the data with proper formatting
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(assessments, f, ensure_ascii=False, indent=2)
        
        # Verify file was created and has content
        if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
            print(f"Successfully saved to {cache_file}")
            return True
        else:
            print(f"File creation verification failed for {cache_file}")
            return False
            
    except Exception as e:
        print(f"Error saving assessments: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

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
    
    # Buttons for actions
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        fetch_button = st.button("🔄 Fetch", help="Fetch sheets from Google Drive")
    
    with col2:
        save_button = st.button("💾 Save", help="Save current sheet list to file")
    
    with col3:
        load_button = st.button("📂 Load", help="Load sheet list from file")
    
    # Main content area
    col_left, col_right = st.columns([1, 2])
    
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
        if selected_sheet:
            # Display selected sheet information
            st.subheader(f"📄 {selected_sheet['name']}")
            
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

            # Report status messages container - positioned right after the button
            report_status = st.empty()
            
            # REPORT GENERATION PROCESS
            if generate_button:
                # Create unique output directories for this sheet
                sheet_output_dir = os.path.join(output_dir, selected_sheet['name'])
                sheet_charts_dir = os.path.join(charts_dir, selected_sheet['name'])
                
                with st.spinner(f"Generating report for {selected_sheet['name']}..."):
                    try:
                        result = generate_report_for_sheet(
                            sheet_id=selected_sheet['id'],
                            output_dir=sheet_output_dir,
                            charts_dir=sheet_charts_dir,
                            convert_to_pdf=convert_to_pdf,
                            pdf_method=pdf_method,
                            use_cache=use_cached
                        )
                        
                        if result['success']:
                            st.success("✅ Report generated successfully!")
                            
                            # Display file paths and check if files actually exist
                            if result['html_path']:
                                html_exists = os.path.exists(result['html_path'])
                                status_icon = "✅" if html_exists else "❌"
                                st.markdown(f"**📄 HTML Report:** {status_icon} `{result['html_path']}`")
                            
                            if result['pdf_path']:
                                pdf_exists = os.path.exists(result['pdf_path'])
                                status_icon = "✅" if pdf_exists else "❌"
                                st.markdown(f"**📄 PDF Report:** {status_icon} `{result['pdf_path']}`")
                            
                            if result['chart_files']:
                                st.markdown(f"**📈 Charts Generated:** {len(result['chart_files'])} files")

                            st.info("Click 'Update Assessments' to load the newly generated assessment texts")
                        else:
                            st.error(f"❌ Report generation failed: {result['message']}")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating report: {e}")
                        st.session_state.report_results[selected_sheet['name']] = {
                            'success': False,
                            'message': str(e)
                        }
            
            # ASSESSMENT TABS SECTION - ALWAYS SHOWN
            st.markdown("---")
            st.subheader("📝 Assessment Texts")
            
            # Add Update Assessments button
            update_col1, update_col2 = st.columns([1, 3])
            with update_col1:
                update_button = st.button(
                    "🔄 Update Assessments",
                    key="update_assessments",
                    help="Load latest assessment texts from cache"
                )
            with update_col2:
                st.info("Click to load the latest assessment texts from cache")

            # Initialize assessment data structure in session state if needed
            sheet_id = selected_sheet['id']
            if sheet_id not in st.session_state.edited_assessments:
                st.session_state.edited_assessments[sheet_id] = {}
            
            # Update assessments from cache only when update button is clicked
            if update_button:
                cache_file = os.path.join("./cache", f"{sheet_id}_assessments.json")
                if os.path.exists(cache_file):
                    try:
                        with open(cache_file, 'r', encoding='utf-8') as f:
                            st.session_state.edited_assessments[sheet_id] = json.load(f)
                            st.success("✅ Successfully loaded assessment texts from cache")
                    except Exception as e:
                        st.error(f"Error loading assessment data: {str(e)}")
                else:
                    st.warning("No cached assessments found. Generate a report first.")
            
            # Get the current assessment data (might be empty)
            current_assessments = st.session_state.edited_assessments.get(sheet_id, {})

            # Create tabs that are ALWAYS displayed
            tab_labels = ["📊 Posture", "🏋️ Core", "🦶 Ankle", "🦵 Knee", "🍑 Hip", "💪 Shoulder", "📋 Conclusion"]
            tab_keys = ["posture", "core", "ankle", "knee", "hip", "shoulder", "overall_conclusion"]
            
            tabs = st.tabs(tab_labels)
            
            # Render each tab with its content (empty or filled)
            for i, (tab, key) in enumerate(zip(tabs, tab_keys)):
                with tab:
                    st.markdown(f"### {tab_labels[i].split(' ')[1]} Assessment")
                    
                    # Get text if available, otherwise empty
                    text = current_assessments.get(key, "")
                    display_text = text.replace('<br>', '\n') if text else ""
                    
                    # Always show editable text area
                    edited_text = st.text_area(
                        f"Edit {tab_labels[i].split(' ')[1]} Assessment",
                        value=display_text,
                        height=300,
                        key=f"edit_{key}_{sheet_id}"
                    )
                    
                    # Update session state if text changed
                    if edited_text != display_text:
                        # Store with HTML line breaks
                        current_assessments[key] = edited_text.replace('\n', '<br>')
                        st.session_state.edited_assessments[sheet_id] = current_assessments
                        st.info("Changes detected! Click 'Save Edited Assessments' below to save.")
            
            # SAVE BUTTON - ALWAYS SHOWN
            st.markdown("### Save Changes")
            save_col1, save_col2 = st.columns([1, 3])
            
            with save_col1:
                if st.button(
                    "💾 Save Edited Assessments", 
                    key=f"save_assessments_{sheet_id}", 
                    help="Save edited assessment texts to cache file",
                    type="primary"
                ):
                    # Direct save approach
                    current_data = st.session_state.edited_assessments.get(sheet_id, {})
                    if current_data:
                        try:
                            success = save_assessment_to_cache(sheet_id, current_data)
                            if success:
                                st.success("✅ Successfully saved edited assessments!")
                                st.balloons()
                            else:
                                st.error("❌ Failed to save assessments")
                        except Exception as e:
                            st.error(f"Error saving: {str(e)}")
                    else:
                        st.warning("No assessment data to save")
            
            with save_col2:
                st.info("💡 Click to save any edited assessment texts back to cache. This will affect future reports.")
            
            # DEBUG TOOLS
            with st.expander("🔍 Debug Tools"):
                st.write("Debugging tools for assessment editor:")
                
                # Button to print debug info about current assessments
                if st.button("🔍 Debug Assessment Data", key=f"debug_{sheet_id}"):
                    st.write("Current Assessment Data:")
                    st.write(f"Sheet ID: {sheet_id}")
                    st.write(f"Session state has key: {sheet_id in st.session_state.edited_assessments}")
                    
                    if sheet_id in st.session_state.edited_assessments:
                        data = st.session_state.edited_assessments[sheet_id]
                        st.write(f"Data type: {type(data)}")
                        st.write(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                        st.json(data)
                    else:
                        st.write("No data found for this sheet ID in session state")
                
                # Button to force create a test file
                if st.button("🔧 Test File Creation", key=f"test_file_{sheet_id}"):
                    try:
                        test_file = os.path.join("./cache", "test_write.txt")
                        os.makedirs("./cache", exist_ok=True)
                        with open(test_file, 'w') as f:
                            f.write("Test file creation succeeded")
                        
                        if os.path.exists(test_file):
                            st.success(f"✅ Successfully created test file: {test_file}")
                        else:
                            st.error(f"❌ Failed to create test file: {test_file}")
                    except Exception as e:
                        st.error(f"❌ Error creating test file: {str(e)}")
                
                # Button to clear session state
                if st.button("🗑️ Clear Session State", key=f"clear_session_{sheet_id}"):
                    if sheet_id in st.session_state.edited_assessments:
                        del st.session_state.edited_assessments[sheet_id]
                        st.success(f"✅ Cleared session state for sheet ID: {sheet_id}")
                        st.rerun()  # Changed from st.experimental_rerun()
                    else:
                        st.info(f"No session state found for sheet ID: {sheet_id}")
            
            # Additional information
            st.markdown("---")
            st.markdown("**Additional Information:**")
            
            # Sheet URL (for reference)
            sheet_url = f"https://docs.google.com/spreadsheets/d/{selected_sheet['id']}/edit"
            st.markdown(f"🔗 [Open in Google Sheets]({sheet_url})")
                
        else:
            st.info("👈 Select a sheet from the list to view its details.")
    
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