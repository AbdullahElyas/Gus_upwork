# creating a function which takes input the sheetid and outputs the thoracic curvature lumber curvature and pelvic tilt angles
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import re
from graphplot import create_radar_chart


def extract_sheet_metrics_posture(sheet_id, worksheet,worksheet_first,worksheet_third):
#     scopes = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]

    # creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    # client = gspread.authorize(creds)

    # # Open the Google Sheet
    # sheet = client.open_by_key(sheet_id)

    # # read the values from 7th row in the second sheet
    # worksheet = sheet.get_worksheet(1)
    values = worksheet.row_values(7)

    # get the numeric value from the sixth column of values list
    FHP = float(values[5]) if len(values) > 5 and values[5] else 0

    # read the values from 19th row in the second sheet
    values_19 = worksheet.row_values(19)

    # get the numeric value from the sixth column of values list
    TC = float(values_19[5]) if len(values_19) > 5 and values_19[5] else 0

    # read the values from 21th row in the second sheet 
    values_21 = worksheet.row_values(21)
    # get the numeric value from the sixth column of values list
    LC = float(values_21[5]) if len(values_21) > 5 and values_21[5] else 0

    # read the values from 9th row and 4th column in the second sheet
    values_9 = worksheet.row_values(9)
    if len(values_9) > 3 and values_9[3]:
        try:
            Pelvis = float(values_9[3])
        except ValueError:
            print(f"Invalid Pelvis value in row 9, column 4 for sheet ID {sheet_id}. Using default value 0.")
            Pelvis = 0
    else:
        print(f"No Pelvis value found in row 9, column 4 for sheet ID {sheet_id}. Using default value 0.")
        Pelvis = 0

    # read the values from 9th row 6th column and 8th column in the second sheet
    values_9 = worksheet.row_values(9)
    if len(values_9) > 5 and values_9[5]:
        try:
            Pelvis_Left = float(values_9[5])
        except ValueError:
            print(f"Invalid Pelvis value in row 9, column 6 for sheet ID {sheet_id}. Using default value 0.")
            Pelvis_Left = 0
    else:
        print(f"No Pelvis value found in row 9, column 6 for sheet ID {sheet_id}. Using default value 0.")
        Pelvis_Left = 0

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
    # worksheet_first = sheet.get_worksheet(0)
    values_first = worksheet_first.row_values(1)
    if len(values_first) > 2 and values_first[2]:
        Gender = values_first[2]
    else:
        print(f"No Gender value found in row 1, column 3 for sheet ID {sheet_id}. Using default value 'Unknown'.")
        Gender = 'Male'
    
    # Mean_pelvis should be lesser of Pelvis_Left and Pelvis_Right
    Mean_pelvis = min(Pelvis_Left, Pelvis_Right)
  
    # read row 49 from sheet 3 and get the numeric value from the 4th column 6th 8th and 10th column
    
    values_49 = worksheet_third.row_values(49)
    if len(values_49) > 3 and values_49[3]:
        try:
            Rotaion_Ribcage_Left = float(values_49[3])
        except ValueError:
            print(f"Invalid Rotaion_Ribcage value in row 49, column 4 for sheet ID {sheet_id}. Using default value 0.")
            Rotaion_Ribcage_Left = 0
    else:
        print(f"No Rotaion_Ribcage value found in row 49, column 4 for sheet ID {sheet_id}. Using default value 0.")
        Rotaion_Ribcage_Left = 0
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
    if len(values_51) > 3 and values_51[3]:
        try:
            Rotaion_Ribcage_Flexion_Left = float(values_51[3])
        except ValueError:
            print(f"Invalid Rotaion_Ribcage value in row 51, column 4 for sheet ID {sheet_id}. Using default value 0.")
            Rotaion_Ribcage_Flexion_Left = 0
    else:
        print(f"No Rotaion_Ribcage value found in row 51, column 4 for sheet ID {sheet_id}. Using default value 0.")
        Rotaion_Ribcage_Flexion_Left = 0
    if len(values_51) > 7 and values_51[7]:
        try:
            Rotaion_Ribcage_Flexion_Right = float(values_51[7])
        except ValueError:
            print(f"Invalid Rotaion_Ribcage value in row 51, column 8 for sheet ID {sheet_id}. Using default value 0.")
            Rotaion_Ribcage_Flexion_Right = 0   
    else:
        print(f"No Rotaion_Ribcage value found in row 51, column 8 for sheet ID {sheet_id}. Using default value 0.")
        Rotaion_Ribcage_Flexion_Right = 0


    posture_assessment_1 = ""

        # Define Posture2 (Sway Back Posture) based on gender and pelvis tilt
    if Gender == 'Male':
        if Mean_pelvis <= 7 and TC > 35 and LC > 35:
            posture_assessment_1 = "These readings indicate you have a Sway Back Posture"
        elif Mean_pelvis > 7 and TC > 35:
            posture_assessment_1 = "These readings indicate you have a Sway Back Posture"
        elif 2 <= Mean_pelvis <= 7 and TC > 35 and LC < 30:
            posture_assessment_1 = "These readings indicate you have a Forward Head Posture"
        elif TC <= 35 and LC <= 30:
            posture_assessment_1 = "These readings indicate you have a Flat Back Posture"
        elif TC > 35 and 30 <= LC < 35:
            posture_assessment_1 = "These readings indicate you have a kyphotic back posture"
        else:
            posture_assessment_1 = ""
    elif Gender == 'Female':
        if Mean_pelvis <= 10 and TC > 35 and LC > 35:
            posture_assessment_1 = "These readings indicate you have a Sway Back Posture"
        elif Mean_pelvis > 10 and TC > 35:
            posture_assessment_1 = "These readings indicate you have a Sway Back Posture"
        elif 2 <= Mean_pelvis <= 10 and TC > 35 and LC < 30:
            posture_assessment_1 = "These readings indicate you have a Forward Head Posture"
        elif TC <= 35 and LC <= 30:
            posture_assessment_1 = "These readings indicate you have a Flat Back Posture"
        else:
            posture_assessment_1 = ""


    posture_assessment_2 = ""
    if TC > 40 and LC < 30:    #  if TC > 40 kyphosis
        posture_assessment_2 = "kyphosis"
    elif TC < 30 and LC > 40:  # if LC > 40 lordosis
        posture_assessment_2 = "lordosis"
    elif TC > 40 and LC > 40:  
        posture_assessment_2 = "kyphosis and lordosis"




        # if FHP > 3:
    posture_assessment_3 = ""
    if 3 < FHP < 5:
        posture_assessment_3 = "So where your forward head posture is slightly increased"
    elif FHP >= 5:
        posture_assessment_3 = "So where your forward head posture is increased"
    elif FHP <= 3 and TC >35:
        posture_assessment_3 = "So where your thoracic curvature is increased"
    





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


#    Make a formatted input string for the prompt for report generation
    # Gender, FHP, TC, LC,posture_assessment_1, posture_assessment_2, posture_assessment_3, LC_Category
    Input_string = f"Gender: {Gender}, FHP: {FHP}, TC: {TC}, LC: {LC}, Posture Assessment 1: {posture_assessment_1}, Posture Assessment 2: {posture_assessment_2}, Posture Assessment 3: {posture_assessment_3}, LC Category: {LC_Category}"

    


    return Gender, FHP, TC, LC, Pelvis_Left, Pelvis_Right, Mean_pelvis, posture_assessment_1, posture_assessment_2, posture_assessment_3, LC_Category, Rotaion_Ribcage_Left, Rotaion_Ribcage_Right, Rotaion_Ribcage_Flexion_Left, Rotaion_Ribcage_Flexion_Right, Input_string
def TextGen_Posture(sheet_id, worksheet,first_worksheet,third_worksheet):
    # Extract metrics from the Google Sheet
    Gender,FHP, TC, LC, Pelvis_Left, Pelvis_Right, Mean_pelvis, Posture1, Posture2, Posture3,LC_Category,Rotaion_Ribcage_Left,Rotaion_Ribcage_Right, Rotaion_Ribcage_Flexion_Left,  Rotaion_Ribcage_Flexion_Right, Input_string = extract_sheet_metrics_posture(sheet_id,worksheet,first_worksheet,third_worksheet)
    # Template for TextGen Posture From the postural assessment we found some positive results as well as some areas we could concentrate on for improvement. Your forward head posture was measured at 1.1cm (normal is deemed 0-3cm). Your thoracic (upper back) curvature was above our gold standard range, you measured 45 degrees, normal is considered 30-35. We saw a reduced curvature in your lumbar spine, you measured 14 degrees with normal being considered 30-35.
    if Gender == 'Male' and Mean_pelvis < 4:
        text_pelvis = ', showing your posterior tilt and matches the findings of a reduced lumbar curvature as the lumbar spine directly articulates with the sacrum and its joints with the pelvis.'
    elif Gender == 'Female' and Mean_pelvis < 7:
        text_pelvis = ', showing your posterior tilt and matches the findings of a reduced lumbar curvature as the lumbar spine directly articulates with the sacrum and its joints with the pelvis.'
    else:
        text_pelvis = '.'

    if TC <= 32.5:
        tc_status = "below our gold standard range"
    elif 32.5 < TC:
        tc_status = "above our gold standard range"
  

    template1 = f"""From the postural assessment we found some positive results as well as some areas we could concentrate on for improvement.
Your forward head posture was measured at {FHP}cm (normal is deemed 0-3cm). Your thoracic (upper back) curvature was {tc_status}, you measured {TC} degrees, normal is considered 30-35. We saw {"a reduced curvature" if LC < 30 else "a neutral curvature" if 30 <= LC <= 35 else "an increased curvature"} in your lumbar spine, you measured {LC} degrees with normal being considered 30-35."""
    # You were able to rotate your spine 46 degrees to the left and 50 degrees to the right, and could laterally flex (side bend) 38 degrees to the left and 37 degrees to the right. 
    template2 = f"""You were able to rotate your spine {Rotaion_Ribcage_Left} degrees to the left and {Rotaion_Ribcage_Right} degrees to the right, and could laterally flex (side bend) {Rotaion_Ribcage_Flexion_Left} degrees to the left and {Rotaion_Ribcage_Flexion_Right} degrees to the right."""

    # The angle of pelvic tilt in quiet standing describes the orientation of the pelvis in the sagittal plane. It is determined by the muscular and ligamentous forces that act between the pelvis and adjacent segments. You were 6 (left) and 6 (right), normal is 7-10 degrees for females. The lumbar spine directly articulates with the sacrum and its joints with the pelvis. 
    template3 = f"""The angle of pelvic tilt in quiet standing describes the orientation of the pelvis in the sagittal plane. It is determined by the muscular and ligamentous forces that act between the pelvis and adjacent segments. You were {Pelvis_Left} (left) and {Pelvis_Right} (right), normal is {'4-7 degrees for males' if Gender == 'Male' else '7-10 degrees for females'}{text_pelvis} """

    return template1, template2, template3,Input_string
def extract_sheet_metrics_corefunction(sheet_id, worksheet,worksheet_first,worksheet_third):
    # Call the main extraction function
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

    # creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    # client = gspread.authorize(creds)

    # # Open the Google Sheet
    # sheet = client.open_by_key(sheet_id)

    # # Get the first worksheet
    # worksheet = sheet.get_worksheet(1)

    # Extract data from the worksheet
    data = worksheet.get_all_values()

    # Process the data as needed
    # For example, you might want to extract specific columns
    # and perform calculations or transformations
    # In data search for following string

    ffat_status = "Not found"
    stva_status = "Not found"
    ptva_status = "Not found"
    lact_status = "Not found"
    LAST_Strength = "Not found"
    ffat_note = ''
    stva_note = ''
    ptva_note = ''
    lact_note = ''
    LAST_note = ''
    JUAST_Strength = "Not found"
    JUAST_note = ''


    FFAT = 'Forward Flexion Activation Test'
    for row in data:
        if FFAT in row:
            index = data.index(row)
            if index < len(data):
                ffat_data = data[index]
                print("FFAT Data:", ffat_data)
                if len(ffat_data) > 8:
                    ffat_pass = ffat_data[3]
                    ffat_fail = ffat_data[8]
                    # get the ffat_note from 12th column
                    ffat_note = ffat_data[12] if len(ffat_data) > 12 else ''
                    print(f"FFAT Pass: {ffat_pass}, FFAT Fail: {ffat_fail}, FFAT Note: {ffat_note}")

                    # Convert string values to boolean logic
                    if ffat_pass == 'TRUE' and ffat_fail != 'TRUE':
                        ffat_status = "Pass"
                    elif ffat_fail == 'TRUE' and ffat_pass != 'TRUE':
                        ffat_status = "Fail"
                    elif ffat_pass == 'FALSE' and ffat_fail == 'FALSE':
                        ffat_status = "Undetermined"  # Both true - conflicting
                    else:
                        ffat_status = "Undetermined"  # Neither true or empty values
            break
    else:
        print("FFAT Data not found in the sheet.")

    STVA = 'Standing TVA Activation Test'
    for row in data:
        if STVA in row:
            index = data.index(row)
            if index < len(data):
                stva_data = data[index]
                print("STVA Data:", stva_data)
                if len(stva_data) > 8:
                    stva_pass = stva_data[3]
                    stva_fail = stva_data[8]
                    # get the stva_note from 12th column
                    stva_note = stva_data[12] if len(stva_data) > 12 else ''
                    print(f"STVA Pass: {stva_pass}, STVA Fail: {stva_fail}, STVA Note: {stva_note}")

                    # Convert string values to boolean logic
                    if stva_pass == 'TRUE' and stva_fail != 'TRUE':
                        stva_status = "Pass"
                    elif stva_fail == 'TRUE' and stva_pass != 'TRUE':
                        stva_status = "Fail"
                    elif stva_pass == 'FALSE' and stva_fail == 'FALSE':
                        stva_status = "Undetermined"
                    else:
                        stva_status = "Undetermined"
            break

    PTVA = 'Prone TVA Test'
    for row in data:
        if PTVA in row:
            index = data.index(row)
            if index < len(data):
                ptva_data = data[index]
                print("PTVA Data:", ptva_data)
                if len(ptva_data) > 8:
                    ptva_pass = ptva_data[3]
                    ptva_fail = ptva_data[8]
                    # get the ptva_note from 12th column
                    ptva_note = ptva_data[12] if len(ptva_data) > 12 else ''
                    print(f"PTVA Pass: {ptva_pass}, PTVA Fail: {ptva_fail}, PTVA Note: {ptva_note}")

                    # Convert string values to boolean logic
                    if ptva_pass == 'TRUE' and ptva_fail != 'TRUE':
                        ptva_status = "Pass"
                    elif ptva_fail == 'TRUE' and ptva_pass != 'TRUE':
                        ptva_status = "Fail"
                    elif ptva_pass == 'FALSE' and ptva_fail == 'FALSE':
                        ptva_status = "Undetermined"
                    else:
                        ptva_status = "Undetermined"
            break

    LACT = 'Lower Abdominal Coordination Test'
    for row in data:
        if LACT in row:
            index = data.index(row)
            if index < len(data):
                lact_data = data[index]
                print("LACT Data:", lact_data)
                if len(lact_data) > 8:
                    lact_pass = lact_data[3]
                    lact_fail = lact_data[8]
                    # get the lact_note from 12th column
                    lact_note = lact_data[12] if len(lact_data) > 12 else ''
                    print(f"LACT Pass: {lact_pass}, LACT Fail: {lact_fail}, LACT Note: {lact_note}")

                    # Convert string values to boolean logic
                    if lact_pass == 'TRUE' and lact_fail != 'TRUE':
                        lact_status = "Pass"
                    elif lact_fail == 'TRUE' and lact_pass != 'TRUE':
                        lact_status = "Fail"
                    elif lact_pass == 'FALSE' and lact_fail == 'FALSE':
                        lact_status = "Undetermined"
                    else:
                        lact_status = "Undetermined"
            break

        # now search for 'Lower Abdominal Strength Test' in the data ...in that row in 4th colum the values will be in format 0-100% or Please select store that value in LAST_Strength
    LAST = 'Lower Abdominal Strength Test'
    for row in data:
        if LAST in row:
            index = data.index(row)
            if index < len(data):
                last_data = data[index]
                print("LAST Data:", last_data)
                if len(last_data) > 3:
                    LAST_Strength = last_data[3]
                    print(f"LAST Strength: {LAST_Strength}")
                    LAST_note = last_data[12] if len(last_data) > 12 else ''
                    print(f"LAST Note: {LAST_note}")
            break

    # now search for 'Janda's Upper Abdominal Strength Test' in the data ...in that row in 4th colum the values will be in format 0-100% or Please select store that value in LAST_Strength
    JUAST = "Janda's Upper Abdominal Strength Test"
    for row in data:
        if JUAST in row:
            index = data.index(row)
            if index < len(data):
                juast_data = data[index]
                print("JUAST Data:", juast_data)
                if len(juast_data) > 3:
                    JUAST_Strength = juast_data[3]
                    print(f"JUAST Strength: {JUAST_Strength}")
                    JUAST_note = juast_data[12] if len(juast_data) > 12 else ''
                    print(f"JUAST Note: {JUAST_note}")
            break

    # # now search the worksheet with the name 'Report' or 'New Datavis' 
    # report_worksheet = None
    # try:
    #     report_worksheet = sheet.worksheet('Report')
    # except gspread.WorksheetNotFound:
    #     try:
    #         report_worksheet = sheet.worksheet('NEW Datavis')
    #     except gspread.WorksheetNotFound:
    #         print("Neither 'Report' nor 'New Datavis' worksheet found.")
    # if report_worksheet:
    #     # search each row 2nd column of report_worksheet whose first word is 'LENGTH TENSION' and then store the whole cell string
    #     # If no such row is found, print a message and return None
    #     length_tension_row = None
    #     for row in report_worksheet.get_all_values():
            
    #         if row[1].startswith('LENGTH TENSION'):
    #             length_tension_row = row
    #             # Now search for string 'ASSESSMENT OF THE CORE FUNCTION:'  if found then store text coming after it
    #             if len(row) > 2 and 'ASSESSMENT OF THE CORE FUNCTION:' in row[1]:
    #                 core_function_assessment = row[1].split('ASSESSMENT OF THE CORE FUNCTION:')[1].strip()
    #                 # print(f"Core Function Assessment: {core_function_assessment}")

    #             break
    #     if length_tension_row is None:
    #         print(f"No 'LENGTH TENSION' row found in 'Report' or 'NEW Datavis' worksheet for sheet ID {sheet_id}.")
    # Lower Abdominal Strength Test string possible options "Please select", "0-100%"
    if LAST_Strength == "Please select":
        LAST_Strength_result = ""
    elif LAST_Strength == "100%":
        LAST_Strength_result = "Lower Core could brace well"
    elif LAST_Strength == "90%":
        LAST_Strength_result = "Lower Core could brace sufficiently"
    elif LAST_Strength == "80%":
        LAST_Strength_result = "Lower Core could brace moderately"
    elif LAST_Strength == "70%":
        LAST_Strength_result = "Lower core could not brace efficiently"
    elif LAST_Strength == "60%":
        LAST_Strength_result = "Lower core could not brace well"
    else:
        LAST_Strength_result = ""

    # Janda's Upper Abdominal Strength Test string possible options "Please select", "0-100%"
    if JUAST_Strength == "Please select":
        JUAST_Strength_result = ""
    elif JUAST_Strength == "Fail":
        JUAST_Strength_result = "Upper Core could not brace well"
    elif JUAST_Strength == "100% (mastoid process)":
        JUAST_Strength_result = "Upper Core could brace sufficiently"
    elif JUAST_Strength == "80% (across chest)":
        JUAST_Strength_result = "Upper Core could brace moderately"
    elif JUAST_Strength == "60% (arms out)":
        JUAST_Strength_result = "Upper core could not brace well"
    else:
        JUAST_Strength_result = ""

    # Lower Abdominal Coordination Test
    if lact_status == "Pass":
        lact_result = "Lower Abdominal Coordination Test was a pass"
    elif lact_status == "Fail":
        lact_result = "Lower Abdominal Coordination Test was a fail"
    else:
        lact_result = ""

    # Get only LC using function extract_sheet_metrics_posture
    _, _, _, LC, _, _, _, _, _, _, _, _, _, _, _, _ = extract_sheet_metrics_posture(sheet_id, worksheet,worksheet_first,worksheet_third)

    # categorize the lumbar curvature based on the values
    LC_Category = ""
    if LC < 15 and LAST_Strength_result != "Lower Core could brace well":
        LC_Category = "Significantly Decreased lumber curvature  which is likely contributing to the reduced lower abdominal strength"
    elif 15 <= LC < 25 and LAST_Strength_result != "Lower Core could brace well":
        LC_Category = "Decreased lumber curvature  which is likely contributing to the reduced lower abdominal strength"
    elif 25 <= LC < 30 and LAST_Strength_result != "Lower Core could brace well":
        LC_Category = "Slightly Decreased lumber curvature  which is likely contributing to the reduced lower abdominal strength"
    elif 30 <= LC < 35 and LAST_Strength_result != "Lower Core could brace well":
        LC_Category = ""
    elif 35 <= LC < 40 and LAST_Strength_result != "Lower Core could brace well":
        LC_Category = "Slightly Increased lumber curvature  which is likely contributing to the reduced lower abdominal strength"
    elif 40 <= LC < 50 and LAST_Strength_result != "Lower Core could brace well":
        LC_Category = "Increased lumber curvature  which is likely contributing to the reduced lower abdominal strength"
    elif LC >= 50 and LAST_Strength_result != "Lower Core could brace well":
        LC_Category = "Significantly Increased lumber curvature  which is likely contributing to the reduced lower abdominal strength"


    # # append the LC_Category , lact_result, JUAST_Strength_result, LAST_Strength_result in string_core_function
    # if lact_status != "Pass" and LAST_Strength_result != "Lower Core could brace well" and JUAST_Strength_result != "Upper Core could brace well":
    #     string_core_function = f"{LC_Category}, {lact_result} ({lact_note}), {JUAST_Strength_result} ({JUAST_note}), {LAST_Strength_result} ({LAST_note}) "
    # else:
    #     string_core_function = ""
    string_core_function = f"{LC_Category}, {lact_result} ({lact_note}), {JUAST_Strength_result} ({JUAST_note}), {LAST_Strength_result} ({LAST_note}) "
    


    return ffat_status, stva_status, ptva_status, lact_status, LAST_Strength, JUAST_Strength, ffat_note, stva_note, ptva_note, lact_note, LAST_note, JUAST_note, string_core_function

