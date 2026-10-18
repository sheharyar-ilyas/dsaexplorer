
def CountingSort(arr, reverse=False):
    result = list(arr)
    comparisons = 0
    moves = 0

    if not result:
        return result, comparisons, moves

    if any(not isinstance(x, int) or isinstance(x, bool)
           for x in result):
        raise ValueError("Counting Sort requires integer values.")

    minimum = min(result)
    maximum = max(result)
    value_range = maximum - minimum + 1

    if value_range > max(1_000_000, len(result) * 100):
        raise ValueError(
            "Counting Sort is unsuitable for this large value range. "
            "Choose Merge Sort or Quick Sort instead."
        )

    count = [0] * value_range

    for value in result:
        count[value - minimum] += 1
        moves += 1

    sorted_values = []

    indexes = range(value_range - 1, -1, -1) if reverse \
        else range(value_range)

    for index in indexes:
        value = index + minimum

        for _ in range(count[index]):
            sorted_values.append(value)
            moves += 1

    return sorted_values, comparisons, moves