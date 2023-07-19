from typing import List

"""
Time complexity: O(logn)
Space complexity: O(1)
"""


class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        
        if k > arr[-1] - len(arr):
            return arr[-1] + (k - arr[-1] + len(arr))
        if k <= (arr[0] - 1):
            return k
        
        left = 0
        right = len(arr) - 1
        while True:
            mid = (left + right) // 2
            curr_miss_ints = arr[mid] - mid - 1
            if curr_miss_ints < k:
                next_miss_ints = arr[mid + 1] - mid - 2
                if next_miss_ints >= k:
                    return arr[mid] + k - curr_miss_ints
                left = mid + 1
            else:
                prev_miss_ints = arr[mid - 1] - mid
                if prev_miss_ints < k:
                    return arr[mid - 1] + k - prev_miss_ints
                right = mid - 1


s = Solution()

# Expecting 6
# arr = [2]
# k = 5

# Expecting 6
# arr = [1, 2, 3, 4]
# k = 2

# Expecting 2
# arr = [1, 3]
# k = 1

# Expecting 14
arr = [5,6,7,8,9]
k = 9



result = s.findKthPositive(arr, k)
print(result)

"""
Runtime
- 72ms
- Beats 42.06%

Memory
- 16.37mb
- Beats 91.45%
"""
