import streamlit as st
from source.questionnaire.questionnaire_loader import QuestionnaireLoader
from source.single_question.missing_questions import QualtricsAgeQuestion, RedcapEventNameQuestion, TimestampQuestion
from source.single_question.questions_loader import QuestionLoader
import sys
import os
from source.utils.info_objects import QuestionnaireInfo, QuestionInfo, ScoringInfo
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, os.getcwd())

hidden_attributes = {
    QuestionnaireInfo: ['scoring_info',],
    QuestionInfo:['questionnaire_name', 'questionnaire_alternative_name', 'validator'],
    ScoringInfo:['questionnaire_name', 'need_clarification'],
    QualtricsAgeQuestion:['questionnaire_name', 'questionnaire_alternative_name'],
    RedcapEventNameQuestion:['questionnaire_name', 'questionnaire_alternative_name'],
    TimestampQuestion:['questionnaire_name', 'questionnaire_alternative_name'],

}

# --- Cache the heavy stuff ---
@st.cache_resource(show_spinner=False)
def get_questionnaires():
    return QuestionnaireLoader().load_questionnaires()

@st.cache_resource(show_spinner=False)
def get_questions():
    return QuestionLoader().load_questions()

@st.cache_resource(show_spinner=False)
def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource(show_spinner=False)
def get_question_model():
    """Multilingual model suitable for EN/HE question search (E5 style)."""
    return SentenceTransformer("intfloat/multilingual-e5-base")

@st.cache_data(show_spinner=False)
def compute_desc_embeddings(descriptions):
    model = get_model()
    return model.encode(descriptions, convert_to_tensor=True)

@st.cache_data(show_spinner=False)
def get_question_texts_and_embeddings():
    """Return filtered question objects and their embeddings using E5 'passage:' prefix."""
    questions_list = get_questions()
    all_questions = [q for q in questions_list.questions if q.question_text]
    # exclusions
    static_exclude = ['intro', 'ending', 'ending_parent_f', 'ending_parent_m', 'er_questionnaire_clin', 'covid19']
    suffix_exclude = {q.questionnaire_name for q in all_questions if (
        q.questionnaire_name.endswith("_f") or q.questionnaire_name.endswith("_father") or q.questionnaire_name.endswith("_stu")
    )}
    excluded_names = set(static_exclude) | suffix_exclude
    question_objs = [q for q in all_questions if q.questionnaire_name not in excluded_names]
    texts = [f"passage: {q.question_text}" for q in question_objs]
    model = get_question_model()
    embeddings = model.encode(texts, convert_to_tensor=True)
    return question_objs, embeddings


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
        print(f"{scoring_data = }\n {key = }\n{value = }")
        if key == 'aggregation_function':
            st.markdown(f"**{key}:** {repr(value)}")
        elif value is None:
            continue
        elif type(value) == int:
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
                          questionnaire_desc, top_k=4):
    model = get_model()
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = cosine_similarity([query_embedding], desc_embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    print(f"\n\n\n\n\n\n\n\n{query_embedding = }")
    print(f"{top_indices = }")
    print(f"{similarities.shape = }")
    print(f"{desc_embeddings.shape = }")
    return questionnaire_desc.iloc[top_indices]


def search_questions(query, question_embeddings, top_k=10):
    """Return indices of top matching questions based on their text using E5 'query:' prefix."""
    model = get_question_model()
    query_embedding = model.encode(f"query: {query}", convert_to_tensor=True)
    similarities = cosine_similarity([query_embedding], question_embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    return top_indices


st.set_page_config(page_title="Questionnaire Metadata Explorer", layout="wide")
st.title("🧠 Questionnaire Metadata Explorer")

# set RAG search-bar

# Sidebar: Select questionnaire

# --- Sidebar: Search and selection ---
st.sidebar.header("Search or Select Questionnaire")
questionnaires = get_questionnaires()
questionnaire_names = questionnaires.get_all_questionnaires()
questionnaire_desc = questionnaires.get_questionnaires_desc()
questionnaire_desc = questionnaire_desc[~questionnaire_desc['Description'].isna()]
questions = get_questions()

# Precompute and cache embeddings
desc_embeddings = compute_desc_embeddings(questionnaire_desc['Description'].tolist())
question_objs, question_embeddings = get_question_texts_and_embeddings()

# Controls
search_scope = st.sidebar.radio("Search in", ["Descriptions", "Questions"], index=0, horizontal=True)
query = st.sidebar.text_input("Search by topic or text (e.g., 'anxiety', 'פגיעה עצמית')")
top_k = st.sidebar.selectbox(label="Top K", options=range(1,21), index=5)

q_name = None
matched_questions = []
if query.strip():
    if search_scope == "Descriptions":
        results = search_questionnaires(query, desc_embeddings,
                                        questionnaire_desc, top_k=int(top_k))
        print(f"{len(questionnaire_desc) = }")
        top_names = results['name'].tolist()
        st.sidebar.markdown("**Top Matches:**")
        q_name = st.sidebar.selectbox("Questionnaire", top_names, index=0)
    else:
        # Questions search
        top_q_indices = search_questions(query, question_embeddings, top_k=int(top_k))
        matched_questions = [question_objs[i] for i in top_q_indices]
        # Show quick preview of matches
        with st.sidebar.expander("Top question matches", expanded=True):
            for idx, q in enumerate(matched_questions):
                preview_text = q.question_text or ""
                preview = preview_text if len(preview_text) <= 120 else preview_text[:117] + "..."
                st.markdown(f"**{idx+1}.** {preview}  ")
                st.caption(f"{q.questionnaire_name} · {q.variable_name}")
        # Let user choose among matched questionnaires (deduped, order-preserving)
        dedup_qnames = []
        for q in matched_questions:
            if q.questionnaire_name not in dedup_qnames:
                dedup_qnames.append(q.questionnaire_name)
        if len(dedup_qnames) == 0:
            q_name = st.sidebar.selectbox("Questionnaire", questionnaire_names, index=0)
        else:
            st.sidebar.markdown("**Matched Questionnaires:**")
            q_name = st.sidebar.selectbox("Questionnaire", dedup_qnames, index=0)
else:
    q_name = st.sidebar.selectbox("Questionnaire", questionnaire_names, index=0)


selected_q = questionnaires.get_by_name(q_name)

# Tabs for Metadata, Scoring, Questions (+ Results)
if selected_q is None:
    st.error(f"No data found for questionnaire: {q_name}")
else:
    tabs = st.tabs(["Metadata", "Scoring", "Questions", "Results"])
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

    with tabs[3]:
        st.subheader("🔎 Search Results")
        if search_scope == "Questions" and query.strip() and matched_questions:
            for q in matched_questions:
                st.markdown(f"**{q.questionnaire_name}** · `{q.variable_name}`")
                st.write(q.question_text)
                if q.choices:
                    st.caption(f"Choices: {q.choices}")
                st.markdown("---")
        else:
            st.info("Run a question search to see matched questions here.")
