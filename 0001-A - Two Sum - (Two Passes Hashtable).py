from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        mapping = {}
        for index, number in enumerate(nums):
            mapping[number] = index
        for index, number in enumerate(nums):
            complement = target - number
            if complement in mapping and index != mapping[complement]:
                return [index, mapping[complement]]


s = Solution()
input_ = [3, 2, 4]
result = s.twoSum(input_, 6)
print(result)

"""
Runtime
- 73 ms
- Beats: 71.60%

Memory
- 17.6 MB
- Beats 25.88%
"""
