# Counting SOrt

# def CountingSort(arr):
#     size = len(arr)

#     Output = [0] * size


def CountingSort(arr):

    negativeArrays = []
    positiveArrays = []

    for i in range(len(arr)):
        if arr[i] < 0:
            negativeArrays.append(arr[i])
        else:
            positiveArrays.append(arr[i])

    size = len(positiveArrays)
    output = [0]* size
    count  = [0]* (max(positiveArrays) + 1)

    for i in range(len(positiveArrays)):
        count[positiveArrays[i]] +=1
    
    for i in range(1, max(positiveArrays) + 1):
        count[i] += count[i-1]
    
    i = size - 1

    while i>=0:
        output[count[positiveArrays[i]]-1] = positiveArrays[i]
        count[positiveArrays[i]] -= 1
        i = i -1
    
    for i in range(size):
        positiveArrays[i] = output[i]
    
    negativeArrays.sort()
    negativeArrays.extend(positiveArrays)

    return negativeArrays



# arr = [-5, -10, 0, -3, 8, 5,-1, 10]
# print(CountingSort(arr))

    