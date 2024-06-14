class bubble_sort:
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

# arr = [23,9,17,5,13,3,21,11,25,7,20,14,6,26,2,10,15,1,24,8]

# result = sort.bubble_sort(arr)
# print(result)