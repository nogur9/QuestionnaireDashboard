import pandas as pd

from source.single_question.questions_loader import QuestionLoader
from source.utils.info_objects import ScoringInfo, QuestionInfo
from typing import List
from source.consts.enums import QuestionType
from source.consts.data_files_paths import participant_types_file_path
from source.consts.scores.clusters import Clusters
from source.consts.scores.questionnaire_columns import Scores_Columns, DEFAULT
from source.consts.scores.reverse_items import Reverse_Items
import sys
import os


sys.path.insert(0, os.getcwd())


class ScoreUtilsLoader:

    type_rename_dict = {
        'm': 'f',
        'mother': 'father'
    }

    def __init__(self):
        self.question_list = QuestionLoader().load_questions()
        self.scores_columns = Scores_Columns.copy()
        self.clusters = Clusters.copy()
        self.reverse_items = Reverse_Items.copy()
        self.load()


    def load(self):
        scores_columns = self.scores_columns.copy()
        scores_columns = self.duplicate_mother_and_father(scores_columns, score_d_type = 'columns_list')
        scores_columns = self._rewrite_default_columns(scores_columns)
        self.scores_columns = scores_columns

        reverse_items = self.reverse_items.copy()
        reverse_items = self.duplicate_mother_and_father(reverse_items, score_d_type = 'columns_list')
        self.reverse_items = reverse_items

        clusters = self.clusters.copy()
        clusters = self.duplicate_mother_and_father(clusters, score_d_type = 'clusters_dict')
        self.clusters = clusters


    def add_min_max_scores(self, questionnaire: str):
        min_score, max_score = None, None
        try:
            scoring_columns = [self.question_list.get_by_variable_name(q) \
                         for q in self.scores_columns[questionnaire]]

            min_score, max_score = self.get_score_range(scoring_columns)
        except Exception as e:
            pass
            #print(f"No score range for {questionnaire}")

        return {"min_score":  min_score, "max_score": max_score}



    def duplicate_mother_and_father(self, scoring_data, score_d_type: str):

        updated_scoring_data = scoring_data.copy()
        participant_types_df = pd.read_csv(participant_types_file_path).copy()
        participant_types_df = participant_types_df.query(f"participant_type == 'Mother'")

        for q_score in scoring_data:
            if type(q_score) == ScoringInfo:
                q_name, q_scoring_info = q_score.questionnaire_name, q_score
            else:
                q_name, q_scoring_info = q_score, scoring_data[q_score]

            if q_name in participant_types_df.questionnaire.to_list():

                if score_d_type == 'columns_list':  # list of columns
                    new_q_name, new_scoring_info = self._rename_questions(q_name, q_scoring_info)
                    updated_scoring_data[new_q_name] = new_scoring_info

                elif score_d_type == 'clusters_dict':  # clusters dict
                    new_scoring_info = {}
                    new_q_name = self._replace_suffix(q_name)
                    for cluster, columns in q_scoring_info.items():
                        new_cluster_title, new_cluster_items = self._rename_questions(cluster, columns)
                        new_scoring_info[new_cluster_title] = new_cluster_items
                    updated_scoring_data[new_q_name] = new_scoring_info

                elif score_d_type == 'scores_info':
                    new_q_name = self._replace_suffix(q_name)
                    new_scoring_info = ScoringInfo(
                        questionnaire_name = new_q_name,
                        columns = self.scores_columns[new_q_name],
                        aggregation_function = q_scoring_info.aggregation_function,
                        reversed_columns = self.reverse_items.get(new_q_name, []),
                        clusters = self.clusters.get(new_q_name, {}),
                        need_clarification = q_scoring_info.need_clarification,
                        min_score = q_scoring_info.min_score,
                        max_score = q_scoring_info.max_score,
                    )
                    updated_scoring_data.append(new_scoring_info)
                else:
                    raise ValueError

        return updated_scoring_data


    def _rename_questions(self, questionnaire, items):
        new_title = self._replace_suffix(questionnaire)
        if items == DEFAULT:
            new_items = DEFAULT
        else:
            new_items = []
            for q in items:
                new_items.append(self._replace_suffix(q))
        return new_title, new_items


    def _replace_suffix(self, q_name):
        q_name_parts = q_name.split('_')
        suffix = q_name_parts[-1]
        q_name_parts[-1] = self.type_rename_dict.get(suffix, suffix) # get the suffix parallel, or return that value
        new_q_name = "_".join(q_name_parts)
        return new_q_name


    def _rewrite_default_columns(self, scoring_columns):
        def is_score_col(q: QuestionInfo):
            if q.is_timestamp:
                return False
            elif q.is_exceptional_item:
                return False
            elif q.question_type in [QuestionType.Textual, QuestionType.NoType]: # need to check, QuestionType.Categorical]:
                return False
            else:
                return True
        scoring_columns = scoring_columns.copy()
        questions_info = QuestionLoader().load_questions()

        for questionnaire, items in scoring_columns.items():
            if items == DEFAULT:
                questions = questions_info.get_by_questionnaire(questionnaire)
                scoring_questions = [q for q in questions if is_score_col(q)]
                scoring_columns[questionnaire] = [q.variable_name for q in scoring_questions]

        return scoring_columns


    @ staticmethod
    def get_score_range(questions: List[QuestionInfo]):
        min_score, max_score = None, None
        for q in questions:
            assert q.question_type == QuestionType.Ordinal
            if min_score and max_score:
                assert min_score == min(q.validator.possible_values)
                assert max_score == max(q.validator.possible_values)
            else:
                min_score = min(q.validator.possible_values)
                max_score = max(q.validator.possible_values)

        return min_score, max_score