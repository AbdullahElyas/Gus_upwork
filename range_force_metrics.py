def extract_range_force_footankle(sheet_id, data_overview_sheet, second_worksheet):
    # Extract data from the worksheet
    all_values = data_overview_sheet.get_all_values()
    
    # Initialize variables
    dorsiflexion_range_left = dorsiflexion_range_right = None
    plantarflexion_range_left = plantarflexion_range_right = None
    dorsiflexion_force_left = dorsiflexion_force_right = None
    plantarflexion_force_left = plantarflexion_force_right = None

    # Search for ANKLE RANGE header row
    ankle_range_header_row = None
    for i, row in enumerate(all_values):
        # Check if the row contains all three strings: "ANKLE", "RANGE (Degrees)", "RANGE (Relative)"
        row_text = ' '.join(str(cell) for cell in row).upper()
        if "ANKLE" in row_text and "RANGE (DEGREES)" in row_text and "RANGE (RELATIVE)" in row_text:
            ankle_range_header_row = i
            print(f"Found ANKLE RANGE header at row {i}: {row}")
            break

    if ankle_range_header_row is not None:
        # Search for Dorsiflexion in the rows following the header
        dorsiflexion_range_row = None
        for i in range(ankle_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "DORSIFLEXION" in row_text:
                dorsiflexion_range_row = i
                print(f"Found Dorsiflexion Range at row {i}: {all_values[i]}")
                break
        
        if dorsiflexion_range_row is not None:
            dorsiflexion_values = all_values[dorsiflexion_range_row]
            dorsiflexion_range_left = dorsiflexion_values[3] if len(dorsiflexion_values) > 3 else None
            dorsiflexion_range_right = dorsiflexion_values[5] if len(dorsiflexion_values) > 5 else None

        # Search for Plantarflexion in the rows following the header
        plantarflexion_range_row = None
        for i in range(ankle_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "PLANTARFLEXION" in row_text:
                plantarflexion_range_row = i
                print(f"Found Plantarflexion Range at row {i}: {all_values[i]}")
                break
        
        if plantarflexion_range_row is not None:
            plantarflexion_values = all_values[plantarflexion_range_row]
            plantarflexion_range_left = plantarflexion_values[3] if len(plantarflexion_values) > 3 else None
            plantarflexion_range_right = plantarflexion_values[5] if len(plantarflexion_values) > 5 else None
    else:
        print("ANKLE RANGE header not found.")

    # Search for ANKLE FORCE header row
    ankle_force_header_row = None
    for i, row in enumerate(all_values):
        row_text = ' '.join(str(cell) for cell in row).upper()
        # Check for FORCE (DEGREES)
        if "ANKLE" in row_text and "FORCE (DEGREES)" in row_text and "FORCE (RELATIVE)" in row_text:
            ankle_force_header_row = i
            print(f"Found ANKLE FORCE header at row {i}: {row}")
            break
        # Check for FORCE (KG)
        elif "ANKLE" in row_text and "FORCE (KG)" in row_text and "FORCE (RELATIVE)" in row_text:
            ankle_force_header_row = i
            print(f"Found ANKLE FORCE header at row {i}: {row}")
            break
        # Check for FORCE (NEWTONS)
        elif "ANKLE" in row_text and "FORCE (NEWTONS)" in row_text and "FORCE (PERCENTILE)" in row_text:
            ankle_force_header_row = i
            print(f"Found ANKLE FORCE header at row {i}: {row}")
            break

    if ankle_force_header_row is not None:
        # Search for Dorsiflexion in the rows following the header
        dorsiflexion_force_row = None
        for i in range(ankle_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "DORSIFLEXION" in row_text:
                dorsiflexion_force_row = i
                print(f"Found Dorsiflexion Force at row {i}: {all_values[i]}")
                break
        
        if dorsiflexion_force_row is not None:
            dorsiflexion_force_values = all_values[dorsiflexion_force_row]
            dorsiflexion_force_left = dorsiflexion_force_values[3] if len(dorsiflexion_force_values) > 3 else None
            dorsiflexion_force_right = dorsiflexion_force_values[5] if len(dorsiflexion_force_values) > 5 else None

        # Search for Plantarflexion in the rows following the header
        plantarflexion_force_row = None
        for i in range(ankle_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "PLANTARFLEXION" in row_text:
                plantarflexion_force_row = i
                print(f"Found Plantarflexion Force at row {i}: {all_values[i]}")
                break
        
        if plantarflexion_force_row is not None:
            plantarflexion_force_values = all_values[plantarflexion_force_row]
            plantarflexion_force_left = plantarflexion_force_values[3] if len(plantarflexion_force_values) > 3 else None
            plantarflexion_force_right = plantarflexion_force_values[5] if len(plantarflexion_force_values) > 5 else None
    else:
        print("ANKLE FORCE header not found.")

    return (
        dorsiflexion_range_left,
        dorsiflexion_range_right,
        plantarflexion_range_left,
        plantarflexion_range_right,
        dorsiflexion_force_left,
        dorsiflexion_force_right,
        plantarflexion_force_left,
        plantarflexion_force_right
    )


def extract_range_force_knee(sheet_id, data_overview_sheet):
    # Extract data from the worksheet
    all_values = data_overview_sheet.get_all_values()
    
    # Initialize variables
    flexion_range_left = flexion_range_right = None
    extension_range_left = extension_range_right = None
    flexion_force_left = flexion_force_right = None
    extension_force_left = extension_force_right = None

    # Search for KNEE RANGE header row
    knee_range_header_row = None
    for i, row in enumerate(all_values):
        # Check if the row contains all three strings: "KNEE", "RANGE (Degrees)", "RANGE (Relative)"
        row_text = ' '.join(str(cell) for cell in row).upper()
        if "KNEE" in row_text and "RANGE (DEGREES)" in row_text and "RANGE (RELATIVE)" in row_text:
            knee_range_header_row = i
            print(f"Found KNEE RANGE header at row {i}: {row}")
            break

    if knee_range_header_row is not None:
        # Search for Flexion in the rows following the header
        flexion_range_row = None
        for i in range(knee_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "FLEXION" in row_text:
                flexion_range_row = i
                print(f"Found Flexion Range at row {i}: {all_values[i]}")
                break
        
        if flexion_range_row is not None:
            flexion_values = all_values[flexion_range_row]
            flexion_range_left = flexion_values[3] if len(flexion_values) > 3 else None
            flexion_range_right = flexion_values[5] if len(flexion_values) > 5 else None

        # Search for Extension in the rows following the header
        extension_range_row = None
        for i in range(knee_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "EXTENSION" in row_text:
                extension_range_row = i
                print(f"Found Extension Range at row {i}: {all_values[i]}")
                break
        
        if extension_range_row is not None:
            extension_values = all_values[extension_range_row]
            extension_range_left = extension_values[3] if len(extension_values) > 3 else None
            extension_range_right = extension_values[5] if len(extension_values) > 5 else None
    else:
        print("KNEE RANGE header not found.")

    # Search for KNEE FORCE header row
    knee_force_header_row = None
    for i, row in enumerate(all_values):
        row_text = ' '.join(str(cell) for cell in row).upper()
        # Check for FORCE (DEGREES)
        if "KNEE" in row_text and "FORCE (DEGREES)" in row_text and "FORCE (RELATIVE)" in row_text:
            knee_force_header_row = i
            print(f"Found KNEE FORCE header at row {i}: {row}")
            break
        # Check for FORCE (KG)
        elif "KNEE" in row_text and "FORCE (KG)" in row_text and "FORCE (RELATIVE)" in row_text:
            knee_force_header_row = i
            print(f"Found KNEE FORCE header at row {i}: {row}")
            break
        # Check for FORCE (NEWTONS)
        elif "KNEE" in row_text and "FORCE (NEWTONS)" in row_text and "FORCE (PERCENTILE)" in row_text:
            knee_force_header_row = i
            print(f"Found KNEE FORCE header at row {i}: {row}")
            break

    if knee_force_header_row is not None:
        # Search for Flexion in the rows following the header
        flexion_force_row = None
        for i in range(knee_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "FLEXION" in row_text:
                flexion_force_row = i
                print(f"Found Flexion Force at row {i}: {all_values[i]}")
                break
        
        if flexion_force_row is not None:
            flexion_force_values = all_values[flexion_force_row]
            flexion_force_left = flexion_force_values[3] if len(flexion_force_values) > 3 else None
            flexion_force_right = flexion_force_values[5] if len(flexion_force_values) > 5 else None

        # Search for Extension in the rows following the header
        extension_force_row = None
        for i in range(knee_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "EXTENSION" in row_text:
                extension_force_row = i
                print(f"Found Extension Force at row {i}: {all_values[i]}")
                break
        
        if extension_force_row is not None:
            extension_force_values = all_values[extension_force_row]
            extension_force_left = extension_force_values[3] if len(extension_force_values) > 3 else None
            extension_force_right = extension_force_values[5] if len(extension_force_values) > 5 else None
    else:
        print("KNEE FORCE header not found.")

    return (
        flexion_range_left,
        flexion_range_right,
        extension_range_left,
        extension_range_right,
        flexion_force_left,
        flexion_force_right,
        extension_force_left,
        extension_force_right
    )

def extract_range_force_hip(sheet_id, data_overview_sheet):
    # Extract data from the worksheet
    all_values = data_overview_sheet.get_all_values()
    
    # Initialize variables for range
    flexion_range_left = flexion_range_right = None
    extension_range_left = extension_range_right = None
    abduction_range_left = abduction_range_right = None
    adduction_range_left = adduction_range_right = None
    ext_rotation_range_left = ext_rotation_range_right = None
    int_rotation_range_left = int_rotation_range_right = None
    
    # Initialize variables for force
    flexion_force_left = flexion_force_right = None
    extension_force_left = extension_force_right = None
    abduction_force_left = abduction_force_right = None
    adduction_force_left = adduction_force_right = None
    ext_rotation_force_left = ext_rotation_force_right = None
    int_rotation_force_left = int_rotation_force_right = None

    # Search for HIP RANGE header row
    hip_range_header_row = None
    for i, row in enumerate(all_values):
        # Check if the row contains all three strings: "HIP", "RANGE (Degrees)", "RANGE (Relative)"
        row_text = ' '.join(str(cell) for cell in row).upper()
        if "HIP" in row_text and "RANGE (DEGREES)" in row_text and "RANGE (RELATIVE)" in row_text:
            hip_range_header_row = i
            print(f"Found HIP RANGE header at row {i}: {row}")
            break

    if hip_range_header_row is not None:
        # Search for Flexion in the rows following the header
        flexion_range_row = None
        for i in range(hip_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "FLEXION" in row_text:
                flexion_range_row = i
                print(f"Found Flexion Range at row {i}: {all_values[i]}")
                break
        
        if flexion_range_row is not None:
            flexion_values = all_values[flexion_range_row]
            flexion_range_left = flexion_values[3] if len(flexion_values) > 3 else None
            flexion_range_right = flexion_values[5] if len(flexion_values) > 5 else None

        # Search for Extension in the rows following the header
        extension_range_row = None
        for i in range(hip_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "EXTENSION" in row_text:
                extension_range_row = i
                print(f"Found Extension Range at row {i}: {all_values[i]}")
                break
        
        if extension_range_row is not None:
            extension_values = all_values[extension_range_row]
            extension_range_left = extension_values[3] if len(extension_values) > 3 else None
            extension_range_right = extension_values[5] if len(extension_values) > 5 else None

        # Search for Abduction in the rows following the header
        abduction_range_row = None
        for i in range(hip_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "ABDUCTION" in row_text:
                abduction_range_row = i
                print(f"Found Abduction Range at row {i}: {all_values[i]}")
                break
        
        if abduction_range_row is not None:
            abduction_values = all_values[abduction_range_row]
            abduction_range_left = abduction_values[3] if len(abduction_values) > 3 else None
            abduction_range_right = abduction_values[5] if len(abduction_values) > 5 else None

        # Search for Adduction in the rows following the header
        adduction_range_row = None
        for i in range(hip_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "ADDUCTION" in row_text:
                adduction_range_row = i
                print(f"Found Adduction Range at row {i}: {all_values[i]}")
                break
        
        if adduction_range_row is not None:
            adduction_values = all_values[adduction_range_row]
            adduction_range_left = adduction_values[3] if len(adduction_values) > 3 else None
            adduction_range_right = adduction_values[5] if len(adduction_values) > 5 else None

        # Search for EXT Rotation in the rows following the header
        ext_rotation_range_row = None
        for i in range(hip_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "EXT ROTATION" in row_text or "EXTERNAL ROTATION" in row_text:
                ext_rotation_range_row = i
                print(f"Found EXT Rotation Range at row {i}: {all_values[i]}")
                break
        
        if ext_rotation_range_row is not None:
            ext_rotation_values = all_values[ext_rotation_range_row]
            ext_rotation_range_left = ext_rotation_values[3] if len(ext_rotation_values) > 3 else None
            ext_rotation_range_right = ext_rotation_values[5] if len(ext_rotation_values) > 5 else None

        # Search for INT Rotation in the rows following the header
        int_rotation_range_row = None
        for i in range(hip_range_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "INT ROTATION" in row_text or "INTERNAL ROTATION" in row_text:
                int_rotation_range_row = i
                print(f"Found INT Rotation Range at row {i}: {all_values[i]}")
                break
        
        if int_rotation_range_row is not None:
            int_rotation_values = all_values[int_rotation_range_row]
            int_rotation_range_left = int_rotation_values[3] if len(int_rotation_values) > 3 else None
            int_rotation_range_right = int_rotation_values[5] if len(int_rotation_values) > 5 else None

    else:
        print("HIP RANGE header not found.")

    # Search for HIP FORCE header row
    hip_force_header_row = None
    for i, row in enumerate(all_values):
        row_text = ' '.join(str(cell) for cell in row).upper()
        # Check for FORCE (KG) first
        if "HIP" in row_text and "FORCE (KG)" in row_text and "FORCE (RELATIVE)" in row_text:
            hip_force_header_row = i
            print(f"Found HIP FORCE header at row {i}: {row}")
            break
        # Then check for FORCE (DEGREES)
        elif "HIP" in row_text and "FORCE (DEGREES)" in row_text and "FORCE (RELATIVE)" in row_text:
            hip_force_header_row = i
            print(f"Found HIP FORCE header at row {i}: {row}")
            break
        # Then check for FORCE (NEWTONS)
        elif "HIP" in row_text and "FORCE (NEWTONS)" in row_text and "FORCE (PERCENTILE)" in row_text:
            hip_force_header_row = i
            print(f"Found HIP FORCE header at row {i}: {row}")
            break

    if hip_force_header_row is not None:
        # Search for Flexion in the rows following the header
        flexion_force_row = None
        for i in range(hip_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "FLEXION" in row_text:
                flexion_force_row = i
                print(f"Found Flexion Force at row {i}: {all_values[i]}")
                break
        
        if flexion_force_row is not None:
            flexion_force_values = all_values[flexion_force_row]
            flexion_force_left = flexion_force_values[3] if len(flexion_force_values) > 3 else None
            flexion_force_right = flexion_force_values[5] if len(flexion_force_values) > 5 else None

        # Search for Extension in the rows following the header
        extension_force_row = None
        for i in range(hip_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "EXTENSION" in row_text:
                extension_force_row = i
                print(f"Found Extension Force at row {i}: {all_values[i]}")
                break
        
        if extension_force_row is not None:
            extension_force_values = all_values[extension_force_row]
            extension_force_left = extension_force_values[3] if len(extension_force_values) > 3 else None
            extension_force_right = extension_force_values[5] if len(extension_force_values) > 5 else None

        # Search for Abduction in the rows following the header
        abduction_force_row = None
        for i in range(hip_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "ABDUCTION" in row_text:
                abduction_force_row = i
                print(f"Found Abduction Force at row {i}: {all_values[i]}")
                break
        
        if abduction_force_row is not None:
            abduction_force_values = all_values[abduction_force_row]
            abduction_force_left = abduction_force_values[3] if len(abduction_force_values) > 3 else None
            abduction_force_right = abduction_force_values[5] if len(abduction_force_values) > 5 else None

        # Search for Adduction in the rows following the header
        adduction_force_row = None
        for i in range(hip_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "ADDUCTION" in row_text:
                adduction_force_row = i
                print(f"Found Adduction Force at row {i}: {all_values[i]}")
                break
        
        if adduction_force_row is not None:
            adduction_force_values = all_values[adduction_force_row]
            adduction_force_left = adduction_force_values[3] if len(adduction_force_values) > 3 else None
            adduction_force_right = adduction_force_values[5] if len(adduction_force_values) > 5 else None

        # Search for EXT Rotation in the rows following the header
        ext_rotation_force_row = None
        for i in range(hip_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "EXT ROTATION" in row_text or "EXTERNAL ROTATION" in row_text:
                ext_rotation_force_row = i
                print(f"Found EXT Rotation Force at row {i}: {all_values[i]}")
                break
        
        if ext_rotation_force_row is not None:
            ext_rotation_force_values = all_values[ext_rotation_force_row]
            ext_rotation_force_left = ext_rotation_force_values[3] if len(ext_rotation_force_values) > 3 else None
            ext_rotation_force_right = ext_rotation_force_values[5] if len(ext_rotation_force_values) > 5 else None

        # Search for INT Rotation in the rows following the header
        int_rotation_force_row = None
        for i in range(hip_force_header_row + 1, len(all_values)):
            row_text = ' '.join(str(cell) for cell in all_values[i]).upper()
            if "INT ROTATION" in row_text or "INTERNAL ROTATION" in row_text:
                int_rotation_force_row = i
                print(f"Found INT Rotation Force at row {i}: {all_values[i]}")
                break
        
        if int_rotation_force_row is not None:
            int_rotation_force_values = all_values[int_rotation_force_row]
            int_rotation_force_left = int_rotation_force_values[3] if len(int_rotation_force_values) > 3 else None
            int_rotation_force_right = int_rotation_force_values[5] if len(int_rotation_force_values) > 5 else None

    else:
        print("HIP FORCE header not found.")

    return (
        flexion_range_left,
        flexion_range_right,
        extension_range_left,
        extension_range_right,
        abduction_range_left,
        abduction_range_right,
        adduction_range_left,
        adduction_range_right,
        ext_rotation_range_left,
        ext_rotation_range_right,
        int_rotation_range_left,
        int_rotation_range_right,
        flexion_force_left,
        flexion_force_right,
        extension_force_left,
        extension_force_right,
        abduction_force_left,
        abduction_force_right,
        adduction_force_left,
        adduction_force_right,
        ext_rotation_force_left,
        ext_rotation_force_right,
        int_rotation_force_left,
        int_rotation_force_right
    )


def extract_range_force_shoulder(sheet_id, data_overview_sheet):
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
    shoulder_external_rotation_range = "External Rotation"
    shoulder_internal_rotation_range = "Internal Rotation"
    shoulder_flexion_range = "Flexion"
    shoulder_extension_range = "Extension"
    shoulder_external_rotation_force = "External Rotation"
    shoulder_internal_rotation_force = "Internal Rotation"
    shoulder_flexion_force = "Flexion"
    shoulder_iso_i = 'Shoulder "I" ISO'
    shoulder_iso_y = 'Shoulder "Y" ISO'
    shoulder_iso_t = 'Shoulder "T" ISO'
    shoulder_iso_i_alt = 'Shoulder ISO "I"'
    shoulder_iso_y_alt = 'Shoulder ISO "Y"'
    shoulder_iso_t_alt = 'Shoulder ISO "T"'

    # search for strings in row "SHOULDER" "LEFT" "RIGHT" and "GS" if all these strings are present in row array then store its index

    # Search for SHOULDER RANGE header row
    shoulder_range_header_row = None
    for i, row in enumerate(all_values):
        # Check if the row contains all three strings: "SHOULDER", "RANGE (Degrees)", "RANGE (Relative)"
        row_text = ' '.join(str(cell) for cell in row).upper()
        if "SHOULDER" in row_text and "RANGE (DEGREES)" in row_text and "RANGE (RELATIVE)" in row_text:
            shoulder_range_header_row = i
            print(f"Found SHOULDER RANGE header at row {i}: {row}")
            break

    if shoulder_range_header_row is None:
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

    # Only search from shoulder_range_header_row onwards
    search_rows_range = all_values[shoulder_range_header_row + 1:] if shoulder_range_header_row is not None else all_values

    # Search for External Rotation Range
    ext_rotation_range_row = next((i for i, row in enumerate(search_rows_range) if shoulder_external_rotation_range in row), None)
    if ext_rotation_range_row is not None:
        ext_rotation_range_values = search_rows_range[ext_rotation_range_row]
        shoulder_ext_rotation_range_left = ext_rotation_range_values[3] if len(ext_rotation_range_values) > 3 else "unavailable data"
        shoulder_ext_rotation_range_right = ext_rotation_range_values[5] if len(ext_rotation_range_values) > 5 else "unavailable data"
        print(f"External Rotation Range - Left: {shoulder_ext_rotation_range_left}, Right: {shoulder_ext_rotation_range_right}")
    else:
        shoulder_ext_rotation_range_left = shoulder_ext_rotation_range_right = "unavailable data"

    # Search for Internal Rotation Range
    int_rotation_range_row = next((i for i, row in enumerate(search_rows_range) if shoulder_internal_rotation_range in row), None)
    if int_rotation_range_row is not None:
        int_rotation_range_values = search_rows_range[int_rotation_range_row]
        shoulder_int_rotation_range_left = int_rotation_range_values[3] if len(int_rotation_range_values) > 3 else "unavailable data"
        shoulder_int_rotation_range_right = int_rotation_range_values[5] if len(int_rotation_range_values) > 5 else "unavailable data"
        print(f"Internal Rotation Range - Left: {shoulder_int_rotation_range_left}, Right: {shoulder_int_rotation_range_right}")
    else:
        shoulder_int_rotation_range_left = shoulder_int_rotation_range_right = "unavailable data"

    # Search for Flexion Range
    flexion_range_row = next((i for i, row in enumerate(search_rows_range) if shoulder_flexion_range in row), None)
    if flexion_range_row is not None:
        flexion_range_values = search_rows_range[flexion_range_row]
        shoulder_flexion_range_left = flexion_range_values[3] if len(flexion_range_values) > 3 else "unavailable data"
        shoulder_flexion_range_right = flexion_range_values[5] if len(flexion_range_values) > 5 else "unavailable data"
        print(f"Flexion Range - Left: {shoulder_flexion_range_left}, Right: {shoulder_flexion_range_right}")
    else:
        shoulder_flexion_range_left = shoulder_flexion_range_right = "unavailable data"

    # Search for Extension Range
    extension_range_row = next((i for i, row in enumerate(search_rows_range) if shoulder_extension_range in row), None)
    if extension_range_row is not None:
        extension_range_values = search_rows_range[extension_range_row]
        shoulder_extension_range_left = extension_range_values[3] if len(extension_range_values) > 3 else "unavailable data"
        shoulder_extension_range_right = extension_range_values[5] if len(extension_range_values) > 5 else "unavailable data"
        print(f"Extension Range - Left: {shoulder_extension_range_left}, Right: {shoulder_extension_range_right}")
    else:
        shoulder_extension_range_left = shoulder_extension_range_right = "unavailable data"


    # Search for SHOULDER FORCE header row
    shoulder_force_header_row = None
    for i, row in enumerate(all_values):
        row_text = ' '.join(str(cell) for cell in row).upper()
        # Check for FORCE (KG), FORCE (DEGREES), or FORCE (NEWTONS)
        if (
            ("SHOULDER" in row_text and "FORCE (KG)" in row_text and "FORCE (RELATIVE)" in row_text)
            or ("SHOULDER" in row_text and "FORCE (DEGREES)" in row_text and "FORCE (RELATIVE)" in row_text)
            or ("SHOULDER" in row_text and "FORCE (NEWTONS)" in row_text and "FORCE (PERCENTILE)" in row_text)
        ):
            shoulder_force_header_row = i
            print(f"Found SHOULDER FORCE header at row {i}: {row}")
            break


    if shoulder_force_header_row is not None:
        # Only search from shoulder_force_header_row onwards
        search_rows_force = all_values[shoulder_force_header_row + 1:] if shoulder_force_header_row is not None else all_values

        # Search for External Rotation Force
        ext_rotation_force_row = next((i for i, row in enumerate(search_rows_force) if shoulder_external_rotation_force in row), None)
        if ext_rotation_force_row is not None:
            ext_rotation_force_values = search_rows_force[ext_rotation_force_row]
            shoulder_ext_rotation_force_left = ext_rotation_force_values[3] if len(ext_rotation_force_values) > 3 else "unavailable data"
            shoulder_ext_rotation_force_right = ext_rotation_force_values[5] if len(ext_rotation_force_values) > 5 else "unavailable data"
            print(f"External Rotation Force - Left: {shoulder_ext_rotation_force_left}, Right: {shoulder_ext_rotation_force_right}")
        else:
            shoulder_ext_rotation_force_left = shoulder_ext_rotation_force_right = "unavailable data"

        # Search for Internal Rotation Force
        int_rotation_force_row = next((i for i, row in enumerate(search_rows_force) if shoulder_internal_rotation_force in row), None)
        if int_rotation_force_row is not None:
            int_rotation_force_values = search_rows_force[int_rotation_force_row]
            shoulder_int_rotation_force_left = int_rotation_force_values[3] if len(int_rotation_force_values) > 3 else "unavailable data"
            shoulder_int_rotation_force_right = int_rotation_force_values[5] if len(int_rotation_force_values) > 5 else "unavailable data"
            print(f"Internal Rotation Force - Left: {shoulder_int_rotation_force_left}, Right: {shoulder_int_rotation_force_right}")
        else:
            shoulder_int_rotation_force_left = shoulder_int_rotation_force_right = "unavailable data"

        # Search for Flexion Force
        flexion_force_row = next((i for i, row in enumerate(search_rows_force) if shoulder_flexion_force in row), None)
        if flexion_force_row is not None:
            flexion_force_values = search_rows_force[flexion_force_row]
            shoulder_flexion_force_left = flexion_force_values[3] if len(flexion_force_values) > 3 else "unavailable data"
            shoulder_flexion_force_right = flexion_force_values[5] if len(flexion_force_values) > 5 else "unavailable data"
            print(f"Flexion Force - Left: {shoulder_flexion_force_left}, Right: {shoulder_flexion_force_right}")
        else:
            shoulder_flexion_force_left = shoulder_flexion_force_right = "unavailable data"

        # Search for Shoulder "I" ISO
        i_iso_row = next((i for i, row in enumerate(search_rows_force) if shoulder_iso_i in row), None)
        if i_iso_row is not None:
            i_iso_values = search_rows_force[i_iso_row]
            shoulder_i_iso_left = i_iso_values[3] if len(i_iso_values) > 3 else "unavailable data"
            shoulder_i_iso_right = i_iso_values[5] if len(i_iso_values) > 5 else "unavailable data"
            print(f'Shoulder "I" ISO - Left: {shoulder_i_iso_left}, Right: {shoulder_i_iso_right}')
        else:
            shoulder_i_iso_left = shoulder_i_iso_right = "unavailable data"

        # Search for Shoulder "Y" ISO
        y_iso_row = next((i for i, row in enumerate(search_rows_force) if shoulder_iso_y in row), None)
        if y_iso_row is not None:
            y_iso_values = search_rows_force[y_iso_row]
            shoulder_y_iso_left = y_iso_values[3] if len(y_iso_values) > 3 else "unavailable data"
            shoulder_y_iso_right = y_iso_values[5] if len(y_iso_values) > 5 else "unavailable data"
            print(f'Shoulder "Y" ISO - Left: {shoulder_y_iso_left}, Right: {shoulder_y_iso_right}')
        else:
            shoulder_y_iso_left = shoulder_y_iso_right = "unavailable data"

        # Search for Shoulder "T" ISO
        t_iso_row = next((i for i, row in enumerate(search_rows_force) if shoulder_iso_t in row), None)
        if t_iso_row is not None:
            t_iso_values = search_rows_force[t_iso_row]
            shoulder_t_iso_left = t_iso_values[3] if len(t_iso_values) > 3 else "unavailable data"
            shoulder_t_iso_right = t_iso_values[5] if len(t_iso_values) > 5 else "unavailable data"
            print(f'Shoulder "T" ISO - Left: {shoulder_t_iso_left}, Right: {shoulder_t_iso_right}')
        else:
            shoulder_t_iso_left = shoulder_t_iso_right = "unavailable data"

        # Search for Shoulder ISO "I" (alternative format)
        i_iso_alt_row = next((i for i, row in enumerate(search_rows_force) if shoulder_iso_i_alt in row), None)
        if i_iso_alt_row is not None:
            i_iso_alt_values = search_rows_force[i_iso_alt_row]
            shoulder_i_iso_alt_left = i_iso_alt_values[3] if len(i_iso_alt_values) > 3 else "unavailable data"
            shoulder_i_iso_alt_right = i_iso_alt_values[5] if len(i_iso_alt_values) > 5 else "unavailable data"
            print(f'Shoulder ISO "I" - Left: {shoulder_i_iso_alt_left}, Right: {shoulder_i_iso_alt_right}')
        else:
            shoulder_i_iso_alt_left = shoulder_i_iso_alt_right = "unavailable data"

        # Search for Shoulder ISO "Y" (alternative format)
        y_iso_alt_row = next((i for i, row in enumerate(search_rows_force) if shoulder_iso_y_alt in row), None)
        if y_iso_alt_row is not None:
            y_iso_alt_values = search_rows_force[y_iso_alt_row]
            shoulder_y_iso_alt_left = y_iso_alt_values[3] if len(y_iso_alt_values) > 3 else "unavailable data"
            shoulder_y_iso_alt_right = y_iso_alt_values[5] if len(y_iso_alt_values) > 5 else "unavailable data"
            print(f'Shoulder ISO "Y" - Left: {shoulder_y_iso_alt_left}, Right: {shoulder_y_iso_alt_right}')
        else:
            shoulder_y_iso_alt_left = shoulder_y_iso_alt_right = "unavailable data"

        # Search for Shoulder ISO "T" (alternative format)
        t_iso_alt_row = next((i for i, row in enumerate(search_rows_force) if shoulder_iso_t_alt in row), None)
        if t_iso_alt_row is not None:
            t_iso_alt_values = search_rows_force[t_iso_alt_row]
            shoulder_t_iso_alt_left = t_iso_alt_values[3] if len(t_iso_alt_values) > 3 else "unavailable data"
            shoulder_t_iso_alt_right = t_iso_alt_values[5] if len(t_iso_alt_values) > 5 else "unavailable data"
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
    else:
        shoulder_ext_rotation_force_left = shoulder_ext_rotation_force_right = "unavailable data"
        shoulder_int_rotation_force_left = shoulder_int_rotation_force_right = "unavailable data"
        shoulder_flexion_force_left = shoulder_flexion_force_right = "unavailable data"
        shoulder_i_iso_left_final = shoulder_i_iso_right_final = "unavailable data"
        shoulder_y_iso_left_final = shoulder_y_iso_right_final = "unavailable data"
        shoulder_t_iso_left_final = shoulder_t_iso_right_final = "unavailable data"
    

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