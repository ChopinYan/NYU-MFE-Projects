import argparse
import json
import logging
import os
import sys
from types import SimpleNamespace as Namespace

import fall2021py.utils.etl_util as etlu
import fall2021py.utils.misc_util as miscu


RETURN_SUCCESS = 0
RETURN_FAILURE = 1
APP = 'FlowData utility'


def main(argv):
    try:
        # Parse command line arguments.
        args, process_name, process_type, process_config = _interpret_args(argv)

        # Initialize standard logging \ destination file handlers.
        # TODO: Finish/fix logging below.
        std_filename = ".\\fall2021py\\flowdata.log"
        logging.basicConfig(filename=std_filename, filemode='a',
                            format='%(asctime)s - %(message)s', level=logging.DEBUG)
        logging.info('')
        logging.info(f'Entering {APP}')

        # Preparation step.
        # TODO: Change below initializations to be conversion
        #  from Namespace to dict (args, feature_config).
        mapping_args = miscu.convert_namespace_to_dict(args)  # dictionary (input of run_extraction())
        mapping_conf = miscu.convert_namespace_to_dict(process_config)

        # Workflow steps.
        if process_type == 'extraction':
            run_extraction(mapping_args, mapping_conf)
        elif process_type == 'transformation':
            run_transformation(mapping_args, mapping_conf)
        else:
            logging.warning(f'Incorrect feature type: [{process_type}]')

        logging.info(f'Leaving {APP}')
        return RETURN_SUCCESS
    except FileNotFoundError as nf_error:
        logging.error(f'Leaving {APP} incomplete with errors')
        return f'ERROR: {str(nf_error)}'
    except KeyError as key_error:
        logging.error(f'Leaving {APP} incomplete with errors')
        return f'ERROR: {key_error.args[0]}'
    except Exception as gen_exc:
        logging.error(f'Leaving {APP} incomplete with errors')
        raise gen_exc


def _interpret_args(argv):
    """
    Read, parse, and interpret given command line arguments.
    Also, define default value.
    :param argv: Given argument parameters.
    :return: Full mapping of arguments, including all default values.
    """
    arg_parser = argparse.ArgumentParser(APP)
    arg_parser.add_argument('-log', dest='log_path', help='Fully qualified logging file')
    arg_parser.add_argument('-process', dest='process', help='Process type', required=True)

    # Extract and interpret rest of the arguments, using static config file, based on given specific feature.
    process_arg = argv[argv.index('-process') + 1]
    process_args = process_arg.rsplit('_', 1)
    process_name = process_args[0]
    process_type = process_args[1]
    current_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(current_path, f'..\\config\\{process_name}.json')) as file_config:
        mapping_config = json.load(file_config, object_hook=lambda d: Namespace(**d))
        if process_type == 'extraction':
            process_config = vars(mapping_config.extraction)
        elif process_type == 'transformation':
            process_config = vars(mapping_config.transformation)

        feature_args = vars(mapping_config.feature_args)
        # Add necessary arguments to <arg_parser> instance, using static JSON-based configuration.
        if feature_args:
            for key, value in feature_args.items():
                if isinstance(value, Namespace):
                    value = vars(value)
                arg_parser.add_argument(key, dest=value['dest'], help=value['help'], required=value['required'])
    return arg_parser.parse_args(argv), process_name, process_type, process_config


