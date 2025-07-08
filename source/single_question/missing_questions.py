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



class RedcapEventNameQuestion(QuestionInfo):

    def __init__(self):

        params = {
        'variable_name': 'redcap_event_name',
        'question_text': 'redcap_event_name',
        'question_type': QuestionType.Categorical,
        'questionnaire_name': 'intro',
        }
        super().__init__(**params)




class TimestampQuestion(QuestionInfo):

    def __init__(self, variable_name, questionnaire):

        params = {
        'variable_name': variable_name,
        'question_text': 'timestamp',
        'question_type': QuestionType.Date,
        'questionnaire_name': questionnaire,
        'is_timestamp': True
        }
        super().__init__(**params)
