from dataframes import questionnires_with_wrong_names_path_df
from source.utils.questions_mapping_creator import QuestionsMappingCreator


class SimpleQuestionMap(QuestionsMappingCreator):

    rename_map = {}


    def __init__(self, rename=True):

        super().__init__()
        self.questions_info = []
        self.rename = rename

        self.rename_map = \
            {i['questionnaire']: i['new_name'] for _, i in questionnires_with_wrong_names_path_df.iterrows()}

    def load(self):
        results = self.run()
        if self.rename:
            for current_name, correct_name in self.rename_map.items():
                results.loc[results['questionnaire'] == current_name, 'questionnaire'] = correct_name
        return results

    def _setup_for_mapping_question(self, questionnaire, question):
        new_map = {'questionnaire': questionnaire, 'standard_question_name': question}
        self._log_question_info(questionnaire, question)
        return new_map


    def _add_qualtrics_question(self, question, questionnaire, new_map):
        return new_map


    def _add_redcap_question(self, question, questionnaire, transformation_rule, new_map):
        return new_map


    def _log_question_info(self, questionnaire, question):
        question_row = {'question_name': question, 'questionnaire':questionnaire}
        self.questions_info.append(question_row)



if __name__ == "__main__":
    q_map = SimpleQuestionMap().run()
    print(1)