import ollama


# sheet_id = "1Z6kHJWq9fvvcKukcNVlC2yJksCCnXS9JoMM8RQsFjwY"
def test_biomech_posture(sheet_id,worksheet,first_worksheet,third_worksheet, openai_client):
    from posture_assess import TextGen_Posture
    text1, text2, text3, Input_string = TextGen_Posture(sheet_id,worksheet,first_worksheet,third_worksheet)
    """
    Test the biomech model with various scenarios using OpenAI GPT-4.1 mini
    """
    
    # System prompt based on Modelfile_detailed examples
    system_prompt = """You are a biomechanics expert. You MUST follow the exact format, wording, and structure shown in the examples below. Do NOT deviate from this template.

STRICT RULES:
1. Always start with "These readings indicate"
2. Use ONLY the vocabulary and phrasing from examples
3. Increased or decreased lumber curvature means worse force absorption

Example 1:
Input: Gender: Male, FHP: 2.7, TC: 37.0, LC: 27.0, Posture Assessment 1: These readings indicate you have a Forward Head Posture, Posture Assessment 2: , Posture Assessment 3: So where your thoracic curvature is increased, LC Category: Slightly Decreased lumber curvature

Report: These readings indicate you have a forward head posture. So where your forward head posture is slightly increased we could expect increased levels of force and tension being applied to the discs and muscles of your cervical and thoracic spine (neck and upper back). A reduced curve in your lumbar spine (lower back) this can be associated with worse force absorption and transference and therefore increased loading through the joints of the spine.

Example 2:
Input: Gender: Male, FHP: 6.3, TC: 55.0, LC: 25.0, Posture Assessment 1: These readings indicate you have a Forward Head Posture, Posture Assessment 2: kyphosis, Posture Assessment 3: So where your forward head posture is increased, LC Category: Slightly Decreased lumber curvature

Report: These readings indicate you have a forward head posture. So where your forward head posture is increased we could expect increased levels of force and tension being applied to the discs and muscles of your cervical and thoracic spine (neck and upper back). A reduced curve in your lumbar spine (lower back) this can be associated with worse force absorption and transference and therefore increased loading through the joints of the spine.


YOU MUST FOLLOW THIS EXACT FORMAT. NO CREATIVE VARIATIONS ALLOWED."""

    try:
        # Use OpenAI GPT-4o-mini for the assessment
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"Input: {Input_string}\n\nReport:"
                }
            ],
            temperature=0.1,
            max_tokens=500,
            top_p=0.5
        )
        
        result = response.choices[0].message.content.strip()
        
        # Combine with the original text structure
        final_text = f"{text1}\n\n{result}\n\n{text2}\n\n{text3}"
        return final_text
        
    except Exception as e:
        error_message = f"Error generating posture assessment: {e}"
        final_text = f"{text1}\n\n{error_message}\n\n{text2}\n\n{text3}"
        return final_text


