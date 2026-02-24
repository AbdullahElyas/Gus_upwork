


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
4. Always write in English spelling(Not American English). For example use emphasising instead of emphasizing ,stabiliser instead of stabilizer.Use programme instead of program.
5. NEVER use the phrase "gold standard". Always use "expected value" instead (e.g. "above our expected value range", "below our expected value").

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
        if text2.strip():
            final_text = f"{text1}\n\n{result}\n\n{text2}\n\n{text3}"
        else:
            final_text = f"{text1}\n\n{result}\n\n{text3}"      
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
                if part.strip() and not part.strip() == '()':
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
- Always write in English spelling(Not American English). For example use emphasising instead of emphasizing ,stabiliser instead of stabilizer.Use programme instead of program.

Your responses should:
1. Start with explaining that core function assessments examine TVA strength, coordination, and multifidus activation
2. Identify muscle compensation patterns (QL dominance, lower back musculature taking over)
3. Connect lumbar curvature to core strength issues
4. Summarize test results mentioned in input
5. End with recommendations if any deficit is found for example focusing on deep core muscle training and coordination using these lines "We would like to teach you to use your deep lying core muscles, build their strength and work on their co-ordination with a large emphasis on your lower abdominals."

Example:
Input: Slightly Decreased lumber curvature which is likely contributing to the reduced lower abdominal strength, Lower Abdominal Coordination Test was a fail (Left was worse - right was much better ), Upper Core could brace sufficiently , Lower core could not brace well

Output: The core function assessments mainly look at TVA strength and coordination as well as some multifidus activation. The test highlighted a some dominance of your QL's and remaining lower back musculature to want to 'take over', as they were a little active throughout the lower abdominal tests. You have a reduced curvature in your lumbar spine which is likely contributing to the reduced lower abdominal strength. To note; co-ordination tested were a fail with the left side performing worse than the right. When we tested your upper core function, you could brace sufficiently, however your lower core could not brace well. We would like to teach you to use your deep lying core muscles, build their strength and work on their co-ordination with a larger emphasis on your lower abdominals.

Use professional biomechanical terminology while maintaining clarity. Adapt your assessment based on the specific test results provided, noting asymmetries and varying performance levels between upper and lower core functions."""

        # Generate response using OpenAI GPT-4o-mini
        if clean_input:
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": string_core_function
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
        left_foot_text, right_foot_text, asymmetry_foot = TextGen_FootAnkle(sheet_id, data_overview_sheet, second_worksheet)

        # Combine left and right foot data into input string
        input_string = f"{left_foot_text}\n{right_foot_text}\n{asymmetry_foot}"
        
        print(f"Foot/Ankle Input: {input_string}")
        
        # System prompt based on Modelfile_foot_ankle - optimized with one example
        system_prompt = """You are a biomechanics and foot/ankle assessment expert. Your response must follow this exact 3-part structure:

1. The Left foot: Detailed assessment of left foot position, movement capabilities, range, and strength (4-5 sentences)
2. The Right foot: Comparative assessment of right foot, highlighting similarities/differences with left foot (3-4 sentences)  
3. Foot and Ankle summary: Overall assessment starting with symmetry discussion, followed by key findings and recommendations (4-5 sentences)

Key assessment principles:
- Centre of mass over 2nd metatarsal = Neutral position
- Everted position = Centre of mass medial to 2nd metatarsal (towards 1st metatarsal or beyond)
- If notes mention "between 1st and 2nd" or "beside 2nd towards 1st" = Everted position
- Inverted position = Centre of mass lateral to 2nd metatarsal (towards 5th metatarsal or beyond)
- Poor range/strength requires specific training recommendations
- Emphasize midfoot articulation and fascial control
- Include subconscious movement recommendations for tissue lengthening
- There should be no subheading for left and right foot .....Foot and Ankle summary subheading shouldbe there in the last paragraph

Note: Always write in English spelling(Not American English). For example use emphasising instead of emphasizing ,stabiliser instead of stabilizer.Use programme instead of program.

Example:
Input: Left Foot Position: neutral position, between 1st and 2nd metatarsal, Pronation: foot can pronate, Left : {'pronation': 'can pronate', 'supination': 'can supinate'}, Left Foot: Dorsiflexion - range and strength are both good; Plantarflexion - good range but poor strength. Right Foot Position: neutral position, besides 2nd towards 1st, Pronation: foot can pronate, Right : {'pronation': 'can pronate', 'supination': 'can supinate'}, Right Foot: Dorsiflexion - range and strength are both good; Plantarflexion - good range but poor strength Symmetry is there.

