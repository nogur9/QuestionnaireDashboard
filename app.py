import sys
import os

from source.questionnaire.questionnaire_loader import QuestionnaireLoader
from source.single_question.questions_loader import QuestionLoader
from source.utils.info_objects import QuestionInfo, QuestionnaireInfo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.getcwd())
import inspect
import streamlit as st
from app_utils import (_nonempty, _as_url, _unique_compact_list, _enum_to_str,
                       _hash_color, _style_questions_df, _badge,
                       _render_question_cards, _scoring_method_label,
                       _clusters_reverse_index, _validate_scoring, _to_jsonable)
import pandas as pd
from typing import List
import textwrap


#sys.path.append(r'C:\Users\USER\PycharmProjects\schneider-depression-lab')
#os.chdir(r'C:\Users\USER\PycharmProjects\schneider-depression-lab')



def display_questions_info(displayed_question_list: List["QuestionInfo"], *,
                           group_mode: str = "Flat"):
    """
    Pretty 'Questions' tab:
    - color-coded by question type and data source
    - filters, search, grouping
    """
    if not _nonempty(displayed_question_list):
        st.info("No questions found for this questionnaire.")
        return

    # Build a compact DataFrame for fast rendering
    recs = []
    for q in displayed_question_list:
        q_type = _enum_to_str(q.question_type)
        source = q.project_source or ""
        text_short = textwrap.shorten(str(q.question_text or ""), width=120, placeholder="…")
        recs.append({
            "Var": q.variable_name,
            "Text": text_short,
            "Type": q_type,
            "Source": source,
            "Timestamp": "✓" if q.is_timestamp else "",
            "Exceptional": "✓" if q.is_exceptional_item else "",
            "Ancestor": q.ancestor or "",
            "Choices": len(q.choices) if isinstance(q.choices, dict) else 0,
            "Branching?": "✓" if _nonempty(q.branching_logic) else "",
            "Validator": getattr(q.validator, "name", getattr(q.validator, "pattern", "")) if q.validator else "",
        })

    df = pd.DataFrame.from_records(recs)

    # Palettes (colorblind-friendly leaning)
    palette = [
        "#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd",
        "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf",
        "#4c78a8","#f58518","#54a24b","#e45756","#72b7b2",
    ]

    # Stable color maps
    type_values = sorted([t for t in df["Type"].unique() if _nonempty(t)])
    source_values = df["Source"].dropna().unique().tolist()

    type_colors = {t: _hash_color(t, palette) for t in type_values}
    source_colors = {s: _hash_color(s, palette[::-1]) for s in source_values}

    # --- Controls row ---
    with st.container():
        c1, c2, c3, c4, c5 = st.columns([2.2,2.2,2,1.2,1.2])
        with c1:
            search = st.text_input("Search Var/Text", placeholder="search…")
        with c2:
            types_sel = st.multiselect("Type", options=type_values, default=[])
        with c3:
            sources_sel = st.multiselect("Source", options=source_values, default=source_values)
        with c4:
            only_ts = st.toggle("Timestamp only", value=False)
        with c5:
            only_exc = st.toggle("Exceptional only", value=False)

    # Apply filters
    mask = pd.Series(True, index=df.index)
    if _nonempty(search):
        s = search.lower()
        mask &= df["Var"].str.lower().str.contains(s) | df["Text"].str.lower().str.contains(s)
    if _nonempty(types_sel):
        mask &= df["Type"].isin(types_sel)
    if _nonempty(sources_sel):
        mask &= df["Source"].isin(sources_sel)
    if only_ts:
        mask &= (df["Timestamp"] == "✓")
    if only_exc:
        mask &= (df["Exceptional"] == "✓")

    dff = df.loc[mask].copy()

    # --- Legends (badges) ---
    with st.expander("Legend / color keys", expanded=False):
        st.markdown("**Type**")
        st.markdown(" ".join(_badge(t, type_colors[t]) for t in type_values), unsafe_allow_html=True)
        if source_values:
            st.markdown("**Source**")
            st.markdown(" ".join(_badge(s, source_colors[s]) for s in source_values), unsafe_allow_html=True)



    st.caption(f"{len(dff):,} questions match filters")
    styler = _style_questions_df(dff, type_colors, source_colors)
    st.dataframe(styler, use_container_width=True, hide_index=True, height=min(680, 42 + 28*min(len(dff), 22)))

    # After rendering Flat / Group by Type / Group by Source:
    st.markdown("")  # small spacer
    enable_cards = st.toggle("Card view with clickable choices", value=False, help="Shows a scrollable list where each row has a 'Choices' popover.")
    if enable_cards:
        _render_question_cards(dff, type_colors, source_colors, displayed_question_list)



