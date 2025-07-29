import pandas as pd

from dataframes import participant_types_file_path_df, scmci_path_df
from source.questionnaire.question_columns_mapper import SimpleQuestionMap
from source.scores.scores_loader import ScoresLoader
from source.single_question.questions_loader import QuestionLoader
from source.utils.info_objects import QuestionnairesList, QuestionnaireInfo
import sys
import os

sys.path.insert(0, os.getcwd())


class QuestionnaireLoader:

    scmci_participant_type_map = {
        'Research Assistant, based on medical records': "Student",
         'Child/Adolescent': "Child",
         'Adolescent': "Child",
         'Parents\n(Mother & Father)': "Parents",
         'Parents\n(Mother & Father separtly)\nM-Mother\nF-Father': "Parents",
         'Clinician':"Clinician",
         'Clinician (Therapist)': "Clinician",
         'Research Clinical Staff': "Student",
         'Research Clinical Staf': "Student",
         'Research Clinical Staff,  Based on medical records': "Student"
     }


    def __init__(self):
        self.questionnaires_list = None
        self.participant_types_map = self._get_participants_type_map()
        self.questions_list = QuestionLoader().load_questions()
        self.scores_list = ScoresLoader().load()
        self.questions_map_df = SimpleQuestionMap().load()


    def load_questionnaires(self):
        questionnaire_collection = self._get_questionnaires_collection()
        questionnaires_list = QuestionnairesList(questionnaire_collection)
        self.questionnaires_list = questionnaires_list
        return questionnaires_list

    def _get_participants_type_map(self):
        participant_types_df = participant_types_file_path_df.copy()
        participant_types_map = {row.questionnaire: row.participant_type for _, row in participant_types_df.iterrows()}
        return participant_types_map

    def _create_questionnaire_info_entry(self, questionnaire_name):
        questions = self.questions_list.get_by_questionnaire(questionnaire_name)
        items = self.questions_list.get_by_questionnaire(questionnaire_name, get_q_names=True)
        exceptional_items = [item.variable_name for item in questions if item.is_exceptional_item]
        timestamp_items = [item.variable_name for item in questions if item.is_timestamp]
        research_data = self._get_data_from_scmci(items, exceptional_items, timestamp_items)

        basic_info = {
        'name': questionnaire_name,
        'items': items,
        'exceptional_items': exceptional_items,
        'timestamp_items': timestamp_items,
        'participant_type': self.participant_types_map.get(questionnaire_name),
        'scoring_info': self.scores_list.get_by_questionnaire(questionnaire_name),
        }

        if questions:
            basic_info['name_in_database'] = questions[0].questionnaire_database_name
        if research_data is not None:
            questionnaire_info = QuestionnaireInfo(
                **basic_info, **research_data
            )
        else:
            questionnaire_info = QuestionnaireInfo(**basic_info)
        return questionnaire_info


    def _get_questionnaires_collection(self):
        questionnaire_collection = []

        for questionnaire_name in list(self.questions_map_df.questionnaire.unique()):
            # self._assert_question_list_size(questionnaire_name, self.questions_map_df,
            # , exceptional_items, timestamp_items)
            questionnaires_info = self._create_questionnaire_info_entry(questionnaire_name)
            questionnaire_collection.append(questionnaires_info)

        return questionnaire_collection


    def _assert_question_list_size(self, questionnaire_name, questions_map_df,
                                   exceptional_items, timestamp_items):
        q_from_sql = questions_map_df.query(f"questionnaire == '{questionnaire_name}'").standard_question_name.to_list()
        q_from_questions_list = self.questions_list.get_by_questionnaire(questionnaire_name, get_q_names=True)
        q_from_sql = [q for q in q_from_sql if q not in exceptional_items + timestamp_items]
        q_from_questions_list = [q for q in q_from_questions_list if q not in exceptional_items + timestamp_items]

        diff = set(q_from_sql).difference(set(q_from_questions_list)) | \
                   set(q_from_questions_list).difference(set(q_from_sql))
        if len(diff) > 0:
            print(f"contradiction found between predefined questions and collected question {questionnaire_name}: {diff}")
#           assert  len(diff) == 0, f"contradiction found between predefined questions and collected question {questionnaire_name}: {diff}"

    def _get_data_from_scmci(self, questions, exceptional_items, timestamp_items):

        def get_questionnaire(x, questions_list):
            is_present = [(q in x) for q in questions_list]
            return all(is_present)
        essential_questions = [q for q in questions if q not in exceptional_items + timestamp_items]
        df = scmci_path_df.copy()
        df['q_list'] = df['Variable Name'].str.split("\n")
        mask = df['q_list'].apply(get_questionnaire, args=[essential_questions])

        if mask.any():
            questionnaire_row = df.loc[mask].iloc[0]

            return {
                'Abbreviated_Name': questionnaire_row['Abbreviated Name'],
                'Full_Name': questionnaire_row['Full Name'],
                'Description': questionnaire_row['Brief Description (full Method for paper description in "paragraph details")'],
                'Reference': questionnaire_row['Reference'],
                'Scoring_Instructions': questionnaire_row['Scoring Instructions\n(For syntax use Scales File 2021)'],
            }


if __name__ == "__main__":
    # ql = QuestionnaireLoader()
    # results = ql.load_questionnaires()
    ql = QuestionLoader().load_questions().questions
    ql = [i.variable_name for i in ql]
    qm = SimpleQuestionMap().load().standard_question_name.to_list()
    print(1)
