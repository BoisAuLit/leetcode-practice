from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        mapping = {}
        for i in range(len(nums)):
            mapping[nums[i]] = i
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in mapping:
                if i != mapping[complement]:
                    return [i, mapping[complement]]


s = Solution()
input_ = [3, 2, 4]
result = s.twoSum(input_, 6)
print(result)
