
# # Selection Sort

# def SelectionSort(arr):
#     for i in range(len(arr)-1):
#         min_idx = i
#         for j in range(i+1, len(arr)):
#             if arr[min_idx] > arr[j]:
#                 min_idx = j
        
#         arr[min_idx], arr[i] = arr[i], arr[min_idx]
    
#     return arr


def SelectionSort(arr, reverse=False):
    result = list(arr)
    comparisons = 0
    moves = 0
    n = len(result)

    for i in range(n - 1):
        selected = i

        for j in range(i + 1, n):
            comparisons += 1

            if (result[j] < result[selected] and not reverse) or \
               (result[j] > result[selected] and reverse):
                selected = j

        if selected != i:
            result[i], result[selected] = (
                result[selected], result[i]
            )
            moves += 1

    return result, comparisons, moves