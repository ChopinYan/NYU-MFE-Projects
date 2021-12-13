import copy


# Tuple
def tuple_types(input_tuple):
    """
    checks every element of given tuple and reports back on its type;
    :param input_tuple: a tuple
    :return: type
    """
    return tuple(type(element) for element in input_tuple)


def remove_element_tuple(input_tuple, element):
    """
    removes an element from given tuple;
    :param input_tuple: a tuple
    :param element: a specific element we want to remove
    :return: renewed tuple
    """
    index = input_tuple.index(element)
    return input_tuple[:index] + input_tuple[index + 1:]


# String
def check_containment(input_string, lookup_string):
    """
    checks for substring availability in given string
    :param input_string: given string
    :param lookup_string: substring
    :return: boolean whether substring is in the given string
    """
    return lookup_string in input_string


def reverse(input_string):
    """
    reverses given string
    :param input_string: given string
    :return: reversed string
    """
    return input_string[::-1]


# List
def concatenate(list1, list2):
    """
    concatenates two lists index-wise
    :param list1:
    :param list2:
    :return: concatenated list
    """
    # if two lists are of different length only return the joint one
    return [(m, n) for m, n in zip(list1, list2)]


def flatten(input_nested):
    """
    flatten the nested lists or tuples
    :param input_nested:
    :return:
    """
    for single_element in input_nested:
        if not isinstance(single_element, (list, tuple)):
            yield single_element
        else:
            yield from flatten(single_element)


def concatenate_list_of_lists(input_list):
    """
    the argument to the function is the list of lists;
    concatenate all list elements index-wise
    :param input_list: a list of lists
    :return: concatenated list
    """
    concat_list = input_list[0]
    for single_list in input_list[1:]:
        concat_list = concatenate(concat_list, single_list)

    for i in range(len(concat_list)):
        concat_list[i] = tuple(flatten(concat_list[i]))

    return concat_list


def remove_element_list(input_list, element):
    """
    removes an element from given
    :param input_list: given list
    :param element: specific element we want to remove
    :return: revised list
    """
    if element in input_list:
        input_list.remove(element)
        # recursive operation if element given is duplicated
        remove_element_list(input_list, element)
    return input_list


def deep_copy(input_list):
    """
    does the deep copy of given list
    :param input_list:
    :return: deep copy
    """
    return copy.deepcopy(input_list)


# Dictionary
def find(input_dict, input_key):
    """
    find all elements with specified key;
    make sure to account for the case where given dictionary is a dict of dicts;
    this function should traverse all elements of inner dict elements;
    function returns resulted tuple of key, value pairs or such elements
    :param input_key:
    :param input_dict:
    :return:
    """
    temp_list = []
    # if outer key: just return the value
    if input_key in input_dict.keys():
        temp_list.append(input_dict[input_key])

    # if not: check values (inner dictionary)
    for value in input_dict.values():
        # if value is a dictionary, recurse into more inner values
        if isinstance(value, dict):
            temp_list.append(find(value, input_key))

    return temp_list


def min_value(input_dict):
    """
    returns the key, corresponding to the min value from given dictionary
    :param input_dict:
    :return: the key of minimum value
    """
    for key, value in input_dict.items():
        if value == min(input_dict.values()):
            return key


def main():
    """ test """
    # tuple test
    tuple_test = (10.0, [10.0], 10, {"value": 10})
    print(tuple_types(tuple_test))
    print(remove_element_tuple(tuple_test, [10.0]))

    # string test
    string_test = "Hello World!"
    string_lkup = "Hello"
    print(check_containment(string_test, string_lkup))
    print(reverse(string_test))

    # list test
    list_fst, list_scd = [1, 2, 3], [3, 4, 5, 6]
    list_of_lists = [[1, 2, 3, 4], [3, 6], [7, 8, 9]]
    print(concatenate(list_fst, list_scd))
    print(concatenate_list_of_lists(list_of_lists))
    print(remove_element_list(list_fst, 2))
    print(deep_copy(list_fst))
    print("Is the id address of initial list "
          "the same as the deep copied one? %s"
          % str(id(list_fst) == id(deep_copy(list_fst))))

    # dictionary test
    dict_fst = {"a": 1, "b": 2, "c": {"d": 3, "e": 4}}
    print(f"the value of given key is {find(dict_fst, 'e')}")
    dict_scd = {"a": 1, "b": 2, "c": 5}
    print(f"the key of the minimum value is {min_value(dict_scd)}")


if __name__ == "__main__":
    main()
