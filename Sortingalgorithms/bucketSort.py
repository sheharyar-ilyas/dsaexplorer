# # Bucket Sort

# # For sorting in buckets we use the insertion sort
# def InsertionSort(arr):
#     for i in range(1, len(arr)):
#         key = arr[i]
#         j = i - 1
#         while j >= 0 and key < arr[j]:
#             arr[j+1] = arr[j]
#             j = j - 1  
                
#         arr[j+1] = key
#     return arr

# def BucketSort(arr):
#     if len(arr) <= 1:
#         return arr

#     n = len(arr)
#     bucket = []

#     for i in range(n):
#         bucket.append([])

#     max_val = max(arr)

#     for i in range(n):
#         if arr[i] == max_val:
#             index = n - 1
#         else:
#             index = int((arr[i] / max_val) * (n - 1))
            
#         bucket[index].append(arr[i])
    

#     for i in range(n):
#         bucket[i] = InsertionSort(bucket[i])

#     k = 0
#     for i in range(n):
#         for j in range(len(bucket[i])):
#             arr[k] = bucket[i][j]
#             k += 1
    
#     return arr


# arr = [0.7, 0.9, 0.5, 0.34, 0.8, 0.9]
# # arr = [7, 9, 5, 34, 8, 9]
# print(BucketSort(arr))

def BucketSort(arr, reverse=False):
    result = list(arr)
    comparisons = 0
    moves = 0
    n = len(result)

    if n <= 1:
        return result, comparisons, moves

    if any(not isinstance(x, (int, float)) or isinstance(x, bool)
           or not __import__("math").isfinite(x) for x in result):
        raise ValueError(
            "Bucket Sort requires finite numeric values."
        )

    minimum = min(result)
    maximum = max(result)

    if minimum == maximum:
        return result, comparisons, moves

    buckets = [[] for _ in range(n)]
    value_range = maximum - minimum

    for value in result:
        index = int((value - minimum) / value_range * (n - 1))
        buckets[index].append(value)
        moves += 1

    sorted_values = []

    for bucket in buckets:
        for i in range(1, len(bucket)):
            key = bucket[i]
            j = i - 1

            while j >= 0:
                comparisons += 1

                if bucket[j] > key:
                    bucket[j + 1] = bucket[j]
                    moves += 1
                    j -= 1
                else:
                    break

            bucket[j + 1] = key
            moves += 1

        sorted_values.extend(bucket)
        moves += len(bucket)

    if reverse:
        sorted_values.reverse()

    return sorted_values, comparisons, moves