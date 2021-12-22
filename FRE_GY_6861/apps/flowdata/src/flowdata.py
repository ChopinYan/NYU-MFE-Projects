import argparse
import json
import logging
import os
import sys
from types import SimpleNamespace as Namespace

import fall2021py.utils.etl_util as etlu
import fall2021py.utils.misc_util as miscu
from fall2021py.utils.misc_util import log_trace
# import fall2021py.apps.flowdata.src.plugin_util


RETURN_SUCCESS = 0
RETURN_FAILURE = 1
APP = 'FlowData utility'


def main(argv):
    try:
        # Parse command line arguments.
        args, process_name, process_type, process_config = _interpret_args(argv)

        # Initialize standard logging \ destination file handlers.
        if args.log_path:
            std_filename = args.log_path
        else:
            std_filename = ".\\fall2021py\\flowdata.log"

        logging.basicConfig(filename=std_filename, filemode='a',
                            format='%(asctime)s - %(message)s', level=logging.DEBUG)
        logging.info('')
        logging.info(f'Entering {APP}')

        # Preparation step.
        mapping_args = miscu.convert_namespace_to_dict(args)
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


@ log_trace
def run_extraction(args, config):
    """
    Extraction process
    :param args: dict; Command line arguments mapping
    :param config: dict; Configuration mapping
    :return: null
    """

    # --------------------------------
    # Input section
    # --------------------------------

    # Prepare additional input parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <input> config section.
    input_update_with = {'path': miscu.eval_elem_mapping(args, 'input_path'), 'description': config['description']}
    input_config = miscu.eval_elem_mapping(config, 'input')
    input_read_config = miscu.eval_update_mapping(input_config, "read", input_update_with)

    # Run read ETL feature.
    df_target = etlu.read_feature(input_read_config)

    # Engage plugin from <input> config section, if available.
    input_plugin = miscu.eval_func(input_config, "plugin")
    if input_plugin:
        df_target = input_plugin(df_target)

    # --------------------------------
    # Mapping section
    # --------------------------------

    # Prepare additional mapping parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <mapping> config section.
    mapping_update_with = {'path': miscu.eval_elem_mapping(args, 'mapping_path'), 'description': config['description']}
    mapping_config = miscu.eval_elem_mapping(config, 'mapping')
    mapping_read_config = miscu.eval_update_mapping(mapping_config, 'read', mapping_update_with)

    # Run mapping ETL feature.
    df_target = etlu.mapping_feature(df_target, mapping_config)

    # Engage plugin from <mapping> config section, if available.
    mapping_plugin = miscu.eval_func(mapping_config, "plugin")
    if mapping_plugin:
        df_target = mapping_plugin(df_target)

    # --------------------------------
    # Assignment section
    # --------------------------------

    # Prepare assign_var configuration section, by getting values from args configuration.
    # assign_config = miscu.eval_elem_mapping(config, 'assign')
    # assign_config_var = miscu.eval_elem_mapping(assign_config, 'col_var')
    # assign_update_with = dict()
    # for col_name, args_key in assign_config_var.items():
    #     assign_update_with[col_name] = args[args_key]
    # assign_config_var = miscu.eval_update_mapping(assign_config, 'col_var', assign_update_with)
    #
    # # Run assignment ETL feature.
    # df_target = etlu.assign_feature(df_target, assign_config)
    #
    # # Engage plugin from <assign> config section, if available.
    # assign_plugin = miscu.eval_func(assign_config, "plugin")
    # if assign_plugin:
    #     df_target = assign_plugin(df_target)

    # --------------------------------
    # Output section
    # --------------------------------

    # Prepare additional output parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <output> config section.
    output_update_with = {'path': miscu.eval_elem_mapping(args, 'output_path'), 'description': config['description']}
    output_config = miscu.eval_elem_mapping(config, 'output')
    output_write_config = miscu.eval_update_mapping(output_config, 'write', output_update_with)

    # --------------------------------
    # Rearrange section
    # --------------------------------

    # Run rearrange ETL feature.
    rearrange_config = miscu.eval_elem_mapping(output_config, 'rearrange')
    df_target = etlu.rearrange_feature(df_target, rearrange_config)

    # Engage plugin from <output> config section, if available.
    output_plugin = miscu.eval_func(output_config, "plugin")
    if output_plugin:
        df_target = output_plugin(df_target)

    # Run write ETL feature.
    etlu.write_feature(df_target, output_write_config)


