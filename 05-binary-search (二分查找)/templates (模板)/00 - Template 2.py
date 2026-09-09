"""
这个 Template 和 Template 1 的最大区别是 ⭐️ 这一行

另外一个区别: Post-processing
Loop/Recursion ends when you have 1 element left.
Need to assess if the remaining element meets the condition.
"""

def binarySearch(nums, target):
    if len(nums) == 0:
        return -1

    left, right = 0, len(nums) - 1
    
    while left < right: # ⭐️
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1 # ✅ 这一点非常关键
        else:
            right = mid

    # Post-processing:
    # End Condition: left == right
    if nums[left] == target:
        return left
    return -1
