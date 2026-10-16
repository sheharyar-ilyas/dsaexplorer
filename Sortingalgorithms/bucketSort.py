# Bucket Sort

# For sorting in buckets we use the insertion sort
def InsertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j = j - 1  
                
        arr[j+1] = key
    return arr

def BucketSort(arr):
    if len(arr) <= 1:
        return arr

    n = len(arr)
    bucket = []

    for i in range(n):
        bucket.append([])

    max_val = max(arr)

    for i in range(n):
        if arr[i] == max_val:
            index = n - 1
        else:
            index = int((arr[i] / max_val) * (n - 1))
            
        bucket[index].append(arr[i])
    

    for i in range(n):
        bucket[i] = InsertionSort(bucket[i])

    k = 0
    for i in range(n):
        for j in range(len(bucket[i])):
            arr[k] = bucket[i][j]
            k += 1
    
    return arr


arr = [0.7, 0.9, 0.5, 0.34, 0.8, 0.9]
# arr = [7, 9, 5, 34, 8, 9]
print(BucketSort(arr))
