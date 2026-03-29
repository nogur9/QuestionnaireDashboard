import streamlit as st
import sys
import os
from typing import List, Dict, Optional, Iterable, Any, Tuple
import pandas as pd
import hashlib
from dataclasses import asdict, is_dataclass
import inspect
import textwrap

from source.data_etl.questionnaires_metadata.info_objects import QuestionInfo
from source.data_etl.questionnaires_metadata.stepped_care.single_question.questions_loader import QuestionLoader
from source.data_preprocessing.pathology_variables.pathologies_map import PathologiesNames
from source.data_preprocessing.pathology_variables.pathology_variable import PathologyVariable

sys.path.insert(0, os.getcwd())


def _enum_name(e: Any) -> str:
    """Safe enum name."""
    try:
        return getattr(e, "name", str(e))
    except Exception:
        return str(e)


def _enum_to_str(e) -> str:
    # Handles Enum or plain strings
    return getattr(e, "name", str(e))


def _badge(label: str, color: str) -> str:
    # Small rounded badge (render in st.markdown(..., unsafe_allow_html=True))
    return f"""
    <span style="
        display:inline-block;
        padding:2px 7px;
        border-radius:999px;
        background:{color}22;
        color:{color};
        border:1px solid {color}55;
        font-size:12px;
        margin-right:6px;
        white-space:nowrap;">
        {label}
    </span>
    """


def _nonempty(x) -> bool:
    if x is None:
        return False
    if isinstance(x, (list, dict, set, tuple)):
        return len(x) > 0
    if isinstance(x, str):
        return x.strip() != ""
    return True


def _hash_color(label: str, palette: List[str]) -> str:
    # Stable color for a given label
    h = int(hashlib.sha1(label.encode("utf-8")).hexdigest(), 16)
    return palette[h % len(palette)]


def _style_questions_df(df: pd.DataFrame,
                        type_colors: Dict[str, str],
                        source_colors: Dict[str, str]) -> "pd.io.formats.style.Styler":
    def color_type_col(s: pd.Series):
        return [f"background-color: {type_colors.get(v, '#00000010')+'22'}" for v in s]

    def color_source_col(s: pd.Series):
        return [f"background-color: {source_colors.get(v, '#00000010')+'22'}" for v in s]

    styler = (df.style
        .apply(color_type_col, subset=["Type"])
        .apply(color_source_col, subset=["Source"])
    )
    styler = styler.set_properties(**{
        "white-space": "nowrap",
        "text-overflow": "ellipsis",
        "overflow": "hidden",
        "font-size": "0.92rem",
    })
    return styler


def _to_jsonable(obj: Any) -> Any:
    """Dataclass/enums → JSONable for st.json."""
    try:
        if is_dataclass(obj):
            d = asdict(obj)
            if "aggregation_function" in d:
                d["aggregation_function"] = _enum_name(obj.aggregation_function)
            return d
    except Exception:
        pass
    if hasattr(obj, "__dict__"):
        return {k: _to_jsonable(v) for k, v in obj.__dict__.items()}
    return obj


