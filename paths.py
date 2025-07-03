import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, 'Data', 'myfile.csv')

scmci_path = os.path.join(BASE_DIR, 'Data', "Depression_Clinic_SCMCI_study_measures_2024.xlsx")
DataDictionary_path = os.path.join(BASE_DIR, 'Data',"ImmiRiskIPT2022_DataDictionary_2025-06-18.csv")


redcap_column_names_path = os.path.join(BASE_DIR, 'Data', "redcap_column_names.xlsx")
qualtrics_column_names_path = os.path.join(BASE_DIR, 'Data',"qualtrics_column_names.xlsx")
imputation_map_path = os.path.join(BASE_DIR, 'Data',"imputation_map.csv")


exceptional_items_path = os.path.join(BASE_DIR, 'Data',"questions_excluded_from_scores_calculation.xlsx")
participant_types_file_path = os.path.join(BASE_DIR, 'Data',"participant_types.csv")