@ miscu.log_trace
def run_extraction(args, config):

    # --------------------------------
    # Input section
    # --------------------------------

    # Prepare additional input parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <input> config section.
    input_update_with = {'path': miscu.eval_elem_mapping(args, 'input_path'), 'description': config['description']}
    input_config = miscu.eval_elem_mapping(config, 'input')
    # 'input' -- 'read' feature in the configuration json file
    # for example
    # {'file_type': 'csv',
    #  'separator': ',',
    #  'apply_dtype': {'Date': 'str',
    #                  'Open': 'float',
    #                  'High': 'float',
    #                  'Low': 'float',
    #                  'Close': 'float',
    #                  'stk_code': 'str'},
    #  'path': 'D:\\常用\\NYU\\2021Fall\\Course\\FRE-GY 6861\\fall2021py\\data\\stock_extraction_input.csv',
    #  'description': 'POTUS Account'}
    input_read_config = miscu.eval_update_mapping(input_config, "read", input_update_with)

    # Run read ETL feature.
    df_target = etlu.read_feature(input_read_config)

    # Engage plugin from <input> config section, if available.
    input_plugin = miscu.eval_elem_mapping(input_config, "plugin")
    if input_plugin:
        df_target = input_plugin(df_target)

    # --------------------------------
    # Mapping section
    # --------------------------------

    # Prepare additional mapping parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <mapping> config section.
    mapping_update_with = {'path': miscu.eval_elem_mapping(args, 'mapping_path'), 'description': config['description']}
    mapping_config = miscu.eval_elem_mapping(config, 'mapping')
    # this is a config with values under key 'read', together with values under key 'path' and 'description'
    # for example
    # {'file_type': 'excel',
    #  'skip_rows': 0,
    #  'use_cols': 'A,B',
    #  'sheet_name': 0,
    #  'apply_dtype': {'INS': 'str', 'INS_ACCOUNT': 'str'},
    #  'path': 'D:\\常用\\NYU\\2021Fall\\Course\\FRE-GY 6861\\fall2021py\\data\\sergefeldman_extraction_mapping.csv',
    #  'description': 'serge'}
    # this function will automatically update values of key 'read' under original dictionary
    mapping_read_config = miscu.eval_update_mapping(mapping_config, 'read', mapping_update_with)

    # Run mapping ETL feature.
    # still use the mapping_config as it includes updated dict under key 'read'
    # and other key-value pairs like 'left on' for merge function
    # for example
    # {'read': {'file_type': 'excel',
    #           'skip_rows': 0,
    #           'use_cols': 'A,B',
    #           'sheet_name': 0,
    #           'apply_dtype': {'INS': 'str', 'INS_ACCOUNT': 'str'},
    #           'path': 'D:\\常用\\NYU\\2021Fall\\Course\\FRE-GY 6861\\fall2021py\\
    #                    data\\sergefeldman_extraction_mapping.csv',
    #           'description': 'serge'},
    #  'left_on': ['INS_CODE'],
    #  'right_on': ['INS'],
    #  'plugin': None}
    # which can be used for function mapping_feature()
    df_target = etlu.mapping_feature(df_target, mapping_config)

    # --------------------------------
    # Output section
    # --------------------------------

    # TODO: Implement and complete this section with the following steps:

    # TODO: Prepare additional output parameters and update appropriate configuration section.
    #  add configuration 'write' to json file
    #  and enhance write_feature() under etl_util.py (write() should be used from file_util.py)

    # TODO: Inject 'path' and 'description' into <output> config section.
    output_update_with = {'path': miscu.eval_elem_mapping(args, 'output_path'), 'description': config['description']}
    output_config = miscu.eval_elem_mapping(config, 'output')
    # update original configuration with updated configuration 'write'
    output_write_config = miscu.eval_update_mapping(output_config, 'write', output_update_with)

    # TODO: Run write ETL feature.
    etlu.write_feature(df_target, output_config)

    return df_target


@ miscu.log_trace
def run_transformation(args, config):
    """
    Transformation process
    :param args: dict; Command line arguments mapping
    :param config: dict; Configuration mapping
    :return: null
    """

    # --------------------------------
    # Input section
    # --------------------------------

    # Extract normalized data source (output of Extraction process)

    # --------------------------------
    # Aggregate section
    # --------------------------------

    # Run aggregate ETL feature to sum AMOUNT column, grouping by the combination of EXT_ACCOUNT, MAP_ACCOUNT, TYPE.

    # --------------------------------
    # Assignment section
    # --------------------------------

    # Run assignment ETL feature (as per requirements).

    # --------------------------------
    # Duplication section
    # --------------------------------

    # Run duplicate ETL feature (as per requirements).
    # Sign of Amount value of duplicated row will be flipped

    # --------------------------------
    # Output section
    # --------------------------------

    # --------------------------------
    # Rearrange section
    # --------------------------------

    # Run rearrange ETL feature.

    # Engage plugin from <output> config section.
    # Our plugin will add Total Amount value.

    # Run write ETL feature.


if __name__ == '__main__':
    # Call main process.
    sys.exit(main(sys.argv[1:]))
    # command
    # python. / flowdata.py - process sergefeldman_extraction - log
    # c:\temp\flowdata.log - input
    # c:\download\git\fall2021\data\sergefeldman_extaction.csv - mapping
    # c:\download\git\fall2021\data\sergefeldman_mapping.csv - output
    # c:\download\git\fall2021\data\sergefeldman_output.csv

    # python -m fall2021py.apps.flowdata.src.flowdata -process potus_extraction -log D:\常用\NYU\2021Fall\Course\FRE-GY_6861\fall2021py\flowdata.log -input D:\常用\NYU\2021Fall\Course\FRE-GY_6861\fall2021py\data\potus_extraction_input.csv -mapping D:\常用\NYU\2021Fall\Course\FRE-GY_6861\fall2021py\data\potus_extraction_mapping.xlsx -output D:\常用\NYU\2021Fall\Course\FRE-GY_6861\fall2021py\data\potus_extraction_output.xlsx
