
import requests
from google.oauth2 import service_account
import google.auth.transport.requests
import gspread
from googleapiclient.discovery import build

# CONFIG
SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = "1L964TaAjOiI2HT1jPcdZbY8KeWeSPD22wvxVKfKUVdg"
SHEET_GID = "5"
OUTPUT_FILE = "exported_sheet_with_print_areas.pdf"
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
client = gspread.authorize(creds)

spreadsheet = client.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.get_worksheet(int(SHEET_GID))

spreadsheet_id = spreadsheet.id
worksheet_gid = worksheet.id  # This is important!

def set_print_areas_and_export_pdf(spreadsheet_id, worksheet_gid, print_ranges, output_file):
    """
    Set print areas first, then export PDF with those settings
    """
    # STEP 1: Set up credentials for both API and export
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    
    # Refresh token for PDF export
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    access_token = creds.token
    
    # Build service for API calls
    service = build('sheets', 'v4', credentials=creds)
    
    print("🔧 Setting print areas...")
    
    # STEP 2: Set print areas using API
    batch_requests = []
    
    # Clear existing named ranges first
    try:
        # Get existing named ranges
        spreadsheet_info = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        named_ranges = spreadsheet_info.get('namedRanges', [])
        
        # Delete existing PrintArea ranges
        for named_range in named_ranges:
            if named_range['name'].startswith('PrintArea_'):
                batch_requests.append({
                    'deleteNamedRange': {
                        'namedRangeId': named_range['namedRangeId']
                    }
                })
    except Exception as e:
        print(f"Note: Could not clear existing ranges: {e}")
    
    # Set new print areas (each range will be on a separate page)
    for i, print_range in enumerate(print_ranges):
        batch_requests.append({
            'addNamedRange': {
                'namedRange': {
                    'name': f'PrintArea_{i+1}',
                    'range': {
                        'sheetId': int(worksheet_gid),
                        'startRowIndex': print_range['start_row'],
                        'endRowIndex': print_range['end_row'],
                        'startColumnIndex': print_range['start_col'],
                        'endColumnIndex': print_range['end_col']
                    }
                }
            }
        })
    
    # Execute API requests to set print areas
    if batch_requests:
        try:
            response = service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': batch_requests}
            ).execute()
            print("✅ Print areas set successfully!")
            
            # Wait a moment for changes to propagate
            import time
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error setting print areas: {e}")
            return False
    
    # STEP 3: Export PDF with print areas applied
    print("📄 Exporting PDF with print areas...")
    
    export_url = (
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export"
        f"?format=pdf&gid={worksheet_gid}"
        f"&portrait=false&size=A4"
        f"&top_margin=0.50&bottom_margin=0.50&left_margin=0.50&right_margin=0.50"
        f"&sheetnames=false&printtitle=false"
        f"&scale=1"           # Use normal scale to respect print areas
        f"&fitw=false"        # Don't fit to width - use print areas instead
        f"&gridlines=true"    # Show gridlines to see the areas clearly
        f"&pagenumbers=true"  # Show page numbers
         f"&r1=0&r2=20&c1=0&c2=5"
    )
    
    # Download PDF
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(export_url, headers=headers)
    
    # Save to file
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"✅ PDF saved as {output_file}")
        return True
    else:
        print(f"❌ Failed to export PDF. Status code: {response.status_code}")
        print(response.text)
        return False

# STEP 4: Define your print ranges (page breaks)
print_ranges = [
    {'start_row': 0, 'end_row': 15, 'start_col': 0, 'end_col': 14},   # Page 1: A1:K15
    {'start_row': 100, 'end_row': 179, 'start_col': 0, 'end_col': 14},  # Page 2: A16:K30
    {'start_row': 200, 'end_row': 273, 'start_col': 0, 'end_col': 14}   # Page 3: A31:K45
]

# STEP 5: Execute the complete process
success = set_print_areas_and_export_pdf(
    spreadsheet_id, 
    worksheet_gid, 
    print_ranges, 
    OUTPUT_FILE
)

if success:
    print("🎉 Complete! PDF exported with custom print areas/page breaks")
else:
    print("❌ Process failed")
