import ollama


sheet_id = "1Z6kHJWq9fvvcKukcNVlC2yJksCCnXS9JoMM8RQsFjwY"
def test_biomech_posture(sheet_id,worksheet,first_worksheet,third_worksheet):
    from posture_assess import TextGen_Posture
    text1, text2, text3, Input_string = TextGen_Posture(sheet_id,worksheet,first_worksheet,third_worksheet)
    """
    Test the biomech model with various scenarios
    """
    test_cases = [
        Input_string
    ]
    results = []
    for case in test_cases:
        try:
            response = ollama.chat(
                model='biomech33',
                messages=[
                    {
                        "role": "user",
                        "content": f"Input: {case}\n\nReport:"
                    }
                ]
            )
            results.append(response['message']['content'])
        except Exception as e:
            results.append(f"Error: {e}")
    final_text = f"{text1}\n\n{results[0]}\n\n{text2}\n\n{text3}"
    return final_text

def test_biomech_core_function(sheet_id, worksheet):
    """
    Test the core function model with data from a specific sheet
    Takes sheet_id and extracts core function data to generate assessment
    """
    from posture_assess import extract_sheet_metrics_corefunction
    
    try:
        # Extract core function metrics from the sheet
        ffat_status, stva_status, ptva_status, lact_status, LAST_Strength, JUAST_Strength, ffat_note, stva_note, ptva_note, lact_note, LAST_note, JUAST_note, string_core_function = extract_sheet_metrics_corefunction(sheet_id, worksheet)

        # Clean up the input string to remove empty tests and notes
        input_parts = []
        
        # Add lumbar curvature info (this should always be present)
        if string_core_function:
            parts = string_core_function.split(', ')
            for part in parts:
                # Skip parts that are just empty brackets or contain only empty brackets
                if part.strip() and not part.strip() == '()' and '()' not in part:
                    input_parts.append(part.strip())
                # Include parts with actual notes (not empty brackets)
                elif '(' in part and ')' in part and part.strip() != '()':
                    # Extract content between brackets
                    note_content = part[part.find('(')+1:part.find(')')]
                    if note_content.strip():  # Only include if there's actual content
                        input_parts.append(part.strip())
        
        # Create clean input string
        clean_input = ', '.join(input_parts) if input_parts else ""
        
        print(f"Original input: {string_core_function}")
        print(f"Cleaned input: {clean_input}")
        
        # Generate response using the biotech_core_expert model
        if clean_input:
            response = ollama.chat(
                model='biotech_core_expert',
                messages=[
                    {
                        "role": "user", 
                        "content": clean_input
                    }
                ]
            )
            return response['message']['content']
        else:
            return "No valid core function data available for assessment."
        
    except Exception as e:
        return f"Error processing core function assessment: {e}"
def test_biomech_foot(sheet_id,data_overview_sheet,second_worksheet):
    """
    Test the foot and ankle model with data from a specific sheet
    Takes sheet_id and extracts foot/ankle data to generate assessment
    """
    from posture_assess import TextGen_FootAnkle
    
    try:
        # Extract foot and ankle metrics from the sheet
        left_foot_text, right_foot_text, foot_ankle_assessment, asymmetry_foot = TextGen_FootAnkle(sheet_id, data_overview_sheet, second_worksheet)

        # Combine left and right foot data into input string
        input_string = f"{left_foot_text}\n{right_foot_text}\n{asymmetry_foot}"
        
        print(f"Foot/Ankle Input: {input_string}")
        
        # Generate response using the foot_ankle_expert model
        if input_string.strip():
            response = ollama.chat(
                model='biotech_foot_expert',
                messages=[
                    {
                        "role": "user", 
                        "content": input_string
                    }
                ]
            )
            return response['message']['content']
        else:
            return "No valid foot and ankle data available for assessment."
        
    except Exception as e:
        return f"Error processing foot and ankle assessment: {e}"

def test_biomech_hip(sheet_id, data_overview_sheet):
    """
    Test the hip model with data from a specific sheet
    Takes sheet_id and extracts hip data to generate assessment
    """
    from posture_assess import TextGen_Hip
    
    try:
        # Extract hip metrics from the sheet
        _, _, _, hip_metrics, deficit_summary, _, largest_movement_summary = TextGen_Hip(sheet_id, data_overview_sheet)

        # Create comprehensive input string with all hip data
        input_parts = []
        
        # Add individual hip movement summaries
        input_parts.append("Hip Movement Analysis:")
        for movement, summary in hip_metrics.items():
            # Format movement name for display
            display_name = movement.replace('_', ' ').title()
            input_parts.append(f"• {display_name}: {summary}")
        
        # Add deficit summary if available
        if deficit_summary and deficit_summary.strip():
            input_parts.append(f"\nDeficit Summary: {deficit_summary}")

        # Add largest movement summary if available (it's a string, not a dict)
        if largest_movement_summary and largest_movement_summary.strip():
            input_parts.append(f"\nOpposing Movement Analysis: {largest_movement_summary}")

        # Combine all parts into input string
        input_string = "\n".join(input_parts)
        
        print(f"Hip Input: {input_string}")
        
        # Generate response using the biotech_hip_expert model
        if input_string.strip():
            response = ollama.chat(
                model='biotech_hip_expert',
                messages=[
                    {
                        "role": "user", 
                        "content": input_string
                    }
                ]
            )
            return response['message']['content']
        else:
            return "No valid hip data available for assessment."
        
    except Exception as e:
        return f"Error processing hip assessment: {e}"

