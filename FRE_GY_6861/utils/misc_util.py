from argparse import Namespace as ArgNamespace
import importlib
from types import SimpleNamespace
from inspect import signature
import logging


INDENTATION = 0
FUNCTION_NAME = None


def log_trace(func):
    """
    function decorator
    :param func: function
    :return:
    """
    def wrapper(*args, **kwargs):
        global INDENTATION
        global FUNCTION_NAME
        if FUNCTION_NAME != func.__name__:
            INDENTATION += 4
            logging.info(" " * INDENTATION + f'Entering Function: {func.__name__} '
                                             f'with argument {str(signature(func))}')
        output = func(*args, **kwargs)
        if FUNCTION_NAME != func.__name__:
            logging.info(" " * INDENTATION + f'Leaving Function: {func.__name__}')
            INDENTATION -= 4
        FUNCTION_NAME = func.__name__
        return output
    return wrapper


@ log_trace
def convert_namespace_to_dict(mapping):
    """
    Recursively convert given mapping of type SimpleNamespace or argparse.Namespace into dict
    :param mapping: SimpleNamespace or argparse.Namespace; Provided mapping
    :return: dict; Converted mapping of type dict
    """
    if isinstance(mapping, SimpleNamespace) or isinstance(mapping, ArgNamespace):
        mapping_target = vars(mapping)
    else:
        mapping_target = mapping

    # Make recursive call.
    if isinstance(mapping_target, dict):
        for (key, value) in mapping_target.items():
            mapping_target[key] = convert_namespace_to_dict(value)

    return mapping_target


@ log_trace
def eval_elem_mapping(mapping, key, default_value=None):
    """
    Evaluate given mapping and returns value element, based on provided key
    :param mapping: dict; Provided mapping
    :param key: int or str; Provided key
    :param default_value: int or str; default=None; Default value
    :return: Resulted mapping value
    """
    value_target = mapping[key] if isinstance(mapping, dict) and key in mapping else default_value
    return value_target if value_target else default_value


@ log_trace
def eval_func(mapping, func_key):
    """
    Extract function name from configuration mapping and construct function / callable object
    :param mapping: dict; Provided mapping
    :param func_key: int or str; Provided key
    :return: Resulted function object
    """
    func_target = None
    if func_key in mapping and mapping[func_key]:
        module_name, func_name = mapping[func_key].rsplit(".", 1)
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, func_name):
                func_target = getattr(module, func_name)
        except Exception:
            pass

    return func_target


@ log_trace
def eval_func2(mapping, func_key):
    """
    Extract function name from configuration mapping and construct function / callable object
    :param mapping: dict; Provided mapping
    :param func_key: int or str; Provided key
    :return: Resulted function object
    """
    func_target = None
    if func_key in mapping and mapping[func_key]:
        func_target = eval(mapping[func_key])

    return func_target


@ log_trace
def eval_update_mapping(mapping, key, update_with):
    """
    Evaluate given mapping and if an element of dict type exists, update it with provided parameter.
    :param mapping: dict; Provided mapping
    :param key: int or str; Provided key
    :param update_with: dict; Provided dict to update with
    :return: Resulted mapping
    """
    mapping_target = eval_elem_mapping(mapping, key, dict())
    if mapping_target:
        if isinstance(mapping_target, dict) and update_with and isinstance(update_with, dict):
            mapping_target.update(update_with)
    return mapping_target
