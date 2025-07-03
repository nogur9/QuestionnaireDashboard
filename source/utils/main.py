import os
import sys
import streamlit as st


sys.path.insert(0, os.getcwd())
from source.data_etl.questionnaires_metadata.single_question.questions_loader import QuestionLoader
from source.data_etl.questionnaires_metadata.questionnaire.questionnaire_loader import QuestionnaireLoader


def explore_object(obj, name='object', level=0, max_depth=5):
    """Recursively explore object attributes with collapsible sections."""
    if level > max_depth:
        st.markdown(f"{' ' * (level * 4)}- `{name}`: 🔁 Max depth reached")
        return

    if hasattr(obj, '__dict__'):
        with st.expander(f"{' ' * level * 2}🔹 {repr(obj)}"):
            attributes = [attr for attr in dir(obj) if not attr.startswith('__')]
            if not attributes:
                st.write("No public attributes.")
            for attr in attributes:
                try:
                    value = getattr(obj, attr)

                    st.markdown(f"📄 `{attr}`: \n`{repr(value)}`")
                except Exception as e:
                    st.markdown(f"⚠️ `{attr}`: Error - {e}")
    else:
        st.markdown(f"{' ' * (level * 4)}- `{name}`: `{repr(obj)}`")


st.title("🔍 Questionnaires Explorer")

# Load questionnaires and questions
questionnaires = QuestionnaireLoader().load_questionnaires()
question_names = questionnaires.get_all_questionnaires()
questions = QuestionLoader().load_questions()

# Select questionnaire with search
q_name = st.selectbox("Select a questionnaire", question_names, index=0)

# Display selected questionnaire
st.header(f"Questionnaire - {q_name}")
explore_object(questionnaires.get_by_name(q_name))

st.header("Score")
explore_object(questionnaires.get_by_name(q_name).scoring_info)

st.header("Questions")
for q in questions.get_by_questionnaire(q_name):
    explore_object(q)