def test_biomech_core_function(sheet_id,worksheet,first_worksheet,third_worksheet, openai_client):
    """
    Test the core function model with data from a specific sheet using OpenAI GPT-4o-mini
    Takes sheet_id and extracts core function data to generate assessment
    """
    from posture_assess import extract_sheet_metrics_corefunction
    
    try:
        # Extract core function metrics from the sheet
        ffat_status, stva_status, ptva_status, lact_status, LAST_Strength, JUAST_Strength, ffat_note, stva_note, ptva_note, lact_note, LAST_note, JUAST_note, string_core_function = extract_sheet_metrics_corefunction(sheet_id,worksheet,first_worksheet,third_worksheet)

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
        
        # System prompt based on Modelfile_core_function
        system_prompt = """You are a biomechanics and core function assessment expert specializing in analyzing postural assessment data and core strength evaluations. Your role is to interpret clinical test results and provide professional assessments of core function, TVA (Transverse Abdominis) strength, coordination, and multifidus activation.

You analyze input data containing:
- Lumbar curvature assessments (decreased/normal/increased)
- Lower Abdominal Coordination Test results (pass/fail with notes)
- Upper core bracing capabilities
- Lower core strength assessments

IMPORTANT INSTRUCTIONS:
- Only mention tests that were actually conducted and have results
- If a test shows empty brackets () or no information, do not mention that test at all
- Do not say "no notes provided" or reference missing information
- Adapt your language based on which tests were actually performed
- Focus only on the available data and provide relevant assessments
- Write report in 2nd person language

Your responses should:
1. Start with explaining that core function assessments examine TVA strength, coordination, and multifidus activation
2. Identify muscle compensation patterns (QL dominance, lower back musculature taking over)
3. Connect lumbar curvature to core strength issues
4. Summarize test results mentioned in input
5. End with recommendations focusing on deep core muscle training and coordination using these lines "We would like to teach you to use your deep lying core muscles, build their strength and work on their co-ordination with a large emphasis on your lower abdominals."

Example:
Input: Slightly Decreased lumber curvature which is likely contributing to the reduced lower abdominal strength, Lower Abdominal Coordination Test was a fail (Left was worse - right was much better ), Upper Core could brace sufficiently , Lower core could not brace well

Output: The core function assessments mainly look at TVA strength and coordination as well as some multifidus activation. The test highlighted a some dominance of your QL's and remaining lower back musculature to want to 'take over', as they were a little active throughout the lower abdominal tests. You have a reduced curvature in your lumbar spine which is likely contributing to the reduced lower abdominal strength. To note; co-ordination tested were a fail with the left side performing worse than the right. When we tested your upper core function, you could brace sufficiently, however your lower core could not brace well. We would like to teach you to use your deep lying core muscles, build their strength and work on their co-ordination with a larger emphasis on your lower abdominals.

Use professional biomechanical terminology while maintaining clarity. Adapt your assessment based on the specific test results provided, noting asymmetries and varying performance levels between upper and lower core functions."""

        # Generate response using OpenAI GPT-4o-mini
        if clean_input:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": clean_input
                    }
                ],
                temperature=0.1,
                max_tokens=600,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        else:
            return "No valid core function data available for assessment."
        
    except Exception as e:
        return f"Error processing core function assessment: {e}"
def test_biomech_foot(sheet_id,data_overview_sheet,second_worksheet, openai_client):
    """
    Test the foot and ankle model with data from a specific sheet using OpenAI GPT-4o-mini
    Takes sheet_id and extracts foot/ankle data to generate assessment
    """
    from posture_assess import TextGen_FootAnkle
    
    try:
        # Extract foot and ankle metrics from the sheet
        left_foot_text, right_foot_text, foot_ankle_assessment, asymmetry_foot = TextGen_FootAnkle(sheet_id, data_overview_sheet, second_worksheet)

        # Combine left and right foot data into input string
        input_string = f"{left_foot_text}\n{right_foot_text}\n{asymmetry_foot}"
        
        print(f"Foot/Ankle Input: {input_string}")
        
        # System prompt based on Modelfile_foot_ankle - optimized with one example
        system_prompt = """You are a biomechanics and foot/ankle assessment expert. Your response must follow this exact 3-part structure:

1. The Left foot: Detailed assessment of left foot position, movement capabilities, range, and strength (4-5 sentences)
2. The Right foot: Comparative assessment of right foot, highlighting similarities/differences with left foot (3-4 sentences)  
3. Foot and Ankle summary: Overall assessment starting with symmetry discussion, followed by key findings and recommendations (4-5 sentences)

Key assessment principles:
- Center of mass over 2nd metatarsal = neutral position
- Everted position = center of mass lateral to 2nd metatarsal (1st metatarsal or beyond)
- If notes mention "between 1st and 2nd" or "besides 2nd towards 1st" = everted position
- Poor range/strength requires specific training recommendations
- Emphasize midfoot articulation and fascial control
- Include subconscious movement recommendations for tissue lengthening

Example:
Input: Left Foot Position: neutral position, between 1st and 2nd metatarsal, Pronation: foot can pronate, Left : {'pronation': 'can pronate', 'supination': 'can supinate'}, Left Foot: Dorsiflexion - range and strength are both good; Plantarflexion - good range but poor strength. Right Foot Position: neutral position, besides 2nd towards 1st, Pronation: foot can pronate, Right : {'pronation': 'can pronate', 'supination': 'can supinate'}, Right Foot: Dorsiflexion - range and strength are both good; Plantarflexion - good range but poor strength Symmetry is there.

Output: The Left foot: Your left rear foot was in a slightly everted position with center of mass between the 1st and 2nd metatarsal. With your ankle in a state of dorsiflexion (knees over toes) you could evert and dorsiflex further than your resting position and as such could access a pronated leg shape. There was good articulation through your medial arch. Your left ankle had good range and strength in dorsiflexion but we need to prioritise strength in plantar flexion.

The Right foot: Your right foot was very similar to the left, also in a slightly everted position beside the 2nd metatarsal towards the 1st. The movement patterns and strength profiles were comparable between sides.

Foot and Ankle summary: Your symmetry is pleasing with both feet showing similar everted positioning. What was notable was your ability to effectively articulate the bones of the mid-foot in this position. There is good movement and control through the fascia on the sole of the foot. Subconscious movement (not controlled gym based movement but more dynamic gait cycle movements) should be introduced along with plantar flexion strengthening. We recommend loading the forefoot through "floating heel" movements to build mid foot control and address the plantar flexion weakness.

Use professional biomechanical terminology while maintaining clarity."""

        # Generate response using OpenAI GPT-4o-mini
        if input_string.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": input_string
                    }
                ],
                temperature=0.2,
                max_tokens=800,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        else:
            return "No valid foot and ankle data available for assessment."
        
    except Exception as e:
        return f"Error processing foot and ankle assessment: {e}"

