from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        currMax = currMin = res = nums[0]

        for num in nums[1:]:
            prevMax = currMax
            prevMin = currMin
            currMax = max(num, prevMax * num, prevMin * num)
            currMin = min(num, prevMax * num, prevMin * num)
            res = max(res, currMax)

        return res
