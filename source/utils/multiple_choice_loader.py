import pandas as pd
import re


class MultipleChoiceLoader:

    # column names:
    choices_col = "Choices, Calculations, OR Slider Labels"
    validation_col = "Text Validation Type OR Show Slider Number"
    name_col = 'Variable / Field Name'
    text_col = 'Field Label'
    questionnaire_col = 'Form Name'
    type_col = 'Field Type'
    branching_col = "Branching Logic (Show field only if...)"


    def __init__(self, row):
        self.row = row
        self.choices_dict = self._get_choices_dict()

    def _get_choices_dict(self):
        choices_dict = {}
        raw_choices = self.row[self.choices_col]

        # parse choices
        if not pd.isna(self.row[self.choices_col]):
            choices = re.split(r'\s*\|\s*', raw_choices)
            for choice in choices:
                parts = choice.split(',', 1)
                if len(parts) == 2:
                    key, val = parts
                    key = int(key.strip())
                    val = val.strip()
                    choices_dict[key] = val
        return choices_dict


    def get_radio_type_classification(self):
        from source.consts.enums import QuestionType

        assert self.row[self.type_col] == 'radio'

        if len(self.choices_dict.keys()) == 2:
            if set(self.choices_dict.keys()) == {0, 1}:
                return  QuestionType.CategoricalBinary
            elif set(self.choices_dict.keys()) == {1, 2}:
                return QuestionType.CategoricalBinary

        if self._is_ordinal(self.choices_dict):
            return QuestionType.Ordinal
        else:
            return QuestionType.Categorical



    def _is_ordinal(self, q_choices: dict):
        q_choices = q_choices.copy()
        def contains_number(txt):
            return any(char.isdigit() for char in txt)
        answers_contains_number = [contains_number(ans) for ans in q_choices.values()]
        return all(answers_contains_number)
