from typing import List

"""
Time complexity: O(logn)
Space complexity: O(1)
"""


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        low = 0
        high = len(nums) - 1
        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] > target:
                high = mid - 1
            else:
                low = mid + 1
        return -1


s = Solution()
nums = [-1, 0, 3, 5, 9, 12]
target = 9
result = s.search(nums, target)
print(result)
