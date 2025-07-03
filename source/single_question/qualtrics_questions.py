from source.consts.enums import QuestionType
from source.utils.info_objects import QuestionInfo


class QualtricsAgeQuestion(QuestionInfo):

    def __init__(self):

        params = {
        'variable_name': 'age_child_pre_first',
        'question_text': 'גיל',
        'question_type': QuestionType.Numeric,
        'questionnaire_name': 'opening_child_pre',
        }


        super().__init__(**params)

