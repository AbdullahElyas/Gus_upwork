# creating a function which takes input the sheetid and outputs the thoracic curvature lumber curvature and pelvic tilt angles
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# # load sheet id data 
# # read the data from sheetid_fetch.txt
# with open('sheetid_fetch.txt', 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         name, sheet_id = line.strip().split(' - ')
#         print(f"Sheet Name: {name}, Sheet ID: {sheet_id}")

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1Lc1bOKXUeyRR_W78QMFqJayjb_UJQnx2OSvbxaoEkJ8"
def extract_sheet_metrics_posture(sheet_id):
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

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
    
    # read the values from 9th row and 4th column in the second sheet
    values_9 = worksheet.row_values(9)
    # get the numeric value from the fourth column of values list
    if len(values_9) > 3 and values_9[3]:
        try:
            Pelvis_GS = float(values_9[3])
        except ValueError:
            print(f"Invalid Pelvis value in row 9, column 4 for sheet ID {sheet_id}. Using default value 0.")
            Pelvis_GS = 0
    else:
        print(f"No Pelvis value found in row 9, column 4 for sheet ID {sheet_id}. Using default value 0.")
        Pelvis_GS = 0

    # read the values from 9th row 6th column and 8th column in the second sheet
    values_9 = worksheet.row_values(9)
    # get the numeric value from the sixth column of values list
    if len(values_9) > 5 and values_9[5]:
        try:
            Pelvis_Left = float(values_9[5])
        except ValueError:
            print(f"Invalid Pelvis value in row 9, column 6 for sheet ID {sheet_id}. Using default value 0.")
            Pelvis_Left = 0
    else:
        print(f"No Pelvis value found in row 9, column 6 for sheet ID {sheet_id}. Using default value 0.")
        Pelvis_Left = 0

    # get the numeric value from the eighth column of values list
    if len(values_9) > 7 and values_9[7]:
        try:
            Pelvis_Right = float(values_9[7])
        except ValueError:
            print(f"Invalid Pelvis value in row 9, column 8 for sheet ID {sheet_id}. Using default value 0.")
            Pelvis_Right = 0
    else:
        print(f"No Pelvis value found in row 9, column 8 for sheet ID {sheet_id}. Using default value 0.")
        Pelvis_Right = 0

