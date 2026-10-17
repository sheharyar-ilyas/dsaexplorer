# # Merge Sort

# def MergeSort(arr):

#     if len(arr) <=1:
#         return arr
    
#     mid = len(arr) // 2
#     left_half = arr[:mid]
#     right_half = arr[mid:]

#     left_half = MergeSort(left_half)
#     right_half = MergeSort(right_half)

#     return Merge(left_half, right_half)

# def Merge(left_half, right_half):
#     i, j = 0, 0
#     new = []

#     while i < len(left_half) and j < len(right_half):
#         if left_half[i] < right_half[j]:
#             new.append(left_half[i])
#             i +=1
#         else:
#             new.append(right_half[j])
#             j +=1
    
#     new.extend(left_half[i:])
#     new.extend(right_half[j:])

#     return new


# # arr = [3,2,5,3,11,98,0,-3,-60]
# # print(MergeSort(arr))


def merge(left, right, reverse):
    """Combines two sorted arrays while tracking comparisons and moves."""
    merged = []
    i = j = 0
    comparisons = 0
    moves = 0

    # Step 1: Merge elements in order
    while i < len(left) and j < len(right):
        comparisons += 1
        
        # Determine sorting direction
        take_left = left[i] >= right[j] if reverse else left[i] <= right[j]
        
        if take_left:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
        moves += 1

    # Step 2: Append any remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    # Calculate moves for remaining elements
    moves += (len(left) - i) + (len(right) - j)

    return merged, comparisons, moves


def MergeSort(arr, reverse=False):
    """Recursively splits the array and sums up the total stats."""
    if len(arr) <= 1:
        return list(arr), 0, 0

    # Split the array into halves
    mid = len(arr) // 2
    left_sorted, left_comp, left_moves = MergeSort(arr[:mid], reverse)
    right_sorted, right_comp, right_moves = MergeSort(arr[mid:], reverse)

    # Merge the sorted halves together
    merged, merge_comp, merge_moves = merge(left_sorted, right_sorted, reverse)

    # Accumulate all counts from the splits and the merge
    total_comparisons = left_comp + right_comp + merge_comp
    total_moves = left_moves + right_moves + merge_moves

    return merged, total_comparisons, total_moves