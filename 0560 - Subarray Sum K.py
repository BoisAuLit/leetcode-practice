from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        res = 0
        curSum = 0
        prefixSums = {0: 1}
        for n in nums:
            curSum += n
            diff = curSum - k

            res += prefixSums.get(diff, 0)
            prefixSums[curSum] = 1 + prefixSums.get(curSum, 0)
        return res


s = Solution()


input_ = [1, 1, 1]
k = 2

result = s.subarraySum(input_, 2)
print(result)

"""

"""
