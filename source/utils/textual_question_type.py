import pandas as pd
from bs4 import BeautifulSoup
import re, unicodedata


HEBREW_RANGE = r"\u0590-\u05FF"

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

        var_name = self.row[self.name_col]
        val_type = self.row[self.validation_col]

        if 'id' in var_name.split("_"):
            textual_question_type = QuestionType.Textual

        elif val_type in self.date_type_validation:
            textual_question_type = QuestionType.Date

        elif val_type in self.numeric_type_validation:
            textual_question_type = QuestionType.Numeric

        else:
            textual_question_type = QuestionType.Textual

        return textual_question_type




def normalize_for_match(s: str) -> str:
    """
    Full pass used before similarity:
    HTML -> Hebrew diacritics -> gender collapse -> generic normalize
    (Safe for non-Hebrew too; Hebrew steps no-op if none present.)
    """
    s = clean_html_and_fix_qmark(s)
    s = strip_hebrew_diacritics(s)
    s = collapse_hebrew_gender_variants(s)
    s = normalize_generic(s)
    return s



# ---------- 1) Source cleanup (Hebrew-aware) ----------

def clean_html_and_fix_qmark(s: str) -> str:
    """Remove HTML; if string starts with '?' move it to the end."""
    if pd.isna(s):
        return s
    text = BeautifulSoup(str(s), "html.parser").get_text().strip()
    if text.startswith("?") and len(text) > 1:
        text = text[1:].strip() + "?"
    return text


def strip_hebrew_diacritics(s: str) -> str:
    """Remove nikud/taamim from Hebrew."""
    if pd.isna(s):
        return s
    s = unicodedata.normalize('NFKC', str(s))
    return re.sub(r'[\u0591-\u05C7]', '', s)


def collapse_hebrew_gender_variants(s: str) -> str:
    """
    Collapse patterns like:
      פעיל/ה -> פעיל
      יכול/ה -> יכול
      חסר/ת -> חסר
      אינו/ה -> אינו
    Also normalize spaces around slashes and common spelling 'מידי'->'מדי'.
    """
    if pd.isna(s):
        return s
    s = str(s)
    # tidy slashes and whitespace
    s = re.sub(r'\s*/\s*', '/', s)
    s = re.sub(r'\s+', ' ', s).strip()

    # common spelling
    s = s.replace('מידי', 'מדי')

    # word/ה or word/ת  -> word
    s = re.sub(fr'(\b[{HEBREW_RANGE}]+)/(?:ה|ת)\b', r'\1', s)

    return s


# ---------- 2) Generic canonicalization for matching ----------

def normalize_generic(s: str) -> str:
    """
    Language-agnostic normalization:
    - NFKC, lower()
    - collapse whitespace/underscores, turn hyphens into spaces
    """
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", str(s)).strip().lower()
    s = re.sub(r"[\s_]+", " ", s)
    s = s.replace("-", " ")
    return s



# ---------- 3) Domain simplifiers (optional) ----------

COMMON_REGEX = [
    (re.compile(r"_m(ale)?$"), ""),
    (re.compile(r"_f(emale)?$"), ""),
    (re.compile(r"\bpre\b$"), "pre"),
    (re.compile(r"\bpost\b$"), "post"),
]


def regex_simplify(s: str) -> str:
    """Apply domain-specific suffix/pattern simplifications after normalize_for_match."""
    s = normalize_for_match(s)
    for pat, repl in COMMON_REGEX:
        s = pat.sub(repl, s)
    return s


# ---------- Similarity metrics ----------

def token_set_jaccard(a: str, b: str) -> float:
    ta, tb = set(normalize_for_match(a).split()), set(normalize_for_match(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def levenshtein_cheap(a: str, b: str) -> int:
    # Good enough for short labels; called on normalized text.
    a, b = normalize_for_match(a), normalize_for_match(b)
    if a == b:
        return 0
    # small optimization: difference lower bound
    if abs(len(a) - len(b)) > 3 and max(len(a), len(b)) > 6:
        pass  # keep it simple; skip early exits for clarity
    dp = range(len(b) + 1)
    for i, ca in enumerate(a, 1):
        ndp = [i]
        for j, cb in enumerate(b, 1):
            ndp.append(min(
                dp[j] + 1,  # deletion
                ndp[-1] + 1,  # insertion
                dp[j - 1] + (ca != cb)  # substitution
            ))
        dp = ndp
    return dp[-1]