def display_questionnaire_info(q: QuestionnaireInfo):
    """
    Pretty display for QuestionnaireInfo, with clean header and collapsible long lists.
    """
    # --- Header: best title + badges ---
    primary_name = next(
        (nm for nm in [q.Full_Name, q.name, q.questionnaire_alternative_name] if pd.notna(nm)),
        "Unnamed questionnaire"
    )

    alt_names = _unique_compact_list([
        q.Abbreviated_Name,
        q.questionnaire_alternative_name if q.questionnaire_alternative_name != primary_name else None,
        q.name if q.name != primary_name else None,
    ])

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(f"### {primary_name}")
        if _nonempty(alt_names):
            st.caption("Aliases:")
            st.write(" • " + " | ".join(f"`{n}`" for n in alt_names))

    with col2:
        tag_bits = []
        if _nonempty(q.participant_type):
            tag_bits.append(f"`Participant: {q.participant_type}`")
        if _nonempty(q.project_source):
            tag_bits.append(f"`Source: {q.project_source}`")
        if tag_bits:
            st.caption("Context")
            st.write("\n".join(tag_bits))

    # --- Description / Reference / Scoring instructions ---
    if _nonempty(q.Description):
        with st.expander("📝 Description", expanded=False):
            st.write(q.Description)

    if _nonempty(q.Scoring_Instructions):
        with st.expander("📐 Scoring Instructions", expanded=False):
            st.write(q.Scoring_Instructions)

    if _nonempty(q.Reference):
        with st.expander("🔗 Reference", expanded=False):
            if _as_url(q.Reference):
                # If it's a URL (or looks like one)
                try:
                    st.link_button("Open reference", q.Reference)
                except Exception:
                    st.write(q.Reference)
            else:
                st.write(q.Reference)

    # --- Items (potentially very long) ---
    if _nonempty(q.items):
        with st.expander(f"🧩 Items ({len(q.items)})", expanded=False):
            items = q.items
            df_items = pd.DataFrame({"Item": items})
            st.dataframe(df_items, use_container_width=True, hide_index=True)

    # --- Exceptional & timestamp items side-by-side ---
    colA, colB = st.columns(2)
    with colA:
        if _nonempty(q.exceptional_items):
            with st.expander(f"⚠️ Exceptional items ({len(q.exceptional_items)})", expanded=False):
                st.write(", ".join(map(str, q.exceptional_items)))
    with colB:
        if _nonempty(q.timestamp_items):
            with st.expander(f"⏱️ Timestamp items ({len(q.timestamp_items)})", expanded=False):
                st.write(", ".join(map(str, q.timestamp_items)))

    # --- Items outside project (if present) ---
    if _nonempty(q.items_outside_project):
        with st.expander(f"📦 Items outside project ({len(q.items_outside_project)})", expanded=False):
            # Try to show variable_name if available
            rows = []
            for it in q.items_outside_project:
                label = getattr(it, "variable_name", None)
                label = label or getattr(it, "name", None)
                rows.append(label or str(it))
            st.write(", ".join(map(str, rows)))

    # --- Optional: raw view for debugging ---
    with st.popover("Raw metadata (debug)"):
        raw = {
            "name": q.name,
            "Full_Name": q.Full_Name,
            "Abbreviated_Name": q.Abbreviated_Name,
            "Alternative": q.questionnaire_alternative_name,
            "participant_type": q.participant_type,
            "project_source": q.project_source,
            "Description": (q.Description[:200] + "…") if (pd.notna(q.Description) and len(q.Description) > 200) else q.Description,
            "Reference": q.Reference,
            "Scoring_Instructions": (q.Scoring_Instructions[:200] + "…") if (pd.notna(q.Scoring_Instructions) and len(q.Scoring_Instructions) > 200) else q.Scoring_Instructions,
            "n_items": len(q.items) if _nonempty(q.items) else 0,
            "n_timestamp_items": len(q.timestamp_items) if _nonempty(q.timestamp_items) else 0,
            "n_items_outside_project": len(q.items_outside_project) if _nonempty(q.items_outside_project) else 0,
        }
        st.json(raw)




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
    if scoring_data is None:
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
        return {k: v for k, v in vars(obj).items() if not k.startswith('__')}
    return {}

