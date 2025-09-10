import pandas as pd
from dateutil.parser import parse
from source.utils.multiple_choice_loader import MultipleChoiceLoader, LoadSlider


# validators
class Validator:

    questionnaire_col = 'Form Name'

    def __init__(self, row):
        self.row = row
        self._setup()

    def is_valid(self, value):
        NotImplementedError("Each question type must implement its own validation method.")

    def _setup(self):
        pass


class BinaryValidator(Validator):

    def __init__(self, row):
        super().__init__(row)


    def _setup(self):
        pass

    def is_valid(self, value):
        return value in [0, 1]


class CategoricalValidator(Validator):

    def __init__(self, row):
        super().__init__(row)
        self.possible_values = None
        self._setup()

    def _setup(self):
        choices_dict = MultipleChoiceLoader(self.row).choices_dict
        self.possible_values = list(choices_dict.keys())

    def is_valid(self, value):
        return value in self.possible_values


class NumericValidator(Validator):
    path = ""

    def __init__(self, row):
        super().__init__(row)
        self.min_value = None
        self.max_value = None
        self._setup()

    def _setup(self):
        # value_range = pd.read_csv(self.path)
        # value_range = value_range[value_range.questionnaire == self.row[self.questionnaire_col]]
        # self.min_value = value_range.min_value.values()[0]
        # self.max_value = value_range.max_value.values()[0]
        self.min_value = 0
        self.max_value = 100

    def is_valid(self, value):
        is_valid = (value >= self.min_value) and \
                   (value <= self.max_value)
        return is_valid


class DateValidator(Validator):

    def __init__(self, row):
        super().__init__(row)
        self.possible_values = None
        self._setup()

    def _setup(self):
        choices_dict = MultipleChoiceLoader(self.row).choices_dict
        self.possible_values = list(choices_dict.keys())

    def is_valid(self, value):
        if pd.isna(value): return True # False
        if parse(value) is not None: return True
        #return parse(value) is not None


class SliderValidator(Validator):

    def __init__(self, row):
        super().__init__(row)
        self.details = None
        self._setup()

    def _setup(self):
        self.details = LoadSlider(self.row).details

    def is_valid(self, value):
        is_valid = False
        if str.isdigit(value):
            is_valid = (value >= self.details["min_value"]) and \
                       (value <= self.details["max_value"])

        return is_valid


class NullValidator(Validator):

    def __init__(self, row):
        super().__init__(row)

    def _setup(self):
        pass

    def is_valid(self, value):
        return True
