import os

# Base directory = the folder where this file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Metadata directory inside project
METADATA_DIR = os.path.join(BASE_DIR, "Data")

# Paths to data files
scmci_path_df = os.path.join(METADATA_DIR, "Depression_Clinic_SCMCI_study_measures_2024.xlsx")
stepped_data_dict = os.path.join(METADATA_DIR, "SteppedCareIPC2025_DataDictionary_2025-06-18.csv")
DataDictionary_path_df = os.path.join(METADATA_DIR, "ImmiRiskIPT2022_DataDictionary_2025-06-18.csv")

redcap_column_names_path = os.path.join(METADATA_DIR, "redcap_column_names.xlsx")
qualtrics_column_names_path = os.path.join(METADATA_DIR, "qualtrics_column_names.xlsx")
imputation_map_path = os.path.join(METADATA_DIR, "imputation_map.csv")
stepped_care_map_path = os.path.join(METADATA_DIR, "stepped_care_column_renames_map.csv")

exceptional_items_path_df = os.path.join(METADATA_DIR, "questions_excluded_from_scores_calculation.xlsx")
participant_types_file_path = os.path.join(METADATA_DIR, "participant_types.csv")
questionnaires_database_names_map_path = os.path.join(METADATA_DIR, "questionnaires_database_names_map.xlsx")

invalid_columns_path_df = os.path.join(METADATA_DIR, "invalid_columns.xlsx")
