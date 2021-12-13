# 1 type of tuple elements
def tuple_types(input_tuple):
    result = []
    for i in range(0, len(input_tuple)):
        result.append(type(input_tuple[i]))
    result = tuple(result)
    print(result)


tuple_types(('abc', 3.0, 5))


# 2 remove given element from tuple
def remove_element(input_tuple, element):
    result = list(input_tuple)
    result.remove(element)
    result = tuple(result)
    print(result)


remove_element(('abc', 3.0, 5), 5)


# 3 check for substring availability
def check_containment(input_string, lookup_string):
    if (input_string.count(lookup_string) > 0):
        print('Yes')
    else:
        print('No')


check_containment('New York', 'New')


# 4 reverse given string
def reverse(input_string):
    print(input_string[::-1])


reverse('I love NYC.')


# 5 concatenate 2 list index-wise
def concatenate(list1, list2):
    print(str([i + j for i, j in zip(list1, list2)]))


concatenate(["Do", "i", "be"], ['ta2', 's', 'st'])


# 6 concatenate list of lists
def concatenate_list_of_lists(input_list):
    result = [x for l in input_list for x in l]
    print(result)


concatenate_list_of_lists([[2, 2], [4], [1, 2, 3, 4], [1, 2, 3]])


# 7 remove an element from given list
def remove_element_list(input_list, element):
    input_list.remove(element)
    print(input_list)


remove_element_list([5, 221, 3], 5)

# 8 deep copy of given list
import copy


def deep_copy(input_list):
    result = copy.deepcopy(input_list)
    print(result)


deep_copy([1, 2, 3, 7])


# 9 find all elements with specified key
def find(input_dict):
    list = []
    for key, value in input_dict.items():
        result = []
        if type(value) == dict:
            for key_2, value_2 in value.items():
                result.append(key_2)
                result.append(value_2)
                list.append(result)
        else:
            result_2 = []
            result_2.append(key)
            result_2.append(value)
            list.append(result_2)
    print(tuple(list))


find({'NYC': 10, 'BST': 20, 'TYU': 5, 'LA': {'100': 'Los Angles'}})


# 10 Return the key of min value in given dictionary
def min_value(input_dict):
    print(min(input_dict, key=input_dict.get))


min_value({'NYC': 10, 'BST': 20, 'TYU': 5})
