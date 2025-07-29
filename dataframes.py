import os
import pandas as pd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

scmci_path_df = pd.read_excel(os.path.join(BASE_DIR, 'Data', "Depression_Clinic_SCMCI_study_measures_2024.xlsx"))
DataDictionary_path_df = pd.read_csv(os.path.join(BASE_DIR, 'Data',"ImmiRiskIPT2022_DataDictionary_2025-06-18.csv"))


redcap_column_names_path_df = pd.read_excel(os.path.join(BASE_DIR, 'Data', "redcap_column_names.xlsx"))
qualtrics_column_names_path_df = pd.read_excel(os.path.join(BASE_DIR, 'Data',"qualtrics_column_names.xlsx"))
imputation_map_path_df = pd.read_csv(os.path.join(BASE_DIR, 'Data',"imputation_map.csv"))


exceptional_items_path_df = pd.read_excel(os.path.join(BASE_DIR, 'Data',"questions_excluded_from_scores_calculation.xlsx"))
participant_types_file_path_df = pd.read_csv(os.path.join(BASE_DIR, 'Data',"participant_types.csv"))
questionnaires_database_names_map = pd.read_excel(os.path.join(BASE_DIR, 'Data', "questionnaires_database_names_map.xlsx"))

invalid_columns_path_df = pd.read_excel(os.path.join(BASE_DIR, 'Data', "invalid_columns.xlsx"))