def extract_sheet_metrics_footankle(sheet_id, data_overview_sheet, second_worksheet):
    # # Call the main extraction function
    # scopes = [
    #     'https://www.googleapis.com/auth/spreadsheets',
    #     'https://www.googleapis.com/auth/drive'
    # ]

    # creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    # client = gspread.authorize(creds)

    # # Open the Google Sheet
    # sheet = client.open_by_key(sheet_id)
    # # search sheet with the name 'Data Overview'
    # data_overview_sheet = sheet.worksheet("Data Overview")
    # Extract data from the worksheet
    all_values = data_overview_sheet.get_all_values()
    # search row containing "Dorsiflexion Range"
    dorsiflexion_row = next((i for i, row in enumerate(all_values) if "Dorsiflexion Range" in row), None)
    dorsiflexion_range_left = dorsiflexion_range_right = None
    plantarflexion_range_left = plantarflexion_range_right = None

    if dorsiflexion_row is not None:
        # Extract Dorsiflexion Range values
        dorsiflexion_values = all_values[dorsiflexion_row]
        print("Dorsiflexion Range values:", dorsiflexion_values)
        dorsiflexion_range_left = dorsiflexion_values[3] if len(dorsiflexion_values) > 4 else None
        dorsiflexion_range_right = dorsiflexion_values[4] if len(dorsiflexion_values) > 5 else None
    else:
        print("Dorsiflexion Range not found.")

    # Search for Plantarflexion Range
    plantarflexion_row = next((i for i, row in enumerate(all_values) if "Plantarflexion Range" in row), None)

    if plantarflexion_row is not None:
        plantarflexion_values = all_values[plantarflexion_row]
        print("Plantarflexion Range values:", plantarflexion_values)
        plantarflexion_range_left = plantarflexion_values[3] if len(plantarflexion_values) > 4 else None
        plantarflexion_range_right = plantarflexion_values[4] if len(plantarflexion_values) > 5 else None
    else:
        print("Plantarflexion Range not found.")

    # now do for "Dorsiflexion Force" and "Plantarflexion Force"
    # Search for Dorsiflexion Force
    dorsiflexion_force_row = next((i for i, row in enumerate(all_values) if "Dorsiflexion Force" in row), None)
    dorsiflexion_force_left = dorsiflexion_force_right = None

    if dorsiflexion_force_row is not None:
        dorsiflexion_force_values = all_values[dorsiflexion_force_row]
        print("Dorsiflexion Force values:", dorsiflexion_force_values)
        dorsiflexion_force_left = dorsiflexion_force_values[3] if len(dorsiflexion_force_values) > 4 else None
        dorsiflexion_force_right = dorsiflexion_force_values[4] if len(dorsiflexion_force_values) > 5 else None
    else:
        print("Dorsiflexion Force not found.")

    # Search for Plantarflexion Force
    plantarflexion_force_row = next((i for i, row in enumerate(all_values) if "Plantarflexion Force" in row), None)
    plantarflexion_force_left = plantarflexion_force_right = None

    if plantarflexion_force_row is not None:
        plantarflexion_force_values = all_values[plantarflexion_force_row]
        print("Plantarflexion Force values:", plantarflexion_force_values)
        plantarflexion_force_left = plantarflexion_force_values[3] if len(plantarflexion_force_values) > 4 else None
        plantarflexion_force_right = plantarflexion_force_values[4] if len(plantarflexion_force_values) > 5 else None
    else:
        print("Plantarflexion Force not found.")

    # # Now get the second worksheet
    # second_worksheet = sheet.get_worksheet(1)
    second_values = second_worksheet.get_all_values()

    # Foot and Ankle Assessment Questions
    weight_distribution_question = "Where do you feel weight when standing?"
    supination_tripod_question = "Able to supinate with tripod while rotating?"
    pronation_tripod_question = "Able to pronate with tripod while rotating?"
    big_toe_independence_question = "Can they move big toe independently?"
    lesser_toes_independence_question = "Can they move 2nd-5th toes independently?"
    center_of_mass_rest_question = "Centre of Mass at rest?"
    center_of_mass_pronated_question = "Centre of Mass in pronated leg?"

    # search the above strings one by one and store the 4th and 5th values of the corresponding rows
    weight_distribution_values = next((row for row in second_values if weight_distribution_question in row), None)
    supination_tripod_values = next((row for row in second_values if supination_tripod_question in row), None)
    pronation_tripod_values = next((row for row in second_values if pronation_tripod_question in row), None)
    big_toe_independence_values = next((row for row in second_values if big_toe_independence_question in row), None)
    lesser_toes_independence_values = next((row for row in second_values if lesser_toes_independence_question in row), None)
    center_of_mass_rest_values = next((row for row in second_values if center_of_mass_rest_question in row), None)
    center_of_mass_pronated_values = next((row for row in second_values if center_of_mass_pronated_question in row), None)

    # store the 4th , 9th and 13th values
    weight_distribution_question_left =  weight_distribution_values[3] if weight_distribution_values and len(weight_distribution_values) > 4 else None
    weight_distribution_question_right = weight_distribution_values[8] if weight_distribution_values and len(weight_distribution_values) > 8 else None
    weight_distribution_question_note = weight_distribution_values[12] if weight_distribution_values and len(weight_distribution_values) > 12 else None

    supination_tripod_question_left = supination_tripod_values[3] if supination_tripod_values and len(supination_tripod_values) > 4 else None
    supination_tripod_question_right = supination_tripod_values[8] if supination_tripod_values and len(supination_tripod_values) > 8 else None
    supination_tripod_question_note = supination_tripod_values[12] if supination_tripod_values and len(supination_tripod_values) > 12 else None

    pronation_tripod_question_left = pronation_tripod_values[3] if pronation_tripod_values and len(pronation_tripod_values) > 4 else None
    pronation_tripod_question_right = pronation_tripod_values[8] if pronation_tripod_values and len(pronation_tripod_values) > 8 else None
    pronation_tripod_question_note = pronation_tripod_values[12] if pronation_tripod_values and len(pronation_tripod_values) > 12 else None

    big_toe_independence_question_left = big_toe_independence_values[3] if big_toe_independence_values and len(big_toe_independence_values) > 4 else None
    big_toe_independence_question_right = big_toe_independence_values[8] if big_toe_independence_values and len(big_toe_independence_values) > 8 else None
    big_toe_independence_question_note = big_toe_independence_values[12] if big_toe_independence_values and len(big_toe_independence_values) > 12 else None

    lesser_toes_independence_question_left = lesser_toes_independence_values[3] if lesser_toes_independence_values and len(lesser_toes_independence_values) > 4 else None
    lesser_toes_independence_question_right = lesser_toes_independence_values[8] if lesser_toes_independence_values and len(lesser_toes_independence_values) > 8 else None
    lesser_toes_independence_question_note = lesser_toes_independence_values[12] if lesser_toes_independence_values and len(lesser_toes_independence_values) > 12 else None

    center_of_mass_rest_left = center_of_mass_rest_values[3] if center_of_mass_rest_values and len(center_of_mass_rest_values) > 4 else None
    center_of_mass_rest_right = center_of_mass_rest_values[8] if center_of_mass_rest_values and len(center_of_mass_rest_values) > 8 else None
    center_of_mass_rest_note = center_of_mass_rest_values[12] if center_of_mass_rest_values and len(center_of_mass_rest_values) > 12 else None

    center_of_mass_pronated_left = center_of_mass_pronated_values[3] if center_of_mass_pronated_values and len(center_of_mass_pronated_values) > 4 else None
    center_of_mass_pronated_right = center_of_mass_pronated_values[8] if center_of_mass_pronated_values and len(center_of_mass_pronated_values) > 8 else None
    center_of_mass_pronated_note = center_of_mass_pronated_values[12] if center_of_mass_pronated_values and len(center_of_mass_pronated_values) > 12 else None
    



    return (
        dorsiflexion_range_left,
        dorsiflexion_range_right,
        plantarflexion_range_left,
        plantarflexion_range_right,
        dorsiflexion_force_left,
        dorsiflexion_force_right,
        plantarflexion_force_left,
        plantarflexion_force_right,
        weight_distribution_question_left,
        weight_distribution_question_right,
        weight_distribution_question_note,
        supination_tripod_question_left,
        supination_tripod_question_right,
        supination_tripod_question_note,
        pronation_tripod_question_left,
        pronation_tripod_question_right,
        pronation_tripod_question_note,
        big_toe_independence_question_left,
        big_toe_independence_question_right,
        big_toe_independence_question_note,
        lesser_toes_independence_question_left,
        lesser_toes_independence_question_right,
        lesser_toes_independence_question_note,
        center_of_mass_rest_left,
        center_of_mass_rest_right,
        center_of_mass_rest_note,
        center_of_mass_pronated_left,
        center_of_mass_pronated_right,
        center_of_mass_pronated_note
    )


def TextGen_FootAnkle(sheet_id, data_overview_sheet, second_worksheet):

    # Evaluate the function
    (
        dorsiflexion_range_left,
        dorsiflexion_range_right,
        plantarflexion_range_left,
        plantarflexion_range_right,
        dorsiflexion_force_left,
        dorsiflexion_force_right,
        plantarflexion_force_left,
        plantarflexion_force_right,
        weight_distribution_question_left,
        weight_distribution_question_right,
        weight_distribution_question_note,
        supination_tripod_question_left,
        supination_tripod_question_right,
        supination_tripod_question_note,
        pronation_tripod_question_left,
        pronation_tripod_question_right,
        pronation_tripod_question_note,
        big_toe_independence_question_left,
        big_toe_independence_question_right,
        big_toe_independence_question_note,
        lesser_toes_independence_question_left,
        lesser_toes_independence_question_right,
        lesser_toes_independence_question_note,
        center_of_mass_rest_left,
        center_of_mass_rest_right,
        center_of_mass_rest_note,
        center_of_mass_pronated_left,
        center_of_mass_pronated_right,
        center_of_mass_pronated_note
    ) = extract_sheet_metrics_footankle(sheet_id, data_overview_sheet, second_worksheet)

    # center_of_mass_rest_left and center_of_mass_rest_right can have values -2 Metatarsal -1 Metatarsal 1st Metatarsal  2nd Metatarsal  3rd Metatarsal 4th Metatarsal  5th Metatarsal
    
    # center_of_mass_pronated_right and center_of_mass_pronated_note can have similar values

    # Assess foot position based on center_of_mass_rest_left and center_of_mass_rest_right
    def metatarsal_to_int(metatarsal):
        mapping = {
            "-2 Metatarsal": -2,
            "-1 Metatarsal": -1,
            "1st Metatarsal": 1,
            "2nd Metatarsal": 2,
            "3rd Metatarsal": 3,
            "4th Metatarsal": 4,
            "5th Metatarsal": 5
        }
        if metatarsal is None:
            return None
        metatarsal = str(metatarsal).strip()
        return mapping.get(metatarsal, None)

    def assess_foot_position(metatarsal_rest, metatarsal_pronated):
        val_rest = metatarsal_to_int(metatarsal_rest)
        val_pronated = metatarsal_to_int(metatarsal_pronated)

        if val_rest is None and val_pronated is None:
            return "Unknown", "Unknown"
        
        # Determine foot position
        if val_rest == 2:
            position = "neutral position"
        elif val_rest == 1:
            position = "slightly everted position"
        elif val_rest in [-1, -2]:
            position = "everted position"
        elif val_rest == 3:
            position = "slightly inverted position"
        elif val_rest in [4, 5]:
            position = "inverted position"
        else:
            position = "Unknown"

        # Determine pronation ability
        if val_rest is not None and val_pronated is not None:
            if val_pronated < val_rest:
                pronation = "foot can pronate"
            else:
                pronation = "foot cannot pronate"
        else:
            pronation = ""

        return position, pronation

    left_foot_position,left_pronation = assess_foot_position(center_of_mass_rest_left, center_of_mass_pronated_left)
    right_foot_position,right_pronation = assess_foot_position(center_of_mass_rest_right,center_of_mass_pronated_right)




    # Generate text based on the extracted values
    left_foot_text = f"Left Foot Position: {left_foot_position}"
    if center_of_mass_rest_note:
        left_foot_text += f"  ,{center_of_mass_rest_note}"
    left_foot_text += f", Pronation: {left_pronation}"
    if center_of_mass_pronated_note:
        left_foot_text += f", {center_of_mass_pronated_note}"

    right_foot_text = f"Right Foot Position: {right_foot_position}"
    if center_of_mass_rest_note:
        right_foot_text += f"  ,{center_of_mass_rest_note}"
    right_foot_text += f", Pronation: {right_pronation}"
    if center_of_mass_pronated_note:
        right_foot_text += f", {center_of_mass_pronated_note}"


    # Helper function to check if a value is 'yes' or 'no' and return 'can' or 'can not'
    def check_can_cannot(val):
        if val is None:
            return "Unknown"
        val_str = str(val).strip().lower()
        if val_str == "yes":
            return "can"
        elif val_str == "no":
            return "can not"
        else:
            return "Unknown"

    def get_tripod_pronation_supination_status():
        left_sup = f"{check_can_cannot(supination_tripod_question_left)} supinate"
        if supination_tripod_question_note:
            left_sup += f" ,{supination_tripod_question_note}"
        left_pro = f"{check_can_cannot(pronation_tripod_question_left)} pronate"
        if pronation_tripod_question_note:
            left_pro += f" ,{pronation_tripod_question_note}"

        right_sup = f"{check_can_cannot(supination_tripod_question_right)} supinate"
        if supination_tripod_question_note:
            right_sup += f" ,{supination_tripod_question_note}"
        right_pro = f"{check_can_cannot(pronation_tripod_question_right)} pronate"
        if pronation_tripod_question_note:
            right_pro += f" ,{pronation_tripod_question_note}"

        left_result_ps = {
            "pronation": left_pro,
            "supination": left_sup,
        }
        right_result_ps = {
            "pronation": right_pro,
            "supination": right_sup,
        }
        return left_result_ps, right_result_ps

    left_tripod_status, right_tripod_status = get_tripod_pronation_supination_status()

    # Generate text based on the extracted values
    left_tripod_text = f"Left : {left_tripod_status}"
    right_tripod_text = f"Right : {right_tripod_status}"


    def assess_asymmetry(left,right):
        asymmetry = ""
        try:
            left_num = float(left)
            right_num = float(right)
            # evaluate difference and calculate percentage diffence with left
            if left_num is not None and right_num is not None:
                difference = right_num - left_num
                percentage_difference = (difference / left_num * 100) if left_num != 0 else 0
                # if magnitude of percentage difference is greater than 15% then there is asymmetry
                if abs(percentage_difference) > 15:
                    asymmetry = "Asymmetry is there"
                else:
                    asymmetry = "No asymmetry is there"
                # return
                return asymmetry

            else:
                return asymmetry
        except (TypeError, ValueError):
            return None
        

    # evaluate asymmetry for         dorsiflexion_force_left, dorsiflexion_force_right
    dorsiflexion_asymmetry_force = assess_asymmetry(dorsiflexion_force_left, dorsiflexion_force_right)
    plantarflexion_asymmetry_force = assess_asymmetry(plantarflexion_force_left, plantarflexion_force_right)
    dorsiflexion_asymmetry_range = assess_asymmetry(dorsiflexion_range_left, dorsiflexion_range_right)
    plantarflexion_asymmetry_range = assess_asymmetry(plantarflexion_range_left, plantarflexion_range_right)

    # if any asymmetry is detected in force or range, flag it
    asymmetry_foot= "Symmetry is there."
    if (dorsiflexion_asymmetry_force or plantarflexion_asymmetry_force or
            dorsiflexion_asymmetry_range or plantarflexion_asymmetry_range):
        asymmetry_foot = "Asymmetry is there."
    else:
        asymmetry_foot = "Symmetry is there."

        #     dorsiflexion_range_left,
        # dorsiflexion_range_right,
        # plantarflexion_range_left,
        # plantarflexion_range_right,
        # the variables above have range from 0 to 100
        # make a function to assess the range
    def assess_range_force(range_val, force_val):
        try:
            range_num = float(range_val)
        except (TypeError, ValueError):
            range_num = None
        try:
            force_num = float(force_val)
        except (TypeError, ValueError):
            force_num = None

        if range_num is not None and range_num < 75:
            range_status = "Poor"
        elif range_num is not None:
            range_status = "Good"
        else:
            range_status = "Unknown"

        if force_num is not None and force_num < 75:
            force_status = "Poor"
        elif force_num is not None:
            force_status = "Good"
        else:
            force_status = "Unknown"

        return range_status, force_status

    def summarize_range_force(range_status, force_status):
        if range_status == "Poor" and force_status == "Good":
            return "poor range but good strength"
        elif range_status == "Good" and force_status == "Poor":
            return "good range but poor strength"
        elif range_status == "Poor" and force_status == "Poor":
            return "range and strength are both poor"
        elif range_status == "Good" and force_status == "Good":
            return "range and strength are both good"
        else:
            return ""

    left_dorsiflexion_range_status, left_dorsiflexion_force_status = assess_range_force(dorsiflexion_range_left, dorsiflexion_force_left)
    left_plantarflexion_range_status, left_plantarflexion_force_status = assess_range_force(plantarflexion_range_left, plantarflexion_force_left)

    right_dorsiflexion_range_status, right_dorsiflexion_force_status = assess_range_force(dorsiflexion_range_right, dorsiflexion_force_right)
    right_plantarflexion_range_status, right_plantarflexion_force_status = assess_range_force(plantarflexion_range_right, plantarflexion_force_right)

    # Example usage:
    left_dorsiflexion_summary = summarize_range_force(left_dorsiflexion_range_status, left_dorsiflexion_force_status)
    left_plantarflexion_summary = summarize_range_force(left_plantarflexion_range_status, left_plantarflexion_force_status)
    right_dorsiflexion_summary = summarize_range_force(right_dorsiflexion_range_status, right_dorsiflexion_force_status)
    right_plantarflexion_summary = summarize_range_force(right_plantarflexion_range_status, right_plantarflexion_force_status)

    # Concatenate the summaries for left and right foot
    left_summary = (
        f"Left Foot: Dorsiflexion - {left_dorsiflexion_summary}; Plantarflexion - {left_plantarflexion_summary}. "
        "We would like to prioritize building strength primarily through overcoming isometrics. "
        "You also need to start building some more control and awareness."
    )
    right_summary = f"Right Foot: Dorsiflexion - {right_dorsiflexion_summary}; Plantarflexion - {right_plantarflexion_summary}"

    print(left_summary)
    print(right_summary)

    # append left_foot_text,left_tripod_text and left_summary to left_final_text
    # append right_foot_text,right_tripod_text and right_summary to right_final_text
    left_foot_text += f", {left_tripod_text}, {left_summary}"
    right_foot_text += f", {right_tripod_text}, {right_summary}"

    def extract_foot_report_text(sheet_id):
            # Call the main extraction function
        scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)

            # Open the Google Sheet
        sheet = client.open_by_key(sheet_id)
             # now search the worksheet with the name 'Report' or 'New Datavis'
        report_worksheet = None
        try:
            report_worksheet = sheet.worksheet('Report')
        except gspread.WorksheetNotFound:
            try:
                report_worksheet = sheet.worksheet('NEW Datavis')
            except gspread.WorksheetNotFound:
                print("Neither 'Report' nor 'New Datavis' worksheet found.")
        foot_ankle_assessment = None
        if report_worksheet:
            # search each row 2nd column of report_worksheet whose first word is 'LENGTH TENSION' and then store the whole cell string
            # If no such row is found, print a message and return None
            length_tension_row = None
            for row in report_worksheet.get_all_values():
                if row[5].startswith('ASSESSMENT OF THE FOOT AND ANKLE COMPLEX:'):
                    length_tension_row = row
                    # Now search for string 'ASSESSMENT OF THE FOOT AND ANKLE COMPLEX:' if found then store text coming after it
                    if len(row) > 2 and 'ASSESSMENT OF THE FOOT AND ANKLE COMPLEX:' in row[5]:
                        foot_ankle_assessment = row[5].split('ASSESSMENT OF THE FOOT AND ANKLE COMPLEX:')[1].strip()
                    break
            if length_tension_row is None:
                print(f"No 'ASSESSMENT OF THE FOOT AND ANKLE COMPLEX:' row found in 'Report' or 'NEW Datavis' worksheet for sheet ID {sheet_id}.")
        return foot_ankle_assessment
    
    foot_ankle_assessment = extract_foot_report_text(sheet_id)


    return left_foot_text, right_foot_text, foot_ankle_assessment, asymmetry_foot