Output: Your left rear foot was in a slightly everted position with center of mass between the 1st and 2nd metatarsal. With your ankle in a state of dorsiflexion (knees over toes) you could evert and dorsiflex further than your resting position and as such could access a pronated leg shape. There was good articulation through your medial arch. Your left ankle had good range and strength in dorsiflexion but we need to prioritise strength in plantar flexion.

Your right foot was very similar to the left, also in a slightly everted position beside the 2nd metatarsal towards the 1st. The movement patterns and strength profiles were comparable between sides.

Foot and Ankle summary: Your symmetry is pleasing with both feet showing similar everted positioning. What was notable was your ability to effectively articulate the bones of the mid-foot in this position. There is good movement and control through the fascia on the sole of the foot. Subconscious movement (not controlled gym based movement but more dynamic gait cycle movements) should be introduced along with plantar flexion strengthening. We recommend loading the forefoot through "floating heel" movements to build mid foot control and address the plantar flexion weakness.

Use professional biomechanical terminology while maintaining clarity."""

        # Generate response using OpenAI GPT-4o-mini
        if input_string.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
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
- Above expected value (>100%)
- Sufficient but below expected value (85-100%) 
- Deficit (75-85%)
- Large deficit (<75%)

Required structure: 1) Left hip analysis 2) Right hip analysis 3) Hip summary with functional impact

Key terms: hip joint integrity, pelvic alignment, propulsion, force production, movement patterns, bilateral comparison, range deficits, strength deficits, femur positioning, inverse relationship, closed & open-chain movements, flexor mechanism, extensor mechanism, energy transfer.

Note: Always write in English spelling(Not American English). For example use emphasising instead of emphasizing ,stabiliser instead of stabilizer.Use programme instead of program.
IMPORTANT: NEVER use the phrase "gold standard" anywhere in your output. Always use "expected value" instead.
Example:
Input: Hip Flexion: Range above expected value left/sufficient but below expected value right, Strength large deficit bilaterally, Asymmetry Right > Left 41.1%
Hip Extension: Range sufficient but below expected value bilaterally, Strength large deficit bilaterally
Hip Abduction: Range above expected value bilaterally, Strength sufficient but below expected value left/deficit right, Asymmetry Left > Right 18.4%
Hip Adduction: Range above expected value bilaterally, Strength large deficit left/deficit right, Asymmetry Right > Left 37.8%
Hip External Rotation: Range above expected value bilaterally, Strength sufficient but below expected value bilaterally
Hip Internal Rotation: Range sufficient but below expected value left/above expected value right, Strength sufficient but below expected value bilaterally
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
        concise_input,conclusion_hip = TextGen_Hip_Concise(sheet_id, data_overview_sheet)

        print(f"Concise Hip Input: {concise_input}")
        
        # System prompt based on Modelfile_hip_enhanced - enforced template structure
        system_prompt = """You are a hip assessment expert. You MUST follow the EXACT output template structure shown in the example. DO NOT deviate from this format.

MANDATORY OUTPUT TEMPLATE:
1. Start with: "The Left hip" + analysis paragraph
2. Follow with: "The Right hip" + analysis paragraph  
3. End with: "Hip summary:" + summary paragraph

CLASSIFICATION SYSTEM:
- Above expected value (>100%)
- Sufficient but below expected value (85-100%) 
- Deficit (75-85%)
- Large deficit (<75%)

KEY TERMS: hip joint integrity, pelvic alignment, propulsion, force production, movement patterns, bilateral comparison, range deficits, strength deficits, closed & open-chain movements, flexor mechanism, extensor mechanism, energy transfer.

STRICT TEMPLATE EXAMPLE - FOLLOW THIS EXACT FORMAT:
Input: Hip Flexion: Range above expected value left/sufficient but below expected value right, Strength large deficit bilaterally, Asymmetry Right > Left 41.1%
Hip Extension: Range sufficient but below expected value bilaterally, Strength large deficit bilaterally
Hip Abduction: Range above expected value bilaterally, Strength sufficient but below expected value left/deficit right, Asymmetry Left > Right 18.4%
Hip Adduction: Range above expected value bilaterally, Strength large deficit left/deficit right, Asymmetry Right > Left 37.8%
Hip External Rotation: Range above expected value bilaterally, Strength sufficient but below expected value bilaterally
Hip Internal Rotation: Range sufficient but below expected value left/above expected value right, Strength sufficient but below expected value bilaterally
Overall: Strength deficits Left→Flexion/Extension/Adduction, Right→Flexion/Extension/Abduction/Adduction. 
MANDATORY OUTPUT FORMAT:
The Left hip showed great range with only slight deficit in hip extension. Force production showed much greater deficits with flexion, adduction and extension in the lowest percentiles affecting movement patterns and hip joint integrity.