def get_scoring(obj):
    """Extract scoring info from questionnaire object."""
    return getattr(obj, 'scoring_info', None)

def render_scoring_info(info) -> None:
    """
    Rich, compact Scoring display with a single outer expander (no nested expanders).
    Internally uses tabs + selectors to avoid Streamlit's "nested expander" restriction.
    """
    if info is None:
        st.info("No scoring info available.")
        return

    method_label, scorer_cls = _scoring_method_label(info.aggregation_function)
    clusters = info.clusters or {}
    columns = list(info.columns or [])
    reversed_cols = set(info.reversed_columns or [])
    cluster_rev = _clusters_reverse_index(clusters)
    has_range = info.min_score is not None or info.max_score is not None

    with st.expander("🧮 Scoring", expanded=True):
        # --- Top summary "badges" ---
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            st.markdown(f"**Method:** `{method_label}`")
        with c2:
            st.markdown(f"**Items:** `{len(columns)}`")
        with c3:
            st.markdown(f"**Clusters:** `{len(clusters)}`")
        with c4:
            st.markdown(f"**Range:** `{info.min_score} – {info.max_score}`" if has_range else "**Range:** `—`")

        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown(f"**Need clarification:** {'✅ Yes' if info.need_clarification else '❌ No'}")
        with f2:
            st.markdown(f"**Step-adjust required:** {'✅ Yes' if getattr(info, 'require_step_adj', False) else '❌ No'}")
        with f3:
            st.markdown(f"**Scorer class:** `{getattr(scorer_cls, '__name__', str(scorer_cls))}`" if scorer_cls else "**Scorer class:** `—`")

        st.divider()

        # ---------- Tabs (no nested expanders) ----------
        tab_cols, tab_clusters, tab_checks, tab_advanced = st.tabs(
            ["Columns", "Clusters", "Validations", "Advanced"]
        )

        # --- Columns tab ---
        with tab_cols:
            q = st.text_input("Filter columns", "", placeholder="Type to filter by name or cluster…")
            rows = [
                {"column": col, "reversed": col in reversed_cols, "cluster": cluster_rev.get(col, "")}
                for col in columns
            ]
            cols_df = pd.DataFrame(rows)
            if q:
                q_lower = q.strip().lower()
                cols_df = cols_df.loc[
                    cols_df["column"].str.lower().str.contains(q_lower)
                    | cols_df["cluster"].str.lower().str.contains(q_lower)
                ]
            st.dataframe(cols_df, hide_index=True, use_container_width=True)

        # --- Clusters tab ---
        with tab_clusters:
            if not clusters:
                st.caption("No clusters configured.")
            else:
                # Selector instead of nested expanders
                clist = sorted(clusters.keys())
                sel = st.selectbox("Choose a cluster", clist, index=0)
                selected_cols = clusters.get(sel, []) or []
                cluster_df = pd.DataFrame(
                    {"column": selected_cols, "reversed": [c in reversed_cols for c in selected_cols]}
                )
                # Small metrics row
                m1, m2 = st.columns(2)
                with m1:
                    st.metric("Items in cluster", len(selected_cols))
                with m2:
                    st.metric("Reversed in cluster", int(sum(cluster_df["reversed"])))
                st.dataframe(cluster_df, hide_index=True, use_container_width=True)

        # --- Validations tab ---
        with tab_checks:
            warnings = _validate_scoring(info)
            if warnings:
                for w in warnings:
                    st.warning(w)
            else:
                st.success("No issues detected.")

        # --- Advanced tab (no expander here) ---
        with tab_advanced:
            st.markdown("**Aggregation function (raw):**")
            st.code(repr(info.aggregation_function))
            if scorer_cls:
                try:
                    source = inspect.getsource(scorer_cls)
                    st.markdown(f"**`{scorer_cls.__name__}` source:**")
                    st.code(source, language="python")
                except OSError:
                    st.caption("Source unavailable for this scorer class.")
            if st.toggle("Show raw ScoringInfo JSON", value=False):
                st.json(_to_jsonable(info))


