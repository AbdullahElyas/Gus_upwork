import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


# load sheet id data 
# read the data from sheetid_fetch.txt
with open('sheetid_fetch.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        name, sheet_id = line.strip().split(' - ')
        print(f"Sheet Name: {name}, Sheet ID: {sheet_id}")



scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)


def extract_sheet_metrics(sheet_id):

    # Open the Google Sheet
    sheet = client.open_by_key(sheet_id)

    # read the values from 7th row in the second sheet
    worksheet = sheet.get_worksheet(1)
    values = worksheet.row_values(7)

    # get the numeric value from the sixth column of values list
    FHP = float(values[5]) if len(values) > 5 and values[5] else 0
    # get the numeric value from the fourth column of values list
    FHP_GS = float(values[3]) if len(values) > 3 and values[3] else 0
    # get the numeric value from the tenth column of values list
    DIFF_FHP = float(values[9]) if len(values) > 9 and values[9] else 0

    # read the values from 19th row in the second sheet
    values_19 = worksheet.row_values(19)

    # get the numeric value from the sixth column of values list
    TC = float(values_19[5]) if len(values_19) > 5 and values_19[5] else 0
    # get the numeric value from the fourth column of values list
    TC_GS = float(values_19[3]) if len(values_19) > 3 and values_19[3] else 0
    # get the numeric value from the tenth column of values list
    DIFF_TC = float(values_19[9]) if len(values_19) > 9 and values_19[9] else 0

    # read the values from 21th row in the second sheet 
    values_21 = worksheet.row_values(21)
    # get the numeric value from the sixth column of values list
    LC = float(values_21[5]) if len(values_21) > 5 and values_21[5] else 0
    # get the numeric value from the fourth column of values list
    LC_GS = float(values_21[3]) if len(values_21) > 3 and values_21[3] else 0
    # get the numeric value from the tenth column of values list
    DIFF_LC = float(values_21[9]) if len(values_21) > 9 and values_21[9] else 0



    

    # read the values from 13th row and 4th column in the second sheet
    values_13 = worksheet.row_values(13)
    # get the numeric value from the fourth column of values list
    if len(values_13) > 3 and values_13[3]:
        try:
            C7T1 = float(values_13[3])
        except ValueError:
            print(f"Invalid C7T1 value in row 13, column 4 for sheet ID {sheet_id}. Using default value 0.")
            C7T1 = 0
    else:
        print(f"No C7T1 value found in row 13, column 4 for sheet ID {sheet_id}. Using default value 0.")
        C7T1 = 0

    # read the values from 15th row and fourth column in the second sheet
    values_15 = worksheet.row_values(15)
    # get the numeric value from the fourth column of values list
    if len(values_15) > 3 and values_15[3]:
        try:
            T12L1 = float(values_15[3])
        except ValueError:
            print(f"Invalid T12L1 value in row 15, column 4 for sheet ID {sheet_id}. Using default value 0.")
            T12L1 = 0
    else:
        print(f"No T12L1 value found in row 15, column 4 for sheet ID {sheet_id}. Using default value 0.")
        T12L1 = 0

    # read the values from 17th row and fourth column in the second sheet
    values_17 = worksheet.row_values(17)
    # get the numeric value from the fourth column of values list
    if len(values_17) > 3 and values_17[3]:
        try:
            L5S1 = float(values_17[3])
        except ValueError:
            print(f"Invalid L5S1 value in row 17, column 4 for sheet ID {sheet_id}. Using default value 0.")
            L5S1 = 0
    else:
        print(f"No L5S1 value found in row 17, column 4 for sheet ID {sheet_id}. Using default value 0.")
        L5S1 = 0

    # search for worksheet with name 'Report' or 'NEW Datavis'
    report_worksheet = None
    for ws in sheet.worksheets():
        if ws.title in ['Report', 'NEW Datavis']:
            report_worksheet = ws
            break
    if report_worksheet is None:
        print(f"No 'Report' or 'NEW Datavis' worksheet found in sheet ID {sheet_id}.")
        return None
    
    # search each row 2nd column of report_worksheet whose firt word is 'LENGTH TENSION' and then store the whole cell string

    length_tension_row = None
    for row in report_worksheet.get_all_values():
        if row and row[1].startswith('LENGTH TENSION'):
            length_tension_row = row
            break
    if length_tension_row is None:
        print(f"No 'LENGTH TENSION' row found in 'Report' or 'NEW Datavis' worksheet for sheet ID {sheet_id}.")
        return None
    
    # in length_tension_row[1] search for words forward head posture,sway back posture,flat back posture,kyphotic back posture,kyphotic posture

    keywords = [
        "forward head posture",
        "you have a forward head posture",
        "forward head posture is slightly increased",
        "sway back posture",
        "swayback posture",
        "flat back posture",
        "kyphotic back posture",
        "kyphotic posture",
        "kyphosis",
        "lordosis"
        " increased curve in your lumbar spine",
        "reduced curve in your lumbar spine",
        "slightly increased curvature in your lumbar spine",
        "slightly reduced curve in your lumbar spine",

    ]

    found_keywords = []
    for keyword in keywords:
        if keyword in length_tension_row[1].lower():
            found_keywords.append(keyword)

    if not found_keywords:
        print(f"No relevant keywords found in 'LENGTH TENSION' row for sheet ID {sheet_id}.")
        return None
    
    # search for the keyword 'reduced curve in your lumbar spine' in length_tension_row[1] if not found then return None and store this in keyword_found2
    keyword2 = ['reduced curve in your lumbar spine']
    found_keywords2 = []
    for keyword in keyword2:
        if keyword in length_tension_row[1].lower():
            found_keywords2.append(keyword)
    

  

    return FHP, FHP_GS, DIFF_FHP, TC, TC_GS, DIFF_TC, LC, LC_GS, DIFF_LC, C7T1, T12L1, L5S1, found_keywords,found_keywords2

