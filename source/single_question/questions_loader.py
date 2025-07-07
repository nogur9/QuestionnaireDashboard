from dataframes import DataDictionary_path_df, exceptional_items_path_df
from source.consts.enums import DataDictQuestionType
from source.single_question.qualtrics_questions import QualtricsAgeQuestion
from source.utils.info_objects import QuestionsList, QuestionInfo
from source.utils.multiple_choice_loader import MultipleChoiceLoader
from source.utils.timestamp_creator import TimestampCreator
from dataframes import questionnaires_alternative_names_path_df


class QuestionLoader:
    # column names:
    choices_col = "Choices, Calculations, OR Slider Labels"
    validation_col = "Text Validation Type OR Show Slider Number"
    name_col = 'Variable / Field Name'
    text_col = 'Field Label'
    questionnaire_col = 'Form Name'
    type_col = 'Field Type'
    branching_col = "Branching Logic (Show field only if...)"

    def __init__(self):
        self.questions_collection = []
        self.df = DataDictionary_path_df.copy()
        self.exceptional_items = exceptional_items_path_df.copy()

        self.alternative_names = \
            {i['questionnaire']: i['alternative_name'] for _, i in questionnaires_alternative_names_path_df.iterrows()}


    def load_questions(self):
        for _, row in self.df.iterrows():
            question_data, is_checkbox = self._setup(row)
            if is_checkbox:
                self.questions_collection.extend(self._expend_checkbox_questions(row, question_data))
            else:
                self.questions_collection.append(QuestionInfo(**question_data))

        self._add_missing_questions()
        questions_list = QuestionsList(self.questions_collection)

        return questions_list


    def _setup(self, row):
        question_data = self._extract_basic_info(row)
        question_type, is_checkbox = self._get_question_type(row)
        extra_data = self._add_type_based_information(row, question_type, is_checkbox)
        question_data = question_data | extra_data
        return question_data, is_checkbox


    def _extract_basic_info(self, row):
        question_data = {
            "variable_name": row[self.name_col],
            "question_text": row[self.text_col],
            "questionnaire_name": self.alternative_names.get(row[self.questionnaire_col], row[self.questionnaire_col]), # get the suffix parallel, or return that value
            "questionnaire_alternative_name": row[self.questionnaire_col],
            "branching_logic": row[self.branching_col],
            "is_timestamp": TimestampCreator.is_datetime_column(row[self.name_col]),
            'is_exceptional_item': row[self.name_col] in self.exceptional_items.question_name.tolist()
        }
        return question_data


    def _get_question_type(self, row):
        data_dict_question_type = DataDictQuestionType.from_label(row[self.type_col])
        question_type = data_dict_question_type.get_question_type(row)
        is_checkbox = data_dict_question_type.label == 'checkbox'
        return question_type, is_checkbox


    def _add_missing_questions(self):
        self.questions_collection.append(QualtricsAgeQuestion())


    def _expend_checkbox_questions(self, row, question_data):
        one_hot_encodings = []
        choices_dict = MultipleChoiceLoader(row).choices_dict

        for k, v in choices_dict.items():
            choice_question_data = question_data.copy()
            choice_question_data['variable_name'] = f"{question_data['ancestor']}_{k}"
            choice_question_data['question_text'] = f"{question_data['question_text']}_{v}"
            one_hot_encodings.append(QuestionInfo(**choice_question_data))

        return one_hot_encodings

    def _add_type_based_information(self, row, question_type, is_checkbox):
        if question_type.has_choices_info:
            choices = MultipleChoiceLoader(row).choices_dict
        else:
            choices = None
        if is_checkbox:
            ancestor = row[self.name_col]
        else:
            ancestor = None

        return {
            'question_type': question_type,
            'choices': choices,
            'ancestor': ancestor
        }

if __name__ == "__main__":
    ql = QuestionLoader()
    results = ql.load_questions()
    print(1)