# --- Cache the heavy stuff ---
@st.cache_resource(show_spinner=False)
def get_questionnaires():
    # persists across reruns in this session
    return QuestionnaireLoader().load_questionnaires()

@st.cache_resource(show_spinner=False)
def get_questions():
    return QuestionLoader().load_questions()


st.set_page_config(page_title="Questionnaire Metadata Explorer", layout="wide")
st.title("🧠 Questionnaire Metadata Explorer")


# Sidebar: Select questionnaire
st.sidebar.header("Search or Select Questionnaire")
# Use cached resources
questionnaires = get_questionnaires()
questionnaire_names = questionnaires.get_all_questionnaires()
questionnaire_desc = questionnaires.get_questionnaires_desc()
questionnaire_desc = questionnaire_desc[~questionnaire_desc['Description'].isna()]
# Use cached resources
questions = get_questions()

#start_idx = random.randint(0, len(questionnaire_names))
q_name = st.sidebar.selectbox("Questionnaire", questionnaire_names, index=4)


# Optional: quick way to refresh if your underlying files change
with st.sidebar:
    st.header("Search or Select Questionnaire")
    if st.button("🔄 Reload data"):
        st.cache_resource.clear()   # clear both resource caches


selected_q = questionnaires.get_by_name(q_name)

# Tabs for Metadata, Scoring, Questions
if selected_q is None:
    st.error(f"No data found for questionnaire: {q_name}")
else:
    tabs = st.tabs(["📋 Questionnaire Metadata", "🧾 Items", "🧮 Scoring Method"])
    with tabs[0]:
        st.subheader("📋 Questionnaire Metadata")
        display_questionnaire_info(selected_q)

    with tabs[1]:
        st.subheader("🧾 Items")

        # Get the QuestionInfo list for the selected questionnaire:
        # Adapt this line to your loader/registry API:
        try:
            question_list = questions.get_by_questionnaire(selected_q.name)
        except AttributeError:
            # fallback if 'questions' is a flat list
            question_list = [q for q in questions if q.questionnaire_name == selected_q.name]

        display_questions_info(question_list)

    with tabs[2]:
        st.subheader("🧮 Scoring Method")
        # assuming you already resolved `selected_q: QuestionnaireInfo`
        if selected_q and selected_q.scoring_info:
            render_scoring_info(selected_q.scoring_info)
        else:
            st.info("No scoring information available.")
        # scoring_info = get_scoring(selected_q)
        # scoring_metadata = get_attributes(scoring_info)
        # display_scoring(scoring_metadata)