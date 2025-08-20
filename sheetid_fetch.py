from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CONFIG ---
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Path to your service account JSON file
FOLDER_ID = '1Tp9NL94dqQVD8XiZVjNH4_yT4CGhFER4'  # Not the link! Just the ID
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# --- AUTHENTICATE ---
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# --- QUERY FILES ---
query = f"'{FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"

results = drive_service.files().list(
    q=query,
    spaces='drive',
    fields='files(id, name)',
    pageSize=100
).execute()

sheets = results.get('files', [])

# --- PRINT RESULTS ---
if not sheets:
    print("No Google Sheets found in the folder.")
else:
    print("Google Sheets in folder:")
    for sheet in sheets:
        print(f"Name: {sheet['name']}, ID: {sheet['id']}")

#  save sheet name and ID to a file
#  the names are in format "Sample_1" toSample_26' reorder them so Sample_1 is first
sheets.sort(key=lambda x: int(x['name'].split('_')[1]) if '_' in x['name'] else float('inf'))
sheets = [{'name': sheet['name'], 'id': sheet['id']} for sheet in sheets]
print("Sorted Sheets:")

# Save the sheet names and IDs to a text file

with open('sheetid_fetch.txt', 'w') as f:
    for sheet in sheets:
        f.write(f"{sheet['name']} - {sheet['id']}\n")




# read the data from sheetid_fetch.txt
with open('sheetid_fetch.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        name, sheet_id = line.strip().split(' - ')
        print(f"Sheet Name: {name}, Sheet ID: {sheet_id}")