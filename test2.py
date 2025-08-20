import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Define the scope and credentials for Google Sheets API
# Update your scopes
scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]
service_account_file = 'credentials.json'
creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
service = build('sheets', 'v4', credentials=creds)
sheets_id = "1L964TaAjOiI2HT1jPcdZbY8KeWeSPD22wvxVKfKUVdg"
sheet = service.spreadsheets()

result = sheet.values().get(spreadsheetId=sheets_id, range='Sheet1!A1:B2').execute()
values = result.get('values', [])


