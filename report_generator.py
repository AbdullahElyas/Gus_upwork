import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from jinja2 import Environment, FileSystemLoader
import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
import base64
from io import BytesIO
import range_force_metrics
from dotenv import load_dotenv
import openai
import json
from sheetid_fetch import get_sheet_ids_from_folder
from textllm import (
    test_biomech_conclusion,
    test_biomech_posture,
    test_biomech_core_function,
    test_biomech_foot,
    test_biomech_hip,
    test_biomech_knee,
    test_biomech_shoulder,
    test_biomech_hip_concise
)

# Import your existing functions
from posture_assess import (
    extract_sheet_metrics_footankle,
    extract_sheet_metrics_knee, 
    extract_sheet_metrics_hip,
    extract_sheet_metrics_shoulder,
    extract_sheet_metrics_posture,
    create_radar_chart_foot_ankle,
    create_radar_chart_knee,
    create_radar_chart_hip,
    create_radar_chart_shoulder
)

@dataclass
class AnkleData:
    # Range data
    dorsiflexion_range_left: str
    dorsiflexion_range_right: str
    plantarflexion_range_left: str
    plantarflexion_range_right: str
    
    # Range percentages and asymmetry
    dorsiflexion_left_percent: str
    dorsiflexion_right_percent: str
    dorsiflexion_asymmetry: str
    plantarflexion_left_percent: str
    plantarflexion_right_percent: str
    plantarflexion_asymmetry: str
    
    # Force data
    dorsiflexion_force_left: str
    dorsiflexion_force_right: str
    plantarflexion_force_left: str
    plantarflexion_force_right: str
    
    # Force percentages and asymmetry
    dorsiflexion_force_left_percent: str
    dorsiflexion_force_right_percent: str
    dorsiflexion_force_asymmetry: str
    plantarflexion_force_left_percent: str
    plantarflexion_force_right_percent: str
    plantarflexion_force_asymmetry: str

@dataclass
class KneeData:
    # Range data
    flexion_range_left: str
    flexion_range_right: str
    extension_range_left: str
    extension_range_right: str
    
    # Range percentages and asymmetry
    flexion_left_percent: str
    flexion_right_percent: str
    flexion_asymmetry: str
    extension_left_percent: str
    extension_right_percent: str
    extension_asymmetry: str
    
    # Force data
    flexion_force_left: str
    flexion_force_right: str
    extension_force_left: str
    extension_force_right: str
    hamstring_quad_ratio_left: str
    hamstring_quad_ratio_right: str
    
    # Force percentages and asymmetry
    flexion_force_left_percent: str
    flexion_force_right_percent: str
    flexion_force_asymmetry: str
    extension_force_left_percent: str
    extension_force_right_percent: str
    extension_force_asymmetry: str
    hq_ratio_left_percent: str
    hq_ratio_right_percent: str
    hq_ratio_asymmetry: str

@dataclass
class HipData:
    # Range data
    flexion_range_left: str
    flexion_range_right: str
    extension_range_left: str
    extension_range_right: str
    abduction_range_left: str
    abduction_range_right: str
    adduction_range_left: str
    adduction_range_right: str
    ext_rotation_range_left: str
    ext_rotation_range_right: str
    int_rotation_range_left: str
    int_rotation_range_right: str
    
    # Range percentages and asymmetry
    flexion_left_percent: str
    flexion_right_percent: str
    flexion_asymmetry: str
    extension_left_percent: str
    extension_right_percent: str
    extension_asymmetry: str
    abduction_left_percent: str
    abduction_right_percent: str
    abduction_asymmetry: str
    adduction_left_percent: str
    adduction_right_percent: str
    adduction_asymmetry: str
    ext_rotation_left_percent: str
    ext_rotation_right_percent: str
    ext_rotation_asymmetry: str
    int_rotation_left_percent: str
    int_rotation_right_percent: str
    int_rotation_asymmetry: str
    
    # Force data
    flexion_force_left: str
    flexion_force_right: str
    extension_force_left: str
    extension_force_right: str
    abduction_force_left: str
    abduction_force_right: str
    adduction_force_left: str
    adduction_force_right: str
    ext_rotation_force_left: str
    ext_rotation_force_right: str
    int_rotation_force_left: str
    int_rotation_force_right: str
    
    # Force percentages and asymmetry
    flexion_force_left_percent: str
    flexion_force_right_percent: str
    flexion_force_asymmetry: str
    extension_force_left_percent: str
    extension_force_right_percent: str
    extension_force_asymmetry: str
    abduction_force_left_percent: str
    abduction_force_right_percent: str
    abduction_force_asymmetry: str
    adduction_force_left_percent: str
    adduction_force_right_percent: str
    adduction_force_asymmetry: str
    ext_rotation_force_left_percent: str
    ext_rotation_force_right_percent: str
    ext_rotation_force_asymmetry: str
    int_rotation_force_left_percent: str
    int_rotation_force_right_percent: str
    int_rotation_force_asymmetry: str

@dataclass
class ShoulderData:
    # Range data
    ext_rotation_range_left: str
    ext_rotation_range_right: str
    int_rotation_range_left: str
    int_rotation_range_right: str
    flexion_range_left: str
    flexion_range_right: str
    extension_range_left: str
    extension_range_right: str
    
    # Range percentages and asymmetry
    ext_rotation_left_percent: str
    ext_rotation_right_percent: str
    ext_rotation_asymmetry: str
    int_rotation_left_percent: str
    int_rotation_right_percent: str
    int_rotation_asymmetry: str
    flexion_left_percent: str
    flexion_right_percent: str
    flexion_asymmetry: str
    extension_left_percent: str
    extension_right_percent: str
    extension_asymmetry: str
    
    # Force data
    ext_rotation_force_left: str
    ext_rotation_force_right: str
    int_rotation_force_left: str
    int_rotation_force_right: str
    flexion_force_left: str
    flexion_force_right: str
    i_iso_left: str
    i_iso_right: str
    y_iso_left: str
    y_iso_right: str
    t_iso_left: str
    t_iso_right: str
    
    # Force percentages and asymmetry
    ext_rotation_force_left_percent: str
    ext_rotation_force_right_percent: str
    ext_rotation_force_asymmetry: str
    int_rotation_force_left_percent: str
    int_rotation_force_right_percent: str
    int_rotation_force_asymmetry: str
    flexion_force_left_percent: str
    flexion_force_right_percent: str
    flexion_force_asymmetry: str
    i_iso_left_percent: str
    i_iso_right_percent: str
    i_iso_asymmetry: str
    y_iso_left_percent: str
    y_iso_right_percent: str
    y_iso_asymmetry: str
    t_iso_left_percent: str
    t_iso_right_percent: str
    t_iso_asymmetry: str