The Right hip showed similar range of motion to the left side. While stronger on average, there was notable reduction in force production in flexion, extension and adduction compromising propulsion capacity.

Hip summary: The notable reduction in hip extension range of motion on the left affects pelvic alignment. Hip extension helps stabilise the pelvis and when range of motion and strength are poor this influences proper alignment of the lower limb. Hip extension strength is essential for propulsion and preventing excessive back extension, which leads to inefficient movement patterns.

Internal rotation in closed & open-chain movements plays important roles in squatting and functional activities. Having range and strength here is vital for maintaining hip joint stability. The flexor mechanism also plays a role in force transmission from hip muscles to the lower limb and ground. Optimising rotation mechanics will allow for more efficient energy transfer during both closed and open-chain movements. It's necessary to reduce the current asymmetry present at the hip.

YOU MUST FOLLOW THIS EXACT THREE-PARAGRAPH STRUCTURE. NO DEVIATIONS ALLOWED.
Try to avoid mentioning inverse relationships unless absolutely necessary or critical to the analysis.
There should be no subheading for left and right hip .....Hip summary subheading should be there in the last paragraph
When discussing range or force use explicit language so the range is not confused with strength. Avoid using words like weaker or stronger to describe range. For range use terms like limited, reduced, good, full, excellent.
IMPORTANT: NEVER use the phrase "gold standard" anywhere in your output. Always use "expected value" instead.

Note: Always write in English spelling(Not American English). For example use emphasising instead of emphasizing ,stabiliser instead of stabilizer.Use programme instead of program."""

        # Generate response using OpenAI GPT-4o-mini
        if concise_input and concise_input.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
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
            return response.choices[0].message.content.strip(), conclusion_hip
        else:
            return "No valid hip data available for concise assessment."
        
    except Exception as e:
        return f"Error processing concise hip assessment: {e}", conclusion_hip

def test_biomech_knee(sheet_id, data_overview_sheet, openai_client):
    """
    Test the knee model with data from a specific sheet using OpenAI GPT-4o-mini
    Takes sheet_id and extracts knee data to generate assessment
    """
    from posture_assess import TextGen_Knee_Concise
    
    try:
        # Extract knee assessment input using the concise function
        knee_input,conclusion_knee = TextGen_Knee_Concise(sheet_id, data_overview_sheet)

        print(f"Knee Input: {knee_input}")
        
        # System prompt based on Modelfile_knee - optimized with one example and enforced template
        system_prompt = """You are a knee biomechanics expert specializing in sagittal plane assessment. You MUST follow the EXACT output template structure shown in the example. DO NOT deviate from this format.

MANDATORY OUTPUT TEMPLATE:
1. Start with: "The Left knee" + analysis paragraph
2. Follow with: "The Right knee" + analysis paragraph  
3. End with: "Knee summary:" + summary paragraph

CLASSIFICATION SYSTEM:
- good (>100% expected value)
- sufficient (85-100% expected value) 
- lack (75-85% expected value)
- poor (<75% expected value)

H:Q RATIO CLASSIFICATIONS:
- Poor: <0.45
- Acceptable: 0.45-0.60  
- Good: 0.60-0.75
- High: >0.75

KEY TERMS:  hamstring-to-quadriceps ratio, flexion/extension mechanisms, peak force, bilateral comparison, asymmetry, joint stress, overcoming isometrics, high stability movements.


STRICT TEMPLATE EXAMPLE - FOLLOW THIS EXACT FORMAT:
Input: Knee Flexion
Range Left: lack range 19.0% below expected value
Range Right: lack range 18.0% below expected value
Range Comparison: Right 1.2% stronger than left
Strength Left: poor strength 
Strength Right: poor strength 
Strength Comparison: Right 5.6% stronger than left
Knee Extension
Range Left: good range 3.0% above expected value
Range Right: good range 3.0% above expected value
Range Comparison: Left and right equal
Strength Left: lack strength 
Strength Right: lack strength 
Strength Comparison: Right  
Overall Notes:
Range deficits: Left → Flexion; Right → Flexion
Strength deficits: Left → Flexion, Extension; Right → Flexion, Extension
Hamstring to Quadriceps Ratio:
LEFT SIDE: Hamstring to Quadriceps Ratio: 0.442, Classification: Poor
RIGHT SIDE: Hamstring to Quadriceps Ratio: 0.412, Classification: Poor
BILATERAL COMPARISON: Left H:Q ratio 7.3% higher than right