# Get the gender of the client from 1st row and 3rd column in the first sheet
    worksheet_first = sheet.get_worksheet(0)
    values_first = worksheet_first.row_values(1)
    # Get the gender of the client
    if len(values_first) > 2 and values_first[2]:
        Gender = values_first[2]
    else:
        print(f"No Gender value found in row 1, column 3 for sheet ID {sheet_id}. Using default value 'Unknown'.")
        Gender = 'Male'
    
    # Mean_pelvis should be lesser of Pelvis_Left and Pelvis_Right
    Mean_pelvis = min(Pelvis_Left, Pelvis_Right)
  
    # read row 49 from sheet 3 and get the numeric value from the 4th column 6th 8th and 10th column
    worksheet_third = sheet.get_worksheet(2)
    values_49 = worksheet_third.row_values(49)
    # get the numeric value from the fourth column of values list
    if len(values_49) > 3 and values_49[3]:
        try:
            Rotaion_Ribcage_Left = float(values_49[3])
        except ValueError:
            print(f"Invalid Rotaion_Ribcage value in row 49, column 4 for sheet ID {sheet_id}. Using default value 0.")
            Rotaion_Ribcage_Left = 0
    else:
        print(f"No Rotaion_Ribcage value found in row 49, column 4 for sheet ID {sheet_id}. Using default value 0.")
        Rotaion_Ribcage_Left = 0
    if len(values_49) > 5 and values_49[5]:
        try:
            Rotaion_Ribcage_GS = float(values_49[5])
        except ValueError:
            print(f"Invalid Rotaion_Ribcage value in row 49, column 6 for sheet ID {sheet_id}. Using default value 0.")
            Rotaion_Ribcage_GS = 0
    else:
        print(f"No Rotaion_Ribcage value found in row 49, column 6 for sheet ID {sheet_id}. Using default value 0.")
        Rotaion_Ribcage_GS = 0

    if len(values_49) > 7 and values_49[7]:
        try:
            Rotaion_Ribcage_Right = float(values_49[7])
        except ValueError:
            print(f"Invalid Rotaion_Ribcage value in row 49, column 8 for sheet ID {sheet_id}. Using default value 0.")
            Rotaion_Ribcage_Right = 0   
    else:
        print(f"No Rotaion_Ribcage value found in row 49, column 8 for sheet ID {sheet_id}. Using default value 0.")
        Rotaion_Ribcage_Right = 0

    

    # Now do for ribcage_flexion in row 51 similarly
    values_51 = worksheet_third.row_values(51)
    # get the numeric value from the fourth column of values list
    if len(values_51) > 3 and values_51[3]:
        try:
            Rotaion_Ribcage_Flexion_Left = float(values_51[3])
        except ValueError:
            print(f"Invalid Rotaion_Ribcage value in row 51, column 4 for sheet ID {sheet_id}. Using default value 0.")
            Rotaion_Ribcage_Flexion_Left = 0
    else:
        print(f"No Rotaion_Ribcage value found in row 51, column 4 for sheet ID {sheet_id}. Using default value 0.")
        Rotaion_Ribcage_Flexion_Left = 0
    if len(values_51) > 5 and values_51[5]:
        try:
            Rotaion_Ribcage_Flexion_GS = float(values_51[5])
        except ValueError:
            print(f"Invalid Rotaion_Ribcage value in row 51, column 6 for sheet ID {sheet_id}. Using default value 0.")
            Rotaion_Ribcage_Flexion_GS = 0
    else:
        print(f"No Rotaion_Ribcage value found in row 51, column 6 for sheet ID {sheet_id}. Using default value 0.")
        Rotaion_Ribcage_Flexion_GS = 0
    if len(values_51) > 7 and values_51[7]:
        try:
            Rotaion_Ribcage_Flexion_Right = float(values_51[7])
        except ValueError:
            print(f"Invalid Rotaion_Ribcage value in row 51, column 8 for sheet ID {sheet_id}. Using default value 0.")
            Rotaion_Ribcage_Flexion_Right = 0   
    else:
        print(f"No Rotaion_Ribcage value found in row 51, column 8 for sheet ID {sheet_id}. Using default value 0.")
        Rotaion_Ribcage_Flexion_Right = 0
    

    

    # categorize the lumbar curvature based on the values
    LC_Category = ""
    if LC < 15:
        LC_Category = "Significantly Decreased lumber curvature"
    elif 15 <= LC < 25:
        LC_Category = "Decreased lumber curvature"
    elif 25 <= LC < 30:
        LC_Category = "Slightly Decreased lumber curvature"
    elif 30 <= LC < 35:
        LC_Category = "Normal lumber curvature"
    elif 35 <= LC < 40:
        LC_Category = "Slightly Increased lumber curvature"
    elif 40 <= LC < 50:
        LC_Category = "Increased lumber curvature"
    elif LC >= 50:
        LC_Category = "Significantly Increased lumber curvature"


    # define forward head posture and sway back posture based and flat back posture on this information
    # If gender is Male and mean_pelvis is less than 7 and thoracic curvature is more than 35 degrees and lumbar curvature is greater than 35 degrees then it is sway back posture
    # If gender is Male and mean_pelvis is greater than 7 and thoracic curvature is more than 35 degrees then it is also sway back posture
    Posture1 = ""
    Posture2 = ""
    Posture3 = ""
    
    # Define Posture2 (Sway Back Posture) based on gender and pelvis tilt
    if Gender == 'Male':
        if Mean_pelvis <= 7 and TC > 35 and LC > 35:
            Posture2 = "Sway Back Posture"
        elif Mean_pelvis > 7 and TC > 35:
            Posture2 = "Sway Back Posture"
        else:
            Posture2 = ""
    elif Gender == 'Female':
        if Mean_pelvis <= 10 and TC > 35 and LC > 35:
            Posture2 = "Sway Back Posture"
        elif Mean_pelvis > 10 and TC > 35:
            Posture2 = "Sway Back Posture"
        else:
            Posture2 = ""

    # Define Posture1 (Forward Head Posture) based on gender and pelvis tilt thoracic curvature and lumbar curvature
    if Gender == 'Male':
        if 3 <= Mean_pelvis <= 7 and TC > 35 and LC < 30:
            Posture1 = "Forward Head Posture"
        else:
            Posture1 = ""
    elif Gender == 'Female':
        if 3 <= Mean_pelvis <= 10 and TC > 35 and LC < 30:
            Posture1 = "Forward Head Posture"
        else:
            Posture1 = ""

    # Define Posture3 (Flat Back Posture) based on thoracic and lumbar curvature
     
    if TC < 35 and LC < 30:
        Posture3 = "Flat Back Posture"
    else:
        Posture3 = ""



    return Gender,FHP, FHP_GS, DIFF_FHP, TC, TC_GS, DIFF_TC, LC, LC_GS, DIFF_LC, C7T1, T12L1, L5S1, Pelvis_GS, Pelvis_Left, Pelvis_Right, Mean_pelvis, Posture1, Posture2, Posture3,LC_Category,Rotaion_Ribcage_Left,Rotaion_Ribcage_GS,Rotaion_Ribcage_Right, Rotaion_Ribcage_Flexion_Left, Rotaion_Ribcage_Flexion_GS, Rotaion_Ribcage_Flexion_Right

