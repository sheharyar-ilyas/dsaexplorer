
import sys
sys.setrecursionlimit(20000)

def QuickSort(arr, reverse=False):
    result = list(arr)
    comparisons = 0
    moves = 0

    def quick_sort(low, high):
        nonlocal comparisons, moves

        if low >= high:
            return

        pivot = result[high]
        i = low - 1

        for j in range(low, high):
            comparisons += 1

            condition = (
                result[j] >= pivot if reverse
                else result[j] <= pivot
            )

            if condition:
                i += 1

                if i != j:
                    result[i], result[j] = result[j], result[i]
                    moves += 1

        pivot_index = i + 1

        if pivot_index != high:
            result[pivot_index], result[high] = (
                result[high], result[pivot_index]
            )
            moves += 1

        quick_sort(low, pivot_index - 1)
        quick_sort(pivot_index + 1, high)

    quick_sort(0, len(result) - 1)

    return result, comparisons, moves