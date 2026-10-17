# # Insertion Sort

# def InsertionSort(arr):
#     shifts = 0   
#     comparisons = 0
#     for i in range(1, len(arr)):
#         key = arr[i]
#         j = i - 1
#         while j >= 0:
#             comparisons += 1  
            
#             if key < arr[j]:
#                 arr[j+1] = arr[j]
#                 shifts += 1
#                 j = j - 1
#             else:
#                 break  
                
#         arr[j+1] = key
#     return arr, comparisons, shifts

# arr = [3, 5, 1, -44, 33, 89]
# print(InsertionSort(arr))

def InsertionSort(arr, reverse=False):
    result = list(arr)
    comparisons = 0
    moves = 0

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            should_shift = (
                result[j] < key if reverse
                else result[j] > key
            )

            if not should_shift:
                break

            result[j + 1] = result[j]
            moves += 1
            j -= 1

        result[j + 1] = key
        moves += 1

    return result, comparisons, moves