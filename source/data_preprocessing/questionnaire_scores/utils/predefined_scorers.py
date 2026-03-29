from source.data_preprocessing.questionnaire_scores.utils.questionnaire_scorer import QuestionnaireScorer
from sklearn.preprocessing import MinMaxScaler, StandardScaler


class CustomScorer(QuestionnaireScorer):
    def __init__(
        self,
        score_columns,
        score_name,
        reverse_columns=None,
        max_score=0,
        normalization='MinMax',
    ):
        self.normalization = normalization
        self.reverse_columns = reverse_columns
        self.max_score = max_score

        super().__init__(
            score_name,
            score_columns,
            reversed_columns=self.reverse_columns,
            max_score=self.max_score,
        )


    def _calculate_aggregated_score(self, df, columns):

        if self.normalization == 'z-score':
            scaler = StandardScaler()

        elif self.normalization == 'MinMax':
            scaler = MinMaxScaler()

        elif self.normalization == 'None':
            scaler = None
        else:
            raise ValueError("missing normalization method")
        if scaler is None:
            normalized_df = df.copy()
        else:
            normalized_values = scaler.fit_transform(df[columns])
            normalized_df = df.copy()
            normalized_df[columns] = normalized_values

        return normalized_df[columns].mean(axis=1, skipna=True)



class SumScorer(QuestionnaireScorer):
    def __init__(self, **params):
        super().__init__(**params)

    def _calculate_aggregated_score(self, df, columns):
        return df[columns].sum(axis=1, skipna=True)


class AverageScorer(QuestionnaireScorer):
    def __init__(self, **params):
        super().__init__(**params)

    def _calculate_aggregated_score(self, df, columns):
        return df[columns].mean(axis=1, skipna=True)


class SingleItemScorer(QuestionnaireScorer):
    def __init__(self, **params):
        super().__init__(**params)

    def _calculate_aggregated_score(self, df, columns):
        return df[columns[0]]


class CSSRSScorer(QuestionnaireScorer):
    """
    Scorer for the C-SSRS questionnaire.

    Expected columns (in order):
        c_ssrs_1, c_ssrs_2, c_ssrs_3, c_ssrs_4, c_ssrs_5, c_ssrs_6

    Risk levels:
        0 = no risk
        1 = low risk
        2 = moderate risk
        3 = high risk
    """

    def __init__(self, **params):
        """
        Parameters should at least include:
            - name: base name for the score (e.g. "c_ssrs")
            - columns: list of item columns in the order above
        """
        super().__init__(**params)

    def _calculate_aggregated_score(self, df, columns):
        # Map columns positionally so the scorer is robust to exact column names
        if len(columns) < 6:
            raise ValueError(
                "CSSRSScorer expects at least 6 columns corresponding to c_ssrs_1..c_ssrs_6."
            )

        c1_col, c2_col, c3_col, c4_col, c5_col, c6_col = columns[:6]

        # Start with no-risk = 0
        scores = df.index.to_series().map(lambda _: 0).astype(float)

        # High risk (3): any of items 4–6 endorsed
        high_risk_mask = df[[c4_col, c5_col, c6_col]].eq(1).any(axis=1)
        scores.loc[high_risk_mask] = 3

        # Moderate risk (2): item 3 = 1 and items 4–6 = 0 (and not already high risk)
        moderate_risk_mask = (
            ~high_risk_mask
            & (df[c3_col] == 1)
            & df[[c4_col, c5_col, c6_col]].eq(0).all(axis=1)
        )
        scores.loc[moderate_risk_mask] = 2

        # Low risk (1): item 1 or 2 = 1 and items 3–6 = 0 (and not already higher risk)
        low_risk_mask = (
            ~high_risk_mask
            & ~moderate_risk_mask
            & ((df[c1_col] == 1) | (df[c2_col] == 1))
            & df[[c3_col, c4_col, c5_col, c6_col]].eq(0).all(axis=1)
        )
        scores.loc[low_risk_mask] = 1

        # Remaining rows (not captured above) stay as 0 (no risk)
        return scores