def test_biomech_hip_concise(sheet_id, data_overview_sheet):
    """
    Test the hip model with concise formatted data from a specific sheet
    Uses TextGen_Hip_Concise to generate structured input prompt
    """
    from posture_assess import TextGen_Hip_Concise
    
    try:
        # Extract concise hip assessment input
        concise_input = TextGen_Hip_Concise(sheet_id, data_overview_sheet)

        print(f"Concise Hip Input: {concise_input}")
        
        # Generate response using the biotech_hip_expert model with concise input
        if concise_input and concise_input.strip():
            response = ollama.chat(
                model='biotech_hip_expert_enhanced',
                messages=[
                    {
                        "role": "user", 
                        "content": concise_input
                    }
                ]
            )
            return response['message']['content']
        else:
            return "No valid hip data available for concise assessment."
        
    except Exception as e:
        return f"Error processing concise hip assessment: {e}"

def test_biomech_knee(sheet_id, data_overview_sheet):
    """
    Test the knee model with data from a specific sheet
    Takes sheet_id and extracts knee data to generate assessment
    """
    from posture_assess import TextGen_Knee_Concise
    
    try:
        # Extract knee assessment input using the concise function
        knee_input = TextGen_Knee_Concise(sheet_id, data_overview_sheet)

        print(f"Knee Input: {knee_input}")
        
        # Generate response using the biotech_text_expert_knee model
        if knee_input and knee_input.strip():
            response = ollama.chat(
                model='biotech_knee_expert',
                messages=[
                    {
                        "role": "user", 
                        "content": knee_input
                    }
                ]
            )
            return response['message']['content']
        else:
            return "No valid knee data available for assessment."
        
    except Exception as e:
        return f"Error processing knee assessment: {e}"
    



def test_biomech_shoulder(sheet_id, data_overview_sheet):
    """
    Test the shoulder model with data from a specific sheet
    Takes sheet_id and extracts shoulder data to generate assessment
    """
    from posture_assess import TextGen_Shoulder_Concise
    
    try:
        # Extract shoulder assessment input using the concise function
        shoulder_input = TextGen_Shoulder_Concise(sheet_id, data_overview_sheet)

        print(f"Shoulder Input: {shoulder_input}")
        
        # Generate response using the biotech_shoulder_expert model
        if shoulder_input and shoulder_input.strip():
            response = ollama.chat(
                model='biotech_shoulder_expert',
                messages=[
                    {
                        "role": "user", 
                        "content": shoulder_input
                    }
                ]
            )
            return response['message']['content']
        else:
            return "No valid shoulder data available for assessment."
        
    except Exception as e:
        return f"Error processing shoulder assessment: {e}"
# final_text = test_biomech_posture(sheet_id)
# print(f"Posture Assessment Result: {final_text}")
# result = test_biomech_shoulder(sheet_id)
# print(f"Shoulder Assessment Result: {result}")

# ...existing code...

# Add this to test the shoulder function
# result = test_biomech_shoulder(sheet_id)
# print(f"Shoulder Assessment Result: {result}")
# evaluate the function

# result = test_biomech_hip_concise(sheet_id)
# print(f"Concise Hip Assessment Result: {result}")

# result = test_biomech_knee(sheet_id)
# print(f"Knee Assessment Result: {result}")
# result = test_biomech_hip(sheet_id)
# print(f"Hip Assessment Result: {result}")

# evaluate the function

# result = test_biomech_foot(sheet_id)
# print(f"Foot and Ankle Assessment Result: {result}")
# result = test_biomech_core_function(sheet_id)
# print(f"Core Function Assessment Result: {result}")

# Run the test
# result = test_biomech_model()

# import gspread
# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build

# # Define the scope and credentials for Google Sheets API
# # Update your scopes
# scopes = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]
# creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
# client = gspread.authorize(creds)
# sheets_id = "1Lc1bOKXUeyRR_W78QMFqJayjb_UJQnx2OSvbxaoEkJ8"

# # Open the Google Sheet
# sheet = client.open_by_key(sheets_id)

# # write down this text in a new worksheet named "R2"
# try:
#     r2_sheet = sheet.worksheet("R2")
#     # Write the text in the first cell of the R2 sheet
#     r2_sheet.update('A1', [[result[0]] if result else ["No result"]])
#     # Write the text in the first cell of the R2 sheet
#     r2_sheet.update('A1', [result])
# except Exception as e:
#     print(f"Error updating R2 worksheet: {e}")
