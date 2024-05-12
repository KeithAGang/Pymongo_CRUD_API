import re

def linear_search(arr, search_value, param):
    result = []
    for i in range(len(arr)):
        if isinstance(arr[i][param], list):
            for value in arr[i][param]:
                if re.search(str(search_value), str(value)):
                    result.append(arr[i])
                    break
        elif isinstance(arr[i][param], str):
            if re.search(str(search_value), str(arr[i][param])):
                result.append(arr[i])
        elif isinstance(arr[i][param], int):
            if re.search(str(search_value), str(arr[i][param])):
                result.append(arr[i])
        if i == len(arr) - 1:
            return result
    return False

def binary_search(arr, search_value, param):
    result = []
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if isinstance(arr[mid][param], list):
            for value in arr[mid][param]:
                if value == search_value:
                    result.append(arr[mid])
                    return result
        elif arr[mid][param] == search_value:
            result.append(arr[mid])
            return result
        elif arr[mid][param] < search_value:
            low = mid + 1
        else:
            high = mid - 1
    return False

def hash_table_search(arr, search_value, param):
    hash_table = {item[param]: item for item in arr}
    
    results = []
    for key, item in hash_table.items():
        if isinstance(key, list):
            if search_value in key:
                results.append(item)
        else:
            if search_value == key:
                results.append(item)
    
    return results

def jump_search(arr, search_value, param):
    result = []
    n = len(arr)
    step = int(n**0.5)
    prev = 0
    while isinstance(arr[min(step, n)-1][param], list) or arr[min(step, n)-1][param] < search_value:
        prev = step
        step += int(n**0.5)
        if prev >= n:
            return False
    while isinstance(arr[prev][param], list) or arr[prev][param] < search_value:
        prev += 1
        if prev == min(step, n):
            return False
    if isinstance(arr[prev][param], list):
        for value in arr[prev][param]:
            if value == search_value:
                result.append(arr[prev])
                return result
    elif arr[prev][param] == search_value:
        result.append(arr[prev])
        return result
    else:
        return False

def interpolation_search(arr, search_value, param):
    result = []
    n = len(arr)
    low, high = 0, n - 1
    while low <= high and (isinstance(arr[low][param], list) or arr[low][param] <= search_value <= arr[high][param]):
        if isinstance(arr[low][param], list):
            for value in arr[low][param]:
                if value == search_value:
                    result.append(arr[low])
                    return result
        elif arr[low][param] == search_value:
            result.append(arr[low])
            return result
        elif low == high:
            return result
        mid = low + int((high - low) * (search_value > arr[low][param]) / (arr[high][param] > arr[low][param]))
        if isinstance(arr[mid][param], list):
            for value in arr[mid][param]:
                if value == search_value:
                    result.append(arr[mid])
                    return result
        elif arr[mid][param] < search_value:
            low = mid + 1
        elif arr[mid][param] > search_value:
            high = mid - 1
        else:
            result.append(arr[mid])
            return result
    return result

