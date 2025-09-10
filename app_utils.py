from __future__ import annotations
import streamlit as st
import pandas as pd
from typing import List, Dict, Optional, Iterable, Any, Tuple
import hashlib
from dataclasses import asdict, is_dataclass
import inspect


def _nonempty(x) -> bool:
    if x is None:
        return False
    if isinstance(x, (list, dict, set, tuple)):
        return len(x) > 0
    if isinstance(x, str):
        return x.strip() != ""
    return True

def _as_url(s: str) -> bool:
    if not isinstance(s, str):
        return False
    return s.startswith("http://") or s.startswith("https://") or s.startswith("www.")

def _unique_compact_list(xs: Iterable[str]) -> list[str]:
    seen, out = set(), []
    for x in xs:
        if not _nonempty(x):
            continue
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _enum_to_str(e) -> str:
    # Handles Enum or plain strings
    return getattr(e, "name", str(e))

def _hash_color(label: str, palette: List[str]) -> str:
    # Stable color for a given label
    h = int(hashlib.sha1(label.encode("utf-8")).hexdigest(), 16)
    return palette[h % len(palette)]

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

def _colored_dot(color: str) -> str:
    return f"""<span style="display:inline-block;width:10px;height:10px;border-radius:999px;background:{color};margin-right:6px;"></span>"""

# ---------- Styling helpers for DataFrame ----------
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
    # Keep table compact
    styler = styler.set_properties(**{
        "white-space": "nowrap",
        "text-overflow": "ellipsis",
        "overflow": "hidden",
        "font-size": "0.92rem",
    })
    return styler


def _render_question_cards(dff: pd.DataFrame,
                           type_colors: Dict[str, str],
                           source_colors: Dict[str, str],
                           questions_raw: list[QuestionInfo],
                           limit: int = 250):
    """
    Card list with clickable 'Choices' popovers per question.
    'dff' is the filtered table (with columns Var/Text/Type/Source/...)
    'questions_raw' is the original list (to retrieve full choices & full text)
    """
    # Build a quick index: var_name -> QuestionInfo
    by_var = {q.variable_name: q for q in questions_raw}

    n = len(dff)
    if n == 0:
        st.info("No questions to show.")
        return

    st.caption(f"Showing {min(n, limit):,} of {n:,} (card view)")
    if n > limit:
        st.warning("Large result set—showing the first subset for speed. Refine filters or grouping to see more.")

    for _, row in dff.head(limit).iterrows():
        var = row["Var"]
        q = by_var.get(var)  # safe: None if not found
        txt_full = (q.question_text if q else row["Text"]) or ""
        # layout
        c1, c2 = st.columns([4, 2])
        with c1:
            st.markdown(f"**`{var}`**")
            st.write(txt_full)

            # badges row
            badges_html = ""
            t = row["Type"]
            s = row["Source"]
            if t:
                badges_html += _badge(t, type_colors.get(t, "#888888"))
            if s:
                badges_html += _badge(s, source_colors.get(s, "#888888"))
            if row["Timestamp"] == "✓":
                badges_html += _badge("timestamp", "#4c78a8")
            if row["Exceptional"] == "✓":
                badges_html += _badge("exceptional", "#e45756")
            st.markdown(badges_html, unsafe_allow_html=True)

        with c2:
            # Right column: interactive chips
            cols = st.columns(2)
            # Choices popover (clickable)
            choices_cnt = int(row["Choices"] or 0)
            with cols[0]:
                if choices_cnt > 0:
                    with st.popover(f"Choices {choices_cnt}"):
                        # show as a small table: key -> meaning
                        data = []
                        if q and isinstance(q.choices, dict):
                            for k, v in q.choices.items():
                                data.append({"Value": str(k), "Meaning": str(v)})
                        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True, height=220)
                else:
                    st.caption("Choices —")

            # Extras popover (branching/validator)
            with cols[1]:
                has_branch = (q and _nonempty(q.branching_logic))
                has_val = (q and q.validator)
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




