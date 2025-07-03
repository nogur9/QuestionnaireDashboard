import pandas as pd
import numpy as np

from source.data_etl.new_process.Transferring_Data_to_PostgreSQL.preprocess_data_before_merging.preprocess_manager import \
    PreprocessManager
from source.consts.standard_names import TIMESTAMP_COLUMN_NAME


class TimestampCreator:
    """
    this happening before splitting into measurement times

    Version 1:
    TIMESTAMPS_COLUMNS = ['opening_timestamp', 'mfq_short_timestamp', 'complaint_date',
                    'sciafca_timestamp', 'mfq_short_timestamp', 'chameleon_timestamp',
                    'chameleon_suicide_er_date_stu', 'chameleon_psychiatric_date_stu',
                    'opening_child_pre_timestamp', 'cssrs_timestamp', 'siq_timestamp']
    """

    OPTIONAL_TIMESTAMPS_COLUMNS = ['complaint_date', 'chameleon_suicide_er_date_stu', 'chameleon_psychiatric_date_stu']

    def __init__(self, timestamp_column=TIMESTAMP_COLUMN_NAME, use_all_timestamps_columns = False):
        self.timestamp_column = timestamp_column

        if use_all_timestamps_columns:
            self.optional_timestamp_columns = pd.read_csv(PreprocessManager.timestamps_columns_path)
        else:
            self.optional_timestamp_columns = TimestampCreator.OPTIONAL_TIMESTAMPS_COLUMNS

    def get(self, df: pd.DataFrame):

        # self._add_timestamp_cols(df)

        df = df.copy()
        for col in self.optional_timestamp_columns:
            df[col] = df[col].apply(TimestampCreator.convert_to_datetime)

        df = self.impute(self.optional_timestamp_columns, df)
        return df


    @staticmethod
    def is_datetime_column(col_name):
        is_timestamp = 'timestamp' in col_name
        is_date = 'date' in col_name
        return is_timestamp or is_date


    @staticmethod
    def convert_to_datetime(date_str):
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


    def impute(self, optional_timestamps_data, df):
        df[self.timestamp_column] = None
        is_empty = df[self.timestamp_column].isna()

        for column in optional_timestamps_data:
            df[self.timestamp_column] = np.where(np.array(is_empty), df[column], df[self.timestamp_column])

            # update which columns where filled
            is_empty = df[self.timestamp_column].isna()

        return df


    # redundant
    def _add_timestamp_cols(self, df: pd.DataFrame):
        df_timestamp_columns = [i for i in df.columns if '_timestamp' in i]
        self.optional_timestamp_columns += df_timestamp_columns

