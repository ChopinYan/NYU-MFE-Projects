from datetime import datetime
import pandas as pd
from fall2021py.utils.misc_util import log_trace


@ log_trace
def calc_total_assets_for_all_stocks_plugin(df, config):
    """
    Add average holdings for a single stock together to calculate total assets
    :param config: dict;
    :param df: pd.DataFrame; Provided dataframe
    :return: pd.DataFrame; Resulted dataframe
    """
    new_col_name = config["new_col_name"]
    old_col_name = config["old_col_name"]
    if all([col_name in df for col_name in old_col_name]):
        df[new_col_name] = df[old_col_name].sum(axis=1)

    return df


@ log_trace
def add_hour_min_sec_into_assign_date_plugin(df, config):
    """
    Add hour min and second time to assigned run date
    :param config: dict;
    :param df: pd.DataFrame; Provided dataframe
    :return: pd.DataFrame; Resulted dataframe
    """
    col_need_change = config["col_need_change"]
    if col_need_change in df:
        df[col_need_change] += f' {str(pd.to_datetime(datetime.now())).split(" ")[-1]}'

    return df
