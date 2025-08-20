from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'credentials.json'

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build services
sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# Define the spreadsheet ID
SPREADSHEET_ID = '1L964TaAjOiI2HT1jPcdZbY8KeWeSPD22wvxVKfKUVdg'
# copy image from drive 
def copy_image_to_drive(image_id, folder_id):
    """
    Copy an image from Google Drive to a specified folder.
    """
    copied_file = {
        'name': 'copied_image.png',
        'parents': [folder_id]
    }
    return drive_service.files().copy(fileId=image_id, body=copied_file).execute()

# Function to create a radar chart from Google Sheets data
# paste the drive image to sheet
def paste_image_to_sheet(image_id, sheet_id, cell):
    """
    Paste an image into a Google Sheet at a specified cell.
    """
    requests = [{
        'pasteData': {
            'data': f'=IMAGE("https://drive.google.com/uc?id={image_id}")',
            'type': 'PASTE_NORMAL',
            'delimiter': ','
        }
    }]
    body = {
        'requests': requests
    }
    return sheets_service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=body).execute()