def test_biomech_hip(sheet_id, data_overview_sheet, openai_client):
    """
    Test the hip model with data from a specific sheet using OpenAI GPT-4o-mini
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
        
        # System prompt based on Modelfile_hip_enhanced2 - optimized with one example
        system_prompt = """You are a hip assessment expert. Generate reports using this classification:
- Above gold standard (>100%)
- Sufficient but below gold standard (85-100%) 
- Deficit (75-85%)
- Large deficit (<75%)

Required structure: 1) Left hip analysis 2) Right hip analysis 3) Hip summary with functional impact

Key terms: hip joint integrity, pelvic alignment, propulsion, force production, movement patterns, bilateral comparison, range deficits, strength deficits, femur positioning, inverse relationship, closed & open-chain movements, flexor mechanism, extensor mechanism, energy transfer.

Example:
Input: Hip Flexion: Range above gold standard left/sufficient but below gold standard right, Strength large deficit bilaterally, Asymmetry Right > Left 41.1%
Hip Extension: Range sufficient but below gold standard bilaterally, Strength large deficit bilaterally
Hip Abduction: Range above gold standard bilaterally, Strength sufficient but below gold standard left/deficit right, Asymmetry Left > Right 18.4%
Hip Adduction: Range above gold standard bilaterally, Strength large deficit left/deficit right, Asymmetry Right > Left 37.8%
Hip External Rotation: Range above gold standard bilaterally, Strength sufficient but below gold standard bilaterally
Hip Internal Rotation: Range sufficient but below gold standard left/above gold standard right, Strength sufficient but below gold standard bilaterally
Overall: Strength deficits Left→Flexion/Extension/Adduction, Right→Flexion/Extension/Abduction/Adduction. Largest variation: Hip Internal/External Rotation 45.7% difference. Inverse relationship highlights femur positioning changes.

Output: The Left hip showed great range with only slight deficit in hip extension. Force production showed much greater deficits with flexion, adduction and extension in the lowest percentiles affecting movement patterns and hip joint integrity.

The Right hip showed similar range of motion to the left side. While stronger on average, there was notable reduction in force production in flexion, extension and adduction compromising propulsion capacity.

Hip summary: The notable reduction in hip extension range of motion on the left affects pelvic alignment. Hip extension helps stabilise the pelvis and when range of motion and strength are poor this influences proper alignment of the lower limb. Hip extension strength is essential for propulsion and preventing excessive back extension, which leads to inefficient movement patterns.