MANDATORY OUTPUT FORMAT:
The Left knee achieved good range in extension, 3% above our expected value but was over 30 degrees (19%) below our expected value in flexion . Your left knee was surprisingly weak in flexion  and your hamstring to quadriceps ratio poor. It is important to note that your left knee extension was 9% weaker than the right.

The Right knee had near identical range to the left. While the right knee flexion was stronger, your right knee extension was considerably stronger so your hamstring to quadriceps ratio was worse on the right.

Knee summary: There is some good range available at the knee in extension but there needs to be a large focus on flexion. We would like to improve the flexion peak force in order to increase your hamstring to quadriceps ratio as well as building some tolerance in left knee extension.

YOU MUST FOLLOW THIS EXACT THREE-PARAGRAPH STRUCTURE. NO DEVIATIONS ALLOWED.
There should be no subheading for left and right knee .....Knee summary subheading should be there in the last paragraph
AVOID using numerical values for hamstring to quadriceps ratio in your response; instead, use qualitative descriptors based on the classification system provided.
IMPORTANT: NEVER use the phrase "gold standard" anywhere in your output. Always use "expected value" instead.
Note: Always write in English spelling(Not American English). For example use emphasising instead of emphasizing ,stabiliser instead of stabilizer.Use programme instead of program."""

        # Generate response using OpenAI GPT-4o-mini
        if knee_input and knee_input.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
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
            return response.choices[0].message.content.strip(), conclusion_knee
        else:
            return "No valid knee data available for assessment.", conclusion_knee

    except Exception as e:
        return f"Error processing knee assessment: {e}", conclusion_knee



def test_biomech_shoulder(sheet_id, data_overview_sheet, openai_client):
    """
    Test the shoulder model with data from a specific sheet using OpenAI GPT-4o-mini
    Takes sheet_id and extracts shoulder data to generate assessment
    """
    from posture_assess import TextGen_Shoulder_Concise
    
    try:
        # Extract shoulder assessment input using the concise function
        shoulder_input, conclusion_shoulder = TextGen_Shoulder_Concise(sheet_id, data_overview_sheet)
        if not shoulder_input or not conclusion_shoulder:
            return None, None

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
- When discussing range or force use explicit language so the range is not confused with strength. Do not use words like weaker or stronger to describe range. For range use terms like limited, reduced, good, full, excellent.
- Compare internal and external rotation if necessary or the difference shoulder internal and external rotation and professionally discuss the reason and its implication. If not necessary, do not mention it.
- Always write in English spelling(Not American English). For example use emphasising instead of emphasizing ,stabiliser instead of stabilizer.Use programme instead of program.
- There should be no subheading for left and right shoulder .....Shoulder summary subheading should be there in the last paragraph
- NEVER use the phrase "gold standard" anywhere in your output. Always use "expected value" instead.
Example:
Input: External Rotation Range: Left: above expected value (11.0% above expected value), Right: above expected value (18.0% above expected value), External Rotation: Right 6.3% higher than left; Internal Rotation Range: Left: above expected value (1.0% above expected value), Right: below expected value, Internal Rotation: Left 4.1% higher than right; External Rotation Force: Left: below expected value, Right: below expected value, External Rotation: Left 6.5% higher than right; Internal Rotation Force: Left: notable reduction with respect to expected value, Right: notable reduction with respect to expected value, Internal Rotation: Right 17.7% higher than left; Strength deficits: Left → Internal Rotation; Right → Internal Rotation

Output:  When we tested force, the left shoulder was much stronger in external rotation.

The Right Shoulder had greater external rotation but less internal rotation when compared to the left. The right shoulder was weaker in external rotation but stronger in internal rotation when compared to the left.

Shoulder Summary: Your transverse plane range is biased towards external rotation (mirroring the hip). We should work through both shoulder mobilisation drills but equally scapula mobility and strength while increasing sagittal plane mechanics. Increasing your shoulder internal rotational force will help with the tennis elbow."""

        # Generate response using OpenAI GPT-4o-mini
        if shoulder_input and shoulder_input.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
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
            return response.choices[0].message.content.strip(), conclusion_shoulder
        else:
            return "No valid shoulder data available for assessment.", conclusion_shoulder

    except Exception as e:
        return f"Error processing shoulder assessment: {e}", conclusion_shoulder

