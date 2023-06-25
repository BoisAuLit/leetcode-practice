from typing import List


class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        result = []
        for index, value in enumerate(nums):
            if index == 0:
                result.append(value)
            else:
                result.append(result[index - 1] + value)
        return result


s = Solution()
input_ = [1, 2, 3, 4]
result = s.runningSum(input_)
print(result)

"""
Runtime
- 62 ms
- Beats 23.78%

Memory
- 16.5 MB
- Beats 51.31%
"""