def extract_sheet_metrics_hip(sheet_id, data_overview_sheet):
    # Call the main extraction function
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    # client = gspread.authorize(creds)

    # # Open the Google Sheet
    # sheet = client.open_by_key(sheet_id)
    # # search sheet with the name 'Data Overview'
    # data_overview_sheet = sheet.worksheet("Data Overview")
    # Extract data from the worksheet
    all_values = data_overview_sheet.get_all_values()

    # search for strings in row "HIP" "LEFT" "RIGHT" and "GS" if all these strings are present in row array then store its index
    hip_index = None
    left_index = None
    right_index = None
    gs_index = None
    
    for i, row in enumerate(all_values):
        if "HIP" in row:
            hip_index = i
        if "LEFT" in row:
            left_index = i
        if "RIGHT" in row:
            right_index = i
        if "GS" in row:
            gs_index = i
        if hip_index is not None and left_index is not None and right_index is not None and gs_index is not None:
            print(f"Found indices - HIP: {hip_index}, LEFT: {left_index}, RIGHT: {right_index}, GS: {gs_index}")
            
            break
        else:
            hip_index = None
            left_index = None
            right_index = None
            gs_index = None
    else:
        print("No row found containing all of HIP, LEFT, RIGHT, and GS")
    
        # Initialize hip measurement variables as strings
    hip_flexion_range_left = hip_flexion_range_right = None
    hip_extension_range_left = hip_extension_range_right = None
    hip_abduction_range_left = hip_abduction_range_right = None
    hip_adduction_range_left = hip_adduction_range_right = None
    hip_ext_rotation_range_left = hip_ext_rotation_range_right = None
    hip_int_rotation_range_left = hip_int_rotation_range_right = None
    
    hip_flexion_force_left = hip_flexion_force_right = None
    hip_extension_force_left = hip_extension_force_right = None
    hip_abduction_force_left = hip_abduction_force_right = None
    hip_adduction_force_left = hip_adduction_force_right = None
    hip_ext_rotation_force_left = hip_ext_rotation_force_right = None
    hip_int_rotation_force_left = hip_int_rotation_force_right = None

    # Only search from hip_index onwards
    search_rows = all_values[hip_index:] if hip_index is not None else all_values

    # Search for Hip Flexion Range
    flexion_range_row = next((i for i, row in enumerate(search_rows) if "Flexion Range" in row), None)
    if flexion_range_row is not None:
        flexion_range_values = search_rows[flexion_range_row]
        print("Hip Flexion Range values:", flexion_range_values)
        hip_flexion_range_left = flexion_range_values[3] if len(flexion_range_values) > 3 else None
        hip_flexion_range_right = flexion_range_values[4] if len(flexion_range_values) > 4 else None
    else:
        print("Hip Flexion Range not found.")

    # Search for Hip Extension Range
    extension_range_row = next((i for i, row in enumerate(search_rows) if "Extension Range" in row), None)
    if extension_range_row is not None:
        extension_range_values = search_rows[extension_range_row]
        print("Hip Extension Range values:", extension_range_values)
        hip_extension_range_left = extension_range_values[3] if len(extension_range_values) > 3 else None
        hip_extension_range_right = extension_range_values[4] if len(extension_range_values) > 4 else None
    else:
        print("Hip Extension Range not found.")

    # Search for Hip Abduction Range
    abduction_range_row = next((i for i, row in enumerate(search_rows) if "Abduction Range" in row), None)
    if abduction_range_row is not None:
        abduction_range_values = search_rows[abduction_range_row]
        print("Hip Abduction Range values:", abduction_range_values)
        hip_abduction_range_left = abduction_range_values[3] if len(abduction_range_values) > 3 else None
        hip_abduction_range_right = abduction_range_values[4] if len(abduction_range_values) > 4 else None
    else:
        print("Hip Abduction Range not found.")

    # Search for Hip Adduction Range
    adduction_range_row = next((i for i, row in enumerate(search_rows) if "Adduction Range" in row), None)
    if adduction_range_row is not None:
        adduction_range_values = search_rows[adduction_range_row]
        print("Hip Adduction Range values:", adduction_range_values)
        hip_adduction_range_left = adduction_range_values[3] if len(adduction_range_values) > 3 else None
        hip_adduction_range_right = adduction_range_values[4] if len(adduction_range_values) > 4 else None
    else:
        print("Hip Adduction Range not found.")

    # Search for Hip External Rotation Range
    ext_rotation_range_row = next((i for i, row in enumerate(search_rows) if "EXT Rotation Range" in row), None)
    if ext_rotation_range_row is not None:
        ext_rotation_range_values = search_rows[ext_rotation_range_row]
        print("Hip EXT Rotation Range values:", ext_rotation_range_values)
        hip_ext_rotation_range_left = ext_rotation_range_values[3] if len(ext_rotation_range_values) > 3 else None
        hip_ext_rotation_range_right = ext_rotation_range_values[4] if len(ext_rotation_range_values) > 4 else None
    else:
        print("Hip EXT Rotation Range not found.")

    # Search for Hip Internal Rotation Range
    int_rotation_range_row = next((i for i, row in enumerate(search_rows) if "INT Rotation Range" in row), None)
    if int_rotation_range_row is not None:
        int_rotation_range_values = search_rows[int_rotation_range_row]
        print("Hip INT Rotation Range values:", int_rotation_range_values)
        hip_int_rotation_range_left = int_rotation_range_values[3] if len(int_rotation_range_values) > 3 else None
        hip_int_rotation_range_right = int_rotation_range_values[4] if len(int_rotation_range_values) > 4 else None
    else:
        print("Hip INT Rotation Range not found.")

    # Search for Hip Flexion Force
    flexion_force_row = next((i for i, row in enumerate(search_rows) if "Flexion Force" in row), None)
    if flexion_force_row is not None:
        flexion_force_values = search_rows[flexion_force_row]
        print("Hip Flexion Force values:", flexion_force_values)
        hip_flexion_force_left = flexion_force_values[3] if len(flexion_force_values) > 3 else None
        hip_flexion_force_right = flexion_force_values[4] if len(flexion_force_values) > 4 else None
    else:
        print("Hip Flexion Force not found.")

    # Search for Hip Extension Force
    extension_force_row = next((i for i, row in enumerate(search_rows) if "Extension Force" in row), None)
    if extension_force_row is not None:
        extension_force_values = search_rows[extension_force_row]
        print("Hip Extension Force values:", extension_force_values)
        hip_extension_force_left = extension_force_values[3] if len(extension_force_values) > 3 else None
        hip_extension_force_right = extension_force_values[4] if len(extension_force_values) > 4 else None
    else:
        print("Hip Extension Force not found.")

    # Search for Hip Abduction Force
    abduction_force_row = next((i for i, row in enumerate(search_rows) if "Abduction Force" in row), None)
    if abduction_force_row is not None:
        abduction_force_values = search_rows[abduction_force_row]
        print("Hip Abduction Force values:", abduction_force_values)
        hip_abduction_force_left = abduction_force_values[3] if len(abduction_force_values) > 3 else None
        hip_abduction_force_right = abduction_force_values[4] if len(abduction_force_values) > 4 else None
    else:
        print("Hip Abduction Force not found.")

    # Search for Hip Adduction Force
    adduction_force_row = next((i for i, row in enumerate(search_rows) if "Adduction Force" in row), None)
    if adduction_force_row is not None:
        adduction_force_values = search_rows[adduction_force_row]
        print("Hip Adduction Force values:", adduction_force_values)
        hip_adduction_force_left = adduction_force_values[3] if len(adduction_force_values) > 3 else None
        hip_adduction_force_right = adduction_force_values[4] if len(adduction_force_values) > 4 else None
    else:
        print("Hip Adduction Force not found.")

    # Search for Hip External Rotation Force
    ext_rotation_force_row = next((i for i, row in enumerate(search_rows) if "EXT Rotation Force" in row), None)
    if ext_rotation_force_row is not None:
        ext_rotation_force_values = search_rows[ext_rotation_force_row]
        print("Hip EXT Rotation Force values:", ext_rotation_force_values)
        hip_ext_rotation_force_left = ext_rotation_force_values[3] if len(ext_rotation_force_values) > 3 else None
        hip_ext_rotation_force_right = ext_rotation_force_values[4] if len(ext_rotation_force_values) > 4 else None
    else:
        print("Hip EXT Rotation Force not found.")

    # Search for Hip Internal Rotation Force
    int_rotation_force_row = next((i for i, row in enumerate(search_rows) if "INT Rotation Force" in row), None)
    if int_rotation_force_row is not None:
        int_rotation_force_values = search_rows[int_rotation_force_row]
        print("Hip INT Rotation Force values:", int_rotation_force_values)
        hip_int_rotation_force_left = int_rotation_force_values[3] if len(int_rotation_force_values) > 3 else None
        hip_int_rotation_force_right = int_rotation_force_values[4] if len(int_rotation_force_values) > 4 else None
    else:
        print("Hip INT Rotation Force not found.")

    return (
        hip_flexion_range_left,
        hip_flexion_range_right,
        hip_extension_range_left,
        hip_extension_range_right,
        hip_abduction_range_left,
        hip_abduction_range_right,
        hip_adduction_range_left,
        hip_adduction_range_right,
        hip_ext_rotation_range_left,
        hip_ext_rotation_range_right,
        hip_int_rotation_range_left,
        hip_int_rotation_range_right,
        hip_flexion_force_left,
        hip_flexion_force_right,
        hip_extension_force_left,
        hip_extension_force_right,
        hip_abduction_force_left,
        hip_abduction_force_right,
        hip_adduction_force_left,
        hip_adduction_force_right,
        hip_ext_rotation_force_left,
        hip_ext_rotation_force_right,
        hip_int_rotation_force_left,
        hip_int_rotation_force_right
    )

# Remove the function call at the end
# extract_sheet_metrics_hip(sheet_id)

def categorize_percentage_knee(value_str, measurement_type):
    """
    Categorize knee measurements with separate handling for range and strength
    measurement_type should be either 'range' or 'strength'
    """
    try:
        if value_str is None or value_str == '':
            return "unknown"
        
        percentage = float(value_str)
        
        # Calculate difference from 100 (gold standard)
        difference = percentage - 100
        
        if percentage > 100:
            if measurement_type == 'range':
                return f"good range {abs(difference):.1f}% above gold standard"
            else:  # strength
                return f"good strength {abs(difference):.1f}% above gold standard"
        elif 85 < percentage <= 100:
            if measurement_type == 'range':
                return f"sufficient range {abs(difference):.1f}% below gold standard"
            else:  # strength
                return f"sufficient strength {abs(difference):.1f}% below gold standard"
        elif 75 <= percentage <= 85:
            if measurement_type == 'range':
                return f"lack range {abs(difference):.1f}% below gold standard"
            else:  # strength
                return f"lack strength {abs(difference):.1f}% below gold standard"
        else:  # percentage < 75
            if measurement_type == 'range':
                return f"poor range {abs(difference):.1f}% below gold standard"
            else:  # strength
                return f"poor strength {abs(difference):.1f}% below gold standard"
            
    except (ValueError, TypeError):
        return "unknown"
    


def extract_sheet_metrics_knee(sheet_id, data_overview_sheet):
    # # Call the main extraction function
    # scopes = [
    #     'https://www.googleapis.com/auth/spreadsheets',
    #     'https://www.googleapis.com/auth/drive'
    # ]

    # creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    # client = gspread.authorize(creds)

    # # Open the Google Sheet
    # sheet = client.open_by_key(sheet_id)
    # # search sheet with the name 'Data Overview'
    # data_overview_sheet = sheet.worksheet("Data Overview")
    # Extract data from the worksheet
    all_values = data_overview_sheet.get_all_values()

    # search for strings in row "KNEE" "LEFT" "RIGHT" and "GS" if all these strings are present in row array then store its index
    knee_index = None
    left_index = None
    right_index = None
    gs_index = None
    
    for i, row in enumerate(all_values):
        if "KNEE" in row and "LEFT" in row and "RIGHT" in row and "GS" in row:
            knee_index = i
            # Find column indices
            for j, cell in enumerate(row):
                if cell == "LEFT":
                    left_index = j
                elif cell == "RIGHT":
                    right_index = j
                elif cell == "GS":
                    gs_index = j
            print(f"Found KNEE section at row {knee_index}, LEFT col {left_index}, RIGHT col {right_index}, GS col {gs_index}")
            break
    else:
        print("KNEE section not found")
        return tuple(["unavailable data"] * 14)  # Return 14 "unavailable data" values
    
    # Initialize knee measurement variables as strings
    knee_flexion_range_left = knee_flexion_range_right = None
    knee_extension_range_left = knee_extension_range_right = None
    knee_flexion_force_left = knee_flexion_force_right = None
    knee_extension_force_left = knee_extension_force_right = None

    # Only search from knee_index onwards
    search_rows = all_values[knee_index:] if knee_index is not None else all_values

    # Search for Knee Flexion Range
    flexion_range_row = next((i for i, row in enumerate(search_rows) if "Flexion Range" in row), None)
    if flexion_range_row is not None:
        flexion_range_values = search_rows[flexion_range_row]
        knee_flexion_range_left = flexion_range_values[left_index] if len(flexion_range_values) > left_index else "unavailable data"
        knee_flexion_range_right = flexion_range_values[right_index] if len(flexion_range_values) > right_index else "unavailable data"
        print(f"Knee Flexion Range - Left: {knee_flexion_range_left}, Right: {knee_flexion_range_right}")
    else:
        knee_flexion_range_left = knee_flexion_range_right = "unavailable data"

    # Search for Knee Extension Range
    extension_range_row = next((i for i, row in enumerate(search_rows) if "Extension Range" in row), None)
    if extension_range_row is not None:
        extension_range_values = search_rows[extension_range_row]
        knee_extension_range_left = extension_range_values[left_index] if len(extension_range_values) > left_index else "unavailable data"
        knee_extension_range_right = extension_range_values[right_index] if len(extension_range_values) > right_index else "unavailable data"
        print(f"Knee Extension Range - Left: {knee_extension_range_left}, Right: {knee_extension_range_right}")
    else:
        knee_extension_range_left = knee_extension_range_right = "unavailable data"

    # Search for Knee Flexion Force
    flexion_force_row = next((i for i, row in enumerate(search_rows) if "Flexion Force" in row), None)
    if flexion_force_row is not None:
        flexion_force_values = search_rows[flexion_force_row]
        knee_flexion_force_left = flexion_force_values[left_index] if len(flexion_force_values) > left_index else "unavailable data"
        knee_flexion_force_right = flexion_force_values[right_index] if len(flexion_force_values) > right_index else "unavailable data"
        print(f"Knee Flexion Force - Left: {knee_flexion_force_left}, Right: {knee_flexion_force_right}")
    else:
        knee_flexion_force_left = knee_flexion_force_right = "unavailable data"

    # Search for Knee Extension Force
    extension_force_row = next((i for i, row in enumerate(search_rows) if "Extension Force" in row), None)
    if extension_force_row is not None:
        extension_force_values = search_rows[extension_force_row]
        knee_extension_force_left = extension_force_values[left_index] if len(extension_force_values) > left_index else "unavailable data"
        knee_extension_force_right = extension_force_values[right_index] if len(extension_force_values) > right_index else "unavailable data"
        print(f"Knee Extension Force - Left: {knee_extension_force_left}, Right: {knee_extension_force_right}")
    else:
        knee_extension_force_left = knee_extension_force_right = "unavailable data"

    # Now search for strings in row "KNEE" "FORCE (Degrees)" "FORCE (Relative)" if all these strings are present in row array then store its index
    knee_index = None
    force_degrees_index = None
    force_relative_index = None
    for i, row in enumerate(all_values):
        if "KNEE" in row and "FORCE (Degrees)" in row and "FORCE (Relative)" in row:
            knee_index = i
            print(f"Found KNEE force section at row {knee_index}")
            break

    knee_flexion_force_left_original = None
    knee_flexion_force_right_original = None
    knee_extension_force_left_original = None
    knee_extension_force_right_original = None
    
    search_rows = all_values[knee_index:] if knee_index is not None else all_values
    flexion_force_row = next((i for i, row in enumerate(search_rows) if "Flexion" in row), None)
    if flexion_force_row is not None:
        flexion_force_values = search_rows[flexion_force_row]
        knee_flexion_force_left_original = flexion_force_values[3] if len(flexion_force_values) > 3 else "unavailable data"
        knee_flexion_force_right_original = flexion_force_values[5] if len(flexion_force_values) > 5 else "unavailable data"
        print(f"Knee Flexion Force Original - Left: {knee_flexion_force_left_original}, Right: {knee_flexion_force_right_original}")

    # Search for Knee Extension Force
    extension_force_row = next((i for i, row in enumerate(search_rows) if "Extension" in row), None)
    if extension_force_row is not None:
        extension_force_values = search_rows[extension_force_row]
        knee_extension_force_left_original = extension_force_values[3] if len(extension_force_values) > 3 else "unavailable data"
        knee_extension_force_right_original = extension_force_values[5] if len(extension_force_values) > 5 else "unavailable data"
        print(f"Knee Extension Force Original - Left: {knee_extension_force_left_original}, Right: {knee_extension_force_right_original}")

    # first convert the flexion and extension force original to float and then calculate the Hamstring to quad ratio at right and left by dividing flexion by extension
    if knee_flexion_force_left_original is not None and knee_extension_force_left_original is not None:
        try:
            flexion_left = float(knee_flexion_force_left_original)
            extension_left = float(knee_extension_force_left_original)
            knee_hamstring_quad_ratio_left = flexion_left / extension_left if extension_left != 0 else "unavailable data"
        except (ValueError, TypeError):
            knee_hamstring_quad_ratio_left = "unavailable data"
    else:
        knee_hamstring_quad_ratio_left = "unavailable data"

    if knee_flexion_force_right_original is not None and knee_extension_force_right_original is not None:
        try:
            flexion_right = float(knee_flexion_force_right_original)
            extension_right = float(knee_extension_force_right_original)
            knee_hamstring_quad_ratio_right = flexion_right / extension_right if extension_right != 0 else "unavailable data"
        except (ValueError, TypeError):
            knee_hamstring_quad_ratio_right = "unavailable data"
    else:
        knee_hamstring_quad_ratio_right = "unavailable data"

    print("Knee Hamstring to Quad Ratio original values (Left, Right):", knee_hamstring_quad_ratio_left, knee_hamstring_quad_ratio_right)

    return (
        knee_flexion_range_left,
        knee_flexion_range_right,
        knee_extension_range_left,
        knee_extension_range_right,
        knee_flexion_force_left,
        knee_flexion_force_right,
        knee_extension_force_left,
        knee_extension_force_right,
        knee_flexion_force_left_original,
        knee_flexion_force_right_original,
        knee_extension_force_left_original,
        knee_extension_force_right_original,
        knee_hamstring_quad_ratio_left,
        knee_hamstring_quad_ratio_right
    )