def test_biomech_conclusion(posture_text, hip_text, knee_text, ankle_text, shoulder_text, openai_client):
    """
    Generate a comprehensive biomechanical assessment conclusion using OpenAI GPT-4o-mini
    Takes individual assessment summaries and creates unified conclusion following strict template
    """
    
    try:
        # Combine all assessment inputs into structured format, only include headings if text is present
        input_parts = []
        available_sections = []
        
        if posture_text and posture_text.strip():
            input_parts.append(f"Posture Assessment Summary:\n{posture_text}")
            available_sections.append("posture")
        if hip_text and hip_text.strip():
            input_parts.append(f"Hip Assessment Summary:\n{hip_text}")
            available_sections.append("hip")
        if knee_text and knee_text.strip():
            input_parts.append(f"Knee Assessment Summary:\n{knee_text}")
            available_sections.append("knee")
        if ankle_text and ankle_text.strip():
            input_parts.append(f"Ankle Assessment Summary:\n{ankle_text}")
            available_sections.append("ankle")
        if shoulder_text and shoulder_text.strip():
            input_parts.append(f"Shoulder Assessment Summary:\n{shoulder_text}")
            available_sections.append("shoulder")

        input_string = "\n\n".join(input_parts)
        print(f"Conclusion Input: {input_string}")
        print(f"Available sections: {available_sections}")
        
        # Dynamic system prompt based on available sections
        system_prompt = f"""You are a biomechanical assessment expert creating comprehensive conclusions. You MUST follow the template structure but ONLY include paragraphs for assessment sections that are provided in the input.

AVAILABLE ASSESSMENT SECTIONS: {', '.join(available_sections)}

PARAGRAPH STRUCTURE RULES:
- ONLY write paragraphs for assessment sections that appear in the input
- If Posture Assessment Summary is provided: Include paragraph about posture analysis (forward head posture, thoracic kyphosis, rib cage depression, shoulder positioning, pelvic rotation effects)
- If Hip Assessment Summary is provided: Include paragraph about hip compensation patterns (propulsion strategies, internal rotation limitations, hip extension issues, spine overuse, mid-foot awareness)
- If Knee/Ankle Assessment Summary is provided: Include paragraph about integration (range of motion improvements, tissue loading efficiency, joint articulation, muscle contraction quality, force discrepancies)
- If Shoulder Assessment Summary is provided: Include paragraph about shoulder girdle solutions (ribcage and scapula mechanics, resistance training approach, fascial release, deltoids and rotator cuff focus)

IMPORTANT INSTRUCTIONS:
- DO NOT write paragraphs for missing assessment sections
- DO NOT mention assessments that were not provided in the input
- If Shoulder Assessment Summary is missing from input, DO NOT include the shoulder paragraph
- Adapt the conclusion length based on available data
- Maintain professional biomechanical terminology
- Focus only on the assessments that are actually present
- For posture analysis avoid mentioning anterior or posterior pelvic tilt
- Always write in English spelling(Not American English). For example use emphasising instead of emphasizing ,stabiliser instead of stabilizer.

KEY TERMINOLOGY:
- Posture: thoracic kyphosis, rib cage depression, externally rotated position, internal/external rotation, correctives, gait consequences
- Hip: compensations, forward propulsion, closed-chain movements, force transfer, hip extension, downward force, mid-foot pressurizing
- Integration: range of motion, tissue loading patterns, joint articulation, muscle contraction quality, force discrepancies
- Shoulder: shoulder girdle, ribcage mechanics, scapula mechanics, heavy isometrics, eccentrics, fascial release, deltoids, rotator cuff complex

EXAMPLE STRUCTURE (when all sections are available):
Paragraph 1: Posture analysis (only if Posture Assessment Summary provided)
Paragraph 2: Hip compensation patterns (only if Hip Assessment Summary provided)  
Paragraph 3: Hip/knee/ankle integration (only if Knee or Ankle Assessment Summary provided)
Paragraph 4: Shoulder girdle solutions (only if Shoulder Assessment Summary provided)

EXAMPLE OUTPUT FORMAT (when all sections present):
Our results indicate you have a forward head posture. This is characterised by thoracic kyphosis which creates a depression of the rib cage since the thorax is tipped forward. From a standing position this gives the appearance of the shoulders rounding forward and thus sitting in an externally rotated position. At the pelvis there is often a loss of internal rotation and a magnification of external rotation. Your results would suggest this and you would benefit from some correctives to help address this posture and rib cage dynamics. This position also has consequences during gait.

There are some obvious compensations occurring at the hip; with different strategies are being utilised to generate forward propulsion during gait/running and when pushing through the ground in closed-chain movements common when transferring force. Internal rotation is also closely paired with achieving hip extension, both movements had limitations in your case. When both are reduced this would indicate the spine is being overused to generate a downward force. Alongside working on your downforce, we need to build some awareness of the mid foot and pressurising through the floor.

Our method would be to increase range of motion at the hip and integrate lots of work around the foot to help you load into tissues in the most efficient pattern. This will ensure key areas are not being overloaded. Increasing range will allow for better articulation of the joint, this will in turn improve muscle contraction quality and we can begin the address the force discrepancies at the knee and the hip.

In order to move your shoulder girdle more efficiently, we need to address your ribcage and scapula mechanics. We believe you would adapt to this faster through a high level of resistance (heavy isometrics and eccentrics) after fascial release work. A large emphasis should be on your deltoids and rotator cuff complex as well as the scapula.

REMEMBER: Only include paragraphs for assessment sections that are actually provided in the input. If shoulder assessment is missing, do not include the shoulder paragraph."""

        # Generate response using OpenAI GPT-4o-mini
        if input_string.strip():
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
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
                temperature=0.1,  # Low temperature for consistent template adherence
                max_tokens=800,
                top_p=0.6
            )
            return response.choices[0].message.content.strip()
        else:
            return "No valid assessment data available for conclusion generation."
        
    except Exception as e:
        return f"Error processing biomechanical conclusion: {e}"
    
