import numpy as np


class QuestionnaireScorer:
    def __init__(self, name, columns, reversed_columns=None, clusters=None, min_score=None, max_score=None, missing_threshold=0.5):
        self.name = name
        self.columns = columns
        self.reversed_columns = reversed_columns or []
        self.clusters = clusters or {}
        self.min_score = min_score
        self.max_score = max_score
        self.missing_threshold = missing_threshold

        self._validate_reverse_cols()

    def _validate_reverse_cols(self):
        if self.reversed_columns:
            assert (self.min_score is not None) and (self.max_score is not None)

    def compute_scores(self, df):
        main_score_column = self._get_main_score_column()

        df = self._reverse_items(df)
        df[main_score_column] = self._calculate_aggregated_score(df, self.columns)
        df = self._apply_missing_threshold(df, self._get_main_score_column(), self.columns)
        df, subscale_columns = self._calculate_subscales(df)
        df = self._reverse_items(df)  # return to original

        return df, [self._get_main_score_column()] + subscale_columns

    def _reverse_items(self, df):
        df[self.reversed_columns] = self.max_score - df[self.reversed_columns] + self.min_score
        return df

    def _apply_missing_threshold(self, df, score_column, columns):
        missing_ratio_column = self._get_missing_ratio_column(score_column)
        df[missing_ratio_column] = self._calculate_missing_ratio(df, columns)
        df.loc[df[missing_ratio_column] > self.missing_threshold, score_column] = np.nan
        return df.drop(columns=missing_ratio_column)

    def _calculate_subscales(self, df):
        subscale_columns = []
        for subscale, columns in self.clusters.items():
            df[subscale] = self._calculate_aggregated_score(df, columns)
            df = self._apply_missing_threshold(df, subscale, columns)
            subscale_columns.append(subscale)
        return df, subscale_columns

    @staticmethod
    def _calculate_missing_ratio(df, columns):
        missing_values_sum = df[columns].isnull().sum(axis=1)
        return missing_values_sum / len(columns)

    def _calculate_aggregated_score(self, df, columns):
        """
        This function don't need to accommodate for Reverse-Items or Sub-Scales:
        these parameters are delt in this object (QuestionnaireScorer)
        """
        raise NotImplementedError("Each questionnaire_scores must implement its own _calculate_aggregated_score method.")

    def _get_main_score_column(self):
        return f"{self.name}_score"

    def _get_missing_ratio_column(self, score_column):
        return f"{score_column}_missing_ratio"

    def _get_reverse_column_name(self, column):
        return f"{column}_reverse"

