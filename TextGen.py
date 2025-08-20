from posture_assess import extract_sheet_metrics_posture
from google.oauth2.service_account import Credentials
import gspread
from textllm import test_biomech_model
import csv



        

def TextGen_Posture(sheet_id):
    # Extract metrics from the Google Sheet
    Gender,FHP, TC, LC, Pelvis_Left, Pelvis_Right, Mean_pelvis, Posture1, Posture2, Posture3,LC_Category,Rotaion_Ribcage_Left,Rotaion_Ribcage_Right, Rotaion_Ribcage_Flexion_Left,  Rotaion_Ribcage_Flexion_Right, Input_string = extract_sheet_metrics_posture(sheet_id)
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

# load sheet id data 
# read the data from sheetid_fetch.txt
# sheet_ids = []
# with open('sheetid_fetch.txt', 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         name, sheet_id = line.strip().split(' - ')
#         print(f"Sheet Name: {name}, Sheet ID: {sheet_id}")
#         sheet_ids.append(sheet_id)




sheet_id = "1L964TaAjOiI2HT1jPcdZbY8KeWeSPD22wvxVKfKUVdg"
# # Prepare to collect results for CSV
# csv_rows = []

# for sheet_id in sheet_ids:
text1, text2, text3, Input_string = TextGen_Posture(sheet_id)
    # print(text1)  # Output the generated text for verification
    # print(text2)
    # print(text3)
    # print(Input_string)

llmtext = test_biomech_model(Input_string)
    # print("LLM Text Output:", llmtext)  # Output the LLM response for verification
    # append text1,llmtext,text2,text3 and print them
final_text = f"{text1}\n\n{llmtext[0]}\n\n{text2}\n\n{text3}"
print("Final Text Output:", final_text)  # Output the final text for verification



    # # Find the name for this sheet_id from the lines read earlier
    # for line in lines:
    #     name, sid = line.strip().split(' - ')
    #     if sid == sheet_id:
    #         csv_rows.append([name, Input_string])
    #         break

# # Write results to CSV
# with open('output_summary.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Name', 'Input String'])
#     writer.writerows(csv_rows)