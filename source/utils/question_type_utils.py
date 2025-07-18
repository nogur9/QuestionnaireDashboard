import pandas as pd
from dateutil.parser import parse

from source.utils.multiple_choice_loader import MultipleChoiceLoader


# validators

class Validator:

    questionnaire_col = 'Form Name'

    def __init__(self, row):
        self.row = row
        self._setup()

    def validate(self, value):
        NotImplementedError("Each question type must implement its own validation method.")

    def _setup(self):
        pass


class BinaryValidator(Validator):

    def __init__(self, row):
        super().__init__(row)


    def _setup(self):
        pass

    def validate(self, value):
        assert value in [0, 1]



class CategoricalValidator(Validator):

    def __init__(self, row):
        super().__init__(row)
        self.possible_values = None

    def _setup(self):
        choices_dict = MultipleChoiceLoader(self.row).choices_dict
        self.possible_values = list(choices_dict.keys())


    def validate(self, value):
        assert value in self.possible_values



class NumericValidator(Validator):
    path = ""

    def __init__(self, row):
        super().__init__(row)
        self.min_value = None
        self.max_value = None

    def _setup(self):
        value_range = pd.read_csv(self.path)
        value_range = value_range[value_range.questionnaire == self.row[self.questionnaire_col]]
        self.min_value = value_range.min_value.values()[0]
        self.max_value = value_range.max_value.values()[0]

    def validate(self, value):
        assert value >= self.min_value
        assert value <= self.min_value



class DateValidator(Validator):

    def __init__(self, row):
        super().__init__(row)

    def _setup(self):
        pass

    def validate(self, value):
        assert parse(value) is not None


class NullValidator(Validator):

    def __init__(self, row):
        super().__init__(row)

    def _setup(self):
        pass

    def validate(self, value):
        pass