def _enum_name(e: Any) -> str:
    """Safe enum name."""
    try:
        return getattr(e, "name", str(e))
    except Exception:
        return str(e)

def _scoring_method_label(agg: Any) -> Tuple[str, Optional[type]]:
    """
    Normalize the aggregation_function to a friendly label and (optional) scorer class.
    Supports ScoringMethod, UniqueScoringMethod, C_SSRS_Scoring, or strings/callables.
    """
    # Try the attributes that exist on your enums
    if hasattr(agg, "label"):  # ScoringMethod
        label = getattr(agg, "label", _enum_name(agg))
        scorer_cls = getattr(agg, "scorer_class", None)
        return str(label), scorer_cls

    if hasattr(agg, "questionnaire") and hasattr(agg, "scorer_class"):  # Unique / C_SSRS
        kind = "Unique Scoring" if "Unique" in agg.__class__.__name__ else "C_SSRS Scoring"
        q = getattr(agg, "questionnaire", _enum_name(agg))
        label = f"{kind} · {q}"
        scorer_cls = getattr(agg, "scorer_class", None)
        return label, scorer_cls

    # Fallbacks
    if isinstance(agg, str):
        return agg, None
    if inspect.isclass(agg):
        return agg.__name__, agg
    return str(agg), None


def _clusters_reverse_index(clusters: Optional[Dict[str, List[str]]]) -> Dict[str, str]:
    """Build {column -> cluster_name} mapping for quick lookup."""
    rev = {}
    if not clusters:
        return rev
    for cl_name, cols in clusters.items():
        for c in cols or []:
            # if a column appears in multiple clusters, prefer first seen; flag later in validation
            rev.setdefault(c, cl_name)
    return rev


def _validate_scoring(info) -> List[str]:
    """
    Lightweight validations; returns list of warning strings.
    - reversed columns should be subset of columns
    - duplicates in columns / reversed columns
    - columns belonging to multiple clusters
    """
    warnings: List[str] = []

    cols = list(info.columns or [])
    rev = list(info.reversed_columns or [])
    clusters = info.clusters or {}

    # 1) reversed ⊆ columns
    extra_rev = sorted(set(rev) - set(cols))
    if extra_rev:
        warnings.append(f"`reversed_columns` not in `columns`: {extra_rev}")

    # 2) duplicates
    dup_cols = sorted(pd.Series(cols).value_counts().loc[lambda s: s > 1].index.tolist()) if cols else []
    if dup_cols:
        warnings.append(f"Duplicate entries in `columns`: {dup_cols}")

    dup_rev = sorted(pd.Series(rev).value_counts().loc[lambda s: s > 1].index.tolist()) if rev else []
    if dup_rev:
        warnings.append(f"Duplicate entries in `reversed_columns`: {dup_rev}")

    # 3) columns in multiple clusters
    seen = {}
    multi: Dict[str, List[str]] = {}
    for cl, cl_cols in (clusters or {}).items():
        for c in cl_cols or []:
            if c in seen and seen[c] != cl:
                multi.setdefault(c, [seen[c]]).append(cl)
            else:
                seen[c] = cl
    if multi:
        details = {k: v for k, v in sorted(multi.items())}
        warnings.append(f"Columns assigned to multiple clusters (column: clusters): {details}")

    return warnings


def _to_jsonable(obj: Any) -> Any:
    """Dataclass/enums → JSONable for st.json."""
    try:
        if is_dataclass(obj):
            d = asdict(obj)
            # Convert enum-ish fields
            if "aggregation_function" in d:
                d["aggregation_function"] = _enum_name(obj.aggregation_function)
            return d
    except Exception:
        pass
    # generic fallback
    if hasattr(obj, "__dict__"):
        return {k: _to_jsonable(v) for k, v in obj.__dict__.items()}
    return obj

