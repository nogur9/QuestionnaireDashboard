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

    BinaryOptions = [{0: 'לא', 1:'כן'},
                     {0: 'No', 1:'Yes'},
                     {0: 'לא מילא', 1:'מילא'},
                     {0: 'No - Control', 1:'Yes - Study Cohort'}
                    ]

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
            if set(self.choices_dict.keys()) == {0, 1}: #add yes \ no check
                for binary_option in self.BinaryOptions:
                    if (self.choices_dict[0] == binary_option[0]) and (self.choices_dict[1] == binary_option[1]):
                        return QuestionType.Binary
                else:
                    #print(f"non binary 0-1 {self.choices_dict}")
                    return QuestionType.CategoricalBinary
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



class LoadSlider:

    def __init__(self, row):
        self.row = row
        self.details = self._get_range()

    def _get_range(self):
        max_val = 10 if pd.isna(self.row["Text Validation Max"]) else self.row["Text Validation Max"]
        min_val = 0 if pd.isna(self.row["Text Validation Min"]) else self.row["Text Validation Min"]

        desc = self.row['Choices, Calculations, OR Slider Labels']

        return {
            "max_val" : int(max_val),
            "min_val" : int(min_val),
            "desc": desc
        }