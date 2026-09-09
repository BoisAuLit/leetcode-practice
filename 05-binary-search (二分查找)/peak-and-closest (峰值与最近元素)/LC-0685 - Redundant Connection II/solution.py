from typing import List
from bisect import bisect_left
from collections import deque


class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        n = len(arr)
        left = bisect_left(arr, x) - 1 # This is very crucial
        right = left + 1
        result = deque()
        while len(result) != k:
            d1 = d2 = float("inf")
            if 0 <= left <= n - 1:
                d1 = abs(arr[left] - x)
            if 0 <= right <= n - 1:
                d2 = abs(arr[right] - x)
            if d1 <= d2:
                result.appendleft(arr[left])
                left -= 1
            else:
                result.append(arr[right])
                right += 1
        return list(result)


# # Test case 1: Expecting [1, 1, 2, 3]
# s = Solution()
# arr = [1, 1, 2, 3, 4, 5]
# k = 4
# x = -1
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 2: Expecting [1, 2, 3, 4]
# s = Solution()
# arr = [1, 2, 3, 4, 5]
# k = 4
# x = 3
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 3: Expecting [10]
# s = Solution()
# arr = [1, 1, 1, 10, 10, 10]
# k = 1
# x = 9
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 4: Expecting [1,1,2,3,3,3]
# s = Solution()
# arr = [1, 1, 2, 3, 3, 3, 4, 6, 8, 8]
# k = 6
# x = 1
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 5: Expecting [2,3,3]
# s = Solution()
# arr = [1,1,2,2,2,2,2,3,3]
# k = 3
# x = 3
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 5: Expecting [3,3,4]
# s = Solution()
# arr = [0, 0, 1, 2, 3, 3, 4, 7, 7, 8]
# k = 3
# x = 5
# result = s.findClosestElements(arr, k, x)
# print(result)
