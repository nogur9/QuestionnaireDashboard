from enum import Enum
from typing import List
from source.utils.custom_scorers import SumScorer, AverageScorer, SingleItemScorer
from source.utils.question_type_utils import *
from source.utils.questionnaire_scorer import QuestionnaireScorer
from source.utils.textual_question_type import TextQuestionType


class ScoringMethod(Enum):
    SUM = 'Sum', SumScorer
    AVERAGE = 'Average', AverageScorer
    SINGLE_ITEM = 'Single Item', SingleItemScorer
    No_Scoring = 'No Scoring Needed', None
    Missing_Implementation_Scoring = 'Missing Implementation', None

    def __init__(self, label: str, scorer_class: QuestionnaireScorer):
        self.label = label
        self.scorer_class = scorer_class

    def __repr__(self):
        return self.label


class UniqueScoringMethod(Enum):
    SWAN_SCORING = None, 'swan_scoring'
    SPC_CLIN_SCORING = None, 'spc_clinician_scoring'
    Chameleon_Scoring =  None, 'chameleon'
    Cpss_c_Scoring = None, 'cpss_c'
    Cps_Clin_Scoring = None, 'cps_clin'

    def __init__(self, scorer_class: QuestionnaireScorer, questionnaire: str):
        self.scorer_class = scorer_class
        self.questionnaire = questionnaire

    def __repr__(self):
        return "Unique Scoring for:" + self.questionnaire

    @classmethod
    def from_questionnaire(cls, questionnaire):
        for item in cls:
            if item.questionnaire == questionnaire:
                return item



class C_SSRS_Scoring(Enum):
    cssrs_t_clin = None, 'cssrs_t_clin'
    cssrs_t_stu = None, 'cssrs_t_stu'
    cssrs_intake = None, 'cssrs_intake'
    cssrs = None, 'cssrs'
    cssrs_fw_maya = None, 'cssrs_fw_maya'
    cssrs_c_intake = None, 'cssrs_c_intake'
    cssrs_c_measurs = None, 'cssrs_c_measurs'
    cssrs_clin_ssc= None, 'cssrs_clin_ssc'

    def __init__(self, scorer_class: QuestionnaireScorer, questionnaire: str):
        self.scorer_class = scorer_class
        self.questionnaire = questionnaire


    def __repr__(self):
        return "C_SSRS Scoring for:" + self.questionnaire


    @classmethod
    def from_questionnaire(cls, questionnaire):
        for item in cls:
            if item.questionnaire == questionnaire:
                return item




class QuestionType(Enum):
    Binary = ('Binary', BinaryValidator, False)
    CategoricalBinary = ('Categorical Binary', CategoricalValidator, True)
    Numeric = ('Numeric', NumericValidator, False)
    Ordinal = ('Ordinal', CategoricalValidator, True)
    Categorical = ('Categorical', CategoricalValidator, True)
    Textual = ('Textual', NullValidator, False)
    Date = ('Date', DateValidator, False)
    NoType = ('None', NullValidator, False)
    Slider = ('Slider', SliderValidator, True)

    def __init__(self, label: str, validator:Validator, has_choices_info: bool):
        self.label = label
        self.validator = validator
        self.has_choices_info = has_choices_info

    def __repr__(self):
        return self.label


    @classmethod
    def from_label(cls, label):
        for item in cls:
            if item.label == label:
                return item



class DataDictQuestionType(Enum):
    Checkbox = 'checkbox', lambda x: QuestionType.Binary
    radio = 'radio', lambda x:  MultipleChoiceLoader(x).get_radio_type_classification(),
    calc = 'calc', lambda x :QuestionType.NoType,
    text = 'text', lambda x: TextQuestionType(x).get_type_classification(),
    dropdown = 'dropdown',  lambda x :QuestionType.Categorical
    notes = 'notes',  lambda x :QuestionType.Textual
    yesno = 'yesno',  lambda x :QuestionType.Binary
    slider = 'slider', lambda x :QuestionType.Slider

    def __init__(self, label: str, get_question_type):
        self.label = label
        self.get_question_type = get_question_type


    @classmethod
    def from_label(cls, label):
        for item in cls:
            if item.label == label:
                return item


class DataSource(Enum):
    Qualtrics = "Qualtrics", "qualtrics_name"
    RedCap = "RedCap", "redcap_name"
    QualtricsImputation = "Imputation_for_Qualtrics", "imputation_table_name"


    def __init__(self, label: str, column_name_map: str):
        self.label = label
        self.column_name_map = column_name_map
