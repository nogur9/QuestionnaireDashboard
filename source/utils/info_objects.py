from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from source.consts.enums import QuestionType, ScoringMethod
import pandas as pd

from source.utils.question_type_utils import Validator


@dataclass
class ScoringInfo:
    """Metadata for scoring logic of a questionnaire."""
    questionnaire_name: str
    aggregation_function: ScoringMethod
    columns: List
    reversed_columns: List[str]
    clusters: Optional[Dict[str, List[str]]]
    need_clarification: bool
    min_score: Optional[int] = None
    max_score: Optional[int] = None
    def __repr__(self):
        return f"{self.questionnaire_name} Score method"


@dataclass
class ScoresList:
    """Holds a list of all scoring metadata and provides query methods."""
    scores: List[ScoringInfo]

    def get_by_questionnaire(self, questionnaire_name: str) -> Optional[ScoringInfo]:
        return next((s for s in self.scores if s.questionnaire_name == questionnaire_name), None)



@dataclass
class QuestionInfo:
    """Metadata for a single question."""
    variable_name: str
    question_text: str
    question_type: QuestionType
    questionnaire_name: str
    questionnaire_database_name: str = "",
    is_timestamp: bool = False
    is_exceptional_item: bool = False
    ancestor: Optional[str] = None  # if type = checkbox
    choices: Optional[Dict[str, str]] = None  # value: meaning
    branching_logic: Optional[str] = None
    validator: Optional[Validator] = None

    def __repr__(self):
        return self.variable_name


@dataclass
class QuestionsList:
    """Holds a list of all questions' metadata and provides query methods."""
    questions: List[QuestionInfo]


    def __post_init__(self):
        variables = [q.variable_name for q in self.questions]
        unique_variables = set(variables)
        assert len(variables) == len(unique_variables)


    def get_by_variable_name(self, variable_name: str) -> Optional[QuestionInfo]:
        requested_qs = [q for q in self.questions if q.variable_name == variable_name]
        if len(requested_qs) == 0:
            print(f"question not found {variable_name}")
            return None

        elif len(requested_qs) > 1:
            raise Warning(f"found duplicated question {variable_name}")

        return requested_qs[0]

    def get_timestamp_questions(self, get_q_names=False):
        if get_q_names:
            return [q.variable_name for q in self.questions if q.is_timestamp]
        else:
            return [q for q in self.questions if q.is_timestamp]

    def get_by_questionnaire(self, questionnaire_name: str, get_q_names=False):
        if get_q_names:
            return [q.variable_name for q in self.questions if q.questionnaire_name == questionnaire_name]
        else:
            return [q for q in self.questions if q.questionnaire_name == questionnaire_name]

    def search_by_label(self, word: str) -> List[QuestionInfo]:
        return [q for q in self.questions if word.lower() in q.question_text.lower()]

    def append(self, question_info: QuestionInfo):
        self.questions.append(question_info)

    def get_question_names(self):
        return [i.variable_name for i in self.questions]




@dataclass
class QuestionnaireInfo:
    """Metadata for a single questionnaire."""
    name: str
    items: List[str]
    participant_type: Optional[str] = None
    exceptional_items: List[str] = field(default_factory=list)
    timestamp_items: List[str] = field(default_factory=list)
    scoring_info:ScoringInfo = None
    name_in_database: str = None,
    Abbreviated_Name:Optional[str] = None
    Full_Name:Optional[str] = None
    Description:Optional[str] = None
    Reference:Optional[str] = None
    Scoring_Instructions:Optional[str] = None

    def __repr__(self):
        return self.name

    def get_standard_questions(self) -> List[str]:
        questions = [q for q in self.items if (q not in self.exceptional_items) and \
                                              (q not in self.timestamp_items)]
        return questions

@dataclass
class QuestionnairesList:
    """Holds a list of all questionnaires' metadata and provides query methods."""
    questionnaires: List[QuestionnaireInfo]

    def get_by_name(self, name: str) -> Optional[QuestionnaireInfo]:
        requested_q = [q for q in self.questionnaires if q.name.lower() == name.lower()]
        if len(requested_q) == 0:
            raise Warning(f"questionnaire not found {name}")

        elif len(requested_q) > 1:
            raise Warning(f"found duplicated questionnaire {name}")

        return requested_q[0]

    def get_all_questionnaires(self) -> List[str]:
        all_questionnaires = [q.name for q in self.questionnaires]
        return all_questionnaires

    def get_questionnaires_desc(self):
        qs = [{'name': q.name, 'Description':q.Description} for \
         q in self.questionnaires if q.Description is not None]
        return pd.DataFrame(qs)
