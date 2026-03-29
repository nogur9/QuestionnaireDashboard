from __future__ import annotations

from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd


class QuestionnaireScorer:
    """
    Base class for computing questionnaire scores.

    Responsibilities:
    - Handle reverse-coded items given min/max score.
    - Apply a missingness threshold per score / subscale.
    - Delegate the core aggregation logic to subclasses via _calculate_aggregated_score.
    """

    def __init__(
        self,
        name: str,
        columns: Sequence[str],
        reversed_columns: Sequence[str] | None = None,
        clusters: Dict[str, Sequence[str]] | None = None,
        min_score: float | None = None,
        max_score: float | None = None,
        missing_threshold: float = 0,
    ):
        self.name = name
        self.columns = list(columns)
        self.reversed_columns = list(reversed_columns or [])
        self.clusters = dict(clusters or {})
        self.min_score = min_score
        self.max_score = max_score
        self.missing_threshold = missing_threshold

        self._validate_reverse_cols()

    def _validate_reverse_cols(self) -> None:
        if self.reversed_columns:

            assert (
                self.min_score is not None and self.max_score is not None
            ), f"min_score and max_score must be set when using reversed_columns. {self.name = }"

    def compute_scores(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Compute main score and subscale scores for this questionnaire.

        Returns:
            (updated_df, score_columns)
        """
        df = df.copy()
        main_score_column = self._get_main_score_column()

        # Work on a reversed copy, compute all scores, then restore original values.
        df = self._reverse_items(df)
        df[main_score_column] = self._calculate_aggregated_score(df, self.columns)
        if self.missing_threshold > 0:
            df = self._apply_missing_threshold(df, main_score_column, self.columns)
        df, subscale_columns = self._calculate_subscales(df)
        df = self._reverse_items(df)  # return items to original coding

        return df, [main_score_column] + subscale_columns

    def _reverse_items(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Reverse-score selected items in-place (1 <-> max, etc.).
        """
        if not self.reversed_columns:
            return df

        # Operate only on columns that actually exist in the DataFrame
        existing_cols = [c for c in self.reversed_columns if c in df.columns]
        if not existing_cols:
            return df

        df[existing_cols] = self.max_score - df[existing_cols] + self.min_score
        return df

    def _apply_missing_threshold(
        self, df: pd.DataFrame, score_column: str, columns: Iterable[str]
    ) -> pd.DataFrame:
        missing_ratio_column = self._get_missing_ratio_column(score_column)
        df[missing_ratio_column] = self._calculate_missing_ratio(df, list(columns))
        df.loc[df[missing_ratio_column] > self.missing_threshold, score_column] = np.nan
        return df.drop(columns=missing_ratio_column)

    def _calculate_subscales(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        subscale_columns: List[str] = []
        for subscale_name, subscale_items in self.clusters.items():
            df[subscale_name] = self._calculate_aggregated_score(df, subscale_items)
            df = self._apply_missing_threshold(df, subscale_name, subscale_items)
            subscale_columns.append(subscale_name)
        return df, subscale_columns

    @staticmethod
    def _calculate_missing_ratio(df: pd.DataFrame, columns: Sequence[str]) -> pd.Series:
        missing_values_sum = df[columns].isnull().sum(axis=1)
        return missing_values_sum / len(columns)

    def _calculate_aggregated_score(
        self, df: pd.DataFrame, columns: Sequence[str]
    ) -> pd.Series:
        """
        Subclasses must implement the actual aggregation over `columns`
        (e.g. sum, mean, custom weighted scores, etc.).
        """
        raise NotImplementedError(
            "Each questionnaire scorer must implement `_calculate_aggregated_score`."
        )

    def _get_main_score_column(self) -> str:
        return f"{self.name}_score"

    def _get_missing_ratio_column(self, score_column: str) -> str:
        return f"{score_column}_missing_ratio"

    def _get_reverse_column_name(self, column: str) -> str:
        return f"{column}_reverse"

