from source.consts.enums import QuestionType
from source.data_etl.questionnaires_metadata.info_objects import QuestionInfo
from source.consts.standard_names import RedcapEventName


class QualtricsAgeQuestion(QuestionInfo):

    def __init__(self):

        params = {
        'variable_name': 'age_child_pre_first',
        'question_text': 'גיל',
        'question_type': QuestionType.Numeric,
        'questionnaire_name': 'opening_child_pre',
        "project_source": 'both'
        }


        super().__init__(**params)



class RedcapEventNameQuestion(QuestionInfo):

    def __init__(self):

        params = {
        'variable_name': RedcapEventName,
        'question_text': RedcapEventName,
        'question_type': QuestionType.Categorical,
        'questionnaire_name': 'intro',
        "is_timestamp": False,
        "project_source": 'both'
        }
        super().__init__(**params)




class TimestampQuestion(QuestionInfo):

    def __init__(self, variable_name, questionnaire):

        params = {
        'variable_name': variable_name,
        'question_text': 'timestamp',
        'question_type': QuestionType.Date,
        'questionnaire_name': questionnaire,
        'is_timestamp': True,
        }

        super().__init__(**params)