# ...existing imports and functions...

import re as _re

def _extract_deficits_from_section(section_name: str, text: str):
    """
    Parse a conclusion/summary text and return a list of concrete deficit
    strings.  Returns an empty list when no meaningful deficits are found,
    which means the section should be excluded from the priority list.

    Handles every conclusion format used in the pipeline:
      - Hip / Knee  → "Range Deficits:" / "Strength Deficits:" with "Left →" / "Right →"
      - Shoulder    → "Deficits:" with "Left:" / "Right:" or the sentinel
                       "No significant deficits …"
      - Posture     → "Posture Assessment: <type>" (empty type = no deficit)
      - Ankle       → Free-form LLM prose; scan for deficit keywords
    """
    if not text or not text.strip():
        return []

    deficits: list[str] = []
    text_lower = text.lower()

    # ── Shoulder ──────────────────────────────────────────────────────
    if section_name == "shoulder":
        if "no significant deficits" in text_lower or "no  significant deficits" in text_lower:
            return []
        # Parse structured "Deficits:" block
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.lower().startswith("left:") or stripped.lower().startswith("right:"):
                items = stripped.split(":", 1)[1].strip()
                if items:
                    deficits.append(stripped)
        return deficits

    # ── Hip / Knee (identical structured format) ──────────────────────
    if section_name in ("hip", "knee"):
        for line in text.splitlines():
            stripped = line.strip()
            # Lines like "Left → Flexion, Extension, Internal Rotation"
            if "→" in stripped:
                after_arrow = stripped.split("→", 1)[1].strip()
                if after_arrow:  # has actual items
                    deficits.append(stripped)
        return deficits

    # ── Posture ───────────────────────────────────────────────────────
    if section_name == "posture":
        # metrics[7] = posture_assessment_1  (e.g. "These readings indicate …")
        posture_keywords = [
            "sway back", "forward head", "flat back", "kyphotic",
            "kyphosis", "lordosis",
        ]
        for kw in posture_keywords:
            if kw in text_lower:
                deficits.append(kw)
        return deficits

    # ── Ankle / Foot (free-form prose) ────────────────────────────────
    if section_name == "foot":
        deficit_keywords = [
            "poor", "lacking", "lack", "deficit", "limited",
            "restricted", "weak", "reduced", "insufficient",
            "asymmetry",
        ]
        for kw in deficit_keywords:
            if kw in text_lower:
                deficits.append(kw)
        return deficits

    return deficits


