import pandas as pd
import numpy as np
from datetime import datetime

import fall2021py.utils.file_util as fileu
import fall2021py.utils.misc_util as miscu
from fall2021py.utils.misc_util import log_trace


@ log_trace
def apply_dtype_feature(df, config):
    """
    ETL feature to apply data types to dataframe columns and limit columns to ones specified
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Resulted dataframe
    Sample:
    "apply_dtype": {
        "INSURANCE_CODE": "str",
        "INSURANCE_AMOUNT": "float",
        "CLIENT_TYPE": "int"
    }
    """
    if config and isinstance(config, dict):
        for column_key, type_value in config.items():
            if column_key in df:
                # str type.
                if type_value is str or type_value == 'str':
                    df[column_key] = df[column_key].fillna('')
                    df[column_key] = df[column_key].astype(str)
                # int type.
                elif type_value is int or type_value == 'int':
                    df[column_key] = df[column_key].fillna(0)
                    df[column_key] = df[column_key].astype(int)
                # float type.
                elif type_value is float or type_value == 'float':
                    df[column_key] = df[column_key].fillna(0.0)
                    df[column_key] = df[column_key].astype(float)
                # TODO: Implement datetime.date type
                elif type_value == 'datetime':
                    df[column_key] = df[column_key].fillna(method='bfill')
                    df[column_key] = df[column_key].apply(lambda _: datetime.strptime(_, "%Y-%m-%d"))
            else:
                raise KeyError(f'Column <{column_key}> is missing from given dataframe')

        # Limit dataframe to specified columns.
        df = df[list(config.keys())]
    return df


@ log_trace
def read_feature(config):
    """
    ETL feature to read a file, based on provided ETL configuration section
    This is a composite feature, since it can call apply_dtype_feature, if appropriate config section exists
    :param config: dict; Provided configuration mapping
    :return: pd.DataFrame; Resulted dataframe
    """
    df_target = fileu.read(description=miscu.eval_elem_mapping(config, 'description'),
                           path=miscu.eval_elem_mapping(config, 'path'),
                           file_type=miscu.eval_elem_mapping(config, 'file_type', default_value='excel'),
                           separator=miscu.eval_elem_mapping(config, 'separator', default_value=','),
                           skip_rows=miscu.eval_elem_mapping(config, 'skip_rows', default_value=0),
                           use_cols=miscu.eval_elem_mapping(config, 'use_cols', default_value=None),
                           sheet_name=miscu.eval_elem_mapping(config, 'sheet_name', default_value=0))

    # removes any spaces or specified characters at the start and end of a string
    df_target.columns = df_target.columns.str.strip()

    # Call apply_dtype_feature, if appropriate config section exists
    apply_dtype_config = miscu.eval_elem_mapping(config, 'apply_dtype')
    if apply_dtype_config:
        df_target = apply_dtype_feature(df_target, apply_dtype_config)

    return df_target


@ log_trace
def mapping_feature(df, config):
    """
    ETL feature to merge given dataframe with extracted mapping dataframe
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Resulted dataframe
    """
    df_mapping = read_feature(config['read'])
    df_target = pd.merge(df, df_mapping, how='left',  # merge depends on the left (left index retained)
                         left_on=miscu.eval_elem_mapping(config, 'left_on'),  # left df index
                         right_on=miscu.eval_elem_mapping(config, 'right_on'))  # right df index
    df_target.drop(columns=miscu.eval_elem_mapping(config, 'right_on'), inplace=True)  # drop original right index

    return df_target


@ log_trace
def write_feature(df, config):
    """
    ETL feature to write a dataset to a file, based on provided ETL configuration section
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return null
    """
    fileu.write(df,
                description=miscu.eval_elem_mapping(config, 'description'),
                path=miscu.eval_elem_mapping(config, 'path'),
                file_type=miscu.eval_elem_mapping(config, 'file_type', default_value='excel'),
                index=miscu.eval_elem_mapping(config, 'index'),
                separator=miscu.eval_elem_mapping(config, 'separator', default_value=','),
                mode=miscu.eval_elem_mapping(config, 'mode', default_value='new'))