def TextGen_Knee_Concise(sheet_id,data_overview_sheet):
    """
    Generate concise knee assessment input prompt
    """
    (
    knee_flexion_range_left,
    knee_flexion_range_right,
    knee_extension_range_left,
    knee_extension_range_right,
    knee_flexion_force_left,
    knee_flexion_force_right,
    knee_extension_force_left,
    knee_extension_force_right,
    knee_flexion_force_left_original,
    knee_flexion_force_right_original,
    knee_extension_force_left_original,
    knee_extension_force_right_original,
    knee_hamstring_quad_ratio_left,
    knee_hamstring_quad_ratio_right
    ) = extract_sheet_metrics_knee(sheet_id,data_overview_sheet)

    # Categorize all measurements with specific types
    movements = {
        'Knee Flexion': {
            'range_left': categorize_percentage_knee(knee_flexion_range_left, 'range'),
            'range_right': categorize_percentage_knee(knee_flexion_range_right, 'range'),
            'strength_left': categorize_percentage_knee(knee_flexion_force_left, 'strength'),
            'strength_right': categorize_percentage_knee(knee_flexion_force_right, 'strength'),
            'range_left_val': knee_flexion_range_left,
            'range_right_val': knee_flexion_range_right,
            'strength_left_val': knee_flexion_force_left,
            'strength_right_val': knee_flexion_force_right
        },
        'Knee Extension': {
            'range_left': categorize_percentage_knee(knee_extension_range_left, 'range'),
            'range_right': categorize_percentage_knee(knee_extension_range_right, 'range'),
            'strength_left': categorize_percentage_knee(knee_extension_force_left, 'strength'),
            'strength_right': categorize_percentage_knee(knee_extension_force_right, 'strength'),
            'range_left_val': knee_extension_range_left,
            'range_right_val': knee_extension_range_right,
            'strength_left_val': knee_extension_force_left,
            'strength_right_val': knee_extension_force_right
        }
    }
    
    # Function to calculate left vs right percentage comparison
    def calculate_side_comparison(left_val, right_val, measurement_type):
        try:
            left_num = float(left_val) if left_val is not None else None
            right_num = float(right_val) if right_val is not None else None

            if left_num is not None and right_num is not None:
                if left_num > right_num:
                    difference = left_num - right_num
                    percentage_diff = (difference / right_num * 100) if right_num != 0 else 0
                    return f"Left {percentage_diff:.1f}% stronger than right"
                elif right_num > left_num:
                    difference = right_num - left_num
                    percentage_diff = (difference / left_num * 100) if left_num != 0 else 0
                    return f"Right {percentage_diff:.1f}% stronger than left"
                else:
                    return "Left and right equal"
            else:
                return "Cannot compare - missing data"
        except (TypeError, ValueError):
            return "Cannot compare - invalid data"
        
    hq_results,hq_report = TextGen_Knee_HQ_Ratio(sheet_id,data_overview_sheet)
    
    # Build concise input prompt
    input_lines = []
    
    # Track deficits for summary
    range_deficits_left = []
    range_deficits_right = []
    strength_deficits_left = []
    strength_deficits_right = []
    
    for movement_name, data in movements.items():
        input_lines.append(f"{movement_name}")
        input_lines.append("")
        
        # Range assessment with individual left/right values
        input_lines.append(f"Range Left: {data['range_left']}")
        input_lines.append(f"Range Right: {data['range_right']}")
        
        # Range comparison
        range_comparison = calculate_side_comparison(data['range_left_val'], data['range_right_val'], "range")
        input_lines.append(f"Range Comparison: {range_comparison}")
        input_lines.append("")
        
        # Strength assessment with individual left/right values
        input_lines.append(f"Strength Left: {data['strength_left']}")
        input_lines.append(f"Strength Right: {data['strength_right']}")
        
        # Strength comparison
        strength_comparison = calculate_side_comparison(data['strength_left_val'], data['strength_right_val'], "strength")
        input_lines.append(f"Strength Comparison: {strength_comparison}")
        input_lines.append("")
        
        # Track deficits for summary (include lack and poor categories)
        if "lack range" in data['range_left'] or "poor range" in data['range_left']:
            range_deficits_left.append(movement_name.replace('Knee ', ''))
        if "lack range" in data['range_right'] or "poor range" in data['range_right']:
            range_deficits_right.append(movement_name.replace('Knee ', ''))
        if "lack strength" in data['strength_left'] or "poor strength" in data['strength_left']:
            strength_deficits_left.append(movement_name.replace('Knee ', ''))
        if "lack strength" in data['strength_right'] or "poor strength" in data['strength_right']:
            strength_deficits_right.append(movement_name.replace('Knee ', ''))
    

        
    
    # Overall Notes section
    input_lines.append("Overall Notes:")
    input_lines.append("")
    
    # Range deficits
    if range_deficits_left or range_deficits_right:
        deficit_parts = []
        if range_deficits_left:
            deficit_parts.append(f"Left → {', '.join(range_deficits_left)}")
        if range_deficits_right:
            deficit_parts.append(f"Right → {', '.join(range_deficits_right)}")
        input_lines.append(f"Range deficits: {'; '.join(deficit_parts)}")
    
    # Strength deficits
    if strength_deficits_left or strength_deficits_right:
        deficit_parts = []
        if strength_deficits_left:
            deficit_parts.append(f"Left → {', '.join(strength_deficits_left)}")
        if strength_deficits_right:
            deficit_parts.append(f"Right → {', '.join(strength_deficits_right)}")
        input_lines.append(f"Strength deficits: {'; '.join(deficit_parts)}")

    # Hamstring to Quadriceps Ratio
    if hq_results:
        input_lines.append("")
        input_lines.append("Hamstring to Quadriceps Ratio:")
        input_lines.append(hq_report)

    # # Flexion vs Extension comparison
    # left_flex_ext_comparison = calc_opposing_comparison(knee_flexion_range_left, knee_extension_range_left, "Left")
    # right_flex_ext_comparison = calc_opposing_comparison(knee_flexion_range_right, knee_extension_range_right, "Right")
    
    # if left_flex_ext_comparison or right_flex_ext_comparison:
    #     input_lines.append("")
    #     input_lines.append("Flexion vs Extension Range:")
    #     input_lines.append(left_flex_ext_comparison)
    #     input_lines.append(right_flex_ext_comparison)
    
    # # Force comparison for flexion vs extension
    # left_flex_ext_force_comparison = calc_opposing_comparison(knee_flexion_force_left, knee_extension_force_left, "Left")
    # right_flex_ext_force_comparison = calc_opposing_comparison(knee_flexion_force_right, knee_extension_force_right, "Right")
    
    # if left_flex_ext_force_comparison or right_flex_ext_force_comparison:
    #     input_lines.append("")
    #     input_lines.append("Flexion vs Extension Strength:")
    #     input_lines.append(left_flex_ext_force_comparison)
    #     input_lines.append(right_flex_ext_force_comparison)

    
    
    
    return "\n".join(input_lines)

def TextGen_Hip_Concise(sheet_id,data_overview_sheet):
    """
    Generate concise hip assessment input prompt
    """
    (
    hip_flexion_range_left,
    hip_flexion_range_right,
    hip_extension_range_left,
    hip_extension_range_right,
    hip_abduction_range_left,
    hip_abduction_range_right,
    hip_adduction_range_left,
    hip_adduction_range_right,
    hip_ext_rotation_range_left,
    hip_ext_rotation_range_right,
    hip_int_rotation_range_left,
    hip_int_rotation_range_right,
    hip_flexion_force_left,
    hip_flexion_force_right,
    hip_extension_force_left,
    hip_extension_force_right,
    hip_abduction_force_left,
    hip_abduction_force_right,
    hip_adduction_force_left,
    hip_adduction_force_right,
    hip_ext_rotation_force_left,
    hip_ext_rotation_force_right,
    hip_int_rotation_force_left,
    hip_int_rotation_force_right
    ) = extract_sheet_metrics_hip(sheet_id,data_overview_sheet)

    # Function to convert string to float and categorize based on percentage
    def categorize_percentage_concise(value_str):
        try:
            if value_str is None or value_str == '':
                return "unknown"
            
            percentage = float(value_str)
            
            if percentage < 75:
                return "large deficit"
            elif 75 <= percentage <= 85:
                return "deficit"
            elif 85 < percentage <= 100:
                return "sufficient but below gold standard"
            else:  # percentage > 100
                return "above our gold standard"
                
        except (ValueError, TypeError):
            return "unknown"
    
    # Categorize all measurements
    movements = {
        'Hip Flexion': {
            'range_left': categorize_percentage_concise(hip_flexion_range_left),
            'range_right': categorize_percentage_concise(hip_flexion_range_right),
            'strength_left': categorize_percentage_concise(hip_flexion_force_left),
            'strength_right': categorize_percentage_concise(hip_flexion_force_right),
            'range_left_val': hip_flexion_range_left,
            'range_right_val': hip_flexion_range_right,
            'strength_left_val': hip_flexion_force_left,
            'strength_right_val': hip_flexion_force_right
        },
        'Hip Extension': {
            'range_left': categorize_percentage_concise(hip_extension_range_left),
            'range_right': categorize_percentage_concise(hip_extension_range_right),
            'strength_left': categorize_percentage_concise(hip_extension_force_left),
            'strength_right': categorize_percentage_concise(hip_extension_force_right),
            'range_left_val': hip_extension_range_left,
            'range_right_val': hip_extension_range_right,
            'strength_left_val': hip_extension_force_left,
            'strength_right_val': hip_extension_force_right
        },
        'Hip Abduction': {
            'range_left': categorize_percentage_concise(hip_abduction_range_left),
            'range_right': categorize_percentage_concise(hip_abduction_range_right),
            'strength_left': categorize_percentage_concise(hip_abduction_force_left),
            'strength_right': categorize_percentage_concise(hip_abduction_force_right),
            'range_left_val': hip_abduction_range_left,
            'range_right_val': hip_abduction_range_right,
            'strength_left_val': hip_abduction_force_left,
            'strength_right_val': hip_abduction_force_right
        },
        'Hip Adduction': {
            'range_left': categorize_percentage_concise(hip_adduction_range_left),
            'range_right': categorize_percentage_concise(hip_adduction_range_right),
            'strength_left': categorize_percentage_concise(hip_adduction_force_left),
            'strength_right': categorize_percentage_concise(hip_adduction_force_right),
            'range_left_val': hip_adduction_range_left,
            'range_right_val': hip_adduction_range_right,
            'strength_left_val': hip_adduction_force_left,
            'strength_right_val': hip_adduction_force_right
        },
        'Hip External Rotation': {
            'range_left': categorize_percentage_concise(hip_ext_rotation_range_left),
            'range_right': categorize_percentage_concise(hip_ext_rotation_range_right),
            'strength_left': categorize_percentage_concise(hip_ext_rotation_force_left),
            'strength_right': categorize_percentage_concise(hip_ext_rotation_force_right),
            'range_left_val': hip_ext_rotation_range_left,
            'range_right_val': hip_ext_rotation_range_right,
            'strength_left_val': hip_ext_rotation_force_left,
            'strength_right_val': hip_ext_rotation_force_right
        },
        'Hip Internal Rotation': {
            'range_left': categorize_percentage_concise(hip_int_rotation_range_left),
            'range_right': categorize_percentage_concise(hip_int_rotation_range_right),
            'strength_left': categorize_percentage_concise(hip_int_rotation_force_left),
            'strength_right': categorize_percentage_concise(hip_int_rotation_force_right),
            'range_left_val': hip_int_rotation_range_left,
            'range_right_val': hip_int_rotation_range_right,
            'strength_left_val': hip_int_rotation_force_left,
            'strength_right_val': hip_int_rotation_force_right
        }
    }
    
    # Function to calculate asymmetry with concise format
    def calculate_asymmetry_concise(left_val, right_val):
        try:
            left_num = float(left_val) if left_val is not None else None
            right_num = float(right_val) if right_val is not None else None

            if left_num is not None and right_num is not None:
                difference = right_num - left_num
                avg_value = (left_num + right_num) / 2
                percentage_difference = (abs(difference) / avg_value * 100) if avg_value != 0 else 0

                if percentage_difference > 15:
                    if difference > 0:
                        return f"Right > Left by {percentage_difference:.1f}%"
                    elif difference < 0:
                        return f"Left > Right by {percentage_difference:.1f}%"
                return None
            else:
                return None
        except (TypeError, ValueError):
            return None
    
    # Function to format bilateral assessment
    def format_bilateral(left_cat, right_cat):
        if left_cat == right_cat and left_cat != "unknown":
            return f"{left_cat} bilaterally"
        else:
            return f"{left_cat} left, {right_cat} right"
    
    # Build concise input prompt
    input_lines = []
    
    # Track deficits for summary (including both deficit categories)
    range_deficits_left = []
    range_deficits_right = []
    strength_deficits_left = []
    strength_deficits_right = []
    
    # Calculate opposing movement asymmetries for largest variation
    opposing_asymmetries = []
    
    for movement_name, data in movements.items():
        input_lines.append(f"{movement_name}")
        input_lines.append("")
        
        # Range assessment
        range_text = format_bilateral(data['range_left'], data['range_right'])
        input_lines.append(f"Range: {range_text}")
        
        # Strength assessment
        strength_text = format_bilateral(data['strength_left'], data['strength_right'])
        input_lines.append(f"Strength: {strength_text}")
        
        # Range asymmetry
        range_asymmetry = calculate_asymmetry_concise(data['range_left_val'], data['range_right_val'])
        if range_asymmetry:
            input_lines.append(f"Asymmetry: {range_asymmetry}")
        
        # Strength asymmetry
        strength_asymmetry = calculate_asymmetry_concise(data['strength_left_val'], data['strength_right_val'])
        if strength_asymmetry and not range_asymmetry:
            input_lines.append(f"Asymmetry: {strength_asymmetry}")
        
        input_lines.append("")
        
        # Track deficits for summary (include both large deficit and deficit)
        if data['range_left'] in ['large deficit', 'deficit']:
            range_deficits_left.append(movement_name.replace('Hip ', ''))
        if data['range_right'] in ['large deficit', 'deficit']:
            range_deficits_right.append(movement_name.replace('Hip ', ''))
        if data['strength_left'] in ['large deficit', 'deficit']:
            strength_deficits_left.append(movement_name.replace('Hip ', ''))
        if data['strength_right'] in ['large deficit', 'deficit']:
            strength_deficits_right.append(movement_name.replace('Hip ', ''))
    
    # Calculate opposing movement asymmetries
    def calc_opposing_asymmetry(left_val, right_val, movement_name, side):
        asym = calculate_asymmetry_concise(left_val, right_val)
        if asym:
            # Extract percentage
            import re
            match = re.search(r'(\d+(\.\d+)?)%', asym)
            if match:
                percent = float(match.group(1))
                return (percent, f"{movement_name} ({side})", asym)
        return None
    
    # Check opposing movements
    opposing_checks = [
        (hip_flexion_range_left, hip_extension_range_left, "Hip Flexion/Extension Range", "Left"),
        (hip_flexion_range_right, hip_extension_range_right, "Hip Flexion/Extension Range", "Right"),
        (hip_abduction_range_left, hip_adduction_range_left, "Hip Abduction/Adduction Range", "Left"),
        (hip_abduction_range_right, hip_adduction_range_right, "Hip Abduction/Adduction Range", "Right"),
        (hip_int_rotation_range_left, hip_ext_rotation_range_left, "Hip Internal/External Rotation", "Left"),
        (hip_int_rotation_range_right, hip_ext_rotation_range_right, "Hip Internal/External Rotation", "Right")
    ]
    
    largest_variation = None
    for left_val, right_val, movement_name, side in opposing_checks:
        result = calc_opposing_asymmetry(left_val, right_val, movement_name, side)
        if result:
            if largest_variation is None or result[0] > largest_variation[0]:
                largest_variation = result
    
    # Overall Notes section
    input_lines.append("Overall Notes:")
    input_lines.append("")
    
    # Range deficits
    if range_deficits_left or range_deficits_right:
        deficit_parts = []
        if range_deficits_left:
            deficit_parts.append(f"Left → {', '.join(range_deficits_left)}")
        if range_deficits_right:
            deficit_parts.append(f"Right → {', '.join(range_deficits_right)}")
        input_lines.append(f"Range deficits: {'; '.join(deficit_parts)}")
    
    # Strength deficits
    if strength_deficits_left or strength_deficits_right:
        deficit_parts = []
        if strength_deficits_left:
            deficit_parts.append(f"Left → {', '.join(strength_deficits_left)}")
        if strength_deficits_right:
            deficit_parts.append(f"Right → {', '.join(strength_deficits_right)}")
        input_lines.append(f"Strength deficits: {'; '.join(deficit_parts)}")
    
    # Largest range variation
    if largest_variation:
        input_lines.append("")
        input_lines.append(f"Largest range variation: {largest_variation[1]} → {largest_variation[0]:.1f}% difference")
        input_lines.append("")
        input_lines.append("Inverse relationship in ROM highlights femur positioning changes")
    
    return "\n".join(input_lines)

