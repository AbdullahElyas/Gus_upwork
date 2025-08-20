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
sheets_id = "1Lc1bOKXUeyRR_W78QMFqJayjb_UJQnx2OSvbxaoEkJ8"

# Open the Google Sheet
sheet = client.open_by_key(sheets_id)

#  get the worksheet with name Report
try:
    report_sheet = sheet.worksheet("Report")
except gspread.exceptions.WorksheetNotFound:
    report_sheet = sheet.add_worksheet(title="Report", rows="100", cols="20")
# Print the values in the first row
values_list = report_sheet.row_values(1)

# write down text in 15th row and 4th column
try:
    # report_sheet.update('D15', 'This is a test message in the Report sheet.')
    # Prepare the formatted text using Google Sheets' rich text formatting (basic, via formulas)
    # First heading (bold), then paragraph, then bold heading, then centered paragraph
    # To make the first line bold and the second line normal, use the Google Sheets API batchUpdate for rich text

    service = build('sheets', 'v4', credentials=creds)
    sheet_id = sheets_id

    # For B125
    cell_b125 = 'B125'
    row_index_b125 = 124  # zero-based index (B125 is row 125, so 124)
    col_index_b125 = 1    # B is column 2, so index 1

    # For D144
    cell_d144 = 'D144'
    row_index_f144 = 143  # D144 is row 144, so 143
    col_index_f144 = 5    # D is column 4, so index 3

    # For 162
    cell_f162 = 'F162'
    row_index_f162 = 161  # F162 is row 162, so 161
    col_index_f162 = 1    # F is column 6, so index 1

    # 
    


    text = (
        "\n\n"
        "First Heading\n"
        "This is a paragraph under the first heading.\n"
        "Core Function\n"
        "This is a paragraph under the Core Function heading."
    )

    # Calculate the start indices for each section
    first_heading_len = len("\n\nFirst Heading\n")
    first_paragraph_len = len("This is a paragraph under the first heading.\n")
    core_function_heading_start = first_heading_len + first_paragraph_len
    core_function_heading_len = len("Core Function\n")

    requests = [
        {
            "updateCells": {
                "rows": [
                    {
                        "values": [
                            {
                                "userEnteredValue": {"stringValue": text},
                                "textFormatRuns": [
                                    {
                                        "startIndex": 0,
                                        "format": {"bold": True}
                                    },
                                    {
                                        "startIndex": first_heading_len,
                                        "format": {"bold": False}
                                    },
                                    {
                                        "startIndex": core_function_heading_start,
                                        "format": {"bold": True}
                                    },
                                    {
                                        "startIndex": core_function_heading_start + core_function_heading_len,
                                        "format": {"bold": False}
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "fields": "userEnteredValue,textFormatRuns",
                "start": {"sheetId": report_sheet.id, "rowIndex": row_index_b125, "columnIndex": col_index_b125}
            }
        },
        {
            "updateCells": {
                "rows": [
                    {
                        "values": [
                            {
                                "userEnteredValue": {"stringValue": text},
                                "textFormatRuns": [
                                    {
                                        "startIndex": 0,
                                        "format": {"bold": True}
                                    },
                                    {
                                        "startIndex": first_heading_len,
                                        "format": {"bold": False}
                                    },
                                    {
                                        "startIndex": core_function_heading_start,
                                        "format": {"bold": True}
                                    },
                                    {
                                        "startIndex": core_function_heading_start + core_function_heading_len,
                                        "format": {"bold": False}
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "fields": "userEnteredValue,textFormatRuns",
                "start": {"sheetId": report_sheet.id, "rowIndex": row_index_f144, "columnIndex": col_index_f144}
            }
        }
        ,
        {
            "updateCells": {
                "rows": [
                    {
                        "values": [
                            {
                                "userEnteredValue": {"stringValue": text},
                                "textFormatRuns": [
                                    {
                                        "startIndex": 0,
                                        "format": {"bold": True}
                                    },
                                    {
                                        "startIndex": first_heading_len,
                                        "format": {"bold": False}
                                    },
                                    {
                                        "startIndex": core_function_heading_start,
                                        "format": {"bold": True}
                                    },
                                    {
                                        "startIndex": core_function_heading_start + core_function_heading_len,
                                        "format": {"bold": False}
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "fields": "userEnteredValue,textFormatRuns",
                "start": {"sheetId": report_sheet.id, "rowIndex": row_index_f162, "columnIndex": col_index_f162}
            }
        }
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": requests}
    ).execute()
    cell_format = {
        "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
        "textFormat": {"fontSize": 12},
        "horizontalAlignment": "LEFT",
        "verticalAlignment": "TOP"
    }
    report_sheet.format('B125', cell_format)
except Exception as e:
    print(f"An error occurred while updating the sheet: {e}")
