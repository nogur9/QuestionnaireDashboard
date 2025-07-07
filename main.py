import streamlit as st
from source.questionnaire.questionnaire_loader import QuestionnaireLoader
from source.single_question.questions_loader import QuestionLoader
import sys
import os

sys.path.insert(0, os.getcwd())

def display_metadata(metadata):
    """Display questionnaire metadata as key-value pairs."""
    if not metadata:
        st.info("No metadata available.")
        return
    for key, value in metadata.items():
        st.markdown(f"**{key}:** {value}")

def display_scoring(scoring_info):
    """Display scoring info in a structured way."""
    if not scoring_info:
        st.info("No scoring information available.")
        return
    if isinstance(scoring_info, dict):
        for key, value in scoring_info.items():
            with st.expander(f"{key}"):
                st.write("meow")
    else:
        st.write(scoring_info)

def display_question(question):
    """Display question details in an expander."""
    if hasattr(question, '__dict__'):
        attrs = {k: v for k, v in vars(question).items() if not k.startswith('__')}
    elif isinstance(question, dict):
        attrs = question
    else:
        st.write(question)
        return
    key_info = attrs.get('text', None) or attrs.get('name', None) or str(question)
    with st.expander(f"{attrs.get('name', 'Question')} - {key_info}"):
        for k, v in attrs.items():
            st.markdown(f"**{k}:** {v}")

def get_metadata(obj):
    """Extract metadata from questionnaire object, fallback to __dict__."""
    if hasattr(obj, 'metadata'):
        return getattr(obj, 'metadata')
    elif hasattr(obj, '__dict__'):
        return {k: v for k, v in vars(obj).items() if not k.startswith('__') and k != 'scoring_info'}
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
        st.subheader("📋 Metadata")
        metadata = get_metadata(selected_q)
        display_metadata(metadata)
    with tabs[1]:
        st.subheader("🧮 Scoring Method")
        scoring_info = get_scoring(selected_q)
        display_scoring(scoring_info)
    with tabs[2]:
        st.subheader("❓ Questions")
        q_list = questions.get_by_questionnaire(q_name)
        if not q_list:
            st.info("No questions found for this questionnaire.")
        else:
            for q in q_list:
                display_question(q)