# Also update the main TextGen_Hip function
def TextGen_Hip(sheet_id,data_overview_sheet):
    """
    Original function modified to also return concise input prompt
    """
    # ... (keep all existing code from the original function)
    
    # At the end, also generate the concise input prompt
    concise_input = TextGen_Hip_Concise(sheet_id)
    
    # Return the original values plus the concise input
    (
    hip_flexion_range_left,
    hip_flexion_range_right,
    hip_extension_range_left,
    hip_extension_range_right,
    hip_abduction_range_left,
    hip_abduction_range_right,
    hip_adduction_range_left,
    hip_adduction_range_right,
    hip_ext_rotation_range_left,
    hip_ext_rotation_range_right,
    hip_int_rotation_range_left,
    hip_int_rotation_range_right,
    hip_flexion_force_left,
    hip_flexion_force_right,
    hip_extension_force_left,
    hip_extension_force_right,
    hip_abduction_force_left,
    hip_abduction_force_right,
    hip_adduction_force_left,
    hip_adduction_force_right,
    hip_ext_rotation_force_left,
    hip_ext_rotation_force_right,
    hip_int_rotation_force_left,
    hip_int_rotation_force_right
) = extract_sheet_metrics_hip(sheet_id,data_overview_sheet)
    
    # Function to convert string to float and categorize based on percentage - UPDATED
    def categorize_percentage(value_str):
        try:
            if value_str is None or value_str == '':
                return "Unknown"
            
            # Convert string to float
            percentage = float(value_str)
            
            # Updated categorize based on percentage thresholds
            if percentage < 75:
                return "large lack of"
            elif 75 <= percentage <= 85:
                return "lack of"
            elif 85 < percentage <= 100:
                return "sufficient but below gold standard"
            else:  # percentage > 100
                return "above our gold standard"
                
        except (ValueError, TypeError):
            return "Unknown"
    
    # Categorize all hip range measurements
    hip_flexion_range_left_category = categorize_percentage(hip_flexion_range_left)
    hip_flexion_range_right_category = categorize_percentage(hip_flexion_range_right)
    hip_extension_range_left_category = categorize_percentage(hip_extension_range_left)
    hip_extension_range_right_category = categorize_percentage(hip_extension_range_right)
    hip_abduction_range_left_category = categorize_percentage(hip_abduction_range_left)
    hip_abduction_range_right_category = categorize_percentage(hip_abduction_range_right)
    hip_adduction_range_left_category = categorize_percentage(hip_adduction_range_left)
    hip_adduction_range_right_category = categorize_percentage(hip_adduction_range_right)
    hip_ext_rotation_range_left_category = categorize_percentage(hip_ext_rotation_range_left)
    hip_ext_rotation_range_right_category = categorize_percentage(hip_ext_rotation_range_right)
    hip_int_rotation_range_left_category = categorize_percentage(hip_int_rotation_range_left)
    hip_int_rotation_range_right_category = categorize_percentage(hip_int_rotation_range_right)
    
    # Categorize all hip force measurements
    hip_flexion_force_left_category = categorize_percentage(hip_flexion_force_left)
    hip_flexion_force_right_category = categorize_percentage(hip_flexion_force_right)
    hip_extension_force_left_category = categorize_percentage(hip_extension_force_left)
    hip_extension_force_right_category = categorize_percentage(hip_extension_force_right)
    hip_abduction_force_left_category = categorize_percentage(hip_abduction_force_left)
    hip_abduction_force_right_category = categorize_percentage(hip_abduction_force_right)
    hip_adduction_force_left_category = categorize_percentage(hip_adduction_force_left)
    hip_adduction_force_right_category = categorize_percentage(hip_adduction_force_right)
    hip_ext_rotation_force_left_category = categorize_percentage(hip_ext_rotation_force_left)
    hip_ext_rotation_force_right_category = categorize_percentage(hip_ext_rotation_force_right)
    hip_int_rotation_force_left_category = categorize_percentage(hip_int_rotation_force_left)
    hip_int_rotation_force_right_category = categorize_percentage(hip_int_rotation_force_right)

    
    
    # Function to assess asymmetry between left and right sides
    def assess_hip_asymmetry(left_val, right_val):
        try:
            left_num = float(left_val) if left_val is not None else None
            right_num = float(right_val) if right_val is not None else None

            if left_num is not None and right_num is not None:
                difference = right_num - left_num
                avg_value = (left_num + right_num) / 2
                percentage_difference = (abs(difference) / avg_value * 100) if avg_value != 0 else 0

                if percentage_difference > 15:
                    if difference > 0:
                        side_info = f"Right is greater by {percentage_difference:.1f}%"
                    elif difference < 0:
                        side_info = f"Left is greater by {percentage_difference:.1f}%"
                    else:
                        side_info = "Both sides are equal"
                    return f"Asymmetry detected ({side_info})"
                else:
                    return f"Symmetrical (difference: {percentage_difference:.1f}%)"
            else:
                return "Unknown"
        except (TypeError, ValueError):
            return "Unknown"
    
    # Assess asymmetry for each movement type
    hip_flexion_range_asymmetry = assess_hip_asymmetry(hip_flexion_range_left, hip_flexion_range_right)
    hip_extension_range_asymmetry = assess_hip_asymmetry(hip_extension_range_left, hip_extension_range_right)
    hip_abduction_range_asymmetry = assess_hip_asymmetry(hip_abduction_range_left, hip_abduction_range_right)
    hip_adduction_range_asymmetry = assess_hip_asymmetry(hip_adduction_range_left, hip_adduction_range_right)
    hip_ext_rotation_range_asymmetry = assess_hip_asymmetry(hip_ext_rotation_range_left, hip_ext_rotation_range_right)
    hip_int_rotation_range_asymmetry = assess_hip_asymmetry(hip_int_rotation_range_left, hip_int_rotation_range_right)
    
    hip_flexion_force_asymmetry = assess_hip_asymmetry(hip_flexion_force_left, hip_flexion_force_right)
    hip_extension_force_asymmetry = assess_hip_asymmetry(hip_extension_force_left, hip_extension_force_right)
    hip_abduction_force_asymmetry = assess_hip_asymmetry(hip_abduction_force_left, hip_abduction_force_right)
    hip_adduction_force_asymmetry = assess_hip_asymmetry(hip_adduction_force_left, hip_adduction_force_right)
    hip_ext_rotation_force_asymmetry = assess_hip_asymmetry(hip_ext_rotation_force_left, hip_ext_rotation_force_right)
    hip_int_rotation_force_asymmetry = assess_hip_asymmetry(hip_int_rotation_force_left, hip_int_rotation_force_right)

    # also assess hip asymmetry between opposing movements like flexion extension, abduction adduction , internal external rotation for right side and left side separately
    hip_flexion_extension_range_asymmetry_left = assess_hip_asymmetry(hip_flexion_range_left, hip_extension_range_left)
    hip_flexion_extension_range_asymmetry_right = assess_hip_asymmetry(hip_flexion_range_right, hip_extension_range_right)
    hip_abduction_adduction_range_asymmetry_left = assess_hip_asymmetry(hip_abduction_range_left, hip_adduction_range_left)
    hip_abduction_adduction_range_asymmetry_right = assess_hip_asymmetry(hip_abduction_range_right, hip_adduction_range_right)
    hip_int_ext_rotation_range_asymmetry_left = assess_hip_asymmetry(hip_int_rotation_range_left, hip_ext_rotation_range_left)
    hip_int_ext_rotation_range_asymmetry_right = assess_hip_asymmetry(hip_int_rotation_range_right, hip_ext_rotation_range_right)

    # check if there is any asymmetry in the opposing movements
    opposing_movement_asymmetries = {
        'Hip Flexion/Extension Range': (hip_flexion_extension_range_asymmetry_left, hip_flexion_extension_range_asymmetry_right),
        'Hip Abduction/Adduction Range': (hip_abduction_adduction_range_asymmetry_left, hip_abduction_adduction_range_asymmetry_right),
        'Hip Internal/External Rotation Range': (hip_int_ext_rotation_range_asymmetry_left, hip_int_ext_rotation_range_asymmetry_right)
    }

    # Only store those with asymmetry
    asymmetry_opposing_movements = {}
    largest_percentage = 0
    largest_movement = ""
    largest_movement_summary = ""
    for movement, (left_asym, right_asym) in opposing_movement_asymmetries.items():
        for side, asym in [("Left", left_asym), ("Right", right_asym)]:
            if asym and str(asym).startswith("Asymmetry detected"):
                asymmetry_opposing_movements[f"{movement} ({side})"] = asym
                # Extract percentage from the string
                import re
                match = re.search(r'(\d+(\.\d+)?)%', str(asym))
                if match:
                    percent = float(match.group(1))
                    if percent > largest_percentage:
                        largest_percentage = percent
                        largest_movement = f"{movement} ({side})"
                        largest_movement_summary = (
                            f"There was an inverse relationship in range of motion highlighting the change in positioning of the femur in the hip."
                            f"The largest variation is observed in {largest_movement} with a difference of {largest_percentage:.1f}%. "

                        )


    # Generate comprehensive hip assessment text
    def generate_hip_summary(range_left_cat, range_right_cat, force_left_cat, force_right_cat, 
                           range_asymmetry, force_asymmetry, movement_name):
        summary = f"{movement_name}: "
        
        # Range assessment
        if range_left_cat == range_right_cat and range_left_cat != "Unknown":
            summary += f"Range shows {range_left_cat} mobility bilaterally"
        else:
            summary += f"Range shows {range_left_cat} mobility on left, {range_right_cat} mobility on right"
        
        # Force assessment
        if force_left_cat == force_right_cat and force_left_cat != "Unknown":
            summary += f", {force_left_cat} strength bilaterally"
        else:
            summary += f", {force_left_cat} strength on left, {force_right_cat} strength on right"
        
        # Asymmetry assessment
        range_asymmetry_str = str(range_asymmetry)
        force_asymmetry_str = str(force_asymmetry)
        if range_asymmetry_str.startswith("Asymmetry detected"):
            summary += f", with noted range asymmetry ({range_asymmetry})"
        if force_asymmetry_str.startswith("Asymmetry detected"):
            summary += f", with noted strength asymmetry ({force_asymmetry})"
        return summary
    
    # Generate individual movement summaries
    hip_flexion_summary = generate_hip_summary(
        hip_flexion_range_left_category, hip_flexion_range_right_category,
        hip_flexion_force_left_category, hip_flexion_force_right_category,
        hip_flexion_range_asymmetry, hip_flexion_force_asymmetry, "Hip Flexion"
    )
    
    hip_extension_summary = generate_hip_summary(
        hip_extension_range_left_category, hip_extension_range_right_category,
        hip_extension_force_left_category, hip_extension_force_right_category,
        hip_extension_range_asymmetry, hip_extension_force_asymmetry, "Hip Extension"
    )
    
    hip_abduction_summary = generate_hip_summary(
        hip_abduction_range_left_category, hip_abduction_range_right_category,
        hip_abduction_force_left_category, hip_abduction_force_right_category,
        hip_abduction_range_asymmetry, hip_abduction_force_asymmetry, "Hip Abduction"
    )
    
    hip_adduction_summary = generate_hip_summary(
        hip_adduction_range_left_category, hip_adduction_range_right_category,
        hip_adduction_force_left_category, hip_adduction_force_right_category,
        hip_adduction_range_asymmetry, hip_adduction_force_asymmetry, "Hip Adduction"
    )
    
    hip_ext_rotation_summary = generate_hip_summary(
        hip_ext_rotation_range_left_category, hip_ext_rotation_range_right_category,
        hip_ext_rotation_force_left_category, hip_ext_rotation_force_right_category,
        hip_ext_rotation_range_asymmetry, hip_ext_rotation_force_asymmetry, "Hip External Rotation"
    )
    
    hip_int_rotation_summary = generate_hip_summary(
        hip_int_rotation_range_left_category, hip_int_rotation_range_right_category,
        hip_int_rotation_force_left_category, hip_int_rotation_force_right_category,
        hip_int_rotation_range_asymmetry, hip_int_rotation_force_asymmetry, "Hip Internal Rotation"
    )
    
    # Identify movements that lack range or strength (print right and left separately) - UPDATED
    def identify_lacking_movements():
        lacking_range_left = []
        lacking_range_right = []
        lacking_strength_left = []
        lacking_strength_right = []

        movements_data = [
            ("Hip Flexion", hip_flexion_range_left_category, hip_flexion_range_right_category, 
             hip_flexion_force_left_category, hip_flexion_force_right_category),
            ("Hip Extension", hip_extension_range_left_category, hip_extension_range_right_category,
             hip_extension_force_left_category, hip_extension_force_right_category),
            ("Hip Abduction", hip_abduction_range_left_category, hip_abduction_range_right_category,
             hip_abduction_force_left_category, hip_abduction_force_right_category),
            ("Hip Adduction", hip_adduction_range_left_category, hip_adduction_range_right_category,
             hip_adduction_force_left_category, hip_adduction_force_right_category),
            ("Hip External Rotation", hip_ext_rotation_range_left_category, hip_ext_rotation_range_right_category,
             hip_ext_rotation_force_left_category, hip_ext_rotation_force_right_category),
            ("Hip Internal Rotation", hip_int_rotation_range_left_category, hip_int_rotation_range_right_category,
             hip_int_rotation_force_left_category, hip_int_rotation_force_right_category),
        ]

        for movement_name, range_left, range_right, force_left, force_right in movements_data:
            if range_left in ["large lack of", "lack of"]:
                lacking_range_left.append(movement_name)
            if range_right in ["large lack of", "lack of"]:
                lacking_range_right.append(movement_name)
            if force_left in ["large lack of", "lack of"]:
                lacking_strength_left.append(movement_name)
            if force_right in ["large lack of", "lack of"]:
                lacking_strength_right.append(movement_name)

        return lacking_range_left, lacking_range_right, lacking_strength_left, lacking_strength_right

    # Identify lacking movements (combine left and right)
    lacking_range_left, lacking_range_right, lacking_strength_left, lacking_strength_right = identify_lacking_movements()


    # Create summary of lacking movements (only movement names)
    deficit_summary = ""
    if lacking_range_left or lacking_range_right or lacking_strength_left or lacking_strength_right:
        deficit_parts = []
        if lacking_range_left:
            deficit_parts.append(f"Range deficits noted on left in: {', '.join(lacking_range_left)}")
        if lacking_range_right:
            deficit_parts.append(f"Range deficits noted on right in: {', '.join(lacking_range_right)}")
        if lacking_strength_left:
            deficit_parts.append(f"Strength deficits noted on left in: {', '.join(lacking_strength_left)}")
        if lacking_strength_right:
            deficit_parts.append(f"Strength deficits noted on right in: {', '.join(lacking_strength_right)}")
        deficit_summary = ". ".join(deficit_parts) + "."
    else:
        deficit_summary = "No significant range or strength deficits noted in hip movements."
    # Extract existing hip report text (similar to foot/ankle function)
    def extract_hip_report_text(sheet_id):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        from google.oauth2.service_account import Credentials
        import gspread
        
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key(sheet_id)
        report_worksheet = None
        try:
            report_worksheet = sheet.worksheet('Report')
        except gspread.WorksheetNotFound:
            try:
                report_worksheet = sheet.worksheet('NEW Datavis')
            except gspread.WorksheetNotFound:
                print("Neither 'Report' nor 'New Datavis' worksheet found.")
        
        hip_assessment = None
        if report_worksheet:
            for row in report_worksheet.get_all_values():
                if len(row) > 7 and 'ASSESSMENT OF THE HIP:' in row[7]:
                    hip_assessment = row[7].split('ASSESSMENT OF THE HIP:')[1].strip()
                    break
            if hip_assessment is None:
                print(f"No 'ASSESSMENT OF THE HIP:' row found in 'Report' or 'NEW Datavis' worksheet for sheet ID {sheet_id}.")
        return hip_assessment
    
    hip_assessment_existing = extract_hip_report_text(sheet_id)
    
    # Generate concise input
    concise_input = TextGen_Hip_Concise(sheet_id)
    
    # Combine all summaries into final hip assessment including deficit summary
    final_hip_assessment = f"{hip_flexion_summary}. {hip_extension_summary}. {hip_abduction_summary}. {hip_adduction_summary}. {hip_ext_rotation_summary}. {hip_int_rotation_summary}. {deficit_summary}"
    
    # Overall asymmetry assessment
    asymmetries = [
        hip_flexion_range_asymmetry, hip_extension_range_asymmetry, hip_abduction_range_asymmetry,
        hip_adduction_range_asymmetry, hip_ext_rotation_range_asymmetry, hip_int_rotation_range_asymmetry,
        hip_flexion_force_asymmetry, hip_extension_force_asymmetry, hip_abduction_force_asymmetry,
        hip_adduction_force_asymmetry, hip_ext_rotation_force_asymmetry, hip_int_rotation_force_asymmetry
    ]
    
    overall_asymmetry = "Asymmetry detected" if "Asymmetry detected" in [str(a) for a in asymmetries] else "Symmetrical"
    
    return (
        final_hip_assessment,
        hip_assessment_existing,
        overall_asymmetry,
        {
            'flexion': hip_flexion_summary,
            'extension': hip_extension_summary,
            'abduction': hip_abduction_summary,
            'adduction': hip_adduction_summary,
            'external_rotation': hip_ext_rotation_summary,
            'internal_rotation': hip_int_rotation_summary
        },
        deficit_summary,  # New return value for deficit summary
        {
            'Lacking Range on right': lacking_range_right,
            'Lacking Strength on right': lacking_strength_right,
            'Lacking Range on left': lacking_range_left,
            'Lacking Strength on left': lacking_strength_left
        },
        largest_movement_summary,
        concise_input  # Add concise input as the last return value
    )
