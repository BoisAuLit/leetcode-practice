from typing import List

"""
Time complexity: O(n2)
Space complexity: O(n)
"""


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        mapping = {}
        result = []
        for index, number in enumerate(nums):
            complement = target - number
            if complement in mapping:
                result.append([number, complement])
            mapping[number] = index
        return result

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = []
        for i in range(len(nums) - 1):
            twoSumResult = self.twoSum(nums[i + 1 :], -nums[i])
            for j in twoSumResult:
                result.append([nums[i]] + j)
        return [list(i) for i in set(tuple(sorted(j)) for j in result)]


s = Solution()
input_ = [-1, 0, 1, 2, -1, -4]
result = s.threeSum(input_)
print(result)
