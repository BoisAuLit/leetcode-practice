from typing import List

"""
Time complexity: O()
Space complexity: O()
"""
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        left =0
        right = len(nums)-1
        while left < right:
            mid = left + (right - left ) //2
            if nums[mid] > nums[mid+1]: # True Condition # Dec function # go left # Find First True i.e first elem where this condition will be True
                right = mid # include mid # mid is potential solution 
            else:
                left = mid +1
        return left

s = Solution()
input_ = 
result = s.XXXXXXXXXXXXX(input_)
print(result)