@ log_trace
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
    input_update_with = {'path': miscu.eval_elem_mapping(args, 'input_path'), 'description': config['description']}
    input_config = miscu.eval_elem_mapping(config, 'input')
    input_read_config = miscu.eval_update_mapping(input_config, "read", input_update_with)

    # Run read ETL feature.
    df_target = etlu.read_feature(input_read_config)

    # Engage plugin from <input> config section, if available.
    input_plugin = miscu.eval_func(input_config, "plugin")
    if input_plugin:
        df_target = input_plugin(df_target)

    # --------------------------------
    # Aggregate section
    # --------------------------------

    # Run aggregate ETL feature to sum AMOUNT column, grouping by the combination of EXT_ACCOUNT, MAP_ACCOUNT, TYPE.
    aggregate_config = miscu.eval_elem_mapping(config, 'aggregate')
    df_target = etlu.aggregate_feature(df_target, aggregate_config)

    # Engage plugin from <aggregate> config section, this plugin is used for calculating total assets.
    aggregate_plugin = miscu.eval_elem_mapping(aggregate_config, "plugin")
    aggregate_plugin_module = miscu.eval_func(aggregate_plugin, "module")
    if aggregate_plugin_module:
        df_target = aggregate_plugin_module(df_target, aggregate_plugin)

    # --------------------------------
    # Assignment section
    # --------------------------------

    # Run assignment ETL feature (as per requirements).
    # Prepare assign_var configuration section, by getting values from args configuration.
    assign_config = miscu.eval_elem_mapping(config, 'assign')
    assign_config_var = miscu.eval_elem_mapping(assign_config, 'col_var')
    assign_update_with = dict()
    for col_name, args_key in assign_config_var.items():
        assign_update_with[col_name] = args[args_key]
    assign_config_var = miscu.eval_update_mapping(assign_config, 'col_var', assign_update_with)

    # Run assignment ETL feature.
    df_target = etlu.assign_feature(df_target, assign_config)

    # Engage plugin from <assign> config section, if available.
    assign_plugin = miscu.eval_elem_mapping(assign_config, "plugin")
    assign_plugin_module = miscu.eval_func(assign_plugin, "module")
    if assign_plugin_module:
        df_target = assign_plugin_module(df_target, assign_plugin)

    # --------------------------------
    # Duplication section
    # --------------------------------

    # Run duplicate ETL feature (as per requirements).
    # Sign of Amount value of duplicated row will be flipped
    duplicate_config = miscu.eval_elem_mapping(config, 'duplicate')
    df_target = etlu.duplicate_feature(df_target, duplicate_config)

    # --------------------------------
    # Output section
    # --------------------------------

    # Prepare additional output parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <output> config section.
    output_update_with = {'path': miscu.eval_elem_mapping(args, 'output_path'),
                          'description': config['description']}
    output_config = miscu.eval_elem_mapping(config, 'output')
    output_write_config = miscu.eval_update_mapping(output_config, 'write', output_update_with)

    # --------------------------------
    # Rearrange section
    # --------------------------------

    # Run rearrange ETL feature.
    rearrange_config = miscu.eval_elem_mapping(output_config, 'rearrange')
    df_target = etlu.rearrange_feature(df_target, rearrange_config)

    # Engage plugin from <output> config section, if available.
    # Our plugin will add Total Amount value.
    output_plugin = miscu.eval_func(output_config, "plugin")
    if output_plugin:
        df_target = output_plugin(df_target)

    # Run write ETL feature.
    etlu.write_feature(df_target, output_write_config)


if __name__ == '__main__':
    # Call main process.
    sys.exit(main(sys.argv[1:]))

    # command
    # python. / flowdata.py - process sergefeldman_extraction - log
    # c:\temp\flowdata.log - input
    # c:\download\git\fall2021\data\sergefeldman_extaction.csv - mapping
    # c:\download\git\fall2021\data\sergefeldman_mapping.csv - output
    # c:\download\git\fall2021\data\sergefeldman_output.csv

    # extraction
    # python - m
    # fall2021py.apps.flowdata.src.flowdata - process
    # potus_extraction - log
    # fall2021py\flowdata.log - input
    # fall2021py\data\potus_extraction_input.csv - mapping
    # fall2021py\data\potus_extraction_mapping.xlsx - output
    # fall2021py\data\potus_extraction_output.xlsx

    # transformation
    # python - m
    # fall2021py.apps.flowdata.src.flowdata - process
    # potus_transformation - log
    # fall2021py\flowdata.log - input
    # fall2021py\data\potus_extraction_output_6.xlsx - mapping
    # fall2021py\data\potus_extraction_mapping.xlsx - output
    # fall2021py\data\potus_transformation_output.xlsx - run_date
    # "2021-12-18" - description
    # "transformation test"