def _summarise_deficits(section_name: str, text: str, deficit_items: list[str]) -> str:
    """
    Return a short, structured summary of what the deficits actually are so
    the LLM prompt receives concrete data rather than raw prose.
    """
    if section_name in ("hip", "knee"):
        # Already has nice "Left → …" / "Right → …" lines
        range_defs = []
        strength_defs = []
        current_group = None
        for line in text.splitlines():
            low = line.strip().lower()
            if "range deficit" in low:
                current_group = "range"
            elif "strength deficit" in low:
                current_group = "strength"
            elif "→" in line.strip():
                if current_group == "range":
                    range_defs.append(line.strip())
                elif current_group == "strength":
                    strength_defs.append(line.strip())
        parts = []
        if range_defs:
            parts.append("Range deficits: " + "; ".join(range_defs))
        if strength_defs:
            parts.append("Strength deficits: " + "; ".join(strength_defs))
        return " | ".join(parts) if parts else "; ".join(deficit_items)

    if section_name == "shoulder":
        return "; ".join(deficit_items)

    if section_name == "posture":
        return ", ".join(deficit_items)

    if section_name == "foot":
        # just flag that deficits exist; the LLM will interpret the prose
        return "Deficits identified in foot/ankle complex"

    return "; ".join(deficit_items)


# ── Tie-break order (lower index = higher clinical priority) ──────
_TIE_BREAK_ORDER = {"hip": 0, "knee": 1, "foot": 2, "shoulder": 3, "posture": 4}


def _score_section_deficits(section_name: str, text: str, deficit_items: list[str]) -> float:
    """
    Calculate a weighted deficit score for a body-part section.

    Higher score = more / more severe deficits = higher priority.

    Weighting rules:
      • Each distinct deficit movement or keyword counts as a base point.
      • Strength deficits are weighted 1.5× (more impactful than range).
      • "poor" / "large deficit" severity keywords get an extra 0.5 per occurrence.
      • Bilateral deficits (same movement listed on both Left and Right) get a
        1.25× multiplier for that movement.

    Section-specific parsing:
      hip / knee  – structured "Range Deficits:" / "Strength Deficits:" blocks
      shoulder    – each "Left:" / "Right:" deficit item = 1 point
      posture     – each keyword match = 1 point
      foot        – severity-weighted keyword count from prose
    """
    if not deficit_items:
        return 0.0

    score = 0.0

    # ── Hip / Knee ────────────────────────────────────────────────────
    if section_name in ("hip", "knee"):
        range_left = []
        range_right = []
        strength_left = []
        strength_right = []
        current_group = None

        for line in text.splitlines():
            low = line.strip().lower()
            if "range deficit" in low:
                current_group = "range"
                continue
            elif "strength deficit" in low:
                current_group = "strength"
                continue

            if "→" not in line:
                continue
            side_part, items_part = line.strip().split("→", 1)
            side = side_part.strip().lower()
            movements = [m.strip() for m in items_part.split(",") if m.strip()]

            if current_group == "range":
                if "left" in side:
                    range_left = movements
                elif "right" in side:
                    range_right = movements
            elif current_group == "strength":
                if "left" in side:
                    strength_left = movements
                elif "right" in side:
                    strength_right = movements

        # Score range deficits (1.0 each, +0.25 if bilateral)
        all_range = set(m.lower() for m in range_left + range_right)
        for m in all_range:
            bilateral = (m in [x.lower() for x in range_left]) and (m in [x.lower() for x in range_right])
            score += 1.25 if bilateral else 1.0

        # Score strength deficits (1.5 each, +0.25 if bilateral)
        all_strength = set(m.lower() for m in strength_left + strength_right)
        for m in all_strength:
            bilateral = (m in [x.lower() for x in strength_left]) and (m in [x.lower() for x in strength_right])
            score += 1.75 if bilateral else 1.5

        return score

    # ── Shoulder ──────────────────────────────────────────────────────
    if section_name == "shoulder":
        left_items = []
        right_items = []
        for item in deficit_items:
            low = item.lower()
            if low.startswith("left:"):
                left_items = [x.strip() for x in item.split(":", 1)[1].split(",") if x.strip()]
            elif low.startswith("right:"):
                right_items = [x.strip() for x in item.split(":", 1)[1].split(",") if x.strip()]

        all_items = set(x.lower() for x in left_items + right_items)
        for it in all_items:
            bilateral = (it in [x.lower() for x in left_items]) and (it in [x.lower() for x in right_items])
            score += 1.25 if bilateral else 1.0
        return score

    # ── Posture ───────────────────────────────────────────────────────
    if section_name == "posture":
        # Posture usually yields only 1 keyword, so weight each at 2.0
        # to keep it competitive with multi-deficit sections.
        return float(len(deficit_items)) * 3.0

    # ── Foot / Ankle (keyword severity) ───────────────────────────────
    if section_name == "foot":
        severity_weights = {
            "poor": 1.5, "weak": 1.5, "insufficient": 1.5,
            "lacking": 1.0, "lack": 1.0, "deficit": 1.0,
            "limited": 0.75, "restricted": 0.75, "reduced": 0.75,
            "asymmetry": 1.0,
        }
        for kw in deficit_items:
            score += severity_weights.get(kw, 1.0)
        return score

    return float(len(deficit_items))