def evaluate_hamstring_quad_ratio(knee_flexion_force_left, knee_extension_force_left, 
                                 knee_flexion_force_right, knee_extension_force_right):
    """
    Evaluate hamstring to quadriceps ratio for both left and right sides
    
    Parameters:
    - knee_flexion_force_left: Left knee flexion force (hamstring)
    - knee_extension_force_left: Left knee extension force (quadriceps)
    - knee_flexion_force_right: Right knee flexion force (hamstring)
    - knee_extension_force_right: Right knee extension force (quadriceps)
    
    Returns:
    - Dictionary with left and right H:Q ratios and classifications
    """
    
    def calculate_hq_ratio_single_side(flexion_force, extension_force, side):
        """
        Calculate H:Q ratio for a single side
        """
        try:
            # Convert to float if needed
            flexion_val = float(flexion_force) if flexion_force is not None else 0
            extension_val = float(extension_force) if extension_force is not None else 0
            
            # Apply multipliers
            # Flexion (hamstring) * 0.31
            adjusted_flexion = flexion_val 
            # Extension (quadriceps) * 0.71  
            adjusted_extension = extension_val 
            
            # Check valid input
            if adjusted_flexion <= 0 or adjusted_extension <= 0:
                return {
                    'ratio': None,
                    'classification': f"Invalid: {side} forces must be positive",
                    'adjusted_flexion': adjusted_flexion,
                    'adjusted_extension': adjusted_extension,
                    'original_flexion': flexion_val,
                    'original_extension': extension_val
                }
            
            # Calculate H:Q ratio
            ratio = adjusted_flexion / adjusted_extension
            
            # Classify ratio
            if ratio < 0.55:
                ratio_class = "Poor"
            elif 0.55 <= ratio <= 0.75:
                ratio_class = "Good"
            else:  # ratio > 0.75
                # Strength benchmarks
                QUAD_THRESHOLD = 200/9.81   # Apply multiplier to threshold
                HAM_THRESHOLD = 120/9.81    # Apply multiplier to threshold
                
                if adjusted_extension < QUAD_THRESHOLD:
                    ratio_class = "High Ratio due to Weak Quadriceps"
                elif adjusted_flexion > HAM_THRESHOLD * 1.2:  # 20% above normal benchmark
                    ratio_class = "High Ratio due to Strong Hamstrings"
                else:
                    ratio_class = "High Ratio – Mixed Cause"
            
            return {
                'ratio': round(ratio, 3),
                'classification': ratio_class,
                'adjusted_flexion': round(adjusted_flexion, 2),
                'adjusted_extension': round(adjusted_extension, 2),
                'original_flexion': flexion_val,
                'original_extension': extension_val
            }
            
        except (ValueError, TypeError, ZeroDivisionError):
            return {
                'ratio': None,
                'classification': f"Error: Invalid {side} input data",
                'adjusted_flexion': None,
                'adjusted_extension': None,
                'original_flexion': flexion_force,
                'original_extension': extension_force
            }
    
    # Calculate for both sides
    left_result = calculate_hq_ratio_single_side(knee_flexion_force_left, knee_extension_force_left, "Left")
    right_result = calculate_hq_ratio_single_side(knee_flexion_force_right, knee_extension_force_right, "Right")
    
    # Calculate bilateral comparison if both sides are valid
    bilateral_comparison = ""
    if left_result['ratio'] is not None and right_result['ratio'] is not None:
        left_ratio = left_result['ratio']
        right_ratio = right_result['ratio']
        
        if left_ratio > right_ratio:
            difference = left_ratio - right_ratio
            percentage_diff = (difference / right_ratio * 100) if right_ratio != 0 else 0
            bilateral_comparison = f"Left H:Q ratio {percentage_diff:.1f}% higher than right"
        elif right_ratio > left_ratio:
            difference = right_ratio - left_ratio
            percentage_diff = (difference / left_ratio * 100) if left_ratio != 0 else 0
            bilateral_comparison = f"Right H:Q ratio {percentage_diff:.1f}% higher than left"
        else:
            bilateral_comparison = "Left and right H:Q ratios are equal"
    else:
        bilateral_comparison = "Cannot compare - missing or invalid data"

    
    
    return {
        'left': left_result,
        'right': right_result,
        'bilateral_comparison': bilateral_comparison

    }

def format_hq_ratio_report(hq_results):
    """
    Format the H:Q ratio results into a readable report
    """
    report_lines = []
    
    report_lines.append("Hamstring to Quadriceps (H:Q) Ratio Analysis:")
    report_lines.append("=" * 50)
    report_lines.append("")
    
    # Left side
    left = hq_results['left']
    report_lines.append("LEFT SIDE:")
    if left['ratio'] is not None:
        # report_lines.append(f"   Flexion Force Percentage: {left['original_flexion']}")
        # report_lines.append(f"   Extension Force Percentage: {left['original_extension']}")
        # report_lines.append(f"   Flexion Force: {left['adjusted_flexion']}")
        # report_lines.append(f"   Extension Force: {left['adjusted_extension']}")
        report_lines.append(f"   Hamstring to Quadriceps Ratio: {left['ratio']}")
        report_lines.append(f"   Classification: {left['classification']}")
    else:
        report_lines.append(f"  {left['classification']}")
    report_lines.append("")
    
    # Right side
    right = hq_results['right']
    report_lines.append("RIGHT SIDE:")
    if right['ratio'] is not None:
        # report_lines.append(f"  Flexion Force Percentage: {right['original_flexion']}")
        # report_lines.append(f"  Extension Force Percentage: {right['original_extension']}")
        # report_lines.append(f"  Flexion Force: {right['adjusted_flexion']}")
        # report_lines.append(f"  Extension Force: {right['adjusted_extension']}")
        report_lines.append(f"  Hamstring to Quadriceps Ratio: {right['ratio']}")
        report_lines.append(f"  Classification: {right['classification']}")
    else:
        report_lines.append(f"  {right['classification']}")
    report_lines.append("")
    
    # Bilateral comparison
    report_lines.append("BILATERAL COMPARISON:")
    report_lines.append(f"  {hq_results['bilateral_comparison']}")
    report_lines.append("")
    
    return "\n".join(report_lines)

def TextGen_Knee_HQ_Ratio(sheet_id,data_overview_sheet):
    """
    Generate H:Q ratio analysis for knee assessment
    """
    # Get knee metrics
    (
    knee_flexion_range_left,
    knee_flexion_range_right,
    knee_extension_range_left,
    knee_extension_range_right,
    knee_flexion_force_left,
    knee_flexion_force_right,
    knee_extension_force_left,
    knee_extension_force_right,
    knee_flexion_force_left_original,
    knee_flexion_force_right_original,
    knee_extension_force_left_original,
    knee_extension_force_right_original,
    knee_hamstring_quad_ratio_left,
    knee_hamstring_quad_ratio_right
    ) = extract_sheet_metrics_knee(sheet_id,data_overview_sheet)

    # Calculate H:Q ratios
    hq_results = evaluate_hamstring_quad_ratio(
        knee_flexion_force_left_original, knee_extension_force_left_original,
        knee_flexion_force_right_original, knee_extension_force_right_original
    )
    
    # Generate formatted report
    formatted_report = format_hq_ratio_report(hq_results)
    
    return hq_results, formatted_report

def extract_knee_report_text(sheet_id):
    """
    Extract knee assessment text from the Report or NEW Datavis worksheet
    """
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    from google.oauth2.service_account import Credentials
    import gspread
    
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(sheet_id)
    report_worksheet = None
    try:
        report_worksheet = sheet.worksheet('Report')
    except gspread.WorksheetNotFound:
        try:
            report_worksheet = sheet.worksheet('NEW Datavis')
        except gspread.WorksheetNotFound:
            print("Neither 'Report' nor 'New Datavis' worksheet found.")
    
    knee_assessment = None
    if report_worksheet:
        for row in report_worksheet.get_all_values():
            if len(row) > 1 and 'ASSESSMENT OF THE KNEE:' in row[1]:
                knee_assessment = row[1].split('ASSESSMENT OF THE KNEE:')[1].strip()
                break
        if knee_assessment is None:
            print(f"No 'ASSESSMENT OF THE KNEE:' row found in 'Report' or 'NEW Datavis' worksheet for sheet ID {sheet_id}.")
    return knee_assessment

def extract_sheet_metrics_shoulder(sheet_id, data_overview_sheet):
    # # Call the main extraction function
    # scopes = [
    #     'https://www.googleapis.com/auth/spreadsheets',
    #     'https://www.googleapis.com/auth/drive'
    # ]

    # creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    # client = gspread.authorize(creds)

    # # Open the Google Sheet
    # sheet = client.open_by_key(sheet_id)
    # # search sheet with the name 'Data Overview'
    # data_overview_sheet = sheet.worksheet("Data Overview")
    # Extract data from the worksheet
    all_values = data_overview_sheet.get_all_values()

    # Shoulder parameter strings
    shoulder_external_rotation_range = "External Rotation Range"
    shoulder_internal_rotation_range = "Internal Rotation Range"
    shoulder_flexion_range = "Flexion Range"
    shoulder_extension_range = "Extension Range"
    shoulder_external_rotation_force = "External Rotation Force"
    shoulder_internal_rotation_force = "Internal Rotation Force"
    shoulder_flexion_force = "Flexion Force"
    shoulder_iso_i = 'Shoulder "I" ISO'
    shoulder_iso_y = 'Shoulder "Y" ISO'
    shoulder_iso_t = 'Shoulder "T" ISO'
    shoulder_iso_i_alt = 'Shoulder ISO "I"'
    shoulder_iso_y_alt = 'Shoulder ISO "Y"'
    shoulder_iso_t_alt = 'Shoulder ISO "T"'

    # search for strings in row "SHOULDER" "LEFT" "RIGHT" and "GS" if all these strings are present in row array then store its index
    shoulder_index = None
    left_index = None
    right_index = None
    gs_index = None
    
    for i, row in enumerate(all_values):
        if "SHOULDER" in row and "LEFT" in row and "RIGHT" in row and "GS" in row:
            shoulder_index = i
            left_index = row.index("LEFT")
            right_index = row.index("RIGHT")
            gs_index = row.index("GS")
            print(f"Found SHOULDER row at index {shoulder_index}")
            print(f"LEFT at column {left_index}, RIGHT at column {right_index}, GS at column {gs_index}")
            break
    else:
        print("SHOULDER section not found")
        return tuple(["unavailable data"] * 26)  # Return 26 "unavailable data" values
    
    # Initialize shoulder measurement variables
    shoulder_ext_rotation_range_left = shoulder_ext_rotation_range_right = None
    shoulder_int_rotation_range_left = shoulder_int_rotation_range_right = None
    shoulder_flexion_range_left = shoulder_flexion_range_right = None
    shoulder_extension_range_left = shoulder_extension_range_right = None
    shoulder_ext_rotation_force_left = shoulder_ext_rotation_force_right = None
    shoulder_int_rotation_force_left = shoulder_int_rotation_force_right = None
    shoulder_flexion_force_left = shoulder_flexion_force_right = None
    shoulder_i_iso_left = shoulder_i_iso_right = None
    shoulder_y_iso_left = shoulder_y_iso_right = None
    shoulder_t_iso_left = shoulder_t_iso_right = None
    shoulder_i_iso_alt_left = shoulder_i_iso_alt_right = None
    shoulder_y_iso_alt_left = shoulder_y_iso_alt_right = None
    shoulder_t_iso_alt_left = shoulder_t_iso_alt_right = None

    # Only search from shoulder_index onwards
    search_rows = all_values[shoulder_index:] if shoulder_index is not None else all_values

    # Search for External Rotation Range
    ext_rotation_range_row = next((i for i, row in enumerate(search_rows) if shoulder_external_rotation_range in row), None)
    if ext_rotation_range_row is not None:
        ext_rotation_range_values = search_rows[ext_rotation_range_row]
        shoulder_ext_rotation_range_left = ext_rotation_range_values[left_index] if len(ext_rotation_range_values) > left_index else "unavailable data"
        shoulder_ext_rotation_range_right = ext_rotation_range_values[right_index] if len(ext_rotation_range_values) > right_index else "unavailable data"
        print(f"External Rotation Range - Left: {shoulder_ext_rotation_range_left}, Right: {shoulder_ext_rotation_range_right}")
    else:
        shoulder_ext_rotation_range_left = shoulder_ext_rotation_range_right = "unavailable data"

    # Search for Internal Rotation Range
    int_rotation_range_row = next((i for i, row in enumerate(search_rows) if shoulder_internal_rotation_range in row), None)
    if int_rotation_range_row is not None:
        int_rotation_range_values = search_rows[int_rotation_range_row]
        shoulder_int_rotation_range_left = int_rotation_range_values[left_index] if len(int_rotation_range_values) > left_index else "unavailable data"
        shoulder_int_rotation_range_right = int_rotation_range_values[right_index] if len(int_rotation_range_values) > right_index else "unavailable data"
        print(f"Internal Rotation Range - Left: {shoulder_int_rotation_range_left}, Right: {shoulder_int_rotation_range_right}")
    else:
        shoulder_int_rotation_range_left = shoulder_int_rotation_range_right = "unavailable data"

    # Search for Flexion Range
    flexion_range_row = next((i for i, row in enumerate(search_rows) if shoulder_flexion_range in row), None)
    if flexion_range_row is not None:
        flexion_range_values = search_rows[flexion_range_row]
        shoulder_flexion_range_left = flexion_range_values[left_index] if len(flexion_range_values) > left_index else "unavailable data"
        shoulder_flexion_range_right = flexion_range_values[right_index] if len(flexion_range_values) > right_index else "unavailable data"
        print(f"Flexion Range - Left: {shoulder_flexion_range_left}, Right: {shoulder_flexion_range_right}")
    else:
        shoulder_flexion_range_left = shoulder_flexion_range_right = "unavailable data"

    # Search for Extension Range
    extension_range_row = next((i for i, row in enumerate(search_rows) if shoulder_extension_range in row), None)
    if extension_range_row is not None:
        extension_range_values = search_rows[extension_range_row]
        shoulder_extension_range_left = extension_range_values[left_index] if len(extension_range_values) > left_index else "unavailable data"
        shoulder_extension_range_right = extension_range_values[right_index] if len(extension_range_values) > right_index else "unavailable data"
        print(f"Extension Range - Left: {shoulder_extension_range_left}, Right: {shoulder_extension_range_right}")
    else:
        shoulder_extension_range_left = shoulder_extension_range_right = "unavailable data"

    # Search for External Rotation Force
    ext_rotation_force_row = next((i for i, row in enumerate(search_rows) if shoulder_external_rotation_force in row), None)
    if ext_rotation_force_row is not None:
        ext_rotation_force_values = search_rows[ext_rotation_force_row]
        shoulder_ext_rotation_force_left = ext_rotation_force_values[left_index] if len(ext_rotation_force_values) > left_index else "unavailable data"
        shoulder_ext_rotation_force_right = ext_rotation_force_values[right_index] if len(ext_rotation_force_values) > right_index else "unavailable data"
        print(f"External Rotation Force - Left: {shoulder_ext_rotation_force_left}, Right: {shoulder_ext_rotation_force_right}")
    else:
        shoulder_ext_rotation_force_left = shoulder_ext_rotation_force_right = "unavailable data"

    # Search for Internal Rotation Force
    int_rotation_force_row = next((i for i, row in enumerate(search_rows) if shoulder_internal_rotation_force in row), None)
    if int_rotation_force_row is not None:
        int_rotation_force_values = search_rows[int_rotation_force_row]
        shoulder_int_rotation_force_left = int_rotation_force_values[left_index] if len(int_rotation_force_values) > left_index else "unavailable data"
        shoulder_int_rotation_force_right = int_rotation_force_values[right_index] if len(int_rotation_force_values) > right_index else "unavailable data"
        print(f"Internal Rotation Force - Left: {shoulder_int_rotation_force_left}, Right: {shoulder_int_rotation_force_right}")
    else:
        shoulder_int_rotation_force_left = shoulder_int_rotation_force_right = "unavailable data"

    # Search for Flexion Force
    flexion_force_row = next((i for i, row in enumerate(search_rows) if shoulder_flexion_force in row), None)
    if flexion_force_row is not None:
        flexion_force_values = search_rows[flexion_force_row]
        shoulder_flexion_force_left = flexion_force_values[left_index] if len(flexion_force_values) > left_index else "unavailable data"
        shoulder_flexion_force_right = flexion_force_values[right_index] if len(flexion_force_values) > right_index else "unavailable data"
        print(f"Flexion Force - Left: {shoulder_flexion_force_left}, Right: {shoulder_flexion_force_right}")
    else:
        shoulder_flexion_force_left = shoulder_flexion_force_right = "unavailable data"

    # Search for Shoulder "I" ISO
    i_iso_row = next((i for i, row in enumerate(search_rows) if shoulder_iso_i in row), None)
    if i_iso_row is not None:
        i_iso_values = search_rows[i_iso_row]
        shoulder_i_iso_left = i_iso_values[left_index] if len(i_iso_values) > left_index else "unavailable data"
        shoulder_i_iso_right = i_iso_values[right_index] if len(i_iso_values) > right_index else "unavailable data"
        print(f'Shoulder "I" ISO - Left: {shoulder_i_iso_left}, Right: {shoulder_i_iso_right}')
    else:
        shoulder_i_iso_left = shoulder_i_iso_right = "unavailable data"

    # Search for Shoulder "Y" ISO
    y_iso_row = next((i for i, row in enumerate(search_rows) if shoulder_iso_y in row), None)
    if y_iso_row is not None:
        y_iso_values = search_rows[y_iso_row]
        shoulder_y_iso_left = y_iso_values[left_index] if len(y_iso_values) > left_index else "unavailable data"
        shoulder_y_iso_right = y_iso_values[right_index] if len(y_iso_values) > right_index else "unavailable data"
        print(f'Shoulder "Y" ISO - Left: {shoulder_y_iso_left}, Right: {shoulder_y_iso_right}')
    else:
        shoulder_y_iso_left = shoulder_y_iso_right = "unavailable data"

    # Search for Shoulder "T" ISO
    t_iso_row = next((i for i, row in enumerate(search_rows) if shoulder_iso_t in row), None)
    if t_iso_row is not None:
        t_iso_values = search_rows[t_iso_row]
        shoulder_t_iso_left = t_iso_values[left_index] if len(t_iso_values) > left_index else "unavailable data"
        shoulder_t_iso_right = t_iso_values[right_index] if len(t_iso_values) > right_index else "unavailable data"
        print(f'Shoulder "T" ISO - Left: {shoulder_t_iso_left}, Right: {shoulder_t_iso_right}')
    else:
        shoulder_t_iso_left = shoulder_t_iso_right = "unavailable data"

    # Search for Shoulder ISO "I" (alternative format)
    i_iso_alt_row = next((i for i, row in enumerate(search_rows) if shoulder_iso_i_alt in row), None)
    if i_iso_alt_row is not None:
        i_iso_alt_values = search_rows[i_iso_alt_row]
        shoulder_i_iso_alt_left = i_iso_alt_values[left_index] if len(i_iso_alt_values) > left_index else "unavailable data"
        shoulder_i_iso_alt_right = i_iso_alt_values[right_index] if len(i_iso_alt_values) > right_index else "unavailable data"
        print(f'Shoulder ISO "I" - Left: {shoulder_i_iso_alt_left}, Right: {shoulder_i_iso_alt_right}')
    else:
        shoulder_i_iso_alt_left = shoulder_i_iso_alt_right = "unavailable data"

    # Search for Shoulder ISO "Y" (alternative format)
    y_iso_alt_row = next((i for i, row in enumerate(search_rows) if shoulder_iso_y_alt in row), None)
    if y_iso_alt_row is not None:
        y_iso_alt_values = search_rows[y_iso_alt_row]
        shoulder_y_iso_alt_left = y_iso_alt_values[left_index] if len(y_iso_alt_values) > left_index else "unavailable data"
        shoulder_y_iso_alt_right = y_iso_alt_values[right_index] if len(y_iso_alt_values) > right_index else "unavailable data"
        print(f'Shoulder ISO "Y" - Left: {shoulder_y_iso_alt_left}, Right: {shoulder_y_iso_alt_right}')
    else:
        shoulder_y_iso_alt_left = shoulder_y_iso_alt_right = "unavailable data"

    # Search for Shoulder ISO "T" (alternative format)
    t_iso_alt_row = next((i for i, row in enumerate(search_rows) if shoulder_iso_t_alt in row), None)
    if t_iso_alt_row is not None:
        t_iso_alt_values = search_rows[t_iso_alt_row]
        shoulder_t_iso_alt_left = t_iso_alt_values[left_index] if len(t_iso_alt_values) > left_index else "unavailable data"
        shoulder_t_iso_alt_right = t_iso_alt_values[right_index] if len(t_iso_alt_values) > right_index else "unavailable data"
        print(f'Shoulder ISO "T" - Left: {shoulder_t_iso_alt_left}, Right: {shoulder_t_iso_alt_right}')
    else:
        shoulder_t_iso_alt_left = shoulder_t_iso_alt_right = "unavailable data"
    shoulder_i_iso_left_final = None
    shoulder_i_iso_right_final = None
    shoulder_y_iso_left_final = None
    shoulder_y_iso_right_final = None
    shoulder_t_iso_left_final = None
    shoulder_t_iso_right_final = None

    # check if shoulder_t_iso_alt_left
    if shoulder_t_iso_alt_left != "unavailable data":
        shoulder_t_iso_left_final = shoulder_t_iso_alt_left
    elif shoulder_t_iso_left != "unavailable data":
        shoulder_t_iso_left_final = shoulder_t_iso_left
    else:
        shoulder_t_iso_left_final = "unavailable data"
    
    if shoulder_t_iso_alt_right != "unavailable data":
        shoulder_t_iso_right_final = shoulder_t_iso_alt_right
    elif shoulder_t_iso_right != "unavailable data":
        shoulder_t_iso_right_final = shoulder_t_iso_right
    else:
        shoulder_t_iso_right_final = "unavailable data"

    # check if shoulder_i_iso_alt_left
    if shoulder_i_iso_alt_left != "unavailable data":
        shoulder_i_iso_left_final = shoulder_i_iso_alt_left
    elif shoulder_i_iso_left != "unavailable data":
        shoulder_i_iso_left_final = shoulder_i_iso_left
    else:
        shoulder_i_iso_left_final = "unavailable data"

    if shoulder_i_iso_alt_right != "unavailable data":
        shoulder_i_iso_right_final = shoulder_i_iso_alt_right
    elif shoulder_i_iso_right != "unavailable data":
        shoulder_i_iso_right_final = shoulder_i_iso_right
    else:
        shoulder_i_iso_right_final = "unavailable data"

    # check if shoulder_y_iso_alt_left
    if shoulder_y_iso_alt_left != "unavailable data":
        shoulder_y_iso_left_final = shoulder_y_iso_alt_left
    elif shoulder_y_iso_left != "unavailable data":
        shoulder_y_iso_left_final = shoulder_y_iso_left
    else:
        shoulder_y_iso_left_final = "unavailable data"

    if shoulder_y_iso_alt_right != "unavailable data":
        shoulder_y_iso_right_final = shoulder_y_iso_alt_right
    elif shoulder_y_iso_right != "unavailable data":
        shoulder_y_iso_right_final = shoulder_y_iso_right
    else:
        shoulder_y_iso_right_final = "unavailable data"

    
    

    return (
        shoulder_ext_rotation_range_left,
        shoulder_ext_rotation_range_right,
        shoulder_int_rotation_range_left,
        shoulder_int_rotation_range_right,
        shoulder_flexion_range_left,
        shoulder_flexion_range_right,
        shoulder_extension_range_left,
        shoulder_extension_range_right,
        shoulder_ext_rotation_force_left,
        shoulder_ext_rotation_force_right,
        shoulder_int_rotation_force_left,
        shoulder_int_rotation_force_right,
        shoulder_flexion_force_left,
        shoulder_flexion_force_right,
        shoulder_i_iso_left_final,
        shoulder_i_iso_right_final,
        shoulder_y_iso_left_final,
        shoulder_y_iso_right_final,
        shoulder_t_iso_left_final,
        shoulder_t_iso_right_final
    )



