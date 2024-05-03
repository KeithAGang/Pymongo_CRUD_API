def bubble_sort(arr, param, order="asc"):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if isinstance(arr[j][param], list):
                if str(arr[j][param][0]).isdigit() and str(arr[j+1][param][0]).isdigit():
                    if int(arr[j][param][0]) > int(arr[j+1][param][0]):
                        arr[j], arr[j+1] = arr[j+1], arr[j]
                else:
                    if str(arr[j][param][0]) > str(arr[j+1][param][0]):
                        arr[j], arr[j+1] = arr[j+1], arr[j]
            elif str(arr[j][param]).isdigit() and str(arr[j+1][param]).isdigit():
                if int(arr[j][param]) > int(arr[j+1][param]):
                    arr[j], arr[j+1] = arr[j+1], arr[j]
            else:
                if str(arr[j][param]) > str(arr[j+1][param]):
                    arr[j], arr[j+1] = arr[j+1], arr[j]
    
    if order == "desc":
        data = arr[::-1]
    else:
        data = arr
    
    response = {
        "data": data,
        "complexities": "Time Complexity: O(n^2), Space Complexity: O(1)"
    }
    return response

def selection_sort(arr, param, order="asc"):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if isinstance(arr[min_idx][param], list):
                if str(arr[min_idx][param][0]).isdigit() and str(arr[j][param][0]).isdigit():
                    if int(arr[min_idx][param][0]) > int(arr[j][param][0]):
                        min_idx = j
                else:
                    if str(arr[min_idx][param][0]) > str(arr[j][param][0]):
                        min_idx = j
            elif str(arr[min_idx][param]).isdigit() and str(arr[j][param]).isdigit():
                if int(arr[min_idx][param]) > int(arr[j][param]):
                    min_idx = j
            else:
                if str(arr[min_idx][param]) > str(arr[j][param]):
                    min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        
    if order == "desc":
        data = arr[::-1]
    else:
        data = arr
    
    response = {
        "data": data,
        "complexities": "Time Complexity: O(n^2), Space Complexity: O(1)"
    }
    return response

def merge_sort(arr, param, order="asc"):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L, param, order)
        merge_sort(R, param, order)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if isinstance(L[i][param], list) and isinstance(R[j][param], list):
                if str(L[i][param][0]).isdigit() and str(R[j][param][0]).isdigit():
                    if int(L[i][param][0]) < int(R[j][param][0]):
                        arr[k] = L[i]
                        i += 1
                    else:
                        arr[k] = R[j]
                        j += 1
                elif str(L[i][param][0]) < str(R[j][param][0]):
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
            elif str(L[i][param]).isdigit() and str(R[j][param]).isdigit():
                if int(L[i][param]) < int(R[j][param]):
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
            elif str(L[i][param]) < str(R[j][param]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            
    if order == "desc":
        data = arr[::-1]
    else:
        data = arr
        
    response = {
        "data": data,
        "complexities": "Time Complexity: O(n log n), Space Complexity: O(n)"
    }
    return response

def insertion_sort(arr, param, order="asc"):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        if order == "asc":
            while j >= 0 and (isinstance(key[param], list) and (str(key[param][0]).isdigit() and int(key[param][0]) < int(arr[j][param][0]) or not str(key[param][0]).isdigit() and str(key[param][0]) < str(arr[j][param][0])) or not isinstance(key[param], list) and (str(key[param]).isdigit() and int(key[param]) < int(arr[j][param]) or not str(key[param]).isdigit() and str(key[param]) < str(arr[j][param]))):
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= 0 and (isinstance(key[param], list) and (str(key[param][0]).isdigit() and int(key[param][0]) > int(arr[j][param][0]) or not str(key[param][0]).isdigit() and str(key[param][0]) > str(arr[j][param][0])) or not isinstance(key[param], list) and (str(key[param]).isdigit() and int(key[param]) > int(arr[j][param]) or not str(key[param]).isdigit() and str(key[param]) > str(arr[j][param]))):
                arr[j + 1] = arr[j]
                j -= 1
        
        arr[j + 1] = key
    
    if order == "desc":
        return {"data": arr[::-1], "complexities": "Time Complexity: O(n^2), Space Complexity: O(1)"}
    else:
        return {"data": arr, "complexities": "Time Complexity: O(n^2), Space Complexity: O(1)"}

def quick_sort(arr, param, order='asc'):
    def partition(arr, low, high, param):
        i = (low-1)
        if isinstance(arr[high][param], list):
            if str(arr[high][param][0]).isdigit():
                pivot = int(arr[high][param][0])
            else:
                pivot = str(arr[high][param][0])
        else:
            if str(arr[high][param]).isdigit():
                pivot = int(arr[high][param])
            else:
                pivot = str(arr[high][param])
        for j in range(low, high):
            if isinstance(arr[j][param], list):
                if str(arr[j][param][0]).isdigit() and int(arr[j][param][0]) <= pivot:
                    i = i+1
                    arr[i], arr[j] = arr[j], arr[i]
                elif not str(arr[j][param][0]).isdigit() and str(arr[j][param][0]) <= pivot:
                    i = i+1
                    arr[i], arr[j] = arr[j], arr[i]
            elif str(arr[j][param]).isdigit() and int(arr[j][param]) <= pivot:
                i = i+1
                arr[i], arr[j] = arr[j], arr[i]
            elif not str(arr[j][param]).isdigit() and str(arr[j][param]) <= pivot:
                i = i+1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return (i+1)

    def _quick_sort(arr, low, high, param):
        if low < high:
            pi = partition(arr, low, high, param)
            _quick_sort(arr, low, pi-1, param)
            _quick_sort(arr, pi+1, high, param)

    _quick_sort(arr, 0, len(arr)-1, param)

    if order == "desc":
        data = arr[::-1]
    else:
        data = arr
        
    response = {
        "data": data,
        "complexities": "Time Complexity: O(n log n), Space Complexity: O(log n)"
    }
    return response
