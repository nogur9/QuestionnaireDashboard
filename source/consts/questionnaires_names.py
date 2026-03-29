from __future__ import annotations

import csv
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, Optional


def _normalize_key(name: str) -> str:
    """
    Internal helper: produce a stable key for lookup.
    """
    return (
        name.strip()
        .lower()
        .replace(" ", "")
        .replace("-", "_")
    )


def _iter_questionnaire_rows() -> Iterable[tuple[str, list[str]]]:
    """
    Yield (name, aliases) tuples from questionnaire_parallel_names.csv.

    - name: value from the "name" column (used as the Enum member name and value)
    - aliases: all non-empty alternatives (including "questionnaire_alternative_name"
      and "Abbreviated_Name")
    """
    # CSV is stored at the project root
    base_dir = Path(__file__).resolve().parents[2]
    csv_path = base_dir / "questionnaire_parallel_names.csv"

    if not csv_path.exists():
        return []

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_name = (row.get("name") or "").strip()
            if not raw_name:
                continue
            # Skip entries that cannot be valid Python identifiers (e.g. "('',)")
            if not raw_name.isidentifier():
                continue

            aliases: list[str] = [raw_name]
            alt = (row.get("questionnaire_alternative_name") or "").strip()
            abbr = (row.get("Abbreviated_Name") or "").strip()
            if alt:
                aliases.append(alt)
            if abbr:
                aliases.append(abbr)
            yield raw_name, aliases


def _build_enum_and_alias_map() -> tuple["Questionnaire", Dict[str, "Questionnaire"]]:
    """
    Create the Questionnaire enum (from the CSV "name" column)
    and a mapping from any alias string to the matching enum member.
    """
    members: Dict[str, str] = {}
    alias_to_member_name: Dict[str, str] = {}

    for name, aliases in _iter_questionnaire_rows():
        # Enum member names must be unique
        if name in members:
            continue
        members[name] = name

        for alias in aliases:
            key = _normalize_key(alias)
            alias_to_member_name[key] = name

    # Dynamically create the Enum class so it always reflects the CSV content
    Questionnaire = Enum("Questionnaire", members)  # type: ignore[misc]

    alias_to_enum: Dict[str, Questionnaire] = {
        key: Questionnaire[member_name] for key, member_name in alias_to_member_name.items()
    }

    return Questionnaire, alias_to_enum


# Public enum: each member name is taken from the CSV "name" column.
# Example: Questionnaire.c_ssrs, Questionnaire.ARI_P_M, ...
Questionnaire, _ALIAS_TO_ENUM = _build_enum_and_alias_map()
print(0)

def normalize_questionnaire_name(name: Optional[str]) -> Optional[str]:
    """
    Normalize a questionnaire identifier (any alias) to its canonical enum name.

    Returns:
        - The enum member `.name` as a string if the identifier is known.
        - A cleaned version of the input (lower-cased, spaces removed, '-' -> '_')
          if it is not found in the aliases.
        - None if `name` is None.
    """
    if name is None:
        return None

    key = _normalize_key(name)

    enum_member = _ALIAS_TO_ENUM.get(key)
    if enum_member is not None:
        return enum_member.name

    # Fallback: return the normalized key as-is
    return key


def normalize_questionnaire_list(names: list[str]) -> list[str]:
    """
    Convenience helper to normalize a list of questionnaire identifiers.
    """
    return [normalize_questionnaire_name(n) for n in names if n is not None]


def get_questionnaire(name: str, raise_error: bool = True) -> Questionnaire:
    """
    Return the `Questionnaire` enum member matching any known alias.

    Accepts:
        - canonical CSV name (e.g. "c_ssrs", "ARI_P_M")
        - alternative name (e.g. "cssrs", "arippps_m")
        - abbreviated name (e.g. "C-SSRS_T_Clin", "MFQ-Short"), case-insensitive.

    Raises:
        KeyError if the identifier is unknown.
    """
    key = _normalize_key(name)

    enum_member = _ALIAS_TO_ENUM.get(key)
    if enum_member is not None:
        return enum_member

    # Also allow exact enum member names (case-insensitive) as a fallback
    for member in Questionnaire:
        if member.name.lower() == key or str(member.value).lower() == key:
            return member
    if raise_error:
        raise KeyError(f"Unknown questionnaire identifier: {name!r}")
    else:
        return None

