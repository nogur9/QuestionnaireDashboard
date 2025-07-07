import streamlit as st
from source.questionnaire.questionnaire_loader import QuestionnaireLoader
from source.single_question.qualtrics_questions import QualtricsAgeQuestion
from source.single_question.questions_loader import QuestionLoader
import sys
import os
import numpy as np
from source.utils.info_objects import QuestionnaireInfo, QuestionInfo, ScoringInfo

sys.path.insert(0, os.getcwd())

hidden_attributes = {
    QuestionnaireInfo: ['scoring_info',],
    QuestionInfo:['questionnaire_name', 'questionnaire_alternative_name'],
    QualtricsAgeQuestion:['questionnaire_name', 'questionnaire_alternative_name'],
    ScoringInfo:['questionnaire_name', 'need_clarification']

}

def display_metadata(questionnaire_data: dict):
    # Display questionnaire metadata as key-value pairs.
    if not questionnaire_data:
        st.info("No questionnaire metadata available.")
        return
    for key, value in questionnaire_data.items():
        if value is None:
            continue
        elif type(value) == list:
            if len(value) == 0:
                continue

        st.markdown(f"**{key}:** {value}")

def display_scoring(scoring_data: dict):
    # Display scoring info in a structured way
    if not scoring_info:
        st.info("No scoring information available.")
        return

    for key, value in scoring_data.items():

        if key == 'aggregation_function':
            st.markdown(f"**{key}:** {repr(value)}")
        elif len(value) == 0:
            continue
        else:
            with st.expander(f"{key}"):
                if isinstance(value, dict):
                    for cluster, items in value.items():
                        st.markdown(f"**{cluster}:** {repr(items)}")
                else:
                    st.markdown(f"**{key}:** {repr(value)}")

def display_question(question_data: dict):
    # Display question details in an expander.
    key_info = question_data['variable_name']
    with st.expander(f"{question_data.get('name', 'Question')} - {key_info}"):
        for k, v in question_data.items():
            if k == 'variable_name':
                continue
            elif k in ['ancestor', 'choices', 'branching_logic']:
                if (v is None) or (type(v) == float): # float -> np.nan
                    continue
            if isinstance(v, dict):
                st.markdown(f"***{k}:***")
                for choice, items in v.items():
                    st.markdown(f"    **{choice}:** {repr(items)}")
            else:
                st.markdown(f"**{k}:** {repr(v)}")

def get_attributes(obj):
    # Extract metadata from questionnaire object, fallback to __dict__.
    if hasattr(obj, '__dict__'):
        ha = hidden_attributes[type(obj)]
        return {k: v for k, v in vars(obj).items() if not k.startswith('__') and k not in ha}
    return {}

def get_scoring(obj):
    """Extract scoring info from questionnaire object."""
    return getattr(obj, 'scoring_info', None)

st.set_page_config(page_title="Questionnaire Metadata Explorer", layout="wide")
st.title("🧠 Questionnaire Metadata Explorer")

# Sidebar: Select questionnaire
st.sidebar.header("Select Questionnaire")
questionnaires = QuestionnaireLoader().load_questionnaires()
question_names = questionnaires.get_all_questionnaires()
questions = QuestionLoader().load_questions()

q_name = st.sidebar.selectbox("Questionnaire", question_names, index=0)
selected_q = questionnaires.get_by_name(q_name)

# Tabs for Metadata, Scoring, Questions
if selected_q is None:
    st.error(f"No data found for questionnaire: {q_name}")
else:
    tabs = st.tabs(["Metadata", "Scoring", "Questions"])
    with tabs[0]:
        st.subheader("📋 Questionnaire Metadata")
        questionnaire_metadata = get_attributes(selected_q)
        display_metadata(questionnaire_metadata)

    with tabs[1]:
        st.subheader("🧮 Scoring Method")
        scoring_info = get_scoring(selected_q)
        scoring_metadata = get_attributes(scoring_info)
        display_scoring(scoring_metadata)

    with tabs[2]:
        st.subheader("❓ Questions")
        q_list = questions.get_by_questionnaire(q_name)
        if not q_list:
            st.info("No questions found for this questionnaire.")
        else:
            for question in q_list:
                question_metadata = get_attributes(question)
                display_question(question_metadata)
