import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from jinja2 import Environment, FileSystemLoader
import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
import base64
from io import BytesIO
from textllm import (
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
    create_radar_chart_shoulder,
    TextGen_Posture,
    TextGen_FootAnkle,
    TextGen_Knee_Concise,
    TextGen_Shoulder_Concise
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
    thoracic_curvature: float
    lumbar_curvature: float
    forward_head_posture: float
    thoracic_percentage: str
    lumbar_percentage: str
    fhp_percentage: str

class BiomechanicalReportGenerator:
    def __init__(self, template_dir: str = "./"):
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
        sheet_id = "1L964TaAjOiI2HT1jPcdZbY8KeWeSPD22wvxVKfKUVdg"

    # Open the Google Sheet
        sheet = client.open_by_key(sheet_id)

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

        # Define gold standards
        self.gold_standards = {
            'ankle': {
                'dorsiflexion_range': 30,
                'plantarflexion_range': 165,
                'dorsiflexion_force': 0.30,
                'plantarflexion_force': 1.50
            },
            'knee': {
                'flexion_range': 160,
                'extension_range': 170,
                'flexion_force': 1.80,
                'extension_force': 3.00,
                'hq_ratio': 0.60
            },
            'hip': {
                'flexion_range': 90,
                'extension_range': 30,
                'abduction_range': 55,
                'adduction_range': 35,
                'ext_rotation_range': 45,
                'int_rotation_range': 40,
                'flexion_force': 1.50,
                'extension_force': 2.50,
                'abduction_force': 1.20,
                'adduction_force': 0.80,
                'ext_rotation_force': 0.60,
                'int_rotation_force': 0.50
            },
            'shoulder': {
                'ext_rotation_range': 90,
                'int_rotation_range': 70,
                'flexion_range': 180,
                'extension_range': 60,
                'ext_rotation_force': 0.35,
                'int_rotation_force': 0.45,
                'flexion_force': 0.55,
                'i_iso': 0.25,
                'y_iso': 0.30,
                't_iso': 0.28
            },
            'thoracic': {
                'thoracic_curvature_min': 30,
                'thoracic_curvature_max': 35,
                'lumbar_curvature_min': 30,
                'lumbar_curvature_max': 35,
                'forward_head_posture_max': 3
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

    def calculate_percentage(self, value, gold_standard, is_force=False):
        """Calculate percentage of gold standard"""
        try:
            val = self.safe_float_convert(value)
            if val == 0 or gold_standard == 0:
                return "0"
            
            if is_force:
                # For force measurements, calculate as percentage of gold standard
                percentage = (val / gold_standard) * 100
            else:
                # For range measurements, calculate as percentage of gold standard
                percentage = (val / gold_standard) * 100
            
            return f"{percentage:.1f}"
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
            if metrics and len(metrics) >= 8:
                # Raw data
                dorsi_range_left = str(metrics[0]) if metrics[0] is not None else "unavailable data"
                dorsi_range_right = str(metrics[1]) if metrics[1] is not None else "unavailable data"
                plant_range_left = str(metrics[2]) if metrics[2] is not None else "unavailable data"
                plant_range_right = str(metrics[3]) if metrics[3] is not None else "unavailable data"
                dorsi_force_left = str(metrics[4]) if metrics[4] is not None else "unavailable data"
                dorsi_force_right = str(metrics[5]) if metrics[5] is not None else "unavailable data"
                plant_force_left = str(metrics[6]) if metrics[6] is not None else "unavailable data"
                plant_force_right = str(metrics[7]) if metrics[7] is not None else "unavailable data"
                
                # Calculate percentages and asymmetry
                gs = self.gold_standards['ankle']
                
                return AnkleData(
                    # Range data (calculated from percentage)
                    dorsiflexion_range_left=self.calculate_range_from_percentage(metrics[0], gs['dorsiflexion_range']),
                    dorsiflexion_range_right=self.calculate_range_from_percentage(metrics[1], gs['dorsiflexion_range']),
                    plantarflexion_range_left=self.calculate_range_from_percentage(metrics[2], gs['plantarflexion_range']),
                    plantarflexion_range_right=self.calculate_range_from_percentage(metrics[3], gs['plantarflexion_range']),
                    
                    # Range percentages and asymmetry
                    dorsiflexion_left_percent=str(metrics[0]),
                    dorsiflexion_right_percent=str(metrics[1]),
                    dorsiflexion_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(metrics[0], gs['dorsiflexion_range']),
                        self.calculate_range_from_percentage(metrics[1], gs['dorsiflexion_range'])
                    ),
                    plantarflexion_left_percent=str(metrics[2]),
                    plantarflexion_right_percent=str(metrics[3]),
                    plantarflexion_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(metrics[2], gs['plantarflexion_range']),
                        self.calculate_range_from_percentage(metrics[3], gs['plantarflexion_range'])
                    ),
                    
                    # Force data (calculated from percentage)
                    dorsiflexion_force_left=self.calculate_range_from_percentage(metrics[4], gs['dorsiflexion_force']),
                    dorsiflexion_force_right=self.calculate_range_from_percentage(metrics[5], gs['dorsiflexion_force']),
                    plantarflexion_force_left=self.calculate_range_from_percentage(metrics[6], gs['plantarflexion_force']),
                    plantarflexion_force_right=self.calculate_range_from_percentage(metrics[7], gs['plantarflexion_force']),
                    
                    # Force percentages and asymmetry
                    dorsiflexion_force_left_percent=str(metrics[4]),
                    dorsiflexion_force_right_percent=str(metrics[5]),
                    dorsiflexion_force_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(metrics[4], gs['dorsiflexion_force']),
                        self.calculate_range_from_percentage(metrics[5], gs['dorsiflexion_force'])
                    ),
                    plantarflexion_force_left_percent=str(metrics[6]),
                    plantarflexion_force_right_percent=str(metrics[7]),
                    plantarflexion_force_asymmetry=self.calculate_asymmetry(
                        self.calculate_range_from_percentage(metrics[6], gs['plantarflexion_force']),
                        self.calculate_range_from_percentage(metrics[7], gs['plantarflexion_force'])
                    )
                )
        except Exception as e:
            print(f"Error extracting ankle data: {e}")
        return None

    def extract_knee_data(self, sheet_id: str) -> Optional[KneeData]:
        """Extract knee data from the sheet with calculations"""
        try:
            metrics = extract_sheet_metrics_knee(sheet_id, self.data_overview_sheet)
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
                
                return KneeData(
                    # Range data (calculated from percentage)
                    flexion_range_left=self.calculate_range_from_percentage(metrics[0], gs['flexion_range']),
                    flexion_range_right=self.calculate_range_from_percentage(metrics[1], gs['flexion_range']),
                    extension_range_left=self.calculate_range_from_percentage(metrics[2], gs['extension_range']),
                    extension_range_right=self.calculate_range_from_percentage(metrics[3], gs['extension_range']),
                    
                    # Range percentages and asymmetry
                    flexion_left_percent=str(metrics[0]),
                    flexion_right_percent=str(metrics[1]),
                    flexion_asymmetry=self.calculate_asymmetry(metrics[0], metrics[1]),
                    extension_left_percent=str(metrics[2]),
                    extension_right_percent=str(metrics[3]),
                    extension_asymmetry=self.calculate_asymmetry(metrics[2], metrics[3]),
                    
                    # Force data (calculated from percentage)
                    flexion_force_left=self.calculate_range_from_percentage(metrics[4], gs['flexion_force']),
                    flexion_force_right=self.calculate_range_from_percentage(metrics[5], gs['flexion_force']),
                    extension_force_left=self.calculate_range_from_percentage(metrics[6], gs['extension_force']),
                    extension_force_right=self.calculate_range_from_percentage(metrics[7], gs['extension_force']),
                    hamstring_quad_ratio_left=self.calculate_range_from_percentage(metrics[12], gs['hq_ratio']),
                    hamstring_quad_ratio_right=self.calculate_range_from_percentage(metrics[13], gs['hq_ratio']),
                    
                    # Force percentages and asymmetry
                    flexion_force_left_percent=str(metrics[4]),
                    flexion_force_right_percent=str(metrics[5]),
                    flexion_force_asymmetry=self.calculate_asymmetry(metrics[4], metrics[5]),
                    extension_force_left_percent=str(metrics[6]),
                    extension_force_right_percent=str(metrics[7]),
                    extension_force_asymmetry=self.calculate_asymmetry(metrics[6], metrics[7]),
                    hq_ratio_left_percent=str(metrics[12]),
                    hq_ratio_right_percent=str(metrics[13]),
                    hq_ratio_asymmetry=self.calculate_asymmetry(metrics[12], metrics[13])
                )
        except Exception as e:
            print(f"Error extracting knee data: {e}")
        return None

    def extract_hip_data(self, sheet_id: str) -> Optional[HipData]:
        """Extract hip data from the sheet with calculations"""
        try:
            metrics = extract_sheet_metrics_hip(sheet_id, self.data_overview_sheet)
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
                
                return HipData(
                    # Range data
                    flexion_range_left=raw_data['flexion_range_left'],
                    flexion_range_right=raw_data['flexion_range_right'],
                    extension_range_left=raw_data['extension_range_left'],
                    extension_range_right=raw_data['extension_range_right'],
                    abduction_range_left=raw_data['abduction_range_left'],
                    abduction_range_right=raw_data['abduction_range_right'],
                    adduction_range_left=raw_data['adduction_range_left'],
                    adduction_range_right=raw_data['adduction_range_right'],
                    ext_rotation_range_left=raw_data['ext_rotation_range_left'],
                    ext_rotation_range_right=raw_data['ext_rotation_range_right'],
                    int_rotation_range_left=raw_data['int_rotation_range_left'],
                    int_rotation_range_right=raw_data['int_rotation_range_right'],
                    
                    # Range percentages and asymmetry
                    flexion_left_percent=self.calculate_percentage(raw_data['flexion_range_left'], gs['flexion_range']),
                    flexion_right_percent=self.calculate_percentage(raw_data['flexion_range_right'], gs['flexion_range']),
                    flexion_asymmetry=self.calculate_asymmetry(raw_data['flexion_range_left'], raw_data['flexion_range_right']),
                    extension_left_percent=self.calculate_percentage(raw_data['extension_range_left'], gs['extension_range']),
                    extension_right_percent=self.calculate_percentage(raw_data['extension_range_right'], gs['extension_range']),
                    extension_asymmetry=self.calculate_asymmetry(raw_data['extension_range_left'], raw_data['extension_range_right']),
                    abduction_left_percent=self.calculate_percentage(raw_data['abduction_range_left'], gs['abduction_range']),
                    abduction_right_percent=self.calculate_percentage(raw_data['abduction_range_right'], gs['abduction_range']),
                    abduction_asymmetry=self.calculate_asymmetry(raw_data['abduction_range_left'], raw_data['abduction_range_right']),
                    adduction_left_percent=self.calculate_percentage(raw_data['adduction_range_left'], gs['adduction_range']),
                    adduction_right_percent=self.calculate_percentage(raw_data['adduction_range_right'], gs['adduction_range']),
                    adduction_asymmetry=self.calculate_asymmetry(raw_data['adduction_range_left'], raw_data['adduction_range_right']),
                    ext_rotation_left_percent=self.calculate_percentage(raw_data['ext_rotation_range_left'], gs['ext_rotation_range']),
                    ext_rotation_right_percent=self.calculate_percentage(raw_data['ext_rotation_range_right'], gs['ext_rotation_range']),
                    ext_rotation_asymmetry=self.calculate_asymmetry(raw_data['ext_rotation_range_left'], raw_data['ext_rotation_range_right']),
                    int_rotation_left_percent=self.calculate_percentage(raw_data['int_rotation_range_left'], gs['int_rotation_range']),
                    int_rotation_right_percent=self.calculate_percentage(raw_data['int_rotation_range_right'], gs['int_rotation_range']),
                    int_rotation_asymmetry=self.calculate_asymmetry(raw_data['int_rotation_range_left'], raw_data['int_rotation_range_right']),
                    
                    # Force data
                    flexion_force_left=raw_data['flexion_force_left'],
                    flexion_force_right=raw_data['flexion_force_right'],
                    extension_force_left=raw_data['extension_force_left'],
                    extension_force_right=raw_data['extension_force_right'],
                    abduction_force_left=raw_data['abduction_force_left'],
                    abduction_force_right=raw_data['abduction_force_right'],
                    adduction_force_left=raw_data['adduction_force_left'],
                    adduction_force_right=raw_data['adduction_force_right'],
                    ext_rotation_force_left=raw_data['ext_rotation_force_left'],
                    ext_rotation_force_right=raw_data['ext_rotation_force_right'],
                    int_rotation_force_left=raw_data['int_rotation_force_left'],
                    int_rotation_force_right=raw_data['int_rotation_force_right'],
                    
                    # Force percentages and asymmetry
                    flexion_force_left_percent=self.calculate_percentage(raw_data['flexion_force_left'], gs['flexion_force'], True),
                    flexion_force_right_percent=self.calculate_percentage(raw_data['flexion_force_right'], gs['flexion_force'], True),
                    flexion_force_asymmetry=self.calculate_asymmetry(raw_data['flexion_force_left'], raw_data['flexion_force_right']),
                    extension_force_left_percent=self.calculate_percentage(raw_data['extension_force_left'], gs['extension_force'], True),
                    extension_force_right_percent=self.calculate_percentage(raw_data['extension_force_right'], gs['extension_force'], True),
                    extension_force_asymmetry=self.calculate_asymmetry(raw_data['extension_force_left'], raw_data['extension_force_right']),
                    abduction_force_left_percent=self.calculate_percentage(raw_data['abduction_force_left'], gs['abduction_force'], True),
                    abduction_force_right_percent=self.calculate_percentage(raw_data['abduction_force_right'], gs['abduction_force'], True),
                    abduction_force_asymmetry=self.calculate_asymmetry(raw_data['abduction_force_left'], raw_data['abduction_force_right']),
                    adduction_force_left_percent=self.calculate_percentage(raw_data['adduction_force_left'], gs['adduction_force'], True),
                    adduction_force_right_percent=self.calculate_percentage(raw_data['adduction_force_right'], gs['adduction_force'], True),
                    adduction_force_asymmetry=self.calculate_asymmetry(raw_data['adduction_force_left'], raw_data['adduction_force_right']),
                    ext_rotation_force_left_percent=self.calculate_percentage(raw_data['ext_rotation_force_left'], gs['ext_rotation_force'], True),
                    ext_rotation_force_right_percent=self.calculate_percentage(raw_data['ext_rotation_force_right'], gs['ext_rotation_force'], True),
                    ext_rotation_force_asymmetry=self.calculate_asymmetry(raw_data['ext_rotation_force_left'], raw_data['ext_rotation_force_right']),
                    int_rotation_force_left_percent=self.calculate_percentage(raw_data['int_rotation_force_left'], gs['int_rotation_force'], True),
                    int_rotation_force_right_percent=self.calculate_percentage(raw_data['int_rotation_force_right'], gs['int_rotation_force'], True),
                    int_rotation_force_asymmetry=self.calculate_asymmetry(raw_data['int_rotation_force_left'], raw_data['int_rotation_force_right'])
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
                
                return ShoulderData(
                    # Range data
                    ext_rotation_range_left=raw_data['ext_rotation_range_left'],
                    ext_rotation_range_right=raw_data['ext_rotation_range_right'],
                    int_rotation_range_left=raw_data['int_rotation_range_left'],
                    int_rotation_range_right=raw_data['int_rotation_range_right'],
                    flexion_range_left=raw_data['flexion_range_left'],
                    flexion_range_right=raw_data['flexion_range_right'],
                    extension_range_left=raw_data['extension_range_left'],
                    extension_range_right=raw_data['extension_range_right'],
                    
                    # Range percentages and asymmetry
                    ext_rotation_left_percent=self.calculate_percentage(raw_data['ext_rotation_range_left'], gs['ext_rotation_range']),
                    ext_rotation_right_percent=self.calculate_percentage(raw_data['ext_rotation_range_right'], gs['ext_rotation_range']),
                    ext_rotation_asymmetry=self.calculate_asymmetry(raw_data['ext_rotation_range_left'], raw_data['ext_rotation_range_right']),
                    int_rotation_left_percent=self.calculate_percentage(raw_data['int_rotation_range_left'], gs['int_rotation_range']),
                    int_rotation_right_percent=self.calculate_percentage(raw_data['int_rotation_range_right'], gs['int_rotation_range']),
                    int_rotation_asymmetry=self.calculate_asymmetry(raw_data['int_rotation_range_left'], raw_data['int_rotation_range_right']),
                    flexion_left_percent=self.calculate_percentage(raw_data['flexion_range_left'], gs['flexion_range']),
                    flexion_right_percent=self.calculate_percentage(raw_data['flexion_range_right'], gs['flexion_range']),
                    flexion_asymmetry=self.calculate_asymmetry(raw_data['flexion_range_left'], raw_data['flexion_range_right']),
                    extension_left_percent=self.calculate_percentage(raw_data['extension_range_left'], gs['extension_range']),
                    extension_right_percent=self.calculate_percentage(raw_data['extension_range_right'], gs['extension_range']),
                    extension_asymmetry=self.calculate_asymmetry(raw_data['extension_range_left'], raw_data['extension_range_right']),
                    
                    # Force data
                    ext_rotation_force_left=raw_data['ext_rotation_force_left'],
                    ext_rotation_force_right=raw_data['ext_rotation_force_right'],
                    int_rotation_force_left=raw_data['int_rotation_force_left'],
                    int_rotation_force_right=raw_data['int_rotation_force_right'],
                    flexion_force_left=raw_data['flexion_force_left'],
                    flexion_force_right=raw_data['flexion_force_right'],
                    i_iso_left=raw_data['i_iso_left'],
                    i_iso_right=raw_data['i_iso_right'],
                    y_iso_left=raw_data['y_iso_left'],
                    y_iso_right=raw_data['y_iso_right'],
                    t_iso_left=raw_data['t_iso_left'],
                    t_iso_right=raw_data['t_iso_right'],
                    
                    # Force percentages and asymmetry
                    ext_rotation_force_left_percent=self.calculate_percentage(raw_data['ext_rotation_force_left'], gs['ext_rotation_force'], True),
                    ext_rotation_force_right_percent=self.calculate_percentage(raw_data['ext_rotation_force_right'], gs['ext_rotation_force'], True),
                    ext_rotation_force_asymmetry=self.calculate_asymmetry(raw_data['ext_rotation_force_left'], raw_data['ext_rotation_force_right']),
                    int_rotation_force_left_percent=self.calculate_percentage(raw_data['int_rotation_force_left'], gs['int_rotation_force'], True),
                    int_rotation_force_right_percent=self.calculate_percentage(raw_data['int_rotation_force_right'], gs['int_rotation_force'], True),
                    int_rotation_force_asymmetry=self.calculate_asymmetry(raw_data['int_rotation_force_left'], raw_data['int_rotation_force_right']),
                    flexion_force_left_percent=self.calculate_percentage(raw_data['flexion_force_left'], gs['flexion_force'], True),
                    flexion_force_right_percent=self.calculate_percentage(raw_data['flexion_force_right'], gs['flexion_force'], True),
                    flexion_force_asymmetry=self.calculate_asymmetry(raw_data['flexion_force_left'], raw_data['flexion_force_right']),
                    i_iso_left_percent=self.calculate_percentage(raw_data['i_iso_left'], gs['i_iso'], True),
                    i_iso_right_percent=self.calculate_percentage(raw_data['i_iso_right'], gs['i_iso'], True),
                    i_iso_asymmetry=self.calculate_asymmetry(raw_data['i_iso_left'], raw_data['i_iso_right']),
                    y_iso_left_percent=self.calculate_percentage(raw_data['y_iso_left'], gs['y_iso'], True),
                    y_iso_right_percent=self.calculate_percentage(raw_data['y_iso_right'], gs['y_iso'], True),
                    y_iso_asymmetry=self.calculate_asymmetry(raw_data['y_iso_left'], raw_data['y_iso_right']),
                    t_iso_left_percent=self.calculate_percentage(raw_data['t_iso_left'], gs['t_iso'], True),
                    t_iso_right_percent=self.calculate_percentage(raw_data['t_iso_right'], gs['t_iso'], True),
                    t_iso_asymmetry=self.calculate_asymmetry(raw_data['t_iso_left'], raw_data['t_iso_right'])
                )
        except Exception as e:
            print(f"Error extracting shoulder data: {e}")
        return None

    def extract_thoracic_data(self, sheet_id: str) -> Optional[ThoracicData]:
        worksheet = self.worksheet
        """Extract thoracic/posture data from the sheet with calculations"""
        try:
            metrics = extract_sheet_metrics_posture(sheet_id,self.worksheet,self.first_worksheet,self.third_worksheet)
            if metrics and len(metrics) >= 3:
                tc = float(metrics[2]) if metrics[1] is not None else 0.0
                lc = float(metrics[3]) if metrics[2] is not None else 0.0
                fhp = float(metrics[1]) if metrics[0] is not None else 0.0
                
                gs = self.gold_standards['thoracic']
                
                # Calculate percentages for thoracic data
                tc_percent = "100" if gs['thoracic_curvature_min'] <= tc <= gs['thoracic_curvature_max'] else f"{(tc / 32.5) * 100:.1f}"
                lc_percent = "100" if gs['lumbar_curvature_min'] <= lc <= gs['lumbar_curvature_max'] else f"{(lc / 32.5) * 100:.1f}"
                fhp_percent = "100" if fhp <= gs['forward_head_posture_max'] else f"{(gs['forward_head_posture_max'] / fhp) * 100:.1f}"
                
                return ThoracicData(
                    thoracic_curvature=tc,
                    lumbar_curvature=lc,
                    forward_head_posture=fhp,
                    thoracic_percentage=tc_percent,
                    lumbar_percentage=lc_percent,
                    fhp_percentage=fhp_percent
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
        """Get assessment texts from LLM functions"""
        assessments = {}
        
        try:
            # Get posture assessment
            posture_result = test_biomech_posture(sheet_id,self.worksheet,self.first_worksheet,self.third_worksheet)
            if posture_result and len(posture_result) >= 4:
                assessments['posture'] = posture_result.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting posture assessment: {e}")
            
        try:
            # Get ankle assessment
            ankle_result = test_biomech_foot(sheet_id,self.data_overview_sheet,self.second_worksheet)
            if ankle_result and len(ankle_result) >= 3:
                assessments['ankle'] = ankle_result.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting ankle assessment: {e}")
            
        try:
            # Get knee assessment
            knee_assessment = test_biomech_knee(sheet_id,self.data_overview_sheet)
            if knee_assessment:
                assessments['knee'] = knee_assessment.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting knee assessment: {e}")
            
        try:
            # Get hip assessment
            hip_assessment = test_biomech_hip_concise(sheet_id,self.data_overview_sheet)
            if hip_assessment:
                assessments['hip'] = hip_assessment.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting hip assessment: {e}")
            
        try:
            # Get shoulder assessment
            shoulder_assessment = test_biomech_shoulder(sheet_id,self.data_overview_sheet)
            if shoulder_assessment:
                assessments['shoulder'] = shoulder_assessment.replace('\n', '<br>')
        except Exception as e:
            print(f"Error getting shoulder assessment: {e}")
            
        return assessments

    def generate_report(self, sheet_id: str, output_path: str = "biomechanical_report.html", 
                       charts_dir: str = "./charts/") -> str:
        """Generate the complete biomechanical assessment report"""
        
        print("Extracting data from sheet...")
        
        # Extract all data
        ankle_data = self.extract_ankle_data(sheet_id)
        knee_data = self.extract_knee_data(sheet_id)
        hip_data = self.extract_hip_data(sheet_id)
        shoulder_data = self.extract_shoulder_data(sheet_id)
        thoracic_data = self.extract_thoracic_data(sheet_id)

        print("Generating radar charts...")
        
        # Generate radar charts
        charts = self.generate_radar_charts(sheet_id, charts_dir)
        
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
            'ankle_assessment': assessments.get('ankle'),
            'knee_assessment': assessments.get('knee'),
            'hip_assessment': assessments.get('hip'),
            'shoulder_assessment': assessments.get('shoulder'),
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
    generator = BiomechanicalReportGenerator(template_dir)
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