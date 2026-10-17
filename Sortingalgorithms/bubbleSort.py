
# # BubbleSort
# def BubbleSort(arr):
#     for i in range(len(arr) - 1):
#         flag = False
#         for j in range(len(arr)-1 - i):
#             if arr[j] > arr[j+1]:
#                 arr[j] , arr[j+1] = arr[j+1], arr[j]
#                 flag = True
#         if flag == False:
#             break

#     return arr


# arr = [2,5,3,2,2,-22,0,5,3,3]
# print(BubbleSort(arr))
    

def BubbleSort(arr, reverse=False):
    result = list(arr)
    comparisons = 0
    moves = 0
    n = len(result)

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            comparisons += 1

            if (result[j] > result[j + 1] and not reverse) or \
               (result[j] < result[j + 1] and reverse):

                result[j], result[j + 1] = (
                    result[j + 1], result[j]
                )
                moves += 1
                swapped = True

        if not swapped:
            break

    return result, comparisons, moves