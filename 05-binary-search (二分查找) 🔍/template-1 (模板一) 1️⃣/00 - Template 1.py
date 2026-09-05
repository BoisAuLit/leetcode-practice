"""
这个 Template 是最简明易懂的 🤩

非常非常非常需要注意的几个点
⭐️. 这里是 p1 <= p2 而不是 p1 < p2 ❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗
----------------------------------------------------------------
✅. 这里将三种情况分析地非常透彻
"""

def binarySearch(nums, target):
    if len(nums) == 0:
        return -1

    left, right = 0, len(nums) - 1
    
    while left <= right: # ⭐️
        mid = (left + right) // 2
        if nums[mid] == target: # ✅
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # End Condition: left > right
    return -1
