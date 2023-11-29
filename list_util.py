from collections import Counter, OrderedDict


def sublist_size(lst):
    size = len(lst)
    N = 11
    if size < 22: N = 7
    if size < 14: N = 5
    if size < 7: N = size
    return N


# dividing list into 'sublist_size' sized sublists
def divide_list(lst, sublist_size):
    divided_lists = list()
    sublist = list()

    for item in lst:
        sublist.append(item)

        if len(sublist) == sublist_size:
            divided_lists.append(sublist)
            sublist = list()

    # If there are any remaining elements in the last sublist, add it
    if sublist:
        divided_lists.append(sublist)

    return divided_lists


# finding most common element in the list
def most_common_element(lst):
    # Count the occurrences of each element in the list
    element_counts = Counter(lst)

    # Find the most common element and its count
    most_common = element_counts.most_common(1)
    if most_common:
        most_common_element, count = most_common[0]

        # Create a new list with the most common element repeated 'count' times
        new_list = [most_common_element] * len(lst)
        return new_list
    else:
        # If the list is empty, return an empty list
        return []


# Removing all the insignificant actions
def list_smoothing(lst):
    sub_size = sublist_size(lst)
    div_list = divide_list(lst, sub_size)

    new_action_list = list()
    for sublist in div_list:
        new_action_list.extend(most_common_element(sublist))

    return new_action_list


# Removing duplicate elements (even those present within other elements)
def remove_duplicate(tokens):
    res = list()
    for i in tokens:
        keep = True
        for j in tokens:
            if i != j and i in j:
                keep = False
                break
        if keep: res.append(i)

    return list(OrderedDict.fromkeys(res))