def sort(array):
    if len(array) >= 2:

        at_least_one_switch = True
        max_index = len(array) - 1

        while at_least_one_switch:
            at_least_one_switch = False

            for i in range(max_index):
                if array[i] > array[i + 1]:
                    array[i], array[i + 1] = array[i + 1], array[i]
                    at_least_one_switch = True

            max_index -= 1

    return array


print sort([1, 2, -4, 0, 6, 12, 0, 1, 3])
