import pandas as pd

from source.consts.standard_names import TIMESTAMP_COLUMN_NAME


class TimestampCreator:
    """
    Create a unified timestamp column **before** splitting into measurement times.

    Behaviour:
    - Looks for all columns whose name ends with ``"_timestamp"``.
    - Converts each of these columns to ``datetime`` (invalid values become ``NaT``).
    - For each row, takes the **earliest (minimum) non-null timestamp** across those
      ``*_timestamp`` columns and stores it in ``self.timestamp_column``.
    """

    def __init__(self, timestamp_column: str = TIMESTAMP_COLUMN_NAME):
        self.timestamp_column = timestamp_column

    def get(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a single unified timestamp column based on all ``*_timestamp`` columns.
        """
        df = df.copy()

        # Use only columns that explicitly end with "_timestamp"
        timestamp_columns = [col for col in df.columns if col.endswith("_timestamp")]

        # If there are no timestamp columns, just create an all-NaT column and return
        if not timestamp_columns:
            df[self.timestamp_column] = pd.NaT
            return df

        # Ensure all candidate columns are proper datetimes
        for col in timestamp_columns:
            df[col] = df[col].apply(self.convert_to_datetime)

        df[timestamp_columns] = df[timestamp_columns].mask(df[timestamp_columns] < pd.Timestamp("2000-01-01"))

        # For each row, choose the earliest non-null timestamp across all *_timestamp columns
        df[self.timestamp_column] = df[timestamp_columns].min(axis=1)

        return df

    @staticmethod
    def convert_to_datetime(date_str):

        if pd.isna(date_str): return pd.NaT
        if pd.notna(pd.to_numeric(date_str, errors='coerce')): return pd.NaT
        try:
            return pd.to_datetime(date_str)
        except ValueError:
            try:
                return pd.to_datetime(int(date_str))
            except ValueError:
                try:
                    return pd.to_datetime(date_str.split(" ")[0], errors='coerce')
                except AttributeError:
                    return pd.NaT
            #
            # except TypeError:
            #     print(f"{date_str = }")



    @staticmethod
    def is_datetime_column(col_name):
        is_timestamp = 'timestamp' in col_name
        is_date = 'date' in col_name
        return is_timestamp or is_date


