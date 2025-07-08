import pandas as pd
from dataframes import (redcap_column_names_path_df, qualtrics_column_names_path_df, imputation_map_path_df,
                        invalid_columns_path_df)
from source.utils.transformation_rules import TRANSFORMATION_RULES




class QuestionsMappingCreator:

    def __init__(self):

        self.redcap_df = redcap_column_names_path_df.copy()
        self.qualtrics_df = qualtrics_column_names_path_df.copy()
        self.imputation_map = imputation_map_path_df.copy()

        self.invalid_columns = invalid_columns_path_df.column_name.to_list()

        self.redcap_df.drop_duplicates(inplace=True)
        self.qualtrics_df.drop_duplicates(inplace=True)

        self.redcap_questionnaires = {}
        self.qualtrics_questionnaires = {}

        self._prepare_questionnaire_columns()


    def run(self, save_map=False):

        column_names_mapping = []
        for questionnaire in TRANSFORMATION_RULES:

            transformation_rule = TRANSFORMATION_RULES[questionnaire]

            if transformation_rule in ['DEFAULT', 'EXTRA QUESTIONS IN REDCAP', 'REDCAP_ONLY']:
                for question in self.redcap_questionnaires[questionnaire]:
                    if question not in self.invalid_columns:
                        new_map = self._setup_for_mapping_question(questionnaire, question)
                        new_map = self._add_redcap_question(question, questionnaire, transformation_rule, new_map)
                        column_names_mapping.append(new_map)


            elif transformation_rule == 'EXTRA QUESTIONS IN QUALTRICS':
                for question in self.qualtrics_questionnaires[questionnaire]:
                    if question not in self.invalid_columns:
                        new_map = self._setup_for_mapping_question(questionnaire, question)
                        new_map = self._add_qualtrics_question(question, questionnaire, new_map)
                        column_names_mapping.append(new_map)
            else:
                raise ValueError
        if save_map:
            self._save(column_names_mapping)
        else:
            return pd.DataFrame(column_names_mapping)


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


    def _add_redcap_question(self, question, questionnaire, transformation_rule, new_map):
        new_map['redcap_name'] = question

        if transformation_rule == 'REDCAP_ONLY':

            new_map['qualtrics_name'] = None

        elif question in self.qualtrics_questionnaires[questionnaire]:
            new_map['qualtrics_name'] = question
        else:
            new_map['qualtrics_name'] = None
        return new_map


    def _setup_for_mapping_question(self, questionnaire, question):
        new_map = {'questionnaire': questionnaire, 'standard_question_name': question}
        new_map = self._add_imputation_column(question, new_map)
        return new_map


    def _add_qualtrics_question(self, question, questionnaire, new_map):
        new_map['qualtrics_name'] = question

        if question in self.redcap_questionnaires[questionnaire]:
            new_map['redcap_name'] = question
        else:
            new_map['redcap_name'] = None
        return new_map


    def _add_imputation_column(self, question, new_map):
        if question in list(self.imputation_map["new_name"]):
            new_map['imputation_table_name'] = self.imputation_map[self.imputation_map["new_name"] == question]["original"].values[0]
        else:
            new_map['imputation_table_name'] = None

        return new_map


    def _save(self, column_names_mapping):
        mapping_df = pd.DataFrame(column_names_mapping)
        mapping_df.to_csv("column_names_mapping.csv", index=False)




if __name__ == "__main__":
    QuestionsMappingCreator().run()