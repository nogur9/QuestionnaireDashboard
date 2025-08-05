from enum import Enum

from source.utils.multiple_choice_loader import MultipleChoiceLoader
from source.utils.question_type_utils import BinaryValidator, CategoricalValidator, NumericValidator, NullValidator, \
    DateValidator, Validator
from source.utils.textual_question_type import TextQuestionType


class ScoringMethod(Enum):
    SUM = 'Sum'
    AVERAGE = 'Average'
    SWAN_SCORING = 'swan_scoring'
    SPC_CLIN_SCORING = 'spc_clinician_scoring'


    def __init__(self, label):
        self.label = label


    def __repr__(self):
        if self.label in ['swan_scoring', 'spc_clinician_scoring']:
            return 'Unique Scoring Method'

        return self.label


class QuestionType(Enum):
    Binary = ('Binary', BinaryValidator, False)
    CategoricalBinary = ('Categorical Binary', CategoricalValidator, True)
    Numeric = ('Numeric', NumericValidator, False)
    Ordinal = ('Ordinal', CategoricalValidator, True)
    Categorical = ('Categorical', CategoricalValidator, True)
    Textual = ('Textual', NullValidator, False)
    Date = ('Date', DateValidator, False)
    NoType = ('None', NullValidator, False)

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


    def __init__(self, label: str, get_question_type):
        self.label = label
        self.get_question_type = get_question_type


    @classmethod
    def from_label(cls, label):
        for item in cls:
            if item.label == label:
                return item
