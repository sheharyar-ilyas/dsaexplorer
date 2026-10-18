
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

    negative = [-x for x in reversed(negative)]

    sorted_values = negative + positive

    if reverse:
        sorted_values.reverse()

    return sorted_values, comparisons, moves


