class QuickSort:
    @staticmethod
    def sort(arr):
        QuickSort._quick_sort(arr, 0, len(arr) - 1)

    @staticmethod
    def _quick_sort(arr, low, high):
        if low < high:
            pi = QuickSort._partition(arr, low, high)
            QuickSort._quick_sort(arr, low, pi - 1)
            QuickSort._quick_sort(arr, pi + 1, high)

    @staticmethod
    def _partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1