def convert_namespace_to_dict(namespace):
    """
    this is a function which can convert a given structure of
    type SimpleNamespace or argparse.Namespace into target structure of type dict
    :param namespace:
    :return: a dictionary
    """
    return vars(namespace)

