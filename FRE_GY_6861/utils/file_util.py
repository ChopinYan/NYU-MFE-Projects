import logging
import pandas as pd
import os


def read(description, path, file_type='excel', separator=',', skip_rows=0, use_cols=None, sheet_name=0):
    """
    Read file, along with validating provided path.
    :param description: str; File description
    :param path: str; Fully qualified file name to read
    :param file_type: str, default='Excel'; Read type with possible values of 'csv' or 'excel'
    :param separator: str, default=','; Values separator
    :param skip_rows: int, default=0; Number of rows to skip
    :param use_cols: int, default=None; A list of columns to read (all others are discarded)
    :param sheet_name: int or str; default=0; A sheet name or index to read
    :return: pd.DataFrame; Resulted dataframe
    """
    df_target = None
    if validate_path(path):
        if file_type.lower() == 'csv':
            # Read csv based file.
            df_target = pd.read_csv(path, sep=separator, skiprows=skip_rows, usecols=use_cols)
        elif file_type.lower() == 'excel':
            # Read Excel based file.
            if len((pd.ExcelFile(path)).sheet_names) > 1:
                df_target = pd.read_excel(path, skiprows=skip_rows, usecols=use_cols, sheet_name=sheet_name)
            else:
                df_target = pd.read_excel(path, skiprows=skip_rows, usecols=use_cols)

    logging.info(f'{description} records <{len(df_target.index)}> were read from <{path}>')
    return df_target


def write(description, df, path, file_type, separator, mode):
    """
    write an Excel file, based on given dataframe
    :param description: str; File description
    :param df: pd.DataFrame; given dataframe ready to be written into a csv or an excel file
    :param path: str; Fully qualified file name to write (maybe modified)
    :param file_type: str, default='Excel'; Read type with possible values of 'csv' or 'excel'
    :param separator: str, default=','; Values separator
    :param mode: str; can either be overwrite or new
    :return:
    """
    # run the function if the path is valid
    if validate_path(path):
        # different method of creating file path with given mode
        if mode == "new":
            new_path = revise_file_path(path)
        elif mode == "overwrite":
            new_path = path
        else:
            logging.error(f'given mode <{mode}> is invalid')
            raise SyntaxError(f'given mode <{mode}> is invalid')

        # write dataframe to the path with given file type
        if file_type.lower() == "csv":
            df.to_csv(new_path, sep=separator, index=False)
            logging.info(f'{description} records <{len(df.index)}> were written to <{path}>')
        elif file_type.lower() == "excel":
            df.to_excel(new_path, index=False)
            logging.info(f'{description} records <{len(df.index)}> were written to <{path}>')
        else:
            logging.error(f'given file type <{file_type}> is invalid')
            raise SyntaxError(f'given file type <{file_type}> is invalid')


def revise_file_path(path):
    """
    revise the file path if it is existing, if not just return the given path
    :param path: str; Fully qualified file path
    :return: str; revised full path of the file
    """
    # define directory name and file name with given path
    directory = os.path.dirname(path)
    file_name = os.path.basename(path)

    # if file do not exists, just use this file path
    if file_name not in os.listdir(directory):
        return path

    # if exists, create new file name for this path:
    else:
        prefix, file_type = os.path.splitext(file_name)
        # if the file name is like x_1 (with a number at the end), new file name should be x_2
        if len(prefix.split('_')[-1]) == 1:
            suffix = eval(prefix.split('_')[-1]) + 1
            new_name = '_'.join(prefix.split('_')[:-1]) + '_' + str(suffix) + file_type
        # if the file nam eis like x (without a number at the end),
        # new file should add a number start with 1 at the end
        else:
            suffix = 1
            new_name = prefix + '_' + str(suffix) + file_type

        # check whether the new name is in the list or not,
        # if exists, continue the process (now the file name already has a number at the end)
        while new_name in os.listdir(directory):
            suffix += 1
            prefix, file_type = os.path.splitext(new_name)
            new_name = '_'.join(prefix.split('_')[:-1]) + '_' + str(suffix) + file_type

        return os.path.join(directory, new_name)


def validate_path(path, path_type="file"):
    """
    Validate provided path.
    :param path_type: str, default='file'; Read type with possible values of 'file' or 'directory'
    :param path: str; Fully qualified path name
    :return: bool; Resulted validation; either true or raise an exception
    """
    if path_type == "file":
        if not os.path.isfile(path):
            logging.error(f'Provided file path is invalid: <{path}>')
            raise FileNotFoundError(f'Provided file path is invalid: <{path}>')

    elif path_type == "directory":
        if not os.path.isdir(path):
            logging.error(f'Provided directory path is invalid: <{path}>')
            raise NotADirectoryError(f'Provided file path is invalid: <{path}>')
    return True


