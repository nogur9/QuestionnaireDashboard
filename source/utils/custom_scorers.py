from source.utils.questionnaire_scorer import QuestionnaireScorer
from sklearn.preprocessing import MinMaxScaler, StandardScaler


class CustomScorer(QuestionnaireScorer):
    def __init__(self, score_columns, score_name, reverse_columns = None,
                 max_score=0, normalization='MinMax'):

        self.normalization = normalization
        self.reverse_columns = reverse_columns
        self.max_score = max_score

        super().__init__(score_name, score_columns,
                         reverse_columns=self.reverse_columns, max_score=self.max_score)


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
        print(f"{self.name = }")
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