Large asymmetries and inverse relationship in rotation affect hip joint integrity. Internal rotation in closed & open-chain movements plays important roles in squatting and functional activities. Having range and strength here is vital for maintaining hip joint stability. The flexor mechanism also plays a role in force transmission from hip muscles to the lower limb and ground. Optimising rotation mechanics will allow for more efficient energy transfer during both closed and open-chain movements. It's necessary to reduce the current asymmetry present at the hip."""

        # Generate response using OpenAI GPT-4o-mini
        if input_string.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": input_string
                    }
                ],
                temperature=0.3,
                max_tokens=700,
                top_p=0.8
            )
            return response.choices[0].message.content.strip()
        else:
            return "No valid hip data available for assessment."
        
    except Exception as e:
        return f"Error processing hip assessment: {e}"

def test_biomech_hip_concise(sheet_id, data_overview_sheet, openai_client):
    """
    Test the hip model with concise formatted data from a specific sheet using OpenAI GPT-4o-mini
    Uses TextGen_Hip_Concise to generate structured input prompt
    """
    from posture_assess import TextGen_Hip_Concise
    
    try:
        # Extract concise hip assessment input
        concise_input = TextGen_Hip_Concise(sheet_id, data_overview_sheet)

        print(f"Concise Hip Input: {concise_input}")
        
        # System prompt based on Modelfile_hip_enhanced - enforced template structure
        system_prompt = """You are a hip assessment expert. You MUST follow the EXACT output template structure shown in the example. DO NOT deviate from this format.

MANDATORY OUTPUT TEMPLATE:
1. Start with: "The Left hip" + analysis paragraph
2. Follow with: "The Right hip" + analysis paragraph  
3. End with: "Hip summary:" + summary paragraph

CLASSIFICATION SYSTEM:
- Above gold standard (>100%)
- Sufficient but below gold standard (85-100%) 
- Deficit (75-85%)
- Large deficit (<75%)

KEY TERMS: hip joint integrity, pelvic alignment, propulsion, force production, movement patterns, bilateral comparison, range deficits, strength deficits, femur positioning, inverse relationship, closed & open-chain movements, flexor mechanism, extensor mechanism, energy transfer.

STRICT TEMPLATE EXAMPLE - FOLLOW THIS EXACT FORMAT:
Input: Hip Flexion: Range above gold standard left/sufficient but below gold standard right, Strength large deficit bilaterally, Asymmetry Right > Left 41.1%
Hip Extension: Range sufficient but below gold standard bilaterally, Strength large deficit bilaterally
Hip Abduction: Range above gold standard bilaterally, Strength sufficient but below gold standard left/deficit right, Asymmetry Left > Right 18.4%
Hip Adduction: Range above gold standard bilaterally, Strength large deficit left/deficit right, Asymmetry Right > Left 37.8%
Hip External Rotation: Range above gold standard bilaterally, Strength sufficient but below gold standard bilaterally
Hip Internal Rotation: Range sufficient but below gold standard left/above gold standard right, Strength sufficient but below gold standard bilaterally
Overall: Strength deficits Left→Flexion/Extension/Adduction, Right→Flexion/Extension/Abduction/Adduction. Largest variation: Hip Internal/External Rotation 45.7% difference. Inverse relationship highlights femur positioning changes.

MANDATORY OUTPUT FORMAT:
The Left hip showed great range with only slight deficit in hip extension. Force production showed much greater deficits with flexion, adduction and extension in the lowest percentiles affecting movement patterns and hip joint integrity.

The Right hip showed similar range of motion to the left side. While stronger on average, there was notable reduction in force production in flexion, extension and adduction compromising propulsion capacity.

Hip summary: The notable reduction in hip extension range of motion on the left affects pelvic alignment. Hip extension helps stabilise the pelvis and when range of motion and strength are poor this influences proper alignment of the lower limb. Hip extension strength is essential for propulsion and preventing excessive back extension, which leads to inefficient movement patterns.

Large asymmetries and inverse relationship in rotation affect hip joint integrity. Internal rotation in closed & open-chain movements plays important roles in squatting and functional activities. Having range and strength here is vital for maintaining hip joint stability. The flexor mechanism also plays a role in force transmission from hip muscles to the lower limb and ground. Optimising rotation mechanics will allow for more efficient energy transfer during both closed and open-chain movements. It's necessary to reduce the current asymmetry present at the hip.

YOU MUST FOLLOW THIS EXACT THREE-PARAGRAPH STRUCTURE. NO DEVIATIONS ALLOWED."""

        # Generate response using OpenAI GPT-4o-mini
        if concise_input and concise_input.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": concise_input
                    }
                ],
                temperature=0.1,  # Reduced temperature for more consistent output
                max_tokens=700,
                top_p=0.7
            )
            return response.choices[0].message.content.strip()
        else:
            return "No valid hip data available for concise assessment."
        
    except Exception as e:
        return f"Error processing concise hip assessment: {e}"