@ log_trace
def rearrange_feature(df, config):
    """
    ETL feature to rename and reorder columns of given dataframe.
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Resulted dataframe
    """
    if not config:
        return df
    else:
        df_target = df

        # Rename columns.
        config_to_rename = miscu.eval_elem_mapping(config, 'col_rename')
        if config_to_rename and isinstance(config_to_rename, dict):
            df_target.rename(columns=config_to_rename, inplace=True)

        # Reorder columns.
        config_to_reorder = miscu.eval_elem_mapping(config, 'col_reorder')
        if config_to_reorder and isinstance(config_to_reorder, list):
            df_target = df_target.reindex(columns=config_to_reorder)

    return df_target


@ log_trace
def aggregate_feature(df, config):
    """
    ETL feature to aggregate given dataframe including group by and pivot table
    :param df: pd.DataFrame; output dataframe from extraction part
    :param config: dict; Provided feature configuration
    :return: pd.DataFrame; aggregated dataframe
    """
    if not config:
        return df
    else:
        df_target = df
        length = len(df_target.index)
        agg_type = miscu.eval_elem_mapping(config, 'type')
        agg_values = miscu.eval_elem_mapping(config, 'values')

        # Whether to calculate total assets or not (position * close price)
        # calc_total_assets is the column name of total assets
        calc_total_assets = miscu.eval_elem_mapping(config, 'calc_total_assets')
        if calc_total_assets:
            df_target[calc_total_assets] = [1] * length
            for col in agg_values:
                df_target[calc_total_assets] *= df_target[col]
            agg_values = [calc_total_assets]

        # Aggregation
        if agg_type == "groupby":
            # group_by version
            df_target = df_target.groupby(
                config["groupby"])[agg_values].apply(eval(config["aggfunc"])).unstack()
        else:
            # pivot_table version
            df_target = pd.pivot_table(
                df_target,
                values=agg_values,
                index=config["index"],
                columns=config["columns"],
                aggfunc=eval(config["aggfunc"]))

        # Flatten MultiIndex and MultiColumns
        if isinstance(df_target.columns, pd.MultiIndex):
            df_target.columns = ["_".join(a) for a in df_target.columns.to_flat_index()]
            df_target.reset_index(inplace=True)

    return df_target


@ log_trace
def assign_feature(df, config):
    """
    ETL feature to assign new columns to a given dataframe
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Resulted dataframe
    """
    if not config:
        return df
    else:
        df_target = df
        length = len(df_target.index)
        config_assign = dict()

        # Assign new columns, using static values.
        config_assign_const = miscu.eval_elem_mapping(config, 'col_const')
        if config_assign_const and isinstance(config_assign_const, dict):
            config_assign.update(config_assign_const)

        # Assign new columns, using variable values.
        config_assign_var = miscu.eval_elem_mapping(config, 'col_var')
        if config_assign_var and isinstance(config_assign_var, dict):
            config_assign.update(config_assign_var)

        for col_name, col_value in config_assign.items():
            df_target[col_name] = [col_value] * length

        return df_target


@ log_trace
def duplicate_feature(df, config):
    """
    ETL feature to flip sign of amount value with additional duplicated rows
    :param config: dict; Provided feature configuration
    :param df: pd.DataFrame; Provided dataframe
    :return: df_target: pd.DataFrame; Resulted dataframe
    """
    # Split column names into two lists of columns (dtype is float/ not float).
    if not config:
        return df

    else:
        number_col, nonnum_col = [], []
        for col in df.columns:
            if isinstance(df[col][0], float):
                number_col.append(col)
            else:
                nonnum_col.append(col)

        # Add additional rows with sign of amount values flipped, others remain the same.
        for i in df.index:
            df.loc[i + 0.5, number_col] = -df.loc[i, number_col]
            df.loc[i + 0.5, nonnum_col] = df.loc[i, nonnum_col]

        # Sort number index.
        df_target = df.sort_index()

        return df_target