Gender,FHP, FHP_GS, DIFF_FHP, TC, TC_GS, DIFF_TC, LC, LC_GS, DIFF_LC, C7T1, T12L1, L5S1, Pelvis_GS, Pelvis_Left, Pelvis_Right, Mean_pelvis, Posture1, Posture2, Posture3,LC_Category,Rotaion_Ribcage_Left,Rotaion_Ribcage_GS,Rotaion_Ribcage_Right, Rotaion_Ribcage_Flexion_Left, Rotaion_Ribcage_Flexion_GS, Rotaion_Ribcage_Flexion_Right = extract_sheet_metrics_posture(sheet_id)


# # Select only the initial few sheets for metric extraction
# NUM_SHEETS_TO_PROCESS = 4  # Change this value as needed
# sheet_ids = []
# with open('sheetid_fetch.txt', 'r') as f:
#     lines = f.readlines()
#     for line in lines[:NUM_SHEETS_TO_PROCESS]:
#         name, sheet_id = line.strip().split(' - ')
#         print(f"Sheet Name: {name}, Sheet ID: {sheet_id}")
#         sheet_ids.append(sheet_id)

# # Write the data to a CSV file
# import time

# # Extract metrics for each sheet
# iter = 0
# metrics = {}
# for sheet_id in sheet_ids:
#     iter += 1
#     print(iter, sheet_id)
#     metrics[sheet_id] = extract_sheet_metrics_posture(sheet_id)
#     if iter % 3 == 0:
#         print(f"Processed {iter} sheets...")
#         # wait for 1 minute to avoid rate limiting
#         time.sleep(60)

# # write the data in metrics to a csv file
# import csv
# with open('extracted_posture_metrics.csv', 'w', newline='') as csvfile:
#     fieldnames = ['Sheet ID', 'Gender', 'FHP', 'FHP_GS', 'DIFF_FHP', 'TC', 'TC_GS', 'DIFF_TC', 'LC', 'LC_GS', 'DIFF_LC', 'C7T1', 'T12L1', 'L5S1', 'Pelvis_GS', 'Pelvis_Left', 'Pelvis_Right', 'Mean_pelvis', 'Posture1', 'Posture2', 'Posture3', 'LC_Category', 'Rotaion_Ribcage_Left', 'Rotaion_Ribcage_GS', 'Rotaion_Ribcage_Right', 'Rotaion_Ribcage_Flexion_Left', 'Rotaion_Ribcage_Flexion_GS', 'Rotaion_Ribcage_Flexion_Right']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for sheet_id, data in metrics.items():
#         if data:
#             writer.writerow({'Sheet ID': sheet_id, 'Gender': data[0], 'FHP': data[1], 'FHP_GS': data[2], 'DIFF_FHP': data[3], 'TC': data[4], 'TC_GS': data[5], 'DIFF_TC': data[6], 'LC': data[7], 'LC_GS': data[8], 'DIFF_LC': data[9], 'C7T1': data[10], 'T12L1': data[11], 'L5S1': data[12], 'Pelvis_GS': data[13], 'Pelvis_Left': data[14], 'Pelvis_Right': data[15], 'Mean_pelvis': data[16], 'Posture1': data[17], 'Posture2': data[18], 'Posture3': data[19], 'LC_Category': data[20], 'Rotaion_Ribcage_Left': data[21], 'Rotaion_Ribcage_GS': data[22], 'Rotaion_Ribcage_Right': data[23], 'Rotaion_Ribcage_Flexion_Left': data[24], 'Rotaion_Ribcage_Flexion_GS': data[25], 'Rotaion_Ribcage_Flexion_Right': data[26]})
#         else:
#             writer.writerow({'Sheet ID': sheet_id})