def _render_question_cards(dff: pd.DataFrame,
                           type_colors: Dict[str, str],
                           source_colors: Dict[str, str],
                           questions_by_var: Dict[str, Optional[QuestionInfo]],
                           limit: int = 250):
    n = len(dff)
    if n == 0:
        st.info("No items to show.")
        return

    st.caption(f"Showing {min(n, limit):,} of {n:,} (card view)")
    if n > limit:
        st.warning("Large result set—showing the first subset for speed. Refine filters to see more.")

    for _, row in dff.head(limit).iterrows():
        var = row["Var"]
        q = questions_by_var.get(var)
        txt_full = (q.question_text if q else row["Text"]) or ""

        c1, c2 = st.columns([4, 2])
        with c1:
            st.markdown(f"**`{var}`**")
            if row.get("Questionnaire"):
                st.caption(f"From: `{row['Questionnaire']}`")
            st.write(txt_full)

            badges_html = ""
            t = row.get("Type", "")
            s = row.get("Source", "")
            if t:
                badges_html += _badge(t, type_colors.get(t, "#888888"))
            if s:
                badges_html += _badge(s, source_colors.get(s, "#888888"))
            st.markdown(badges_html, unsafe_allow_html=True)

        with c2:
            cols = st.columns(2)
            choices_cnt = int(row.get("Choices", 0) or 0)
            with cols[0]:
                if choices_cnt > 0 and q and isinstance(q.choices, dict):
                    with st.popover(f"Choices {choices_cnt}"):
                        data = [{"Value": str(k), "Meaning": str(v)} for k, v in q.choices.items()]
                        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True, height=220)
                else:
                    st.caption("Choices —")

            with cols[1]:
                has_branch = bool(q and _nonempty(q.branching_logic))
                has_val = bool(q and q.validator)
                if has_branch or has_val:
                    with st.popover("Details"):
                        if has_branch:
                            st.markdown("**Branching logic**")
                            st.code(q.branching_logic, language="text")
                        if has_val:
                            st.markdown("**Validator**")
                            vtxt = getattr(q.validator, "name", None) or getattr(q.validator, "pattern", None) or str(q.validator)
                            st.code(vtxt, language="text")
                else:
                    st.caption("Details —")

        st.divider()


