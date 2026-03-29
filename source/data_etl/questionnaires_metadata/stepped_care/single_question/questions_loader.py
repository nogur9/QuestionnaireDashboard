from source.consts.data_files_paths import exceptional_items_path_df, questionnaires_database_names_map_path, \
                                            stepped_data_dict, DataDictionary_path_df
from source.consts.enums import DataDictQuestionType
from source.data_etl.questionnaires_metadata.info_objects import *
from source.data_etl.questionnaires_metadata.stepped_care.single_question.missing_questions import *
from source.utils.question_types.multiple_choice_loader import MultipleChoiceLoader, LoadSlider
from source.utils.question_types.questions_mapping_creator import QuestionsMappingCreator
import pandas as pd
from source.utils.question_types.textual_question_type import normalize_for_match
from source.consts.data_files_paths import participant_types_file_path, scmci_path_df, \
    questionnaires_database_names_map_path

class QuestionLoader:
    # column names:
    choices_col = "Choices, Calculations, OR Slider Labels"
    validation_col = "Text Validation Type OR Show Slider Number"
    name_col = 'Variable / Field Name'
    text_col = 'Field Label'
    questionnaire_col = 'Form Name'
    type_col = 'Field Type'
    branching_col = "Branching Logic (Show field only if...)"

    invalid_types = ['descriptive', 'calc']
    included_calcs = ['srs_sum', 'srs_sum_f', 'ffq_sum']

    type_rename_dict = {
        'm': 'f',
        'mother': 'father'
    }

    def __init__(self, init_validator=True):
        self.init_validator = init_validator
        self.questions_collection = []
        print(f"{exceptional_items_path_df = }")
        self.exceptional_items = pd.read_excel(exceptional_items_path_df)
        self.qmc = QuestionsMappingCreator()
        self.questionnaire_map = self.qmc.run()
        self.df = self.concat_data_dict()

        questionnaires_database_names_map = pd.read_excel(questionnaires_database_names_map_path)

        self.alternative_names = \
            {i['database-name']: i['questionnaire']  for _, i in questionnaires_database_names_map.iterrows()}

        self.participant_types_map = self._get_participants_type_map()


    def _get_participants_type_map(self):
        participant_types_df = pd.read_csv(participant_types_file_path)
        participant_types_map = {row.questionnaire: {'participant_type': row.participant_type, 'parallel': row.parallel}
                                 for _, row in participant_types_df.iterrows()}

        renames = {questionnaire: database_name for questionnaire, database_name in self.alternative_names.items()}
        participant_types_map = {renames.get(q, q): pt for q, pt in participant_types_map.items()}
        return participant_types_map


    def concat_data_dict(self):
        step_data_dict = pd.read_csv(stepped_data_dict)
        immi_data_dict = pd.read_csv(DataDictionary_path_df)

        miss_in_immi = self.questionnaire_map[
            self.questionnaire_map.redcap_name.isna()].standard_question_name.to_list()
        step_exclusive = step_data_dict[step_data_dict[self.name_col].isin(miss_in_immi)]
        df = pd.concat([immi_data_dict, step_exclusive])

        df = df[~(df[self.type_col].isin(self.invalid_types) & ~df[self.name_col].isin(self.included_calcs))]
        #df = df[~(df[self.name_col].isin(self.included_calcs))]
        merged = df.merge(self.questionnaire_map[['stepped_care_name', 'orig_step_name', 'stepped_care_match_type',
                                                  "project_source", "standard_question_name", "database_questionnaire"]],
                          left_on=self.name_col, right_on='standard_question_name', how='left')
        return merged.drop(columns="standard_question_name")


    def load_questions(self):

        for _, row in self.df.iterrows():
            question_data, is_checkbox = self._setup(row)
            if is_checkbox:
                self.questions_collection.extend(self._expend_checkbox_questions(row, question_data))
            else:
                self.questions_collection.append(QuestionInfo(**question_data))

        questions_list = QuestionsList(self.questions_collection)
        self._add_missing_questions(questions_list)
        self._add_parallel_question_names(questions_list)

        return questions_list


    def _replace_suffix(self, q_name):
        q_name_parts = q_name.split('_')
        suffix = q_name_parts[-1]
        q_name_parts[-1] = self.type_rename_dict.get(suffix, suffix) # get the suffix parallel, or return that value
        new_q_name = "_".join(q_name_parts)
        return new_q_name


    def _add_parallel_question_names(self, questions_list):
        for question_info in questions_list.questions:
            questionnaire_name = question_info.questionnaire_name
            if self.participant_types_map.get(questionnaire_name) is None:
                continue

            new_q_name = self._replace_suffix(question_info.variable_name)
            if questions_list.get_by_variable_name(new_q_name) is not None:
                questions_list.update_parallel_question_name(question_info.variable_name, new_q_name)


    def _setup(self, row):
        question_data = self._extract_basic_info(row)
        question_type, is_checkbox = self._get_question_type(row)
        extra_data = self._add_type_based_information(row, question_type, is_checkbox)
        question_data = question_data | extra_data
        return question_data, is_checkbox


    def _extract_basic_info(self, row):
        from source.data_preprocessing.utils.timestamp_creator import TimestampCreator

        """
        questionnaire_database_name = name in redcap data-dictionary
        questionnaire_name = name in redcap columns list (how the researchers calls it)

        """
        questionnaire_name = self._split_questionnaires(row)

        question_data = {
            "variable_name": row[self.name_col],
            "question_text": normalize_for_match(row[self.text_col]),
            "questionnaire_alternative_name":  self.alternative_names.get(questionnaire_name, questionnaire_name), # get the database-name parallel, or return same value
            "is_timestamp": TimestampCreator.is_datetime_column(row[self.name_col]),
            'is_exceptional_item': row[self.name_col] in self.exceptional_items.question_name.tolist(),
            "branching_logic": row[self.branching_col],
            "questionnaire_name": questionnaire_name,
            "step_questionnaire_name": row["orig_step_name"],
            "project_source": row["project_source"]
        }
        return question_data


    def _split_questionnaires(self, row):

        splitting_map = {
            "immirisk_adolescents_mast_athens": {
                'default': "mast",
                'other': "ATHENS"
            },

            "piu_cyberbulling": {
            'default': "piu",
            'other': "cyberbulling"
            }
        }

        questionnaire_name = row[self.questionnaire_col]

        for current_q_name in splitting_map.keys():
            if questionnaire_name == current_q_name:
                default = splitting_map[current_q_name]['default']
                other = splitting_map[current_q_name]['other']

                if row[self.name_col].startswith(other.lower()):
                    return other
                else:
                    return default
        else:
            return questionnaire_name


    def _get_question_type(self, row):
        data_dict_question_type = DataDictQuestionType.from_label(row[self.type_col])
        question_type = data_dict_question_type.get_question_type(row)
        is_checkbox = data_dict_question_type.label == 'checkbox'
        return question_type, is_checkbox


    def _add_missing_questions(self, questions_list: QuestionsList):

        # add qualtrics question
        questions_list.append(QualtricsAgeQuestion())

        # add redcap_event_name
        questions_list.append(RedcapEventNameQuestion())

        missing_questions = [i for i in self.questionnaire_map.standard_question_name.to_list() \
                             if i not in questions_list.get_question_names()]
        for q in missing_questions:
            if q.endswith('_timestamp'):
                questionnaire = self.questionnaire_map.query(f"standard_question_name == '{q}'")['questionnaire'].iloc[0]
                timestamp_q = TimestampQuestion(variable_name=q, questionnaire=questionnaire)
                questions_list.append(timestamp_q)
            #
            # elif q != 'redcap_event_name':
            #     print(f"missing question {q}")


    def _expend_checkbox_questions(self, row, question_data):
        one_hot_encodings = []
        choices_dict = MultipleChoiceLoader(row).choices_dict

        for k, v in choices_dict.items():
            choice_question_data = question_data.copy()
            choice_question_data['variable_name'] = f"{question_data['ancestor']}___{k}"
            choice_question_data['question_text'] = f"{question_data['question_text']} - {v}"
            choice_question_data['project_source'] = question_data['project_source']
            one_hot_encodings.append(QuestionInfo(**choice_question_data))

        return one_hot_encodings

    def _add_type_based_information(self, row, question_type: QuestionType, is_checkbox: bool):
        if question_type.has_choices_info:
            if question_type == QuestionType.Slider:
                choices = LoadSlider(row).details["desc"]
            else:
                choices = MultipleChoiceLoader(row).choices_dict
        else:
            choices = None
        if is_checkbox:
            ancestor = row[self.name_col]
        else:
            ancestor = None
        info = {
            'question_type': question_type,
            'choices': choices,
            'ancestor': ancestor}

        if self.init_validator:
            info["validator"] = question_type.validator(row)
        return info

if __name__ == "__main__":
    ql = QuestionLoader()
    results = ql.load_questions()
    print(1)
