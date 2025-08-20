import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Define the scope and credentials for Google Sheets API
# Update your scopes
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
sheets_id = "1L964TaAjOiI2HT1jPcdZbY8KeWeSPD22wvxVKfKUVdg"
# Open the Google Sheet
sheet = client.open_by_key(sheets_id)
# Select the first worksheet
values_list = sheet.sheet1.row_values(2)
# Print the values in the first row
print(values_list)
# create a new worksheet if it doesn't exist
try:
	new_sheet = sheet.worksheet("New Sheet")
except gspread.exceptions.WorksheetNotFound:
	new_sheet = sheet.add_worksheet(title="New Sheet", rows="100", cols="20")

# Merge row 1 2 and 3 and column 1 2 and 3 in already present sheet named new_sheet
# Make sure the worksheet is selected and exists before merging and updating
new_sheet.merge_cells('A1:C3')
# Write "Client_Data" in A1 cell of new_sheet
new_sheet.update('A1', [['Client_Data\nThis is a test message in the New Sheet.']])
# format the merged cell with bold text
format = {
    "textFormat": {
        "bold": True
    }
}
new_sheet.format('A1', format)
# Save the changes to the worksheet
print("Merged cells and updated the new sheet successfully.")


# extract data from 2nd sheet and 8th row
second_sheet = sheet.get_worksheet(1)  # Get the second worksheet (index 1)
row_8_values = second_sheet.row_values(7)  # Get values from the

# print the values
print("Values from the 8th row of the second sheet:", row_8_values)

# read the values from 11th row of the second sheet
row_11_values = second_sheet.row_values(11)  # Get values from the 11th row (index 10)

# print the values
print("Values from the 11th row of the second sheet:", row_11_values)


# Add this after your existing code
def create_radar_from_sheet_data():
    """
    Create radar chart using data from your second sheet
    """
    # Build the Sheets API service
    service = build('sheets', 'v4', credentials=creds)
    
    # Get the worksheet ID for second sheet
    spreadsheet = service.spreadsheets().get(spreadsheetId=sheets_id).execute()
    second_sheet_id = None
    
    for ws in spreadsheet['sheets']:
        if ws['properties']['index'] == 1:  # Second sheet (index 1)
            second_sheet_id = ws['properties']['sheetId']
            break
    
    # Use data from row 8 (your existing row_8_values)
    # Assume first 5 values are for categories and next 5 are values
    categories = row_8_values[:5] if len(row_8_values) >= 5 else row_8_values
    values = row_11_values[:5] if len(row_11_values) >= 5 else row_11_values
    
    # Add the data to a clean area in new_sheet for the chart
    chart_data = [categories, [float(v) if str(v).replace('.','').isdigit() else 0 for v in values]]
    new_sheet.update('F1:J2', chart_data)
    
    # Create radar chart
    requests = [{
        'addChart': {
            'chart': {
                'spec': {
                    'title': 'Data Analysis Radar Chart',
                    'basicChart': {
                        'chartType': 'RADAR',
                        'legendPosition': 'BOTTOM_LEGEND',
                        'domains': [{
                            'domain': {
                                'sourceRange': {
                                    'sources': [{
                                        'sheetId': new_sheet.id,
                                        'startRowIndex': 0,
                                        'endRowIndex': 1,
                                        'startColumnIndex': 5,  # Column F
                                        'endColumnIndex': 10   # Column J
                                    }]
                                }
                            }
                        }],
                        'series': [{
                            'series': {
                                'sourceRange': {
                                    'sources': [{
                                        'sheetId': new_sheet.id,
                                        'startRowIndex': 1,
                                        'endRowIndex': 2,
                                        'startColumnIndex': 5,
                                        'endColumnIndex': 10
                                    }]
                                }
                            }
                        }]
                    }
                },
                'position': {
                    'overlayPosition': {
                        'anchorCell': {
                            'sheetId': new_sheet.id,
                            'rowIndex': 4,
                            'columnIndex': 5
                        },
                        'widthPixels': 600,
                        'heightPixels': 400
                    }
                }
            }
        }
    }]
    
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=sheets_id,
            body={'requests': requests}
        ).execute()
        print("Radar chart created from sheet data!")
    except Exception as e:
        print(f"Error creating radar chart: {e}")

# Call the function
create_radar_from_sheet_data()