import time
# loop through the sheet ids and extract the metrics
sheet_ids = []
for line in lines:
    name, sheet_id = line.strip().split(' - ')
    sheet_ids.append(sheet_id)

# Extract metrics for each sheet
metrics = {}
iter = 0
for sheet_id in sheet_ids:
    iter += 1
    metrics[sheet_id] = extract_sheet_metrics(sheet_id)
    if iter % 4 == 0:
        print(f"Processed {iter} sheets...")
        # wait for 1 minute to avoid rate limiting
        time.sleep(60)
        
    # 
# write the data in metrics to a csv file
import csv
with open('extracted_metrics.csv', 'w', newline='') as csvfile:
    fieldnames = ['Sheet ID', 'FHP', 'FHP GS', 'DIFF FHP', 'TC', 'TC GS', 'DIFF TC', 
                  'LC', 'LC GS', 'DIFF LC', 'C7T1', 'T12L1', 'L5S1', 
                  'Found Keywords', 'Found Keywords 2']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for sheet_id, data in metrics.items():
        if data:
            FHP, FHP_GS, DIFF_FHP, TC, TC_GS, DIFF_TC, LC, LC_GS, DIFF_LC, C7T1, T12L1, L5S1, found_keywords, found_keywords2 = data
            writer.writerow({
                'Sheet ID': sheet_id,
                'FHP': FHP,
                'FHP GS': FHP_GS,
                'DIFF FHP': DIFF_FHP,
                'TC': TC,
                'TC GS': TC_GS,
                'DIFF TC': DIFF_TC,
                'LC': LC,
                'LC GS': LC_GS,
                'DIFF LC': DIFF_LC,
                'C7T1': C7T1,
                'T12L1': T12L1,
                'L5S1': L5S1,
                'Found Keywords': ', '.join(found_keywords),
                'Found Keywords 2': ', '.join(found_keywords2)
            })
        else:
            writer.writerow({'Sheet ID': sheet_id})

# Print the extracted metrics and found keywords
for sheet_id, data in metrics.items():
    if data:
        FHP, FHP_GS, DIFF_FHP, TC, TC_GS, DIFF_TC, LC, LC_GS, DIFF_LC, C7T1, T12L1, L5S1, found_keywords,found_keywords2 = data
        print(f"Sheet ID: {sheet_id}")
        print(f"FHP: {FHP}, FHP GS: {FHP_GS}, DIFF FHP: {DIFF_FHP}")
        print(f"TC: {TC}, TC GS: {TC_GS}, DIFF TC: {DIFF_TC}")
        print(f"Found Keywords: {', '.join(found_keywords)}")
    else:
        print(f"No valid data extracted for Sheet ID: {sheet_id}")
