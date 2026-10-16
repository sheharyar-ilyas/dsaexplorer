
# BubbleSort
def BubbleSort(arr):
    for i in range(len(arr) - 1):
        flag = False
        for j in range(len(arr)-1 - i):
            if arr[j] > arr[j+1]:
                arr[j] , arr[j+1] = arr[j+1], arr[j]
                flag = True
        if flag == False:
            break

    return arr


arr = [2,5,3,2,2,-22,0,5,3,3]
print(BubbleSort(arr))
    