@dataclass
class ThoracicData:
    ribcage_rotation_left : float
    ribcage_rotation_right : float
    ribcage_flexion_left : float
    ribcage_flexion_right : float
    ribcage_rotation_asymmetry : float
    ribcage_flexion_asymmetry : float
    ribcage_rotation_left_percent : float
    ribcage_rotation_right_percent : float
    ribcage_flexion_left_percent : float
    ribcage_flexion_right_percent : float


class BiomechanicalReportGenerator:
    def __init__(self, template_dir: str = "./", sheet_id: str = ""):
        """Initialize the report generator with template directory"""
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template('biomechanical_report_template.html')
        # get the worksheets
        scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
        drive_service = build('drive', 'v3', credentials=creds)
        

    # Open the Google Sheet
        sheet = client.open_by_key(sheet_id)
        # create an empty string self.Conclusion
        self.Conclusion_Posture = ""
        self.Conclusion_Hip = ""
        self.Conclusion_Knee = ""
        self.Conclusion_Ankle = ""
        self.Conclusion_Shoulder = ""
        self.Conclusion = ""
        self.FOLDER_ID = '1Tp9NL94dqQVD8XiZVjNH4_yT4CGhFER4'  # Not the link! Just the ID
        try:
            self.SheetID = get_sheet_ids_from_folder(self.FOLDER_ID, drive_service)
        except Exception as e:
            print(f"Error fetching sheet IDs from folder: {e}")
            # Fallback: read from text file
            try:
                with open("sheetid_fetch.txt", "r", encoding="utf-8") as f:
                    self.SheetID = [line.strip() for line in f if line.strip()]
            except Exception as e2:
                print(f"Error reading sheet IDs from sheetid_fetch.txt: {e2}")
                self.SheetID = []

    # read the values from 7th row in the second sheet
        worksheet = sheet.get_worksheet(1)
        data_overview_sheet = sheet.worksheet("Data Overview")
        first_worksheet = sheet.get_worksheet(0)
        third_worksheet = sheet.get_worksheet(2)
        self.worksheet = worksheet
        self.second_worksheet = worksheet
        self.data_overview_sheet = data_overview_sheet
        self.first_worksheet = first_worksheet
        self.third_worksheet = third_worksheet
        self.mass = 1
        # Load environment variables from .env file
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            openai_client = openai.OpenAI(api_key=openai_api_key)
            self.openai_client = openai_client
        else:
            self.openai_client = None

        # Define gold standards
        self.gold_standards = {
            'ankle': {
                'dorsiflexion_range': 30,
                'plantarflexion_range': 165,
                'dorsiflexion_force': 0.92,
                'plantarflexion_force': 2.52
            },
            'knee': {
                'flexion_range': 160,
                'extension_range': 170,
                'flexion_force': 0.31,
                'extension_force': 0.71,
                'hq_ratio': 0.60
            },
            'hip': {
                'flexion_range': 90,
                'extension_range': 30,
                'abduction_range': 55,
                'adduction_range': 35,
                'ext_rotation_range': 45,
                'int_rotation_range': 40,
                'flexion_force': 0.43,
                'extension_force': 0.3,
                'abduction_force': 0.23,
                'adduction_force': 0.35,
                'ext_rotation_force': 0.21,
                'int_rotation_force': 0.30
            },
            'shoulder': {
                'ext_rotation_range': 90,
                'int_rotation_range': 70,
                'flexion_range': 180,
                'extension_range': 60,
                'ext_rotation_force': 0.27,
                'int_rotation_force': 0.22,
                'flexion_force': 0.55,
                'i_iso': 0.25,
                'y_iso': 0.30,
                't_iso': 0.28
            },
            'thoracic': {
                'ribcage_rotation': 75,
                'ribcage_flexion': 55

            }
        }
    
    def safe_float_convert(self, value, default=0.0):
        """Safely convert value to float"""
        if value is None or value == "unavailable data" or value == "":
            return default
        try:
            return float(str(value).strip())
        except (ValueError, TypeError):
            return default
    def calculate_range_from_percentage(self, percentage, gold_standard):
        """Calculate range from percentage of gold standard"""
        try:
            perc = self.safe_float_convert(percentage)
            gs = self.safe_float_convert(gold_standard)
            if perc == 0 or gs == 0:
                return "0"
            # Calculate the range value from the percentage
            range_value = (perc / 100) * gs
            return f"{range_value:.1f}"
        except:
            return "0"

    def calculate_force_from_percentage(self, percentage, gold_standard):
        """Calculate force from percentage of gold standard using value * gs * 9.81 / 100"""
        try:
            perc = self.safe_float_convert(percentage)
            gs = self.safe_float_convert(gold_standard)
            if perc == 0 or gs == 0:
                return "0"
            force_value = perc * gs * self.mass * 9.81 / 100
            return f"{force_value:.2f}"
        except:
            return "0"
    
    def calculate_asymmetry(self, left_value, right_value):
        """Calculate asymmetry percentage between left and right"""
        try:
            left = self.safe_float_convert(left_value)
            right = self.safe_float_convert(right_value)
            
            if left == 0 and right == 0:
                return "0"
            
            # Calculate asymmetry as percentage difference from the larger value
            max_val = max(left, right)
            min_val = min(left, right)
            
            if max_val == 0:
                return "0"
            
            asymmetry = ((max_val - min_val) / max_val) * 100
            return f"{asymmetry:.1f}"
        except:
            return "0"

    def extract_ankle_data(self, sheet_id: str) -> Optional[AnkleData]:
        """Extract ankle/foot data from the sheet with calculations"""
        
        try:
            metrics = extract_sheet_metrics_footankle(sheet_id, self.data_overview_sheet, self.second_worksheet)
            metrics_raw = range_force_metrics.extract_range_force_footankle(sheet_id, self.data_overview_sheet, self.second_worksheet)
            if metrics and len(metrics) >= 8:
                # Raw data percentage
                dorsi_range_left = str(metrics[0]) if metrics[0] is not None else "unavailable data"
                dorsi_range_right = str(metrics[1]) if metrics[1] is not None else "unavailable data"
                plant_range_left = str(metrics[2]) if metrics[2] is not None else "unavailable data"
                plant_range_right = str(metrics[3]) if metrics[3] is not None else "unavailable data"
                dorsi_force_left = str(metrics[4]) if metrics[4] is not None else "unavailable data"
                dorsi_force_right = str(metrics[5]) if metrics[5] is not None else "unavailable data"
                plant_force_left = str(metrics[6]) if metrics[6] is not None else "unavailable data"
                plant_force_right = str(metrics[7]) if metrics[7] is not None else "unavailable data"

                # Gold standards
                gs = self.gold_standards['ankle']

                # Prepare force values for asymmetry calculation
                dorsiflexion_force_left_val = metrics_raw[4]
                dorsiflexion_force_right_val = metrics_raw[5]
                plantarflexion_force_left_val = metrics_raw[6]
                plantarflexion_force_right_val = metrics_raw[7]

                # Convert to float if not "unavailable data"
                def safe_force(val):
                    try:
                        if val is not None and str(val) != "unavailable data":
                            return float(val)
                    except Exception:
                        pass
                    return 0.0

                dorsiflexion_force_left_float = safe_force(dorsiflexion_force_left_val)*9.81
                dorsiflexion_force_right_float = safe_force(dorsiflexion_force_right_val)*9.81
                plantarflexion_force_left_float = safe_force(plantarflexion_force_left_val)*9.81
                plantarflexion_force_right_float = safe_force(plantarflexion_force_right_val)*9.81

                return AnkleData(
                    # Range data (calculated from percentage, rounded to whole number)
                    dorsiflexion_range_left=str(round(float(self.calculate_range_from_percentage(metrics[0], gs['dorsiflexion_range'])))),
                    dorsiflexion_range_right=str(round(float(self.calculate_range_from_percentage(metrics[1], gs['dorsiflexion_range'])))),
                    plantarflexion_range_left=str(round(float(self.calculate_range_from_percentage(metrics[2], gs['plantarflexion_range'])))),
                    plantarflexion_range_right=str(round(float(self.calculate_range_from_percentage(metrics[3], gs['plantarflexion_range'])))),
                    
                    # Range percentages and asymmetry
                    dorsiflexion_left_percent=str(round(float(metrics[0]))),
                    dorsiflexion_right_percent=str(round(float(metrics[1]))),
                    dorsiflexion_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(metrics[0], gs['dorsiflexion_range']),
                        self.calculate_range_from_percentage(metrics[1], gs['dorsiflexion_range'])
                    ),
                    plantarflexion_left_percent=str(round(float(metrics[2]))),
                    plantarflexion_right_percent=str(round(float(metrics[3]))),
                    plantarflexion_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(metrics[2], gs['plantarflexion_range']),
                        self.calculate_range_from_percentage(metrics[3], gs['plantarflexion_range'])
                    ),
                    
                    # Force data (raw float values, rounded to whole number)
                    dorsiflexion_force_left=str(round(dorsiflexion_force_left_float)),
                    dorsiflexion_force_right=str(round(dorsiflexion_force_right_float)),
                    plantarflexion_force_left=str(round(plantarflexion_force_left_float)),
                    plantarflexion_force_right=str(round(plantarflexion_force_right_float)),

                    # Force percentages and asymmetry
                    dorsiflexion_force_left_percent=str(round(float(metrics[4]))),
                    dorsiflexion_force_right_percent=str(round(float(metrics[5]))),
                    dorsiflexion_force_asymmetry=self.calculate_asymmetry(
                        dorsiflexion_force_left_float,
                        dorsiflexion_force_right_float
                    ),
                    plantarflexion_force_left_percent=str(round(float(metrics[6]))),
                    plantarflexion_force_right_percent=str(round(float(metrics[7]))),
                    plantarflexion_force_asymmetry=self.calculate_asymmetry(
                        plantarflexion_force_left_float,
                        plantarflexion_force_right_float
                    )
                )
        except Exception as e:
            print(f"Error extracting ankle data: {e}")
        return None

    def extract_knee_data(self, sheet_id: str) -> Optional[KneeData]:
        """Extract knee data from the sheet with calculations"""
        try:
            metrics = extract_sheet_metrics_knee(sheet_id, self.data_overview_sheet)
            metrics_raw = range_force_metrics.extract_range_force_knee(sheet_id, self.data_overview_sheet, self.second_worksheet)
            if metrics and len(metrics) >= 14:
                # Raw data
                flex_range_left = str(metrics[0])
                flex_range_right = str(metrics[1])
                ext_range_left = str(metrics[2])
                ext_range_right = str(metrics[3])
                flex_force_left = str(metrics[4])
                flex_force_right = str(metrics[5])
                ext_force_left = str(metrics[6])
                ext_force_right = str(metrics[7])
                hq_ratio_left = str(metrics[12])
                hq_ratio_right = str(metrics[13])
                
                # Calculate percentages and asymmetry
                gs = self.gold_standards['knee']
                
                # Prepare force values for asymmetry calculation (raw values)
                flexion_force_left_val = metrics_raw[4]
                flexion_force_right_val = metrics_raw[5]
                extension_force_left_val = metrics_raw[6]
                extension_force_right_val = metrics_raw[7]

                def safe_force(val):
                    try:
                        if val is not None and str(val) != "unavailable data":
                            return float(val)
                    except Exception:
                        pass
                    return 0.0

                flexion_force_left_float = safe_force(flexion_force_left_val)*9.81
                flexion_force_right_float = safe_force(flexion_force_right_val)*9.81
                extension_force_left_float = safe_force(extension_force_left_val)*9.81
                extension_force_right_float = safe_force(extension_force_right_val)*9.81

                return KneeData(
                    # Range data (calculated from percentage, rounded to whole number)
                    flexion_range_left=str(round(float(self.calculate_range_from_percentage(metrics[0], gs['flexion_range'])))),
                    flexion_range_right=str(round(float(self.calculate_range_from_percentage(metrics[1], gs['flexion_range'])))),
                    extension_range_left=str(round(float(self.calculate_range_from_percentage(metrics[2], gs['extension_range'])))),
                    extension_range_right=str(round(float(self.calculate_range_from_percentage(metrics[3], gs['extension_range'])))),
                    
                    # Range percentages and asymmetry
                    flexion_left_percent=str(round(float(metrics[0]))),
                    flexion_right_percent=str(round(float(metrics[1]))),
                    flexion_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(metrics[0], gs['flexion_range']),
                        self.calculate_range_from_percentage(metrics[1], gs['flexion_range'])
                    ),
                    extension_left_percent=str(round(float(metrics[2]))),
                    extension_right_percent=str(round(float(metrics[3]))),
                    extension_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(metrics[2], gs['extension_range']),
                        self.calculate_range_from_percentage(metrics[3], gs['extension_range'])
                    ),
                    
                    # Force data (raw values, rounded to whole number)
                    flexion_force_left=str(round(flexion_force_left_float)),
                    flexion_force_right=str(round(flexion_force_right_float)),
                    extension_force_left=str(round(extension_force_left_float)),
                    extension_force_right=str(round(extension_force_right_float)),
                    hamstring_quad_ratio_left=str(round(self.safe_float_convert(metrics[12]))),
                    hamstring_quad_ratio_right=str(round(self.safe_float_convert(metrics[13]))),
                    
                    # Force percentages and asymmetry
                    flexion_force_left_percent=str(round(float(metrics[4]))),
                    flexion_force_right_percent=str(round(float(metrics[5]))),
                    flexion_force_asymmetry=self.calculate_asymmetry(
                        flexion_force_left_float,
                        flexion_force_right_float
                    ),
                    extension_force_left_percent=str(round(float(metrics[6]))),
                    extension_force_right_percent=str(round(float(metrics[7]))),
                    extension_force_asymmetry=self.calculate_asymmetry(
                        extension_force_left_float,
                        extension_force_right_float
                    ),
                    hq_ratio_left_percent=str(round(float(metrics[12]))),
                    hq_ratio_right_percent=str(round(float(metrics[13]))),
                    hq_ratio_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(metrics[12], gs['hq_ratio']),
                        self.calculate_range_from_percentage(metrics[13], gs['hq_ratio'])
                    )
                )
        except Exception as e:
            print(f"Error extracting knee data: {e}")
        return None

    def extract_hip_data(self, sheet_id: str) -> Optional[HipData]:
        """Extract hip data from the sheet with calculations"""
        try:
            metrics = extract_sheet_metrics_hip(sheet_id, self.data_overview_sheet)
            metrics_raw = range_force_metrics.extract_range_force_hip(sheet_id, self.data_overview_sheet)
            if metrics and len(metrics) >= 24:
                # Raw data extraction
                raw_data = {
                    'flexion_range_left': str(metrics[0]),
                    'flexion_range_right': str(metrics[1]),
                    'extension_range_left': str(metrics[2]),
                    'extension_range_right': str(metrics[3]),
                    'abduction_range_left': str(metrics[4]),
                    'abduction_range_right': str(metrics[5]),
                    'adduction_range_left': str(metrics[6]),
                    'adduction_range_right': str(metrics[7]),
                    'ext_rotation_range_left': str(metrics[8]),
                    'ext_rotation_range_right': str(metrics[9]),
                    'int_rotation_range_left': str(metrics[10]),
                    'int_rotation_range_right': str(metrics[11]),
                    'flexion_force_left': str(metrics[12]),
                    'flexion_force_right': str(metrics[13]),
                    'extension_force_left': str(metrics[14]),
                    'extension_force_right': str(metrics[15]),
                    'abduction_force_left': str(metrics[16]),
                    'abduction_force_right': str(metrics[17]),
                    'adduction_force_left': str(metrics[18]),
                    'adduction_force_right': str(metrics[19]),
                    'ext_rotation_force_left': str(metrics[20]),
                    'ext_rotation_force_right': str(metrics[21]),
                    'int_rotation_force_left': str(metrics[22]),
                    'int_rotation_force_right': str(metrics[23])
                }
                
                gs = self.gold_standards['hip']
                
                # Prepare force values for asymmetry calculation (raw values)
                flexion_force_left_val = metrics_raw[12]
                flexion_force_right_val = metrics_raw[13]
                extension_force_left_val = metrics_raw[14]
                extension_force_right_val = metrics_raw[15]
                abduction_force_left_val = metrics_raw[16]
                abduction_force_right_val = metrics_raw[17]
                adduction_force_left_val = metrics_raw[18]
                adduction_force_right_val = metrics_raw[19]
                ext_rotation_force_left_val = metrics_raw[20]
                ext_rotation_force_right_val = metrics_raw[21]
                int_rotation_force_left_val = metrics_raw[22]
                int_rotation_force_right_val = metrics_raw[23]

                def safe_force(val):
                    try:
                        if val is not None and str(val) != "unavailable data":
                            return float(val)
                    except Exception:
                        pass
                    return 0.0

                flexion_force_left_float = safe_force(flexion_force_left_val)*9.81
                flexion_force_right_float = safe_force(flexion_force_right_val)*9.81
                extension_force_left_float = safe_force(extension_force_left_val)*9.81
                extension_force_right_float = safe_force(extension_force_right_val)*9.81
                abduction_force_left_float = safe_force(abduction_force_left_val)*9.81
                abduction_force_right_float = safe_force(abduction_force_right_val)*9.81
                adduction_force_left_float = safe_force(adduction_force_left_val)*9.81
                adduction_force_right_float = safe_force(adduction_force_right_val)*9.81
                ext_rotation_force_left_float = safe_force(ext_rotation_force_left_val)*9.81
                ext_rotation_force_right_float = safe_force(ext_rotation_force_right_val)*9.81
                int_rotation_force_left_float = safe_force(int_rotation_force_left_val)*9.81
                int_rotation_force_right_float = safe_force(int_rotation_force_right_val)*9.81

                return HipData(
                    # Range data (calculated from percentage)
                    flexion_range_left=round(float(self.calculate_range_from_percentage(raw_data['flexion_range_left'], gs['flexion_range']))),
                    flexion_range_right=round(float(self.calculate_range_from_percentage(raw_data['flexion_range_right'], gs['flexion_range']))),
                    extension_range_left=round(float(self.calculate_range_from_percentage(raw_data['extension_range_left'], gs['extension_range']))),
                    extension_range_right=round(float(self.calculate_range_from_percentage(raw_data['extension_range_right'], gs['extension_range']))),
                    abduction_range_left=round(float(self.calculate_range_from_percentage(raw_data['abduction_range_left'], gs['abduction_range']))),
                    abduction_range_right=round(float(self.calculate_range_from_percentage(raw_data['abduction_range_right'], gs['abduction_range']))),
                    adduction_range_left=round(float(self.calculate_range_from_percentage(raw_data['adduction_range_left'], gs['adduction_range']))),
                    adduction_range_right=round(float(self.calculate_range_from_percentage(raw_data['adduction_range_right'], gs['adduction_range']))),
                    ext_rotation_range_left=round(float(self.calculate_range_from_percentage(raw_data['ext_rotation_range_left'], gs['ext_rotation_range']))),
                    ext_rotation_range_right=round(float(self.calculate_range_from_percentage(raw_data['ext_rotation_range_right'], gs['ext_rotation_range']))),
                    int_rotation_range_left=round(float(self.calculate_range_from_percentage(raw_data['int_rotation_range_left'], gs['int_rotation_range']))),
                    int_rotation_range_right=round(float(self.calculate_range_from_percentage(raw_data['int_rotation_range_right'], gs['int_rotation_range']))),
                    
                    # Range percentages and asymmetry
                    flexion_left_percent=str(round(float(raw_data['flexion_range_left']))),
                    flexion_right_percent=str(round(float(raw_data['flexion_range_right']))),
                    flexion_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(raw_data['flexion_range_left'], gs['flexion_range']),
                        self.calculate_range_from_percentage(raw_data['flexion_range_right'], gs['flexion_range'])
                    ),
                    extension_left_percent=str(round(float(raw_data['extension_range_left']))),
                    extension_right_percent=str(round(float(raw_data['extension_range_right']))),
                    extension_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(raw_data['extension_range_left'], gs['extension_range']),
                        self.calculate_range_from_percentage(raw_data['extension_range_right'], gs['extension_range'])
                    ),
                    abduction_left_percent=str(round(float(raw_data['abduction_range_left']))),
                    abduction_right_percent=str(round(float(raw_data['abduction_range_right']))),
                    abduction_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(raw_data['abduction_range_left'], gs['abduction_range']),
                        self.calculate_range_from_percentage(raw_data['abduction_range_right'], gs['abduction_range'])
                    ),
                    adduction_left_percent=str(round(float(raw_data['adduction_range_left']))),
                    adduction_right_percent=str(round(float(raw_data['adduction_range_right']))),
                    adduction_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(raw_data['adduction_range_left'], gs['adduction_range']),
                        self.calculate_range_from_percentage(raw_data['adduction_range_right'], gs['adduction_range'])
                    ),
                    ext_rotation_left_percent=str(round(float(raw_data['ext_rotation_range_left']))),
                    ext_rotation_right_percent=str(round(float(raw_data['ext_rotation_range_right']))),
                    ext_rotation_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(raw_data['ext_rotation_range_left'], gs['ext_rotation_range']),
                        self.calculate_range_from_percentage(raw_data['ext_rotation_range_right'], gs['ext_rotation_range'])
                    ),
                    int_rotation_left_percent=str(round(float(raw_data['int_rotation_range_left']))),
                    int_rotation_right_percent=str(round(float(raw_data['int_rotation_range_right']))),
                    int_rotation_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(raw_data['int_rotation_range_left'], gs['int_rotation_range']),
                        self.calculate_range_from_percentage(raw_data['int_rotation_range_right'], gs['int_rotation_range'])
                    ),
                    
                    # Force data (raw float values)
                    flexion_force_left=round(flexion_force_left_float),
                    flexion_force_right=round(flexion_force_right_float),
                    extension_force_left=round(extension_force_left_float),
                    extension_force_right=round(extension_force_right_float),
                    abduction_force_left=round(abduction_force_left_float),
                    abduction_force_right=round(abduction_force_right_float),
                    adduction_force_left=round(adduction_force_left_float),
                    adduction_force_right=round(adduction_force_right_float),
                    ext_rotation_force_left=round(ext_rotation_force_left_float),
                    ext_rotation_force_right=round(ext_rotation_force_right_float),
                    int_rotation_force_left=round(int_rotation_force_left_float),
                    int_rotation_force_right=round(int_rotation_force_right_float),

                    # Force percentages and asymmetry
                    flexion_force_left_percent=str(round(float(raw_data['flexion_force_left']))),
                    flexion_force_right_percent=str(round(float(raw_data['flexion_force_right']))),
                    flexion_force_asymmetry=self.calculate_asymmetry(
                        flexion_force_left_float,
                        flexion_force_right_float
                    ),
                    extension_force_left_percent=str(round(float(raw_data['extension_force_left']))),
                    extension_force_right_percent=str(round(float(raw_data['extension_force_right']))),
                    extension_force_asymmetry=self.calculate_asymmetry(
                        extension_force_left_float,
                        extension_force_right_float
                    ),
                    abduction_force_left_percent=str(round(float(raw_data['abduction_force_left']))),
                    abduction_force_right_percent=str(round(float(raw_data['abduction_force_right']))),
                    abduction_force_asymmetry=self.calculate_asymmetry(
                        abduction_force_left_float,
                        abduction_force_right_float
                    ),
                    adduction_force_left_percent=str(round(float(raw_data['adduction_force_left']))),
                    adduction_force_right_percent=str(round(float(raw_data['adduction_force_right']))),
                    adduction_force_asymmetry=self.calculate_asymmetry(
                        adduction_force_left_float,
                        adduction_force_right_float
                    ),
                    ext_rotation_force_left_percent=str(round(float(raw_data['ext_rotation_force_left']))),
                    ext_rotation_force_right_percent=str(round(float(raw_data['ext_rotation_force_right']))),
                    ext_rotation_force_asymmetry=self.calculate_asymmetry(
                        ext_rotation_force_left_float,
                        ext_rotation_force_right_float
                    ),
                    int_rotation_force_left_percent=str(round(float(raw_data['int_rotation_force_left']))),
                    int_rotation_force_right_percent=str(round(float(raw_data['int_rotation_force_right']))),
                    int_rotation_force_asymmetry=self.calculate_asymmetry(
                        int_rotation_force_left_float,
                        int_rotation_force_right_float
                    )
                )
        except Exception as e:
            print(f"Error extracting hip data: {e}")
        return None

    def extract_shoulder_data(self, sheet_id: str) -> Optional[ShoulderData]:
        """Extract shoulder data from the sheet with calculations"""
        try:
            metrics = extract_sheet_metrics_shoulder(sheet_id, self.data_overview_sheet)
            if metrics and len(metrics) >= 16:
                # Raw data extraction
                raw_data = {
                    'ext_rotation_range_left': str(metrics[0]),
                    'ext_rotation_range_right': str(metrics[1]),
                    'int_rotation_range_left': str(metrics[2]),
                    'int_rotation_range_right': str(metrics[3]),
                    'flexion_range_left': str(metrics[4]),
                    'flexion_range_right': str(metrics[5]),
                    'extension_range_left': str(metrics[6]),
                    'extension_range_right': str(metrics[7]),
                    'ext_rotation_force_left': str(metrics[8]),
                    'ext_rotation_force_right': str(metrics[9]),
                    'int_rotation_force_left': str(metrics[10]),
                    'int_rotation_force_right': str(metrics[11]),
                    'flexion_force_left': str(metrics[12]),
                    'flexion_force_right': str(metrics[13]),
                    'i_iso_left': str(metrics[14]),
                    'i_iso_right': str(metrics[15]),
                    'y_iso_left': str(metrics[16]) if len(metrics) > 16 else "unavailable data",
                    'y_iso_right': str(metrics[17]) if len(metrics) > 17 else "unavailable data",
                    't_iso_left': str(metrics[18]) if len(metrics) > 18 else "unavailable data",
                    't_iso_right': str(metrics[19]) if len(metrics) > 19 else "unavailable data"
                }
                
                gs = self.gold_standards['shoulder']
                
                def safe_float(val):
                    try:
                        if val is not None and str(val) != "unavailable data" and str(val) != "":
                            return float(str(val).strip())
                    except Exception:
                        pass
                    return 0.0

                def safe_str_round(val):
                    try:
                        return str(round(safe_float(val)))
                    except Exception:
                        return "0"

                def safe_calc_range(val, gs_val):
                    try:
                        return str(round(float(self.calculate_range_from_percentage(val, gs_val))))
                    except Exception:
                        return "0"

                def safe_calc_force(val, gs_val):
                    try:
                        return str(round(float(self.calculate_force_from_percentage(val, gs_val))))
                    except Exception:
                        return "0"

                def safe_asym(left, right, gs_val):
                    try:
                        return self.calculate_asymmetry(
                            self.calculate_range_from_percentage(left, gs_val),
                            self.calculate_range_from_percentage(right, gs_val)
                        )
                    except Exception:
                        return "0"

                def safe_force_asym(left, right, gs_val):
                    try:
                        return self.calculate_asymmetry(
                            self.calculate_force_from_percentage(left, gs_val),
                            self.calculate_force_from_percentage(right, gs_val)
                        )
                    except Exception:
                        return "0"

                return ShoulderData(
                    # Range data (calculated from percentage, rounded to whole number)
                    ext_rotation_range_left=safe_calc_range(raw_data['ext_rotation_range_left'], gs['ext_rotation_range']),
                    ext_rotation_range_right=safe_calc_range(raw_data['ext_rotation_range_right'], gs['ext_rotation_range']),
                    int_rotation_range_left=safe_calc_range(raw_data['int_rotation_range_left'], gs['int_rotation_range']),
                    int_rotation_range_right=safe_calc_range(raw_data['int_rotation_range_right'], gs['int_rotation_range']),
                    flexion_range_left=safe_calc_range(raw_data['flexion_range_left'], gs['flexion_range']),
                    flexion_range_right=safe_calc_range(raw_data['flexion_range_right'], gs['flexion_range']),
                    extension_range_left=safe_calc_range(raw_data['extension_range_left'], gs['extension_range']),
                    extension_range_right=safe_calc_range(raw_data['extension_range_right'], gs['extension_range']),
                    
                    # Range percentages and asymmetry
                    ext_rotation_left_percent=safe_str_round(raw_data['ext_rotation_range_left']),
                    ext_rotation_right_percent=safe_str_round(raw_data['ext_rotation_range_right']),
                    ext_rotation_asymmetry=safe_asym(raw_data['ext_rotation_range_left'], raw_data['ext_rotation_range_right'], gs['ext_rotation_range']),
                    int_rotation_left_percent=safe_str_round(raw_data['int_rotation_range_left']),
                    int_rotation_right_percent=safe_str_round(raw_data['int_rotation_range_right']),
                    int_rotation_asymmetry=safe_asym(raw_data['int_rotation_range_left'], raw_data['int_rotation_range_right'], gs['int_rotation_range']),
                    flexion_left_percent=safe_str_round(raw_data['flexion_range_left']),
                    flexion_right_percent=safe_str_round(raw_data['flexion_range_right']),
                    flexion_asymmetry=safe_asym(raw_data['flexion_range_left'], raw_data['flexion_range_right'], gs['flexion_range']),
                    extension_left_percent=safe_str_round(raw_data['extension_range_left']),
                    extension_right_percent=safe_str_round(raw_data['extension_range_right']),
                    extension_asymmetry=safe_asym(raw_data['extension_range_left'], raw_data['extension_range_right'], gs['extension_range']),
                    
                    # Force data (calculated from percentage, rounded to whole number)
                    ext_rotation_force_left=safe_calc_force(raw_data['ext_rotation_force_left'], gs['ext_rotation_force']),
                    ext_rotation_force_right=safe_calc_force(raw_data['ext_rotation_force_right'], gs['ext_rotation_force']),
                    int_rotation_force_left=safe_calc_force(raw_data['int_rotation_force_left'], gs['int_rotation_force']),
                    int_rotation_force_right=safe_calc_force(raw_data['int_rotation_force_right'], gs['int_rotation_force']),
                    flexion_force_left=safe_calc_force(raw_data['flexion_force_left'], gs['flexion_force']),
                    flexion_force_right=safe_calc_force(raw_data['flexion_force_right'], gs['flexion_force']),
                    i_iso_left=safe_calc_force(raw_data['i_iso_left'], gs['i_iso']),
                    i_iso_right=safe_calc_force(raw_data['i_iso_right'], gs['i_iso']),
                    y_iso_left=safe_calc_force(raw_data['y_iso_left'], gs['y_iso']),
                    y_iso_right=safe_calc_force(raw_data['y_iso_right'], gs['y_iso']),
                    t_iso_left=safe_calc_force(raw_data['t_iso_left'], gs['t_iso']),
                    t_iso_right=safe_calc_force(raw_data['t_iso_right'], gs['t_iso']),
                    
                    # Force percentages and asymmetry
                    ext_rotation_force_left_percent=safe_str_round(raw_data['ext_rotation_force_left']),
                    ext_rotation_force_right_percent=safe_str_round(raw_data['ext_rotation_force_right']),
                    ext_rotation_force_asymmetry=safe_force_asym(raw_data['ext_rotation_force_left'], raw_data['ext_rotation_force_right'], gs['ext_rotation_force']),
                    int_rotation_force_left_percent=safe_str_round(raw_data['int_rotation_force_left']),
                    int_rotation_force_right_percent=safe_str_round(raw_data['int_rotation_force_right']),
                    int_rotation_force_asymmetry=safe_force_asym(raw_data['int_rotation_force_left'], raw_data['int_rotation_force_right'], gs['int_rotation_force']),
                    flexion_force_left_percent=safe_str_round(raw_data['flexion_force_left']),
                    flexion_force_right_percent=safe_str_round(raw_data['flexion_force_right']),
                    flexion_force_asymmetry=safe_force_asym(raw_data['flexion_force_left'], raw_data['flexion_force_right'], gs['flexion_force']),
                    i_iso_left_percent=safe_str_round(raw_data['i_iso_left']),
                    i_iso_right_percent=safe_str_round(raw_data['i_iso_right']),
                    i_iso_asymmetry=safe_force_asym(raw_data['i_iso_left'], raw_data['i_iso_right'], gs['i_iso']),
                    y_iso_left_percent=safe_str_round(raw_data['y_iso_left']),
                    y_iso_right_percent=safe_str_round(raw_data['y_iso_right']),
                    y_iso_asymmetry=safe_force_asym(raw_data['y_iso_left'], raw_data['y_iso_right'], gs['y_iso']),
                    t_iso_left_percent=safe_str_round(raw_data['t_iso_left']),
                    t_iso_right_percent=safe_str_round(raw_data['t_iso_right']),
                    t_iso_asymmetry=safe_force_asym(raw_data['t_iso_left'], raw_data['t_iso_right'], gs['t_iso'])
                )
        except Exception as e:
            print(f"Error extracting shoulder data: {e}")
        return None

    def extract_thoracic_data(self, sheet_id: str) -> Optional[ThoracicData]:
        """Extract thoracic/ribcage data from the sheet with calculations"""

       
        try:
            metrics = extract_sheet_metrics_posture(sheet_id, self.worksheet, self.first_worksheet, self.third_worksheet)
            # append to self.Conclusion metric[7]
            if metrics and len(metrics) > 7:
                self.Conclusion_Posture += "\nPosture Assessment: " + str(metrics[7])
            if metrics and len(metrics) >= 15:
                ribcage_rotation_left = round(self.safe_float_convert(metrics[11]))
                ribcage_rotation_right = round(self.safe_float_convert(metrics[12]))
                ribcage_flexion_left = round(self.safe_float_convert(metrics[13]))
                ribcage_flexion_right = round(self.safe_float_convert(metrics[14]))

                gs = self.gold_standards['thoracic']

                # Calculate asymmetry (keep as float with 1 decimal)
                ribcage_rotation_asymmetry = float(self.calculate_asymmetry(ribcage_rotation_left, ribcage_rotation_right))
                ribcage_flexion_asymmetry = float(self.calculate_asymmetry(ribcage_flexion_left, ribcage_flexion_right))

                # Calculate percentages using gold standards, rounded to whole number
                ribcage_rotation_left_percent = (
                    round((ribcage_rotation_left / gs['ribcage_rotation']) * 100) if gs['ribcage_rotation'] else 0
                )
                ribcage_rotation_right_percent = (
                    round((ribcage_rotation_right / gs['ribcage_rotation']) * 100) if gs['ribcage_rotation'] else 0
                )
                ribcage_flexion_left_percent = (
                    round((ribcage_flexion_left / gs['ribcage_flexion']) * 100) if gs['ribcage_flexion'] else 0
                )
                ribcage_flexion_right_percent = (
                    round((ribcage_flexion_right / gs['ribcage_flexion']) * 100) if gs['ribcage_flexion'] else 0
                )

                return ThoracicData(
                    ribcage_rotation_left=ribcage_rotation_left,
                    ribcage_rotation_right=ribcage_rotation_right,
                    ribcage_flexion_left=ribcage_flexion_left,
                    ribcage_flexion_right=ribcage_flexion_right,
                    ribcage_rotation_asymmetry=ribcage_rotation_asymmetry,
                    ribcage_flexion_asymmetry=ribcage_flexion_asymmetry,
                    ribcage_rotation_left_percent=ribcage_rotation_left_percent,
                    ribcage_rotation_right_percent=ribcage_rotation_right_percent,
                    ribcage_flexion_left_percent=ribcage_flexion_left_percent,
                    ribcage_flexion_right_percent=ribcage_flexion_right_percent
                )
        except Exception as e:
            print(f"Error extracting thoracic data: {e}")
        return None

    # Rest of the methods remain the same (generate_radar_charts, get_assessment_texts, generate_report)
    def generate_radar_charts(self, sheet_id: str, output_dir: str = "./charts/") -> Dict[str, str]:
        """Generate radar charts and return their file paths"""
        os.makedirs(output_dir, exist_ok=True)
        charts = {}
        
        try:
            # Generate ankle chart
            ankle_chart_path = os.path.join(output_dir, "ankle_radar_chart.png")
            create_radar_chart_foot_ankle(sheet_id,self.data_overview_sheet, self.second_worksheet, ankle_chart_path)
            if os.path.exists(ankle_chart_path):
                charts['ankle'] = ankle_chart_path
        except Exception as e:
            print(f"Error generating ankle chart: {e}")
            
        try:
            # Generate knee chart
            knee_chart_path = os.path.join(output_dir, "knee_radar_chart.png")
            create_radar_chart_knee(sheet_id, self.data_overview_sheet, knee_chart_path)
            if os.path.exists(knee_chart_path):
                charts['knee'] = knee_chart_path
        except Exception as e:
            print(f"Error generating knee chart: {e}")
            
        try:
            # Generate hip chart
            hip_chart_path = os.path.join(output_dir, "hip_radar_chart.png")
            create_radar_chart_hip(sheet_id, self.data_overview_sheet, hip_chart_path)
            if os.path.exists(hip_chart_path):
                charts['hip'] = hip_chart_path
        except Exception as e:
            print(f"Error generating hip chart: {e}")
            
        try:
            # Generate shoulder chart
            shoulder_chart_path = os.path.join(output_dir, "shoulder_radar_chart.png")
            create_radar_chart_shoulder(sheet_id, self.data_overview_sheet, shoulder_chart_path)
            if os.path.exists(shoulder_chart_path):
                charts['shoulder'] = shoulder_chart_path
        except Exception as e:
            print(f"Error generating shoulder chart: {e}")
            
        return charts

    def get_assessment_texts(self, sheet_id: str) -> Dict[str, str]:
        """Get assessment texts from LLM functions, with caching"""

        assessments = {}
        cache_dir = "./cache"
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, f"{sheet_id}_assessments.json")

        # Try to load from cache
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                if isinstance(cached, dict):
                    return cached
            except Exception as e:
                print(f"Error loading cached assessments: {e}")

        # If not cached, generate assessments
        try:
            posture_result = test_biomech_posture(sheet_id, self.worksheet, self.first_worksheet, self.third_worksheet, self.openai_client)
            if posture_result and len(posture_result) >= 4:
                assessments['posture'] = posture_result.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting posture assessment: {e}")

        try:
            core_result = test_biomech_core_function(sheet_id, self.worksheet, self.first_worksheet, self.third_worksheet, self.openai_client)
            if core_result and len(core_result) >= 4:
                assessments['core'] = core_result.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting core assessment: {e}")

        try:
            ankle_result = test_biomech_foot(sheet_id, self.data_overview_sheet, self.second_worksheet, self.openai_client)
            if ankle_result and len(ankle_result) >= 3:
                assessments['ankle'] = ankle_result.replace('\n', '<br>')
                self.Conclusion_Ankle += "\nAnkle Assessment Conclusion: " + ankle_result
        except Exception as e:
            print(f"Error getting ankle assessment: {e}")

        try:
            knee_assessment, knee_conclusion = test_biomech_knee(sheet_id, self.data_overview_sheet, self.openai_client)
            if knee_conclusion:
                self.Conclusion_Knee += "\nKnee Assessment Conclusion: " + knee_conclusion
            if knee_assessment:
                assessments['knee'] = knee_assessment.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting knee assessment: {e}")

        try:
            hip_assessment, hip_conclusion = test_biomech_hip_concise(sheet_id, self.data_overview_sheet, self.openai_client)
            if hip_conclusion:
                self.Conclusion_Hip += "\nHip Assessment Conclusion: " + hip_conclusion
            if hip_assessment:
                assessments['hip'] = hip_assessment.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting hip assessment: {e}")

        try:
            shoulder_assessment, shoulder_conclusion = test_biomech_shoulder(sheet_id, self.data_overview_sheet, self.openai_client)
            if shoulder_assessment:
                assessments['shoulder'] = shoulder_assessment.replace('\n', '<br>')
            if shoulder_conclusion:
                self.Conclusion_Shoulder += "\nShoulder Assessment Conclusion: " + shoulder_conclusion
        except Exception as e:
            print(f"Error getting shoulder assessment: {e}")

        try:
            Conclusion_Input = test_biomech_conclusion(
                self.Conclusion_Posture,
                self.Conclusion_Hip,
                self.Conclusion_Knee,
                self.Conclusion_Ankle,
                self.Conclusion_Shoulder,
                self.openai_client
            )
            if Conclusion_Input and len(Conclusion_Input) >= 4:
                assessments['overall_conclusion'] = Conclusion_Input.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting overall conclusion: {e}")

        # Save to cache
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(assessments, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving assessments to cache: {e}")

        return assessments

    def generate_report(self, sheet_id: str, output_path: str = "biomechanical_report.html", 
                       charts_dir: str = "./charts/") -> str:
        """Generate the complete biomechanical assessment report"""
        
        print("Extracting data from sheet...")
        
        # Extract all data
        thoracic_data = self.extract_thoracic_data(sheet_id)
        hip_data = self.extract_hip_data(sheet_id)
        ankle_data = self.extract_ankle_data(sheet_id)
        knee_data = self.extract_knee_data(sheet_id)
        shoulder_data = self.extract_shoulder_data(sheet_id)
        

        print("Generating radar charts...")
        
        # Generate radar charts
        charts = self.generate_radar_charts(sheet_id, charts_dir)
        # charts = self.generate_radar_charts(sheet_id)
        
        print("Getting assessment texts...")
        
        # Get assessment texts
        assessments = self.get_assessment_texts(sheet_id)
        
        print("Rendering HTML report...")
        
        # Prepare template data
        template_data = {
            'ankle_data': ankle_data,
            'knee_data': knee_data,
            'hip_data': hip_data,
            'shoulder_data': shoulder_data,
            'thoracic_data': thoracic_data,
            'posture_assessment': assessments.get('posture'),
            'core_assessment': assessments.get('core'),
            'ankle_assessment': assessments.get('ankle'),
            'knee_assessment': assessments.get('knee'),
            'hip_assessment': assessments.get('hip'),
            'shoulder_assessment': assessments.get('shoulder'),
            'overall_conclusion': assessments.get('overall_conclusion'),
            'ankle_chart': charts.get('ankle'),
            'knee_chart': charts.get('knee'),
            'hip_chart': charts.get('hip'),
            'shoulder_chart': charts.get('shoulder')
        }
        
        # Render the template
        html_content = self.template.render(**template_data)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Report generated successfully: {output_path}")
        return output_path

# Example usage function
def generate_biomechanical_report(sheet_id: str, 
                                output_file: str = "biomechanical_report.html",
                                template_dir: str = "./",
                                charts_dir: str = "./charts/"):
    """
    Convenience function to generate a complete biomechanical assessment report
    
    Args:
        sheet_id: Google Sheets ID
        output_file: Output HTML file path
        template_dir: Directory containing the HTML template
        charts_dir: Directory to save radar charts
    
    Returns:
        Path to the generated HTML report
    """
    generator = BiomechanicalReportGenerator(template_dir, sheet_id)
    return generator.generate_report(sheet_id, output_file, charts_dir)

# Main execution example
if __name__ == "__main__":
    # Example usage
    sheet_id = "1Z6kHJWq9fvvcKukcNVlC2yJksCCnXS9JoMM8RQsFjwY"  # Replace with your sheet ID
    # Generate the report
    report_path = generate_biomechanical_report(
        sheet_id=sheet_id,
        output_file="biomechanical_assessment_report.html",
        template_dir="./",  # Directory containing biomechanical_report_template.html
        charts_dir="./charts/"
    )
    print(f"Biomechanical assessment report generated: {report_path}")
    print("Open the HTML file in a web browser to view the report.")