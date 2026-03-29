import os

base_path = os.path.join(os.path.join(os.path.dirname(__file__), ".."), "..")
BASE_DIR = os.path.dirname(os.path.join(base_path, ".."))
print(f"{BASE_DIR = }")
# metadata
METADATA_DIR = os.path.join(BASE_DIR, "Data/external/metadata")

scmci_path_df = os.path.join(METADATA_DIR, "Depression_Clinic_SCMCI_study_measures_2024.xlsx")
stepped_data_dict = os.path.join(METADATA_DIR, "data_dictionary", "SteppedCareIPC2025_DataDictionary_2025-11-24.csv")
DataDictionary_path_df = os.path.join(METADATA_DIR, "data_dictionary", "ImmiRiskIPT2022_DataDictionary_2025-06-18.csv")


# ETL rules
ETL_RULES_DIR = os.path.join(BASE_DIR, r"Data/external/ETL_rules")

exceptional_items_path_df = os.path.join(ETL_RULES_DIR, "questions_excluded_from_scores_calculation.xlsx")
default_merge_solution_path = os.path.join(ETL_RULES_DIR, "columns_to_apply_default_merge_solution.csv")


# additional data
EXPERIMENT_DATA_DIR = os.path.join(BASE_DIR, r"Data/external/experiment_based_data")
app_patient_ids_path = os.path.join(EXPERIMENT_DATA_DIR, "APP_patient_ids.csv") # ILA research



# raw data
redcap_raw_data = os.path.join(BASE_DIR, r"Data/raw/ImmiRiskIPT2022_DATA_2024-05-02_1230.csv")
qualtrics_raw_data = os.path.join(BASE_DIR, r"Data/raw/Schneider Depression Clinic Database.csv")
qualtrics_imputation_raw_data = os.path.join(BASE_DIR, r"Data/external/Student_Clinician_data_2021.csv")
stepped_raw_data = os.path.join(BASE_DIR, r"Data/raw/SteppedCareIPC2025_DATA_2025-12-01_1450.csv")
redcap_new_data = os.path.join(BASE_DIR, r"Data\raw\ImmiRiskIPT2022_DATA_2026-01-12_0902.csv")


# data_cleaning_instructions
DATA_CLEANING_INSTRUCTIONS_DIR = os.path.join(BASE_DIR, r"Data/external/data_cleaning_instructions")
invalid_columns_path_df = os.path.join(DATA_CLEANING_INSTRUCTIONS_DIR, "invalid_columns.xlsx")
numeric_variables_range_path_df = os.path.join(DATA_CLEANING_INSTRUCTIONS_DIR, "numeric_variables_valid_range.xlsx")
missing_age_path = os.path.join(DATA_CLEANING_INSTRUCTIONS_DIR, "missing_age.csv")
fixing_age_path = os.path.join(DATA_CLEANING_INSTRUCTIONS_DIR, "invalid_age.csv")
GROUP_IMPUTATION_FILE = os.path.join(BASE_DIR, r"Data/external/data_cleaning_instructions/group_imputations_2.xlsx")

# column names
COLUMNS_NAMES_DIR = os.path.join(BASE_DIR, r"Data/external/variables_assignments")

immi_column_names_path = os.path.join(COLUMNS_NAMES_DIR, "immi_risk_column_names.xlsx")
qualtrics_column_names_path = os.path.join(COLUMNS_NAMES_DIR, "qualtrics_column_names.xlsx")
participant_types_file_path = os.path.join(COLUMNS_NAMES_DIR, "participant_types.csv")


# mappings
imputation_map_path = os.path.join(BASE_DIR, os.path.join(COLUMNS_NAMES_DIR, "column_names_matching", "imputation_map.csv"))
stepped_care_map_path = os.path.join(BASE_DIR, os.path.join(COLUMNS_NAMES_DIR, "column_names_matching", "stepped_care_column_renames_map.csv"))
questionnaires_database_names_map_path = os.path.join(BASE_DIR, os.path.join(COLUMNS_NAMES_DIR, "column_names_matching", "questionnaires_database_names_map.xlsx"))



