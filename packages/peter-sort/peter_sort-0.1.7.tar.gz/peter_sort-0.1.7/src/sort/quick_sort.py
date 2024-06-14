class quick_sort:
    def quick_sort(listOfNumbers):
        if len(listOfNumbers) <= 1:
            return listOfNumbers
        else:
            pivot = listOfNumbers[0]
        
        lessThanPivot = []
        moreThanPivot = []

        for number in listOfNumbers[1:]:
            if number > pivot:
                moreThanPivot.append(number)
            else:
                lessThanPivot.append(number)
        
        return quick_sort.quick_sort(lessThanPivot) + [pivot] + quick_sort.quick_sort(moreThanPivot)

# Test the function
# result = quick_sort.quick_sort([3, 12, 3, 4, 5, 61, 2, 4, 3, 8, 17, 53, 64, 3, 4, 6, 5, 8, 9])
# print(result)
