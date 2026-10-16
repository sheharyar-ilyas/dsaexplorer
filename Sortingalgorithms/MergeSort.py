# Merge Sort

def MergeSort(arr):

    if len(arr) <=1:
        return arr
    
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = MergeSort(left_half)
    right_half = MergeSort(right_half)

    return Merge(left_half, right_half)

def Merge(left_half, right_half):
    i, j = 0, 0
    new = []

    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[i]:
            new.append(left_half[i])
            i +=1
        else:
            new.append(right_half[j])
            j +=1
    
    new.extend(left_half[i:])
    new.extend(right_half[j:])

    return new


# arr = [3,2,5,3,11,98,0,-3,-60]
# print(MergeSort(arr))