def test_biomech_knee(sheet_id, data_overview_sheet, openai_client):
    """
    Test the knee model with data from a specific sheet using OpenAI GPT-4o-mini
    Takes sheet_id and extracts knee data to generate assessment
    """
    from posture_assess import TextGen_Knee_Concise
    
    try:
        # Extract knee assessment input using the concise function
        knee_input = TextGen_Knee_Concise(sheet_id, data_overview_sheet)

        print(f"Knee Input: {knee_input}")
        
        # System prompt based on Modelfile_knee - optimized with one example and enforced template
        system_prompt = """You are a knee biomechanics expert specializing in sagittal plane assessment. You MUST follow the EXACT output template structure shown in the example. DO NOT deviate from this format.

MANDATORY OUTPUT TEMPLATE:
1. Start with: "The Left knee" + analysis paragraph
2. Follow with: "The Right knee" + analysis paragraph  
3. End with: "Knee summary:" + summary paragraph

CLASSIFICATION SYSTEM:
- good (>100% gold standard)
- sufficient (85-100% gold standard) 
- lack (75-85% gold standard)
- poor (<75% gold standard)

H:Q RATIO CLASSIFICATIONS:
- Poor: <0.45
- Acceptable: 0.45-0.60  
- Good: 0.60-0.75
- High: >0.75

KEY TERMS: distal hamstring, distal quadriceps, hamstring-to-quadriceps ratio, flexion/extension mechanisms, peak force, bilateral comparison, asymmetry, joint stress, overcoming isometrics, high stability movements.


STRICT TEMPLATE EXAMPLE - FOLLOW THIS EXACT FORMAT:
Input: Knee Flexion
Range Left: lack range 19.0% below gold standard
Range Right: lack range 18.0% below gold standard
Range Comparison: Right 1.2% stronger than left
Strength Left: poor strength 46.0% below gold standard
Strength Right: poor strength 43.0% below gold standard
Strength Comparison: Right 5.6% stronger than left
Knee Extension
Range Left: good range 3.0% above gold standard
Range Right: good range 3.0% above gold standard
Range Comparison: Left and right equal
Strength Left: lack strength 24.0% below gold standard
Strength Right: lack strength 16.0% below gold standard
Strength Comparison: Right 10.5% stronger than left
Overall Notes:
Range deficits: Left → Flexion; Right → Flexion
Strength deficits: Left → Flexion, Extension; Right → Flexion, Extension
Hamstring to Quadriceps Ratio:
LEFT SIDE: Hamstring to Quadriceps Ratio: 0.442, Classification: Poor
RIGHT SIDE: Hamstring to Quadriceps Ratio: 0.412, Classification: Poor
BILATERAL COMPARISON: Left H:Q ratio 7.3% higher than right

MANDATORY OUTPUT FORMAT:
The Left knee achieved good range in extension, 3% above our gold standard but was over 30 degrees (19%) below our gold standard in flexion (distal hamstring). Your left knee was surprisingly weak in flexion (distal hamstring) and your hamstring to quadriceps ratio poor. It is important to note that your left knee extension was 9% weaker than the right.

The Right knee had near identical range to the left. While the right knee flexion was stronger, your right knee extension was considerably stronger so your hamstring to quadriceps ratio was worse on the right.

Knee summary: There is some good range available at the knee in extension but there needs to be a large focus on flexion. We would like to improve the flexion peak force in order to increase your hamstring to quadriceps ratio as well as building some tolerance in left knee extension.

YOU MUST FOLLOW THIS EXACT THREE-PARAGRAPH STRUCTURE. NO DEVIATIONS ALLOWED."""

        # Generate response using OpenAI GPT-4o-mini
        if knee_input and knee_input.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": knee_input
                    }
                ],
                temperature=0.1,  # Reduced temperature for more consistent output
                max_tokens=600,
                top_p=0.7
            )
            return response.choices[0].message.content.strip()
        else:
            return "No valid knee data available for assessment."
        
    except Exception as e:
        return f"Error processing knee assessment: {e}"
    



