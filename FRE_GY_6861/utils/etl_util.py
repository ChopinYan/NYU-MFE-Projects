import pandas as pd
from datetime import datetime

import fall2021py.utils.file_util as fileu
import fall2021py.utils.misc_util as miscu


@ miscu.log_trace
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


@ miscu.log_trace
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


@ miscu.log_trace
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


@ miscu.log_trace
def write_feature(df, config):
    """
    ETL feature to write merged dataframe to the specified file
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return:
    """
    # rename columns and assign static columns if configuration exists
    if miscu.eval_elem_mapping(config, 'col_rename'):
        df = rename_feature(df, config)
    if miscu.eval_elem_mapping(config, 'assign_static'):
        df = assign_static_feature(df, config)

    # then write function to the file
    write_config = miscu.eval_elem_mapping(config, 'write')
    fileu.write(description=miscu.eval_elem_mapping(write_config, 'description'),
                df=df,
                path=miscu.eval_elem_mapping(write_config, 'path'),
                file_type=miscu.eval_elem_mapping(write_config, 'file_type', default_value='excel'),
                separator=miscu.eval_elem_mapping(write_config, 'separator', default_value=','),
                mode=miscu.eval_elem_mapping(write_config, 'mode', default_value='new'))


@ miscu.log_trace
def rename_feature(df, config):
    """
    ETL feature to rename column name of given dataframe
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: pd.DataFrame; dataframe with renamed columns
    """
    # TODO: create col_rename feature
    #  renew dataframe depends on col_rename and other configuration instructions
    rename_config = miscu.eval_elem_mapping(config, 'col_rename')
    if rename_config and isinstance(rename_config, dict):
        df = df.rename(columns=rename_config)
    return df


@ miscu.log_trace
def assign_static_feature(df, config):
    """
    ETL feature to assign static unit for specified columns
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: pd.DataFrame; dataframe with assigned static columns
    """
    assign_static_config = miscu.eval_elem_mapping(config, 'assign_static')
    if assign_static_config and isinstance(assign_static_config, dict):
        for assign_name, assign_unit in assign_static_config.items():
            df[assign_name] = assign_unit
    return df


def aggregation_feature(df, config):
    """
    ETL feature to aggregate the given dataframe including group by and pivot table
    In this case, aggregating are used to see the average position of customer's assets
    :param df: pd.DataFrame; output dataframe from extraction part
    :param config: dict; Provided feature configuration
    :return: pd.DataFrame; aggregated dataframe
    """
    # pivot_table version
    # pd.pivot_table(df, values=['CLOSE', 'POSITION'], index=['CUSTOMER'],
    # columns=['TICKER'], aggfunc=np.mean)

    # groupby version
    # df.groupby(["CUSTOMER", "TICKER"])["CLOSE", "POSITION"].mean().unstack()




