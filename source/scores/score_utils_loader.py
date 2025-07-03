import pandas as pd

from paths import participant_types_file_path_df
from source.consts.scores.clusters import Clusters
from source.consts.scores.questionnaire_columns import Scores_Columns, DEFAULT
from source.consts.scores.reverse_items import Reverse_Items
from source.single_question.questions_loader import QuestionLoader
import sys
import os

sys.path.insert(0, os.getcwd())


class ScoreUtilsLoader:

    type_rename_dict = {
        'm': 'f',
        'mother': 'father'
    }

    def __init__(self):
        self.scores_columns = Scores_Columns.copy()
        self.clusters = Clusters.copy()
        self.reverse_items = Reverse_Items.copy()
        self.load()


    def load(self):
        scores_columns = self.scores_columns.copy()
        scores_columns = self._duplicate_mother_and_father(scores_columns)
        scores_columns = self._rewrite_default_columns(scores_columns)
        self.scores_columns = scores_columns

        reverse_items = self.reverse_items.copy()
        reverse_items = self._duplicate_mother_and_father(reverse_items)
        self.reverse_items = reverse_items


        clusters = self.clusters.copy()
        clusters = self._duplicate_mother_and_father(clusters)
        self.clusters = clusters


    def _duplicate_mother_and_father(self, scoring_data):

        scoring_data = scoring_data.copy()
        participant_types_df = participant_types_file_path_df.copy()
        participant_types_df = participant_types_df.query(f"participant_type == 'Mother'")

        for questionnaire, items in scoring_data.items():
            if questionnaire in participant_types_df.questionnaire:
                if type(items) == list:  # list of columns
                    new_title, new_items = self._rename_questions(questionnaire, items)

                elif type(items) == dict:  # clusters dict
                    new_items = {}
                    new_title = self._replace_suffix(questionnaire)
                    for cluster, columns in items.items():
                        new_cluster_title, new_cluster_items = self._rename_questions(cluster, columns)
                        new_items[new_cluster_title] = new_cluster_items

                else: raise TypeError

                scoring_data[new_title] = new_items
        return scoring_data


    def _rename_questions(self, questionnaire, items):
        new_items = []
        new_title = self._replace_suffix(questionnaire)
        for q in items:
            new_items.append(self._replace_suffix(q))
        return  new_title, new_items

    def _replace_suffix(self, q_name):
        q_name_parts = q_name.split('_')
        suffix = q_name_parts[-1]
        q_name_parts[-1] = self.type_rename_dict.get(suffix, suffix) # get the suffix parallel, or return that value
        new_q_name = "_".join(q_name_parts)
        return new_q_name

    def _rewrite_default_columns(self, scoring_columns):
        scoring_columns = scoring_columns.copy()
        questions_info = QuestionLoader().load_questions()

        for questionnaire, items in scoring_columns.items():
            if items == DEFAULT:
                questions = questions_info.get_by_questionnaire(questionnaire)
                scoring_questions = [q for q in questions if (not q.is_timestamp) and (not q.is_exceptional_item)]

                scoring_columns[questionnaire] = [q.variable_name for q in scoring_questions]

        return scoring_columns
