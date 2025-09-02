def get_sheet_ids_from_folder(folder_id, drive_service):
    """
    Get all Google Sheets IDs from a specified Google Drive folder.
    
    Parameters:
    - folder_id: string ID of the Google Drive folder
    - drive_service: authenticated Google Drive service object
    
    Returns:
    - list of dictionaries with 'name' and 'id' keys for each sheet
    """
    
    # Query files in the folder
    query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"

    results = drive_service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=100
    ).execute()

    sheets = results.get('files', [])

    if not sheets:
        print("No Google Sheets found in the folder.")
        return []
    
    # Sort sheets by numeric suffix (Sample_1, Sample_2, etc.)
    sheets.sort(key=lambda x: int(x['name'].split('_')[1]) if '_' in x['name'] and x['name'].split('_')[1].isdigit() else float('inf'))
    
    # Convert to list of dictionaries with name and id
    sheet_list = [{'name': sheet['name'], 'id': sheet['id']} for sheet in sheets]
    
    return sheet_list

def save_sheet_ids_to_file(sheet_list, filename='sheetid_fetch.txt'):
    """
    Save sheet names and IDs to a text file.
    
    Parameters:
    - sheet_list: list of dictionaries with 'name' and 'id' keys
    - filename: string filename to save to (optional, defaults to 'sheetid_fetch.txt')
    """
    with open(filename, 'w') as f:
        for sheet in sheet_list:
            f.write(f"{sheet['name']} - {sheet['id']}\n")

def read_sheet_ids_from_file(filename='sheetid_fetch.txt'):
    """
    Read sheet names and IDs from a text file.
    
    Parameters:
    - filename: string filename to read from (optional, defaults to 'sheetid_fetch.txt')
    
    Returns:
    - list of dictionaries with 'name' and 'id' keys
    """
    sheet_list = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if ' - ' in line:
                    name, sheet_id = line.strip().split(' - ', 1)
                    sheet_list.append({'name': name, 'id': sheet_id})
    except FileNotFoundError:
        print(f"File {filename} not found.")
    
    return sheet_list

# Example usage:
if __name__ == "__main__":
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    
    # Setup credentials and drive service
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    FOLDER_ID = '1Tp9NL94dqQVD8XiZVjNH4_yT4CGhFER4'
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    
    # Get sheet IDs from folder
    sheets = get_sheet_ids_from_folder(FOLDER_ID, drive_service)
    
    # Print results
    print("Google Sheets in folder:")
    for sheet in sheets:
        print(f"Name: {sheet['name']}, ID: {sheet['id']}")
    
    # Save to file
    save_sheet_ids_to_file(sheets)
    
    # Read back from file
    loaded_sheets = read_sheet_ids_from_file()
    print("\nLoaded from file:")
    for sheet in loaded_sheets:
        print(f"Sheet Name: {sheet['name']}, Sheet ID: {sheet['id']}")