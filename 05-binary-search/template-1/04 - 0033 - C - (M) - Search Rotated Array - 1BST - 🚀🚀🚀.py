from typing import List

"""
For this question, we do
- 1 single binary search.

Which is significantly faster and easier than approaches 1 and 2.
"""
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        left, right = 0, n - 1
        while left <= right:
            mid = left + (right - left) // 2

            # Case 1: find target
            if nums[mid] == target:
                return mid

            # Case 2: subarray on mid's left is sorted
            elif nums[mid] >= nums[left]:
                if target >= nums[left] and target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1

            # Case 3: subarray on mid's right is sorted.
            else:
                if target <= nums[right] and target > nums[mid]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1



nums = [4, 5, 6, 7, 0, 1, 2]
target = 0
s = Solution()
result = s.search(nums, target)
print(result)

# nums = [7, 8, 1, 2, 3, 4, 5, 6]
# target = 2
# s = Solution()
# result = s.search(nums, target)
# print(result)
