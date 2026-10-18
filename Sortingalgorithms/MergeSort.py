
def merge(left, right, reverse):
    merged = []
    i = j = 0
    comparisons = 0
    moves = 0

    while i < len(left) and j < len(right):
        comparisons += 1
        
        take_left = left[i] >= right[j] if reverse else left[i] <= right[j]
        
        if take_left:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
        moves += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    
    moves += (len(left) - i) + (len(right) - j)

    return merged, comparisons, moves


def MergeSort(arr, reverse=False):
    if len(arr) <= 1:
        return list(arr), 0, 0

    mid = len(arr) // 2
    left_sorted, left_comp, left_moves = MergeSort(arr[:mid], reverse)
    right_sorted, right_comp, right_moves = MergeSort(arr[mid:], reverse)

    merged, merge_comp, merge_moves = merge(left_sorted, right_sorted, reverse)

    total_comparisons = left_comp + right_comp + merge_comp
    total_moves = left_moves + right_moves + merge_moves

    return merged, total_comparisons, total_moves