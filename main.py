import streamlit as st
from source.questionnaire.questionnaire_loader import QuestionnaireLoader
from source.single_question.missing_questions import QualtricsAgeQuestion, RedcapEventNameQuestion, TimestampQuestion
from source.single_question.questions_loader import QuestionLoader
import sys
import os
from source.utils.info_objects import QuestionnaireInfo, QuestionInfo, ScoringInfo
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

sys.path.insert(0, os.getcwd())

hidden_attributes = {
    QuestionnaireInfo: ['scoring_info',],
    QuestionInfo:['questionnaire_name', 'questionnaire_alternative_name'],
    ScoringInfo:['questionnaire_name', 'need_clarification'],
    QualtricsAgeQuestion:['questionnaire_name', 'questionnaire_alternative_name'],
    RedcapEventNameQuestion:['questionnaire_name', 'questionnaire_alternative_name'],
    TimestampQuestion:['questionnaire_name', 'questionnaire_alternative_name'],

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

# Define semantic search function
def search_questionnaires(query, desc_embeddings,
                          questionnaire_desc, top_k=3):
    # query_embedding = st.session_state.model.encode(query, convert_to_tensor=True)
    # similarities = cosine_similarity([query_embedding], desc_embeddings)[0]
    # top_indices = similarities.argsort()[-top_k:][::-1]

    #def search_questionnaires(query, top_k=3):

    query_embedding = st.session_state.model.encode(query, convert_to_tensor=True)
    similarities = cosine_similarity([query_embedding], desc_embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    print(f"\n\n\n\n\n\n\n\n{query_embedding = }")
    print(f"{top_indices = }")
    print(f"{similarities.shape = }")
    print(f"{desc_embeddings.shape = }")
    return questionnaire_desc.iloc[top_indices]
    #return questionnaire_desc.iloc[top_indices]['name']


st.set_page_config(page_title="Questionnaire Metadata Explorer", layout="wide")
st.title("🧠 Questionnaire Metadata Explorer")

# set RAG search-bar

# Sidebar: Select questionnaire

# --- Sidebar: Search and selection ---
st.sidebar.header("Search or Select Questionnaire")
questionnaires = QuestionnaireLoader().load_questionnaires()
questionnaire_names = questionnaires.get_all_questionnaires()
questionnaire_desc = questionnaires.get_questionnaires_desc()
questionnaire_desc = questionnaire_desc[~questionnaire_desc['Description'].isna()]
questions = QuestionLoader().load_questions()

# Text input for semantic search
# Prepare sentence embeddings




# --- Load or compute sentence embeddings ---
EMBEDDING_CACHE = "desc_embeddings.pkl"

if os.path.exists(EMBEDDING_CACHE):
    with open(EMBEDDING_CACHE, "rb") as f:
        desc_embeddings = pickle.load(f)
else:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    desc_embeddings = model.encode(questionnaire_desc['Description'].tolist(), convert_to_tensor=True)
    with open(EMBEDDING_CACHE, "wb") as f:
        pickle.dump(desc_embeddings, f)


# Ensure we initialize the model only once
if 'model' not in st.session_state:
    st.session_state.model = SentenceTransformer("all-MiniLM-L6-v2")


query = st.sidebar.text_input("Search by topic (e.g., 'anxiety', 'emotion')")


if query.strip():
    results = search_questionnaires(query,
                            desc_embeddings, questionnaire_desc)
    print(f"{len(questionnaire_desc) = }")
    top_names = results['name'].tolist()
    st.sidebar.markdown("**Top Matches:**")
    # Questionnaire selection
    q_name = st.sidebar.selectbox("Questionnaire", top_names, index=0)
else:
    q_name = st.sidebar.selectbox("Questionnaire", questionnaire_names, index=0)



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