def TextGen_Shoulder_Concise(sheet_id, data_overview_sheet):
    """
    Generate concise shoulder assessment input prompt in new format
    """
    (
        shoulder_ext_rotation_range_left,
        shoulder_ext_rotation_range_right,
        shoulder_int_rotation_range_left,
        shoulder_int_rotation_range_right,
        shoulder_flexion_range_left,
        shoulder_flexion_range_right,
        shoulder_extension_range_left,
        shoulder_extension_range_right,
        shoulder_ext_rotation_force_left,
        shoulder_ext_rotation_force_right,
        shoulder_int_rotation_force_left,
        shoulder_int_rotation_force_right,
        shoulder_flexion_force_left,
        shoulder_flexion_force_right,
        shoulder_i_iso_left_final,
        shoulder_i_iso_right_final,
        shoulder_y_iso_left_final,
        shoulder_y_iso_right_final,
        shoulder_t_iso_left_final,
        shoulder_t_iso_right_final
    ) = extract_sheet_metrics_shoulder(sheet_id, data_overview_sheet)

    def format_shoulder_value(value_str):
        """Format shoulder value with new compact notation"""
        try:
            if value_str is None or value_str == '' or value_str == 'unavailable data':
                return None
            
            percentage = float(value_str)
            
            if percentage > 100:
                above_percentage = percentage - 100
                return f"above gold standard (+{above_percentage:.1f}%)"
            elif percentage >= 85:
                reduction_percentage = 100 - percentage
                return f"good, below gold standard ({reduction_percentage:.1f}%)"
            else:
                reduction_percentage = 100 - percentage
                return f"notable reduction (-{reduction_percentage:.1f}%)"
                
        except (ValueError, TypeError):
            return None
    
    def calculate_asymmetry(left_val, right_val):
        """Calculate asymmetry with new format"""
        try:
            if (left_val is None or left_val == 'unavailable data' or 
                right_val is None or right_val == 'unavailable data'):
                return None
                
            left_num = float(left_val)
            right_num = float(right_val)
            
            if abs(left_num - right_num) < 0.1:  # Essentially equal
                return "Equal bilateral"
            elif left_num > right_num:
                percentage_diff = ((left_num - right_num) / right_num * 100)
                return f"Left > Right (+{percentage_diff:.1f}%)"
            else:
                percentage_diff = ((right_num - left_num) / left_num * 100)
                return f"Right > Left (+{percentage_diff:.1f}%)"
                
        except (ValueError, TypeError, ZeroDivisionError):
            return None
    
    def calculate_opposing_asymmetry(val1_left, val1_right, val2_left, val2_right, name1, name2):
        """Calculate opposing movement asymmetries"""
        comparisons = []
        
        # Left side
        try:
            if (val1_left is not None and val1_left != 'unavailable data' and 
                val2_left is not None and val2_left != 'unavailable data'):
                
                v1 = float(val1_left)
                v2 = float(val2_left)
                
                if v1 > v2:
                    diff = ((v1 - v2) / v2 * 100)
                    comparisons.append(f"Left: {name1} > {name2} (+{diff:.1f}%)")
                elif v2 > v1:
                    diff = ((v2 - v1) / v1 * 100)
                    comparisons.append(f"Left: {name2} > {name1} (+{diff:.1f}%)")
                else:
                    comparisons.append(f"Left: {name1} = {name2}")
        except (ValueError, TypeError, ZeroDivisionError):
            pass
        
        # Right side
        try:
            if (val1_right is not None and val1_right != 'unavailable data' and 
                val2_right is not None and val2_right != 'unavailable data'):
                
                v1 = float(val1_right)
                v2 = float(val2_right)
                
                if v1 > v2:
                    diff = ((v1 - v2) / v2 * 100)
                    comparisons.append(f"Right: {name1} > {name2} (+{diff:.1f}%)")
                elif v2 > v1:
                    diff = ((v2 - v1) / v1 * 100)
                    comparisons.append(f"Right: {name2} > {name1} (+{diff:.1f}%)")
                else:
                    comparisons.append(f"Right: {name1} = {name2}")
        except (ValueError, TypeError, ZeroDivisionError):
            pass
        
        return comparisons
    
    # Build the new format
    lines = []
    lines.append("Shoulder Assessment:")
    lines.append("")
    
    # Track deficits
    left_deficits = []
    right_deficits = []
    
    # Helper function to add movement section
    def add_movement_section(name, left_val, right_val, force_name=None):
        left_formatted = format_shoulder_value(left_val)
        right_formatted = format_shoulder_value(right_val)
        
        if left_formatted is None and right_formatted is None:
            return
        
        lines.append(f"{name}:")
        
        if left_formatted:
            lines.append(f"  Left: {left_formatted}")
            # Track deficits
            try:
                if float(left_val) < 85:
                    deficit_name = force_name if force_name else name
                    left_deficits.append(deficit_name)
            except (ValueError, TypeError):
                pass
        
        if right_formatted:
            lines.append(f"  Right: {right_formatted}")
            # Track deficits
            try:
                if float(right_val) < 85:
                    deficit_name = force_name if force_name else name
                    right_deficits.append(deficit_name)
            except (ValueError, TypeError):
                pass
        
        asymmetry = calculate_asymmetry(left_val, right_val)
        if asymmetry:
            if asymmetry == "Equal bilateral":
                lines.append(f"  Comparison: {asymmetry}")
            else:
                lines.append(f"  Asymmetry: {asymmetry}")
        
        lines.append("")
    
    # Add range movements
    add_movement_section("External Rotation", shoulder_ext_rotation_range_left, shoulder_ext_rotation_range_right)
    add_movement_section("Internal Rotation", shoulder_int_rotation_range_left, shoulder_int_rotation_range_right)
    add_movement_section("Flexion", shoulder_flexion_range_left, shoulder_flexion_range_right)
    add_movement_section("Extension", shoulder_extension_range_left, shoulder_extension_range_right)
    
    # Add force movements (if available)
    if (shoulder_ext_rotation_force_left != 'unavailable data' or shoulder_ext_rotation_force_right != 'unavailable data'):
        add_movement_section("External Rotation Force", shoulder_ext_rotation_force_left, shoulder_ext_rotation_force_right, "External Rotation")
    
    if (shoulder_int_rotation_force_left != 'unavailable data' or shoulder_int_rotation_force_right != 'unavailable data'):
        add_movement_section("Internal Rotation Force", shoulder_int_rotation_force_left, shoulder_int_rotation_force_right, "Internal Rotation")
    
    if (shoulder_flexion_force_left != 'unavailable data' or shoulder_flexion_force_right != 'unavailable data'):
        add_movement_section("Flexion Force", shoulder_flexion_force_left, shoulder_flexion_force_right, "Flexion")
    
    # Add ISO tests (if available)
    if (shoulder_i_iso_left_final != 'unavailable data' or shoulder_i_iso_right_final != 'unavailable data'):
        add_movement_section('Shoulder "I" ISO', shoulder_i_iso_left_final, shoulder_i_iso_right_final, 'Shoulder "I"')
    
    if (shoulder_y_iso_left_final != 'unavailable data' or shoulder_y_iso_right_final != 'unavailable data'):
        add_movement_section('Shoulder "Y" ISO', shoulder_y_iso_left_final, shoulder_y_iso_right_final, 'Shoulder "Y"')
    
    if (shoulder_t_iso_left_final != 'unavailable data' or shoulder_t_iso_right_final != 'unavailable data'):
        add_movement_section('Shoulder "T" ISO', shoulder_t_iso_left_final, shoulder_t_iso_right_final, 'Shoulder "T"')
    
    # Opposing Comparisons
    lines.append("Opposing Comparisons:")
    
    # Flexion vs Extension
    flex_ext_comparisons = calculate_opposing_asymmetry(
        shoulder_flexion_range_left, shoulder_flexion_range_right,
        shoulder_extension_range_left, shoulder_extension_range_right,
        "Flexion", "Extension"
    )
    if flex_ext_comparisons:
        lines.append("  Flexion vs Extension:")
        for comp in flex_ext_comparisons:
            lines.append(f"    {comp}")
        lines.append("")
    
    # Rotation comparisons
    rotation_comparisons = calculate_opposing_asymmetry(
        shoulder_ext_rotation_range_left, shoulder_ext_rotation_range_right,
        shoulder_int_rotation_range_left, shoulder_int_rotation_range_right,
        "External", "Internal"
    )
    if rotation_comparisons:
        lines.append("  Rotation:")
        for comp in rotation_comparisons:
            lines.append(f"    {comp}")
        lines.append("")
    
    # Force rotation comparisons (if available)
    if (shoulder_ext_rotation_force_left != 'unavailable data' or shoulder_int_rotation_force_left != 'unavailable data'):
        force_rotation_comparisons = calculate_opposing_asymmetry(
            shoulder_ext_rotation_force_left, shoulder_ext_rotation_force_right,
            shoulder_int_rotation_force_left, shoulder_int_rotation_force_right,
            "External", "Internal"
        )
        if force_rotation_comparisons:
            lines.append("  Rotation Force:")
            for comp in force_rotation_comparisons:
                lines.append(f"    {comp}")
            lines.append("")
    
    # Deficits
    lines.append("Deficits (<85% GS):")
    if left_deficits:
        lines.append(f"  Left: {', '.join(left_deficits)}")
    if right_deficits:
        lines.append(f"  Right: {', '.join(right_deficits)}")
    
    if not left_deficits and not right_deficits:
        lines.append("  None identified")
    
    return "\n".join(lines)


def extract_shoulder_report_text(sheet_id):
    """
    Extract shoulder assessment text from the Report or NEW Datavis worksheet
    """
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    from google.oauth2.service_account import Credentials
    import gspread
    
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(sheet_id)
    report_worksheet = None
    try:
        report_worksheet = sheet.worksheet('Report')
    except gspread.WorksheetNotFound:
        try:
            report_worksheet = sheet.worksheet('NEW Datavis')
        except gspread.WorksheetNotFound:
            print("Neither 'Report' nor 'New Datavis' worksheet found.")
    
    shoulder_assessment = None
    if report_worksheet:
        for row in report_worksheet.get_all_values():
            if len(row) > 1 and 'ASSESSMENT OF THE SHOULDER:' in row[1]:
                shoulder_assessment = row[1].split('ASSESSMENT OF THE SHOULDER:')[1].strip()
                break
        if shoulder_assessment is None:
            print(f"No 'ASSESSMENT OF THE SHOULDER:' row found in 'Report' or 'NEW Datavis' worksheet for sheet ID {sheet_id}.")
    return shoulder_assessment




def create_radar_chart_foot_ankle(sheet_id, data_overview_sheet, second_worksheet, save_path=None):
    """
    Create radar chart for foot and ankle assessment
    """
    # Extract foot ankle metrics
    (
        dorsiflexion_range_left,
        dorsiflexion_range_right,
        plantarflexion_range_left,
        plantarflexion_range_right,
        dorsiflexion_force_left,
        dorsiflexion_force_right,
        plantarflexion_force_left,
        plantarflexion_force_right,
        weight_distribution_question_left,
        weight_distribution_question_right,
        weight_distribution_question_note,
        supination_tripod_question_left,
        supination_tripod_question_right,
        supination_tripod_question_note,
        pronation_tripod_question_left,
        pronation_tripod_question_right,
        pronation_tripod_question_note,
        big_toe_independence_question_left,
        big_toe_independence_question_right,
        big_toe_independence_question_note,
        lesser_toes_independence_question_left,
        lesser_toes_independence_question_right,
        lesser_toes_independence_question_note,
        center_of_mass_rest_left,
        center_of_mass_rest_right,
        center_of_mass_rest_note,
        center_of_mass_pronated_left,
        center_of_mass_pronated_right,
        center_of_mass_pronated_note
    ) = extract_sheet_metrics_footankle(sheet_id, data_overview_sheet, second_worksheet)

    def safe_float_convert(value):
        """Convert value to float, return 0 if conversion fails"""
        try:
            if value is None or value == '' or value == 'unavailable data':
                return 0
            return float(value)
        except (ValueError, TypeError):
            return 0
    
    # Movement names for foot ankle
    movement_names = [
        'Dorsiflexion Range',
        'Plantarflexion Range', 
        'Dorsiflexion Force',
        'Plantarflexion Force'
    ]
    
    # Create arrays
    left_values = [
        safe_float_convert(dorsiflexion_range_left),
        safe_float_convert(plantarflexion_range_left),
        safe_float_convert(dorsiflexion_force_left),
        safe_float_convert(plantarflexion_force_left)
    ]
    
    right_values = [
        safe_float_convert(dorsiflexion_range_right),
        safe_float_convert(plantarflexion_range_right),
        safe_float_convert(dorsiflexion_force_right),
        safe_float_convert(plantarflexion_force_right)
    ]
    
    # Gold standard array (100 for each movement)
    gold_standard = [100] * len(movement_names)
    
    # Create the radar chart
    fig = create_radar_chart(
        gold_standard=gold_standard,
        left=left_values,
        right=right_values,
        movement_names=movement_names,
        title="Foot & Ankle Assessment",
        save_path=save_path
    )
    
    return fig

def create_radar_chart_knee(sheet_id, data_overview_sheet, save_path=None):
    """
    Create radar chart for knee assessment (excluding hamstring/quad strength)
    """
    # Extract knee metrics
    (
        knee_flexion_range_left,
        knee_flexion_range_right,
        knee_extension_range_left,
        knee_extension_range_right,
        knee_flexion_force_left,
        knee_flexion_force_right,
        knee_extension_force_left,
        knee_extension_force_right,
        knee_flexion_force_left_original,
        knee_flexion_force_right_original,
        knee_extension_force_left_original,
        knee_extension_force_right_original,
        knee_hamstring_quad_ratio_left,
        knee_hamstring_quad_ratio_right
    ) = extract_sheet_metrics_knee(sheet_id, data_overview_sheet)

    def safe_float_convert(value):
        """Convert value to float, return 0 if conversion fails"""
        try:
            if value is None or value == '' or value == 'unavailable data':
                return 0
            return float(value)
        except (ValueError, TypeError):
            return 0
    
    # Movement names for knee (excluding hamstring and quadriceps strength)
    movement_names = [
        'Flexion Range',
        'Extension Range',
        'Flexion Force', 
        'Extension Force'
    ]
    
    # Create arrays
    left_values = [
        safe_float_convert(knee_flexion_range_left),
        safe_float_convert(knee_extension_range_left),
        safe_float_convert(knee_flexion_force_left),
        safe_float_convert(knee_extension_force_left)
    ]
    
    right_values = [
        safe_float_convert(knee_flexion_range_right),
        safe_float_convert(knee_extension_range_right),
        safe_float_convert(knee_flexion_force_right),
        safe_float_convert(knee_extension_force_right)
    ]
    
    # Gold standard array (100 for each movement)
    gold_standard = [100] * len(movement_names)
    
    # Create the radar chart
    fig = create_radar_chart(
        gold_standard=gold_standard,
        left=left_values,
        right=right_values,
        movement_names=movement_names,
        title="Knee Assessment",
        save_path=save_path
    )
    
    return fig