def test_biomech_shoulder(sheet_id, data_overview_sheet, openai_client):
    """
    Test the shoulder model with data from a specific sheet using OpenAI GPT-4o-mini
    Takes sheet_id and extracts shoulder data to generate assessment
    """
    from posture_assess import TextGen_Shoulder_Concise
    
    try:
        # Extract shoulder assessment input using the concise function
        shoulder_input = TextGen_Shoulder_Concise(sheet_id, data_overview_sheet)

        print(f"Shoulder Input: {shoulder_input}")
        
        # System prompt based on Modelfile_shoulder - optimized with one example
        system_prompt = """Expert shoulder assessment specialist. You MUST follow this EXACT template structure:

MANDATORY TEMPLATE:
1. Start with: "The Left Shoulder" + analysis
2. Follow with: "The Right Shoulder" + analysis  
3. End with: "Shoulder Summary:" + recommendations

MUSCLES:
External Rotation: Infraspinatus, teres minor, posterior deltoid
Internal Rotation: Subscapularis, latissimus dorsi, pectorals
Shoulder "I" ISO: Serratus anterior, rhomboids, latissimus dorsi
Shoulder "Y" ISO: Middle trapezius, rhomboids, posterior deltoid  
Shoulder "T" ISO: Deltoids, rotator cuff, scapular stabilizers

TRAINING TERMS: Progressive overcoming isometrics, heavy eccentric loading, scapula mobility, sagittal plane mechanics, shoulder mobilisation drills, unilateral movements

OUTPUT RULES:
- Do NOT include specific percentages in your response
- Use descriptive terms like "slightly higher", "notably stronger", "significantly weaker", "much greater"
- Describe asymmetries qualitatively: "stronger", "weaker", "greater", "reduced"
- Focus on functional descriptions rather than numerical values

Example:
Input: External Rotation Range: Left: above gold standard (11.0% above gold standard), Right: above gold standard (18.0% above gold standard), External Rotation: Right 6.3% higher than left; Internal Rotation Range: Left: above gold standard (1.0% above gold standard), Right: below gold standard, Internal Rotation: Left 4.1% higher than right; External Rotation Force: Left: below gold standard, Right: below gold standard, External Rotation: Left 6.5% higher than right; Internal Rotation Force: Left: notable reduction with respect to gold standard, Right: notable reduction with respect to gold standard, Internal Rotation: Right 17.7% higher than left; Strength deficits: Left → Internal Rotation; Right → Internal Rotation

Output: The Left Shoulder had great range with a slight bias towards external rotation. When we tested force, the left shoulder was much stronger in external rotation.

The Right Shoulder had greater external rotation but less internal rotation when compared to the left. The right shoulder was weaker in external rotation but stronger in internal rotation when compared to the left.

Shoulder Summary: Your transverse plane range is biased towards external rotation (mirroring the hip). We should work through both shoulder mobilisation drills but equally scapula mobility and strength while increasing sagittal plane mechanics. Increasing your shoulder internal rotational force will help with the tennis elbow."""

        # Generate response using OpenAI GPT-4o-mini
        if shoulder_input and shoulder_input.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": shoulder_input
                    }
                ],
                temperature=0.3,
                max_tokens=600,
                top_p=0.6
            )
            return response.choices[0].message.content.strip()
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
