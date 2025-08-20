import requests
from google.oauth2 import service_account
import google.auth.transport.requests
import gspread
from googleapiclient.discovery import build

# CONFIG
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Path to your service account JSON file
SPREADSHEET_ID = "1L964TaAjOiI2HT1jPcdZbY8KeWeSPD22wvxVKfKUVdg"
SHEET_GID = "5"  # GID of the worksheet/tab (usually 0 for first sheet)
OUTPUT_FILE = "exported_sheet3.pdf"

# AUTHENTICATE
scopes = ['https://www.googleapis.com/auth/drive.readonly']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)

auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)
access_token = creds.token
client = gspread.authorize(creds)

spreadsheet = client.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.get_worksheet(int(SHEET_GID))

spreadsheet_id = spreadsheet.id
worksheet_gid = worksheet.id  # This is important!

# # CONSTRUCT EXPORT URL
# export_url = (
#     f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export"
#     f"?format=pdf&gid={worksheet_gid}"
#     f"&portrait=false&size=A4&fitw=true&top_margin=0.50&bottom_margin=0.50"
#     f"&left_margin=0.50&right_margin=0.50&sheetnames=false&printtitle=false"
# )

creds.refresh(auth_req)
access_token = creds.token
    
    # Enhanced export URL with page break settings
export_url = (
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export"
        f"?format=pdf&gid={worksheet_gid}"
        f"&portrait=false&size=A4&fitw=true"
        f"&top_margin=0.50&bottom_margin=0.50&left_margin=0.50&right_margin=0.50"
        f"&sheetnames=false&printtitle=false"
        f"&pagenum=UNDEFINED"  # Page numbering
        f"&attachment=false"   # Display in browser vs download
        f"&scale=2"           # Scale: 1=Normal, 2=Fit to width, 3=Fit to height, 4=Fit to page
        f"&fzr=false"         # Frozen rows
        f"&fzc=false"         # Frozen columns
        f"&gridlines=false"   # Show gridlines
        f"&printnotes=false"  # Print notes
        f"&pagenumbers=false" # Show page numbers
    )




def set_print_areas_with_breaks(spreadsheet_id, print_ranges):
    """
    Set specific print areas which naturally create page breaks
    """
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    
    requests = []
    
    # Clear existing print settings
    requests.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': worksheet_gid,
                'gridProperties': {
                    'hideGridlines': False
                }
            },
            'fields': 'gridProperties.hideGridlines'
        }
    })
    
    # Set print areas (each range will be on a separate page)
    for i, print_range in enumerate(print_ranges):
        requests.append({
            'addNamedRange': {
                'namedRange': {
                    'name': f'PrintArea_{i+1}',
                    'range': {
                        'sheetId': worksheet_gid,
                        'startRowIndex': print_range['start_row'],
                        'endRowIndex': print_range['end_row'],
                        'startColumnIndex': print_range['start_col'],
                        'endColumnIndex': print_range['end_col']
                    }
                }
            }
        })
    
    # Execute requests
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()
        print("Print areas set successfully!")
        return True
    except Exception as e:
        print(f"Error setting print areas: {e}")
        return False

# Example usage
print_ranges = [
    {'start_row': 0, 'end_row': 15, 'start_col': 0, 'end_col': 10},   # Page 1: A1:K15
    {'start_row': 16, 'end_row': 30, 'start_col': 0, 'end_col': 10},  # Page 2: A16:K30
    {'start_row': 31, 'end_row': 45, 'start_col': 0, 'end_col': 10}   # Page 3: A31:K45
]

# set_print_areas_with_breaks("1L964TaAjOiI2HT1jPcdZbY8KeWeSPD22wvxVKfKUVdg", print_ranges)

# DOWNLOAD PDF
headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(export_url, headers=headers)

# SAVE TO FILE
if response.status_code == 200:
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(response.content)
    print(f"Saved as {OUTPUT_FILE}")
else:
    print("Failed to export sheet. Status code:", response.status_code)
    print(response.text)