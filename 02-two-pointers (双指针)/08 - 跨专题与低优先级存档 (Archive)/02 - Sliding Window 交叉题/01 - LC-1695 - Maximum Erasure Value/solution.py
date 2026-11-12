# https://leetcode.com/problems/maximum-erasure-value/

from typing import List

class Solution:
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        l=r=0
        curr_sum = max_sum = 0
        elements = set()
        for r in range(n):
            num = nums[r]
            curr_sum += num
            if num not in elements:
                elements.add(num)
                max_sum = max(max_sum, curr_sum)
                continue
            while nums[l] != num:
                curr_sum -= nums[l]
                elements.remove(nums[l])
                l += 1
            curr_sum -= num
            l += 1
        return max_sum
            
            
            



s = Solution()
nums = [5, 2, 1, 2, 5, 2, 1, 2, 5]
result = s.maximumUniqueSubarray(nums)
print(result)