def test_biomech_priority_list(
    posture_text: str,
    hip_text: str,
    knee_text: str,
    ankle_text: str,
    shoulder_text: str,
    openai_client
) -> str:
    """
    Generate a compact Priority List based on the same inputs used for the conclusion.
    Sections with NO meaningful deficits are excluded entirely.
    Uses British English and short, numbered lines.
    """
    try:
        # ── 1. Parse each section and keep only those with real deficits ──
        section_configs = [
            ("hip",      hip_text),
            ("shoulder", shoulder_text),
            ("foot",     ankle_text),
            ("knee",     knee_text),
            ("posture",  posture_text),
        ]

        scored_sections = []  # list of (name, summary, score)

        for name, txt in section_configs:
            if not txt or not txt.strip():
                continue
            deficits = _extract_deficits_from_section(name, txt)
            if not deficits:
                print(f"[Priority List] Skipping '{name}' – no meaningful deficits found.")
                continue
            summary = _summarise_deficits(name, txt, deficits)
            score = _score_section_deficits(name, txt, deficits)
            scored_sections.append((name, summary, score))
            print(f"[Priority List] '{name}' → score {score:.2f} | {summary}")

        # ── 2. Sort by score descending, tie-break by clinical order ──────
        scored_sections.sort(
            key=lambda x: (-x[2], _TIE_BREAK_ORDER.get(x[0], 99))
        )

        # If nothing to generate from
        if not scored_sections:
            return "Priority List:\nNo significant deficits identified across all assessments."

        # Build ordered input for the LLM
        label_map = {
            "hip": "Hip",
            "shoulder": "Shoulder",
            "foot": "Foot/Ankle",
            "knee": "Knee",
            "posture": "Posture",
        }
        input_parts = []
        available_sections = []
        for rank, (name, summary, score) in enumerate(scored_sections, 1):
            input_parts.append(f"{rank}. {label_map[name]} (priority score: {score:.1f}):\n{summary}")
            available_sections.append(name)

        input_string = "\n\n".join(input_parts)

        # ── 3. Build data-driven prompt (order is pre-determined) ─────────
        system_prompt = f"""You are a biomechanical assessment expert.
Create a compact priority list using ONLY the deficit data provided below.
ALWAYS use British English.

The sections below are ALREADY SORTED by priority (highest impact first).
You MUST output them in the EXACT ORDER given — do NOT re-order.

Adhere strictly to this output template and rules:

TEMPLATE:
Priority List:
1st) <Short priority for the first section listed>
2nd) <Short priority for the second section listed>
...one line per section, in the order provided.

RULES:
- Output lines in the SAME ORDER as the numbered input sections below.
- Each priority line MUST directly reference the SPECIFIC deficits provided in the input data.
- Do NOT invent or assume deficits that are not mentioned in the input.
- For example, if the shoulder input only mentions Shoulder "T", say "Improve shoulder scapular stability (Shoulder T)" — do NOT mention internal rotation or rotator cuff unless the input data says so.
- If a section has only 1-2 deficits, name them specifically (e.g. "Address hip flexion and extension range").
- If a section has 3 or more deficits, keep it general instead of listing every deficit (e.g. "Address hip range and strength deficits" or "Improve overall hip range and force production").
- NEVER list more than 2 specific movements in a single line — summarise broadly instead.
- Use short, direct sentences (max 15 words per line).
- Start each line with an ordinal: 1st), 2nd), 3rd), etc.
- Use action verbs: Address, Increase, Improve, Build, Enhance.
- Avoid raw numbers/percentages and priority scores.
- British English spelling (pressurise, emphasising, stabiliser, programme, etc.).
- No extra commentary, headings, or paragraphs — only the numbered lines.

EXAMPLE (for reference only — adapt to actual deficit data):
Priority List:
1st) Address hip range deficits in flexion and extension, then force.
2nd) Increase knee flexion range and hamstring strength.
3rd) Increase ability to pressurise correctly through the foot.
4th) Improve scapular stability and shoulder T isometric strength.
5th) Address flat back posture and thoracic curvature.

REMEMBER: Keep the order as given. Each line must reflect the SPECIFIC deficits from the input."""

        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_string}
            ],
            temperature=0.1,
            max_tokens=300,
            top_p=0.6
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Priority List:\nError generating priority list: {e}"

# ...existing code...
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
