# noinspection DuplicatedCode
def _merge_sort_in_place(lst: list):
    lst_len = len(lst)
    if lst_len < 2:  # if a list is empty or 1 element long
        return

    lst_sep = lst_len // 2  # the list is split in two
    left = lst[:lst_sep]
    right = lst[lst_sep:]
    left_len = len(left)
    right_len = len(right)

    # the above splitting keeps going until the lists are 1 element long
    _merge_sort_in_place(left)
    _merge_sort_in_place(right)

    i, j, k = 0, 0, 0

    while i < left_len and j < right_len:
        left_val = left[i]
        right_val = right[j]
        if left_val < right_val:
            lst[k] = left_val
            i += 1
        else:
            lst[k] = right_val
            j += 1
        k += 1

    while i < left_len:
        lst[k] = left[i]
        i += 1
        k += 1

    while j < right_len:
        lst[k] = right[j]
        j += 1
        k += 1


# noinspection DuplicatedCode
def _merge_sort_new(lst: list):
    lst_len = len(lst)
    if lst_len < 2:
        return lst

    sorted_lst = [0] * lst_len
    lst_sep = lst_len // 2

    left = lst[:lst_sep]
    right = lst[lst_sep:]
    left_len = len(left)
    right_len = len(right)

    left_sorted = _merge_sort_new(lst[:lst_sep])
    right_sorted = _merge_sort_new(lst[lst_sep:])

    i, j, k = 0, 0, 0

    while i < left_len and j < right_len:
        left_val = left_sorted[i]
        right_val = right_sorted[j]

        if left_val < right_val:
            sorted_lst[k] = left_val
            i += 1
        else:
            sorted_lst[k] = right_val
            j += 1
        k += 1

    while i < left_len:
        sorted_lst[k] = left_sorted[i]
        i += 1
        k += 1

    while j < right_len:
        sorted_lst[k] = right_sorted[j]
        j += 1
        k += 1

    return sorted_lst


def merge_sort(lst: list, in_place=False):
    if in_place:
        _merge_sort_in_place(lst)
    else:
        return _merge_sort_new(lst)
