
class TextQuestionType:

    # column names:
    choices_col = "Choices, Calculations, OR Slider Labels"
    validation_col = "Text Validation Type OR Show Slider Number"
    name_col = 'Variable / Field Name'
    text_col = 'Field Label'
    questionnaire_col = 'Form Name'
    type_col = 'Field Type'
    branching_col = "Branching Logic (Show field only if...)"

    date_type_validation = ['date_dmy', 'time', 'datetime_dmy']
    numeric_type_validation = ['number']

    def __init__(self, row):
        self.row = row
        assert self.row[self.type_col] == 'text'


    def get_type_classification(self):
        from source.consts.enums import QuestionType

        val_type = self.row[self.validation_col]
        if val_type in self.date_type_validation:
            textual_question_type = QuestionType.Date

        elif val_type in self.numeric_type_validation:
            textual_question_type = QuestionType.Numeric

        else:
            textual_question_type = QuestionType.Textual

        return textual_question_type

