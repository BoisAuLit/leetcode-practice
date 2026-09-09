from typing import List


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = right = 0
        nb_zeros = 0
        max_length = 0
        while right < len(nums):
            nb_zeros += int(nums[right] == 0)
            while nb_zeros > k:
                nb_zeros -= int(nums[left] == 0)
                left += 1
            max_length = max(max_length, right - left + 1)
            right += 1
        return max_length


# Test case 1: Expecting 6
s = Solution()
nums = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
k = 2
result = s.longestOnes(nums, k)
print(result)

# Test case 2: Expecting 10
# s = Solution()
# nums = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]
# k = 3
# result = s.longestOnes(nums, k)
# print(result)
