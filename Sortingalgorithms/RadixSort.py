# # Radix Sort

# def RadixSort(arr):
#     if len(arr) <= 1:
#         return arr

#     negative = []
#     positive = []

#     for num in arr:
#         if num < 0:
#             negative.append(abs(num))
#         else:
#             positive.append(num)

#     if len(negative) > 0:
#         maximum_element = max(negative)
#         place = 1

#         while maximum_element // place > 0:
#             CountingSortForRadix(negative, place)
#             place *= 10

#         negative.reverse()

#         for i in range(len(negative)):
#             negative[i] = -negative[i]

#     if len(positive) > 0:
#         maximum_element = max(positive)
#         place = 1

#         while maximum_element // place > 0:
#             CountingSortForRadix(positive, place)
#             place *= 10

#     arr[:] = negative + positive

#     return arr


# def CountingSortForRadix(arr, place):
#     size = len(arr)

#     output = [0] * size
#     count = [0] * 10

#     for i in range(size):
#         index = arr[i] // place
#         count[index % 10] += 1

#     for i in range(1, 10):
#         count[i] += count[i - 1]

#     i = size - 1

#     while i >= 0:
#         index = arr[i] // place
#         output[count[index % 10] - 1] = arr[i]
#         count[index % 10] -= 1
#         i -= 1

#     for j in range(size):
#         arr[j] = output[j]

#     return arr


# # arr1 = [110, -45, 65, 50, -90, 602, 24, -2, 66]

# # print(RadixSort(arr1))


def RadixSort(arr, reverse=False):
    result = list(arr)
    comparisons = 0
    moves = 0

    if not result:
        return result, comparisons, moves

    if any(not isinstance(x, int) or isinstance(x, bool)
           for x in result):
        raise ValueError("Radix Sort requires integer values.")

    def sort_non_negative(values):
        nonlocal moves

        if not values:
            return []

        output = values[:]
        place = 1
        maximum = max(output)

        while maximum // place > 0:
            count = [0] * 10
            temporary = [0] * len(output)

            for value in output:
                digit = (value // place) % 10
                count[digit] += 1

            for i in range(1, 10):
                count[i] += count[i - 1]

            for i in range(len(output) - 1, -1, -1):
                digit = (output[i] // place) % 10
                temporary[count[digit] - 1] = output[i]
                count[digit] -= 1
                moves += 1

            output = temporary
            place *= 10

        return output

    negative = [-x for x in result if x < 0]
    positive = [x for x in result if x >= 0]

    negative = sort_non_negative(negative)
    positive = sort_non_negative(positive)

    # Larger absolute negative values represent smaller numbers.
    negative = [-x for x in reversed(negative)]

    sorted_values = negative + positive

    if reverse:
        sorted_values.reverse()

    return sorted_values, comparisons, moves