# Radix Sort

def RadixSort(arr):
    if len(arr) <= 1:
        return arr

    negative = []
    positive = []

    for num in arr:
        if num < 0:
            negative.append(abs(num))
        else:
            positive.append(num)

    if len(negative) > 0:
        maximum_element = max(negative)
        place = 1

        while maximum_element // place > 0:
            CountingSortForRadix(negative, place)
            place *= 10

        negative.reverse()

        for i in range(len(negative)):
            negative[i] = -negative[i]

    if len(positive) > 0:
        maximum_element = max(positive)
        place = 1

        while maximum_element // place > 0:
            CountingSortForRadix(positive, place)
            place *= 10

    arr[:] = negative + positive

    return arr


def CountingSortForRadix(arr, place):
    size = len(arr)

    output = [0] * size
    count = [0] * 10

    for i in range(size):
        index = arr[i] // place
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = size - 1

    while i >= 0:
        index = arr[i] // place
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for j in range(size):
        arr[j] = output[j]

    return arr


# arr1 = [110, -45, 65, 50, -90, 602, 24, -2, 66]

# print(RadixSort(arr1))

