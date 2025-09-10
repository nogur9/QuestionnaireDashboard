import pandas as pd


class TimestampCreator:

    def __init__(self):
        pass

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