def display_pathology_info(pathology_name: str, variants: List[PathologyVariable], questions_index: Any):
    st.markdown(f"### {pathology_name}")

    items_all: List[str] = []
    for v in variants:
        items_all.extend(list(v.questions or []))
    items_unique = list(dict.fromkeys(items_all))

    q_infos = [questions_index.get_by_variable_name(x) for x in items_unique]
    found = sum(1 for q in q_infos if q is not None)
    missing = [x for x, qi in zip(items_unique, q_infos) if qi is None]

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Variants", len(variants))
    with m2:
        st.metric("Items", len(items_unique))
    with m3:
        st.metric("Items with metadata", found)

    with st.expander("Variants (intake / follow-up flags)", expanded=True):
        rows = []
        for idx, v in enumerate(variants, start=1):
            rows.append({
                "variant": idx,
                "name": v.name,
                "only_intake_evaluation": bool(getattr(v, "only_intake_evaluation", False)),
                "only_follow_up_evaluation": bool(getattr(v, "only_follow_up_evaluation", False)),
                "n_items": len(v.questions or []),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if missing:
        with st.expander(f"Missing item metadata ({len(missing)})", expanded=False):
            st.write(", ".join(f"`{x}`" for x in missing[:250]) + (" …" if len(missing) > 250 else ""))

    with st.popover("Raw pathology metadata (debug)"):
        st.json({
            "pathology_name": pathology_name,
            "variants": [_to_jsonable(v) for v in variants],
            "items_unique": items_unique[:500],
            "missing_items": missing[:500],
        })


def display_pathology_items(items: List[str], questions_index: Any):
    if not items:
        st.info("No items found for this pathology.")
        return

    questions_by_var: Dict[str, Optional[QuestionInfo]] = {v: questions_index.get_by_variable_name(v) for v in items}

    recs = []
    for var in items:
        q = questions_by_var.get(var)
        if q is None:
            recs.append({
                "Var": var,
                "Text": "",
                "Type": "",
                "Source": "",
                "Questionnaire": "",
                "Choices": 0,
                "Branching?": "",
                "Validator": "",
            })
            continue

        q_type = _enum_to_str(q.question_type)
        source = q.project_source or ""
        qname = str(q.questionnaire_name or "")
        text_short = textwrap.shorten(str(q.question_text or ""), width=120, placeholder="…")
        recs.append({
            "Var": q.variable_name,
            "Text": text_short,
            "Type": q_type,
            "Source": source,
            "Questionnaire": qname,
            "Choices": len(q.choices) if isinstance(q.choices, dict) else 0,
            "Branching?": "✓" if _nonempty(q.branching_logic) else "",
            "Validator": getattr(q.validator, "name", getattr(q.validator, "pattern", "")) if q.validator else "",
        })

    df = pd.DataFrame.from_records(recs)

    palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#4c78a8", "#f58518", "#54a24b", "#e45756", "#72b7b2",
    ]

    type_values = sorted([t for t in df["Type"].unique() if _nonempty(t)])
    source_values = df["Source"].dropna().unique().tolist()

    type_colors = {t: _hash_color(t, palette) for t in type_values}
    source_colors = {s: _hash_color(s, palette[::-1]) for s in source_values}

    with st.container():
        c1, c2, c3, c4 = st.columns([2.6, 2.1, 2.1, 1.2])
        with c1:
            search = st.text_input("Search Var/Text/Questionnaire", placeholder="search…")
        with c2:
            types_sel = st.multiselect("Type", options=type_values, default=type_values)
        with c3:
            sources_sel = st.multiselect("Source", options=source_values, default=source_values)
        with c4:
            missing_only = st.toggle("Missing metadata only", value=False)

    mask = pd.Series(True, index=df.index)
    if _nonempty(search):
        s = search.lower()
        mask &= (
            df["Var"].str.lower().str.contains(s)
            | df["Text"].str.lower().str.contains(s)
            | df["Questionnaire"].fillna("").astype(str).str.lower().str.contains(s)
        )
    if _nonempty(types_sel):
        mask &= df["Type"].isin(types_sel)
    if _nonempty(sources_sel):
        mask &= df["Source"].isin(sources_sel)
    if missing_only:
        mask &= (df["Questionnaire"].fillna("").astype(str).str.strip() == "")

    dff = df.loc[mask].copy()

    with st.expander("Legend / color keys", expanded=False):
        if type_values:
            st.markdown("**Type**")
            st.markdown(" ".join(_badge(t, type_colors[t]) for t in type_values), unsafe_allow_html=True)
        if source_values:
            st.markdown("**Source**")
            st.markdown(" ".join(_badge(s, source_colors[s]) for s in source_values), unsafe_allow_html=True)

    st.caption(f"{len(dff):,} items match filters")
    styler = _style_questions_df(dff, type_colors, source_colors)
    st.dataframe(styler, use_container_width=True, hide_index=True, height=min(680, 42 + 28 * min(len(dff), 22)))

    st.markdown("")
    enable_cards = st.toggle("Card view with clickable choices", value=False)
    if enable_cards:
        _render_question_cards(dff, type_colors, source_colors, questions_by_var)


@st.cache_resource(show_spinner=False)
def get_questions():
    return QuestionLoader().load_questions()


st.set_page_config(page_title="Pathology Metadata Explorer", layout="wide")
st.title("🧬 Pathology Metadata Explorer")

st.sidebar.header("Select Pathology")
pathology_options = sorted(PathologiesNames.keys())
selected_pathology = st.sidebar.selectbox("Pathology", pathology_options, index=0 if pathology_options else None)

questions_index = get_questions()

if not selected_pathology:
    st.info("No pathologies found.")
else:
    variants = PathologiesNames.get(selected_pathology, []) or []
    variant_labels = []
    for i, v in enumerate(variants):
        flags = []
        if getattr(v, "only_intake_evaluation", False):
            flags.append("intake")
        if getattr(v, "only_follow_up_evaluation", False):
            flags.append("follow-up")
        suffix = f" ({', '.join(flags)})" if flags else ""
        variant_labels.append(f"Variant {i+1}{suffix} · {len(v.questions or [])} items")

    chosen = st.sidebar.multiselect(
        "Include variants",
        options=list(range(len(variants))),
        default=list(range(len(variants))),
        format_func=lambda i: variant_labels[i] if i < len(variant_labels) else str(i),
    )
    chosen_variants = [variants[i] for i in chosen] if chosen else []

    all_items: List[str] = []
    for v in chosen_variants:
        all_items.extend(list(v.questions or []))
    items_unique = list(dict.fromkeys(all_items))

    tabs = st.tabs(["📋 Pathology Metadata", "🧾 Items"])
    with tabs[0]:
        st.subheader("📋 Pathology Metadata")
        display_pathology_info(selected_pathology, chosen_variants, questions_index)

    with tabs[1]:
        st.subheader("🧾 Items")
        display_pathology_items(items_unique, questions_index)

