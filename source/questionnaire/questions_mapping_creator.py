import pandas as pd
from source.consts.data_files_paths import (
    redcap_column_names_path,
    qualtrics_column_names_path,
    imputation_map_path,
    invalid_columns_path_df,
    stepped_care_map_path,
    questionnaires_database_names_map_path
)
from source.consts.column_renaming_rules import (
    TRANSFORMATION_RULES,
    Stepped_Care_Extras,     # <- you added this; we’ll merge it below
)



class QuestionsMappingCreator:

    """
    SteppedCare comes from an external CSV map: stepped_care_map.csv
    CSV expected columns:
        questionnaire, standard_question_name, stepped_care_name

    """
    def __init__(self):

        self.redcap_df = pd.read_excel(redcap_column_names_path).copy()
        self.qualtrics_df = pd.read_excel(qualtrics_column_names_path).copy()

        self.imputation_map = pd.read_csv(imputation_map_path).copy()
        self.stepped_care_map = pd.read_csv(stepped_care_map_path).copy()
        self.invalid_columns = pd.read_excel(invalid_columns_path_df).column_name.to_list()

        self.redcap_df.drop_duplicates(inplace=True)
        self.qualtrics_df.drop_duplicates(inplace=True)
        self.stepped_care_map.drop_duplicates(inplace=True)

        self.redcap_questionnaires = {}
        self.qualtrics_questionnaires = {}

        self._prepare_questionnaire_columns()
        self.ALL_RULES = {**TRANSFORMATION_RULES, **Stepped_Care_Extras}

        renames = pd.read_excel(questionnaires_database_names_map_path)
        self.renames = {row['questionnaire']: row['database-name'] for _, row in renames.iterrows()}

        self.HANDLERS = {
            'DEFAULT': self._handle_default,
            'EXTRA QUESTIONS IN REDCAP':  self._handle_default,
            'EXTRA QUESTIONS IN QUALTRICS': self._handle_extra_in_qualtrics,
            'REDCAP_ONLY':  self._handle_default,
            # 'EXTRA QUESTIONS IN STEPPEDCARE': _handle_extra_in_stepped,
            'STEPPED_ONLY': self._handle_stepped_only,
        }


    def run(self, save_map=False):

        column_names_mapping = []
        for questionnaire, rule in self.ALL_RULES.items():
            handler = self.HANDLERS.get(rule)
            if handler is None:
                #print(questionnaire)
                raise ValueError(f"Unknown rule: {rule} for questionnaire {questionnaire}")

            rows = handler(questionnaire, rule)
            column_names_mapping.extend(rows)


        column_names_df = pd.DataFrame(column_names_mapping)
        column_names_df['project_source'] = column_names_df.apply(self.project_source, axis=1)
        column_names_df['database_questionnaire'] = column_names_df.questionnaire.apply(lambda x: self.renames.get(x, x))

        if save_map:
            column_names_df.to_csv("column_names_mapping.csv", index=False)

        else:
            return column_names_df


    @staticmethod
    def project_source(row):
        if pd.isna(row['stepped_care_name']):
            return 'immi'
        else:
            if pd.isna(row['redcap_name']):
                return 'step'
            else:
                return 'both'
        raise ValueError

    def _sc_rows(self, questionnaire: str) -> pd.DataFrame:
        return self.stepped_care_map[self.stepped_care_map['questionnaire'] == questionnaire].copy()


    def _handle_default(self, questionnaire, rule):
        """
        Iterate REDCap columns as the canonical driver, attach Qualtrics if present,
        and add SteppedCare from the external CSV if mapped.
        Also used for 'EXTRA QUESTIONS IN REDCAP' and 'REDCAP_ONLY'.
        """
        rows = []
        for question in self.redcap_questionnaires.get(questionnaire, []):
            if question in self.invalid_columns:
                continue
            new_map = self._setup_for_mapping_question(questionnaire, question)
            new_map = self._add_redcap_question(question, questionnaire, rule, new_map)
            new_map = self._add_stepped_care_column(questionnaire, question, new_map)
            rows.append(new_map)
        stepped_rows = self._handle_stepped_only(questionnaire, rule)
        return rows + stepped_rows


    def _handle_extra_in_qualtrics(self, questionnaire, rule):
        """
        Iterate Qualtrics columns as the driver when it is the superset for this questionnaire.
        Attach REDCap if present, plus SteppedCare from CSV if mapped.
        """
        rows = []
        for question in self.qualtrics_questionnaires.get(questionnaire, []):
            if question in self.invalid_columns:
                continue
            new_map = self._setup_for_mapping_question(questionnaire, question)
            new_map = self._add_qualtrics_question(question, questionnaire, new_map)
            new_map = self._add_stepped_care_column(questionnaire, question, new_map)
            rows.append(new_map)
        return rows


    def _handle_stepped_only(self, questionnaire: str, rule: str):
        """
        Questionnaire exists only in SteppedCare.
        We walk the CSV map rows for this questionnaire and produce mappings
        where REDCap/Qualtrics are None.
        """
        rows = []
        questionnaire = self.renames.get(questionnaire, questionnaire)
        q_df = self._sc_rows(questionnaire)
        q_df = q_df[q_df.standard_question_name.isna()]
        for _, r in q_df.iterrows():
            if r['stepped_care_name'] in self.invalid_columns:
                continue
            new_map = self._setup_for_mapping_question(questionnaire, r['stepped_care_name'])
            # SteppedCare name from map
            new_map['stepped_care_name'] = r.get('stepped_care_name')

            new_map['stepped_care_match_type'] = r.get('match_type')
            new_map['orig_step_name'] = r.get('orig_step_name')

            new_map['redcap_name'] = r.get('standard_question_name')
            new_map['qualtrics_name'] = None
            rows.append(new_map)
        return rows

    def _prepare_questionnaire_columns(self):
        for idx, row in self.redcap_df.iterrows():
            if type(row.column_names) == float:
                self.redcap_questionnaires[row['questionnaire_name']] = []
            else:
                self.redcap_questionnaires[row['questionnaire_name']] = row['column_names'].split(',')

        for idx, row in self.qualtrics_df.iterrows():
            if type(row.column_names) == float:
                self.qualtrics_questionnaires[row['questionnaire_name']] = []
            else:
                self.qualtrics_questionnaires[row['questionnaire_name']] = row['column_names'].split(',')


    def _setup_for_mapping_question(self, questionnaire, question):
        new_map = {
            'questionnaire': questionnaire,
            'standard_question_name': question
        }
        new_map = self._add_imputation_column(question, new_map)
        new_map['stepped_care_name'] = None
        return new_map


    def _add_redcap_question(self, question, questionnaire, transformation_rule, new_map):
        new_map['redcap_name'] = question
        if transformation_rule == 'REDCAP_ONLY':
            new_map['qualtrics_name'] = None
        elif question in self.qualtrics_questionnaires[questionnaire]:
            new_map['qualtrics_name'] = question
        else:
            new_map['qualtrics_name'] = None
        return new_map


    def _add_qualtrics_question(self, question, questionnaire, new_map):
        new_map['qualtrics_name'] = question

        if question in self.redcap_questionnaires[questionnaire]:
            new_map['redcap_name'] = question
        else:
            new_map['redcap_name'] = None
        return new_map


    def _add_imputation_column(self, standard_name, new_map):
        if standard_name in list(self.imputation_map["new_name"]):
            origin = self.imputation_map[self.imputation_map["new_name"] == standard_name]["original"]
            new_map['imputation_table_name'] = origin.values[0] if len(origin) else None
        else:
            new_map['imputation_table_name'] = None

        return new_map



    def _add_stepped_care_column(self, questionnaire: str, standard_name: str, new_map: dict):
        """
        A.1: fills stepped_care_name by looking up (questionnaire, standard_question_name)
        in the external CSV map.
        """
        questionnaire = self.renames.get(questionnaire, questionnaire)
        q_df = self._sc_rows(questionnaire)
        if q_df.empty:
            return new_map
        # exact match on standard name
        match = q_df[q_df['standard_question_name'] == standard_name]
        if not match.empty:
            new_map['stepped_care_name'] = match.iloc[0].get('stepped_care_name')
            new_map['stepped_care_match_type'] = match.iloc[0].get('match_type')
            new_map['orig_step_name'] = match.iloc[0].get('orig_step_name')

        return new_map



if __name__ == "__main__":
    a = QuestionsMappingCreator().run()
    print(a)




    #
    # def _handle_extra_in_stepped_care(self, questionnaire: str, rule: str):
    #     """
    #     Add rows for questions that exist in SteppedCare map but are missing from both
    #     REDCap and Qualtrics for this questionnaire.
    #     This complements the default/qualtrics handlers that already add the shared ones.
    #     """
    #     rows = []
    #     rc = set(self.redcap_questionnaires.get(questionnaire, []))
    #     qt = set(self.qualtrics_questionnaires.get(questionnaire, []))
    #
    #     q_df = self._sc_rows(questionnaire)
    #     for _, r in q_df.iterrows():
    #         std = r['standard_question_name']
    #         if pd.isna(std) or std in self.invalid_columns:
    #             continue
    #         if (std not in rc) and (std not in qt):
    #             new_map = self._setup_for_mapping_question(questionnaire, std)
    #             new_map['stepped_care_name'] = r.get('stepped_care_name')
    #             new_map['redcap_name'] = None
    #             new_map['qualtrics_name'] = None
    #             rows.append(new_map)
    #     return rows
    #