def create_radar_chart_hip(sheet_id, data_overview_sheet, save_path=None):
    """
    Create radar chart for hip assessment including both range and force
    """
    # Extract hip metrics
    (
        hip_flexion_range_left,
        hip_flexion_range_right,
        hip_extension_range_left,
        hip_extension_range_right,
        hip_abduction_range_left,
        hip_abduction_range_right,
        hip_adduction_range_left,
        hip_adduction_range_right,
        hip_ext_rotation_range_left,
        hip_ext_rotation_range_right,
        hip_int_rotation_range_left,
        hip_int_rotation_range_right,
        hip_flexion_force_left,
        hip_flexion_force_right,
        hip_extension_force_left,
        hip_extension_force_right,
        hip_abduction_force_left,
        hip_abduction_force_right,
        hip_adduction_force_left,
        hip_adduction_force_right,
        hip_ext_rotation_force_left,
        hip_ext_rotation_force_right,
        hip_int_rotation_force_left,
        hip_int_rotation_force_right
    ) = extract_sheet_metrics_hip(sheet_id,data_overview_sheet)
    
    def safe_float_convert(value):
        """Convert value to float, return 0 if conversion fails"""
        try:
            if value is None or value == '' or value == 'unavailable data':
                return 0
            return float(value)
        except (ValueError, TypeError):
            return 0
    
    # Movement names for hip (including both range and force)
    movement_names = [
        'Flexion Range',
        'Extension Range',
        'Abduction Range',
        'Adduction Range',
        'Ext Rotation Range',
        'Int Rotation Range',
        'Flexion Force',
        'Extension Force',
        'Abduction Force',
        'Adduction Force',
        'Ext Rotation Force',
        'Int Rotation Force'
    ]
    
    # Create arrays
    left_values = [
        safe_float_convert(hip_flexion_range_left),
        safe_float_convert(hip_extension_range_left),
        safe_float_convert(hip_abduction_range_left),
        safe_float_convert(hip_adduction_range_left),
        safe_float_convert(hip_ext_rotation_range_left),
        safe_float_convert(hip_int_rotation_range_left),
        safe_float_convert(hip_flexion_force_left),
        safe_float_convert(hip_extension_force_left),
        safe_float_convert(hip_abduction_force_left),
        safe_float_convert(hip_adduction_force_left),
        safe_float_convert(hip_ext_rotation_force_left),
        safe_float_convert(hip_int_rotation_force_left)
    ]
    
    right_values = [
        safe_float_convert(hip_flexion_range_right),
        safe_float_convert(hip_extension_range_right),
        safe_float_convert(hip_abduction_range_right),
        safe_float_convert(hip_adduction_range_right),
        safe_float_convert(hip_ext_rotation_range_right),
        safe_float_convert(hip_int_rotation_range_right),
        safe_float_convert(hip_flexion_force_right),
        safe_float_convert(hip_extension_force_right),
        safe_float_convert(hip_abduction_force_right),
        safe_float_convert(hip_adduction_force_right),
        safe_float_convert(hip_ext_rotation_force_right),
        safe_float_convert(hip_int_rotation_force_right)
    ]
    
    # Gold standard array (100 for each movement)
    gold_standard = [100] * len(movement_names)
    
    # Create the radar chart
    fig = create_radar_chart(
        gold_standard=gold_standard,
        left=left_values,
        right=right_values,
        movement_names=movement_names,
        title="Hip Assessment",
        save_path=save_path
    )
    
    return fig

def create_radar_chart_shoulder(sheet_id, data_overview_sheet, save_path=None):
    """
    Create radar chart for shoulder assessment with flexible movement names based on available data
    """
    # Extract shoulder metrics
    (
        shoulder_ext_rotation_range_left,
        shoulder_ext_rotation_range_right,
        shoulder_int_rotation_range_left,
        shoulder_int_rotation_range_right,
        shoulder_flexion_range_left,
        shoulder_flexion_range_right,
        shoulder_extension_range_left,
        shoulder_extension_range_right,
        shoulder_ext_rotation_force_left,
        shoulder_ext_rotation_force_right,
        shoulder_int_rotation_force_left,
        shoulder_int_rotation_force_right,
        shoulder_flexion_force_left,
        shoulder_flexion_force_right,
        shoulder_i_iso_left_final,
        shoulder_i_iso_right_final,
        shoulder_y_iso_left_final,
        shoulder_y_iso_right_final,
        shoulder_t_iso_left_final,
        shoulder_t_iso_right_final
    ) = extract_sheet_metrics_shoulder(sheet_id, data_overview_sheet)

    def safe_float_convert(value):
        """Convert value to float, return 0 if conversion fails"""
        try:
            if value is None or value == '' or value == 'unavailable data':
                return 0
            return float(value)
        except (ValueError, TypeError):
            return 0
    
    def is_data_available(left_val, right_val):
        """Check if at least one side has available data"""
        return not (
            (left_val is None or left_val == '' or left_val == 'unavailable data') and
            (right_val is None or right_val == '' or right_val == 'unavailable data')
        )
    
    # Build flexible movement names and values based on available data
    movement_names = []
    left_values = []
    right_values = []
    
    # Check each movement and add only if data is available
    movements_to_check = [
        ('Ext Rotation Range', shoulder_ext_rotation_range_left, shoulder_ext_rotation_range_right),
        ('Int Rotation Range', shoulder_int_rotation_range_left, shoulder_int_rotation_range_right),
        ('Flexion Range', shoulder_flexion_range_left, shoulder_flexion_range_right),
        ('Extension Range', shoulder_extension_range_left, shoulder_extension_range_right),
        ('Ext Rotation Force', shoulder_ext_rotation_force_left, shoulder_ext_rotation_force_right),
        ('Int Rotation Force', shoulder_int_rotation_force_left, shoulder_int_rotation_force_right),
        ('Flexion Force', shoulder_flexion_force_left, shoulder_flexion_force_right),
        ('Shoulder "I" ISO', shoulder_i_iso_left_final, shoulder_i_iso_right_final),
        ('Shoulder "Y" ISO', shoulder_y_iso_left_final, shoulder_y_iso_right_final),
        ('Shoulder "T" ISO', shoulder_t_iso_left_final, shoulder_t_iso_right_final)
    ]
    
    for movement_name, left_val, right_val in movements_to_check:
        if is_data_available(left_val, right_val):
            movement_names.append(movement_name)
            left_values.append(safe_float_convert(left_val))
            right_values.append(safe_float_convert(right_val))
    
    # Ensure we have at least some data to create a chart
    if len(movement_names) == 0:
        print("No shoulder data available for radar chart")
        return None
    
    # Gold standard array (100 for each available movement)
    gold_standard = [100] * len(movement_names)
    
    # Create the radar chart
    fig = create_radar_chart(
        gold_standard=gold_standard,
        left=left_values,
        right=right_values,
        movement_names=movement_names,
        title="Shoulder Assessment",
        save_path=save_path
    )
    
    return fig

def create_all_radar_charts(sheet_id, data_overview_sheet, second_worksheet, save_directory):
    """
    Create all radar charts for a given sheet_id
    """
    import os
    
    charts = {}
    
    try:
        # Foot & Ankle
        charts['foot_ankle'] = create_radar_chart_foot_ankle(
            sheet_id,
            data_overview_sheet,
            second_worksheet,
            save_path=os.path.join(save_directory, f"foot_ankle_radar_{sheet_id}.png")
        )
        print("Foot & Ankle radar chart created successfully")
    except Exception as e:
        print(f"Error creating foot & ankle radar chart: {e}")
    
    try:
        # Knee
        charts['knee'] = create_radar_chart_knee(
            sheet_id,
            data_overview_sheet,
            save_path=os.path.join(save_directory, f"knee_radar_{sheet_id}.png")
        )
        print("Knee radar chart created successfully")
    except Exception as e:
        print(f"Error creating knee radar chart: {e}")
    
    try:
        # Hip
        charts['hip'] = create_radar_chart_hip(
            sheet_id,
            data_overview_sheet,
            save_path=os.path.join(save_directory, f"hip_radar_{sheet_id}.png")
        )
        print("Hip radar chart created successfully")
    except Exception as e:
        print(f"Error creating hip radar chart: {e}")
    
    try:
        # Shoulder
        charts['shoulder'] = create_radar_chart_shoulder(
            sheet_id,
            data_overview_sheet,
            save_path=os.path.join(save_directory, f"shoulder_radar_{sheet_id}.png")
        )
        if charts['shoulder'] is not None:
            print("Shoulder radar chart created successfully")
        else:
            print("Shoulder radar chart skipped - no data available")
    except Exception as e:
        print(f"Error creating shoulder radar chart: {e}")
    
    return charts


# Create individual charts
if __name__ == "__main__":
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id = "1L964TaAjOiI2HT1jPcdZbY8KeWeSPD22wvxVKfKUVdg"
    fig = create_radar_chart_shoulder(sheet_id, "shoulder_chart.png")

    # Create all charts
    charts = create_all_radar_charts(sheet_id, "./charts/")
    # input_lines = TextGen_Shoulder_Concise(sheet_id)
# output = extract_shoulder_report_text(sheet_id)
# print("Input :", input_lines)
# print("Output:", output)

# # evaluate the function
# # Example usage:
# (
#         shoulder_ext_rotation_range_left,
#         shoulder_ext_rotation_range_right,
#         shoulder_int_rotation_range_left,
#         shoulder_int_rotation_range_right,
#         shoulder_flexion_range_left,
#         shoulder_flexion_range_right,
#         shoulder_extension_range_left,
#         shoulder_extension_range_right,
#         shoulder_ext_rotation_force_left,
#         shoulder_ext_rotation_force_right,
#         shoulder_int_rotation_force_left,
#         shoulder_int_rotation_force_right,
#         shoulder_flexion_force_left,
#         shoulder_flexion_force_right,
#         shoulder_i_iso_left_final,
#         shoulder_i_iso_right_final,
#         shoulder_y_iso_left_final,
#         shoulder_y_iso_right_final,
#         shoulder_t_iso_left_final,
#         shoulder_t_iso_right_final

#     ) = extract_sheet_metrics_shoulder(sheet_id)

# print("Shoulder Metrics:")
# print("External Rotation Range Left:", shoulder_ext_rotation_range_left)
# print("External Rotation Range Right:", shoulder_ext_rotation_range_right)
# print("Internal Rotation Range Left:", shoulder_int_rotation_range_left)
# print("Internal Rotation Range Right:", shoulder_int_rotation_range_right)
# print("Flexion Range Left:", shoulder_flexion_range_left)
# print("Flexion Range Right:", shoulder_flexion_range_right)
# print("Extension Range Left:", shoulder_extension_range_left)
# print("Extension Range Right:", shoulder_extension_range_right)
# print("External Rotation Force Left:", shoulder_ext_rotation_force_left)
# print("External Rotation Force Right:", shoulder_ext_rotation_force_right)
# print("Internal Rotation Force Left:", shoulder_int_rotation_force_left)
# print("Internal Rotation Force Right:", shoulder_int_rotation_force_right)
# print("Flexion Force Left:", shoulder_flexion_force_left)
# print("Flexion Force Right:", shoulder_flexion_force_right)
# print("Shoulder \"I\" ISO Left:", shoulder_i_iso_left_final)
# print("Shoulder \"I\" ISO Right:", shoulder_i_iso_right_final)
# print("Shoulder \"Y\" ISO Left:", shoulder_y_iso_left_final)
# print("Shoulder \"Y\" ISO Right:", shoulder_y_iso_right_final)
# print("Shoulder \"T\" ISO Left:", shoulder_t_iso_left_final)
# print("Shoulder \"T\" ISO Right:", shoulder_t_iso_right_final)

# input_lines = TextGen_Knee_Concise(sheet_id)
# output_lines = extract_knee_report_text(sheet_id)

# print("Input :", input_lines)
# print("Output:", output_lines)

# (knee_flexion_range_left,
#  knee_flexion_range_right,
#  knee_extension_range_left,
#  knee_extension_range_right,
#  knee_flexion_force_left,
#  knee_flexion_force_right,
#  knee_extension_force_left,
#  knee_extension_force_right,
#  knee_flexion_force_left_original,
#  knee_flexion_force_right_original,
#  knee_extension_force_left_original,
#  knee_extension_force_right_original,
#  knee_hamstring_quad_ratio_left,
#  knee_hamstring_quad_ratio_right
# ) = extract_sheet_metrics_knee(sheet_id)

# print("Knee Metrics:")
# print("Knee Flexion Range Left:", knee_flexion_range_left)
# print("Knee Flexion Range Right:", knee_flexion_range_right)
# print("Knee Extension Range Left:", knee_extension_range_left)
# print("Knee Extension Range Right:", knee_extension_range_right)
# print("Knee Flexion Force Left:", knee_flexion_force_left)
# print("Knee Flexion Force Right:", knee_flexion_force_right)
# print("Knee Extension Force Left:", knee_extension_force_left)
# print("Knee Extension Force Right:", knee_extension_force_right)
# print("Knee Hamstring/Quad Ratio Left:", knee_hamstring_quad_ratio_left)
# print("Knee Hamstring/Quad Ratio Right:", knee_hamstring_quad_ratio_right)
# # evaluate
# final_hip_assessment, hip_assessment_existing, overall_asymmetry, hip_metrics, deficit_summary, lacking_metrics, largest_movement_summary, concise_input = TextGen_Hip(sheet_id)
# # # print
# # print("Final Hip Assessment:", final_hip_assessment)

# # print("Overall Asymmetry:", overall_asymmetry)
# # print("Hip Metrics:")
# # for key, value in hip_metrics.items():
# #     print(f"  {key}: {value}")
# # print(deficit_summary)
# # # for key, value in lacking_metrics.items():
# # #     print(f"  {key}: {', '.join(value)}")
# # print(largest_movement_summary)
# # # Evaluate all hip metrics and print them
# print("Input::::", concise_input)
# print("Output::::", hip_assessment_existing)


# # (
# #     hip_flexion_range_left,
# #     hip_flexion_range_right,
# #     hip_extension_range_left,
# #     hip_extension_range_right,
# #     hip_abduction_range_left,
# #     hip_abduction_range_right,
# #     hip_adduction_range_left,
# #     hip_adduction_range_right,
# #     hip_ext_rotation_range_left,
# #     hip_ext_rotation_range_right,
# #     hip_int_rotation_range_left,
# #     hip_int_rotation_range_right,
# #     hip_flexion_force_left,
# #     hip_flexion_force_right,
# #     hip_extension_force_left,
# #     hip_extension_force_right,
# #     hip_abduction_force_left,
# #     hip_abduction_force_right,
# #     hip_adduction_force_left,
# #     hip_adduction_force_right,
# #     hip_ext_rotation_force_left,
# #     hip_ext_rotation_force_right,
# #     hip_int_rotation_force_left,
# #     hip_int_rotation_force_right
# # ) = extract_sheet_metrics_hip(sheet_id)
    
# # print("Hip Flexion Range Left:", hip_flexion_range_left)
# # print("Hip Flexion Range Right:", hip_flexion_range_right)
# # print("Hip Extension Range Left:", hip_extension_range_left)
# # print("Hip Extension Range Right:", hip_extension_range_right)
# # print("Hip Abduction Range Left:", hip_abduction_range_left)
# # print("Hip Abduction Range Right:", hip_abduction_range_right)
# # print("Hip Adduction Range Left:", hip_adduction_range_left)
# # print("Hip Adduction Range Right:", hip_adduction_range_right)
# # print("Hip EXT Rotation Range Left:", hip_ext_rotation_range_left)
# # print("Hip EXT Rotation Range Right:", hip_ext_rotation_range_right)
# # print("Hip INT Rotation Range Left:", hip_int_rotation_range_left)
# # print("Hip INT Rotation Range Right:", hip_int_rotation_range_right)
# # print("Hip Flexion Force Left:", hip_flexion_force_left)
# # print("Hip Flexion Force Right:", hip_flexion_force_right)
# # print("Hip Extension Force Left:", hip_extension_force_left)
# # print("Hip Extension Force Right:", hip_extension_force_right)
# # print("Hip Abduction Force Left:", hip_abduction_force_left)
# # print("Hip Abduction Force Right:", hip_abduction_force_right)
# # print("Hip Adduction Force Left:", hip_adduction_force_left)
# # print("Hip Adduction Force Right:", hip_adduction_force_right)
# # print("Hip EXT Rotation Force Left:", hip_ext_rotation_force_left)
# # print("Hip EXT Rotation Force Right:", hip_ext_rotation_force_right)
# # print("Hip INT Rotation Force Left:", hip_int_rotation_force_left)
# # print("Hip INT Rotation Force Right:", hip_int_rotation_force_right)


# #     # print
# # print(left_foot_text)
# # print(right_foot_text)
# # print(foot_ankle_assessment)
# # print(asymmetry_foot)

# #     # Print the extracted values
# # print("Dorsiflexion Range Left:", dorsiflexion_range_left)
# # print("Dorsiflexion Range Right:", dorsiflexion_range_right)
# # print("Plantarflexion Range Left:", plantarflexion_range_left)
# # print("Plantarflexion Range Right:", plantarflexion_range_right)
# # print("Weight Distribution Question Left:", weight_distribution_question_left)
# # print("Weight Distribution Question Right:", weight_distribution_question_right)
# # print("Weight Distribution Question Note:", weight_distribution_question_note)
# # print("Supination Tripod Question Left:", supination_tripod_question_left)
# # print("Supination Tripod Question Right:", supination_tripod_question_right)
# # print("Supination Tripod Question Note:", supination_tripod_question_note)
# # print("Pronation Tripod Question Left:", pronation_tripod_question_left)
# # print("Pronation Tripod Question Right:", pronation_tripod_question_right)
# # print("Pronation Tripod Question Note:", pronation_tripod_question_note)
# # print("Big Toe Independence Question Left:", big_toe_independence_question_left)
# # print("Big Toe Independence Question Right:", big_toe_independence_question_right)
# # print("Big Toe Independence Question Note:", big_toe_independence_question_note)
# # print("Lesser Toes Independence Question Left:", lesser_toes_independence_question_left)
# # print("Lesser Toes Independence Question Right:", lesser_toes_independence_question_right)
# # print("Lesser Toes Independence Question Note:", lesser_toes_independence_question_note)
# # print("Center of Mass Rest Left:", center_of_mass_rest_left)
# # print("Center of Mass Rest Right:", center_of_mass_rest_right)
# # print("Center of Mass Rest Note:", center_of_mass_rest_note)
# # print("Center of Mass Pronated Left:", center_of_mass_pronated_left)
# # print("Center of Mass Pronated Right:", center_of_mass_pronated_right)
# # print("Center of Mass Pronated Note:", center_of_mass_pronated_note)

# # Example usage (uncomment to use):
# # dorsiflexion_values = extract_sheet_metrics_footankle(sheet_id)
# # print("Dorsiflexion Values:", dorsiflexion_values)

#     # Dummy implementation for foot and ankle metrics extraction

# # ffat_status, stva_status, ptva_status, lact_status, LAST_Strength, JUAST_Strength, ffat_note, stva_note, ptva_note, lact_note, LAST_note, JUAST_note, string_core_function = extract_sheet_metrics_corefunction(sheet_id)

# # print(f"FFAT Status: {ffat_status}, STVA Status: {stva_status}, PTVA Status: {ptva_status}, LACT Status: {lact_status}, LAST Strength: {LAST_Strength}, JUAST Strength: {JUAST_Strength}")
# # print(f"FFAT Note: {ffat_note}, STVA Note: {stva_note}, PTVA Note: {ptva_note}, LACT Note: {lact_note}, LAST Note: {LAST_note}, JUAST Note: {JUAST_note}")
# # print(f"Input: {string_core_function}")

