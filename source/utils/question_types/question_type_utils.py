import pandas as pd
import datetime
from source.utils.question_types.multiple_choice_loader import MultipleChoiceLoader, LoadSlider
from source.consts.data_files_paths import numeric_variables_range_path_df

# validators

class Validator:

    questionnaire_col = 'Form Name'
    name_col = 'Variable / Field Name'


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
        if pd.isna(value): return False

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
        if pd.isna(value): return False
        return value in self.possible_values


class NumericValidator(Validator):

    def __init__(self, row):
        super().__init__(row)
        self.min_value = None
        self.max_value = None
        self._setup()

    def _setup(self):

        value_range = pd.read_excel(numeric_variables_range_path_df)
        value_range = value_range[value_range.column == self.row[self.name_col]]
        if value_range.shape[0]:
            self.min_value = value_range.min_limit.values[0]
            self.max_value = value_range.max_limit.values[0]
        else:

            self.min_value = -1000
            self.max_value = 1000

    def is_valid(self, value):
        if pd.isna(value): return False
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
        if isinstance(value, datetime.datetime): return True
        return False
        #return parse(value) is not None


class SliderValidator(Validator):

    def __init__(self, row):
        super().__init__(row)
        self.details = None
        self._setup()

    def _setup(self):
        self.details = LoadSlider(self.row).details

    def is_valid(self, value):
        if pd.isna(value): return False
        is_valid = (value >= self.details["min_val"]) and \
                       (value <= self.details["max_val"])

        return is_valid


class NullValidator(Validator):

    def __init__(self, row):
        super().__init__(row)

    def _setup(self):
        pass

    def is_valid(self, value):
        return True
